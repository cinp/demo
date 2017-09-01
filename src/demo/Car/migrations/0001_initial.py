# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def load_models( app, schema_editor ):
  Model = app.get_model( 'Car', 'Model' )

  m = Model( make='Galaxy', model='Mars', year=2042 )
  m.full_clean()
  m.save()

  m = Model( make='Galaxy', model='Jupiter', year=2012 )
  m.full_clean()
  m.save()

  m = Model( make='Galaxy', model='Neptune', year=2020 )
  m.full_clean()
  m.save()

  m = Model( make='System', model='Small', year=2018 )
  m.full_clean()
  m.save()

  m = Model( make='System', model='Bus', year=2010 )
  m.full_clean()
  m.save()


def load_cars( app, schema_editor ):
  Model = app.get_model( 'Car', 'Model' )
  Car = app.get_model( 'Car', 'Car' )
  User = app.get_model( 'User', 'User' )

  bob = User.objects.get( username='bob' )
  sally = User.objects.get( username='sally' )

  g_mars = Model.objects.get( make='Galaxy', model='Mars' )
  g_jupiter = Model.objects.get( make='Galaxy', model='Jupiter' )
  s_small = Model.objects.get( make='System', model='Small' )

  c = Car( model=g_mars, owner=bob, name='Red_Beast', cost=4200.00 )
  c.full_clean()
  c.save()

  c = Car( model=s_small, owner=bob, name='Commuter', cost=500.00 )
  c.full_clean()
  c.save()

  c = Car( model=g_mars, owner=sally, name='Meteor', cost=100.00 )
  c.full_clean()
  c.save()

  c = Car( model=g_jupiter, owner=sally, name='Smasher', cost=1000.00 )
  c.full_clean()
  c.save()

  c = Car( model=g_mars, owner=sally, name='Meteor2', cost=400.00 )
  c.full_clean()
  c.save()

  c = Car( model=g_mars, name='Star_Hopper', cost=4000.00 )
  c.full_clean()
  c.save()

  c = Car( model=g_mars, name='Star_Chaser', cost=3500.00 )
  c.full_clean()
  c.save()

  c = Car( model=s_small, name='Planet_Hopper', cost=1000.00 )
  c.full_clean()
  c.save()


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('name', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('cost', models.FloatField()),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('make', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='car',
            name='model',
            field=models.ForeignKey(to='Car.Model'),
        ),
        migrations.AddField(
            model_name='car',
            name='owner',
            field=models.ForeignKey(to='User.User', null=True, blank=True),
        ),
        migrations.RunPython( load_models ),
        migrations.RunPython( load_cars ),
    ]
