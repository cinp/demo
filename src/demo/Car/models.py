from django.db import models

from cinp.orm_django import DjangoCInP as CInP

from demo.User.models import User

cinp = CInP( 'Car', '0.1', 'Cars and their Models' )


@cinp.model( property_list=[], not_allowed_verb_list=[] )
class Model( models.Model ):
  """
All the Make/Model/Years for the cars
  """
  make = models.CharField( max_length=100 )
  model = models.CharField( max_length=100 )
  year = models.IntegerField()
  updated = models.DateTimeField( editable=False, auto_now=True )
  created = models.DateTimeField( editable=False, auto_now_add=True )

  @cinp.check_auth()
  @staticmethod
  def checkAuth( user, verb, id_list, action=None ):
    return True

  class Meta:
    unique_together = ( ( 'make', 'model', 'year' ), )

  def __str__( self ):
    return 'Model "{0}" "{1}" "{2}"'.format( self.make, self.model, self.year )


@cinp.model( property_list=[], not_allowed_verb_list=[] )
class Car( models.Model ):
  """
This is all the cars own by the users.
Owner is not required, indicating the car is not curently owned.  When requesting
a list, if your query includes a car that is not yours, you will get a not
authorized(Unless you are a super user).
  """
  name = models.CharField( max_length=50, primary_key=True )
  owner = models.ForeignKey( User, null=True, blank=True, on_delete=models.PROTECT )
  model = models.ForeignKey( Model, on_delete=models.PROTECT )
  cost = models.FloatField( help_text='How much the car is worth' )
  updated = models.DateTimeField( editable=False, auto_now=True )
  created = models.DateTimeField( editable=False, auto_now_add=True )

  @cinp.action( return_type='Float', paramater_type_list=[ { 'type': 'Float', 'doc': 'between 0 and 1' } ] )
  def deprecate( self, percentage ):
    """
Deprecate the Cars value by the specified precentage. Returns the new cost/value of the car.
    """
    if percentage < 0 or percentage > 1:
      raise ValueError( 'Percentage should be a value between 0 and 1 inclusive.' )
    self.cost = self.cost * ( 1 - percentage )
    self.full_clean()
    self.save()
    return self.cost

  @cinp.action( paramater_type_list=[ { 'type': 'Model', 'model': 'demo.User.models.User' } ] )
  def sell( self, new_owner=None ):
    """
Change the ownership of the car to new_owner.  It is valid to sell it to one's
self.  Does not handle any money,  that should be done else where.  If new_owner
is left out, the car becomes unclaimed.
    """
    self.owner = new_owner
    self.full_clean()
    self.save()

  @cinp.list_filter( name='owner', paramater_type_list=[ { 'type': 'Model', 'model': 'demo.User.models.User' } ] )
  @staticmethod
  def filter_site( owner ):
    return Car.objects.filter( owner=owner )

  @cinp.check_auth()
  @staticmethod
  def checkAuth( user, verb, id_list, action=None ):
    if verb in ( 'DESCRIBE', 'LIST' ):
      return True

    if id_list is None:
      return False  # can't get a undefined list of ids

    owner_set = set( [ i.owner for i in Car.objects.filter( pk__in=id_list ) ] )
    if len( owner_set ) != 1:
      return False

    return user == list( owner_set )[0]

  def __str__( self ):
    return 'Car "{0}" belonging to "{1}"'.format( self.make, self.owner )
