CInP Demo
=========

This will demostrate using CInP, the server can be launched with vagrant or
as a Docker container.

Vagrant
-------

::

  cd vagrant
  vagrant up

Give it a bit to download and setup, and you are all set.

Docker
------

::

  docker build . -t cinp/demo
  docker run -p 8888:8888 -d cinp/demo


Talking to CInP
===============

NOTE: you may want to read the generic protocol docs to know what the various
Verbs are and what to expect.

Web Extension
-------------

There is a web extension (Firefox/Chrome Extension) aviable at https://github.com/cinp/web_extension
You can clone that repo and load it into your browser in dev mode, or it is also
published to the Chrome Web Store at https://chrome.google.com/webstore/detail/cinp-generic-client/lacnhpojnjgdohcdggednghjibhgkeop?hl=en-US&gl=US

Commandline/Curl
----------------

First let's Describe try a Describe::

  $ curl -X DESCRIBE -H "CINP-VERSION: 0.9" -v http://127.0.0.1:8888/api/v1/

should output something like::

  *   Trying 127.0.0.1...
  * Connected to 127.0.0.1 (127.0.0.1) port 8888 (#0)
  > DESCRIBE /api/v1/ HTTP/1.1
  > Host: 127.0.0.1:8888
  > User-Agent: curl/7.47.0
  > Accept: */*
  > CINP-VERSION: 0.9
  >
  < HTTP/1.1 200 OK
  < Server: gunicorn/19.4.5
  < Date: Fri, 01 Sep 2017 04:35:41 GMT
  < Connection: close
  < Verb: DESCRIBE
  < Type: Namespace
  < Access-Control-Expose-Headers: Method, Type, Cinp-Version, Count, Position, Total, Multi-Object, Object-Id
  < Cache-Control: max-age=0
  < Cinp-Version: 0.9
  < Access-Control-Allow-Origin: *
  < Content-Type: application/json;charset=utf-8
  < Content-Length: 138
  <
  * Closing connection 0
  {"name": "root", "api-version": "1.0", "namespaces": ["/api/v1/User/"], "doc": "", "models": [], "multi-uri-max": 100, "path": "/api/v1/"}

Let's List the Cars::

  $ curl -X LIST -H "CINP-VERSION: 0.9" -v http://127.0.0.1:8888/api/v1/Car/Car
  *   Trying 127.0.0.1...
  * Connected to 127.0.0.1 (127.0.0.1) port 8888 (#0)
  > LIST /api/v1/Car/Car HTTP/1.1
  > Host: 127.0.0.1:8888
  > User-Agent: curl/7.47.0
  > Accept: */*
  > CINP-VERSION: 0.9
  >
  < HTTP/1.1 200 OK
  < Server: gunicorn/19.4.5
  < Date: Wed, 06 Sep 2017 03:11:01 GMT
  < Connection: close
  < Count: 8
  < Cache-Control: no-cache
  < Cinp-Version: 0.9
  < Total: 8
  < Access-Control-Allow-Origin: *
  < Position: 0
  < Verb: LIST
  < Access-Control-Expose-Headers: Method, Type, Cinp-Version, Count, Position, Total, Multi-Object, Object-Id
  < Content-Type: application/json;charset=utf-8
  < Content-Length: 240
  <
  * Closing connection 0
  ["/api/v1/Car/Car:Commuter:", "/api/v1/Car/Car:Meteor:", "/api/v1/Car/Car:Meteor2:", "/api/v1/Car/Car:Planet_Hopper:", "/api/v1/Car/Car:Red_Beast:", "/api/v1/Car/Car:Smasher:", "/api/v1/Car/Car:Star_Chaser:", "/api/v1/Car/Car:Star_Hopper:"]

There is a List of all the cars, let's get some detail on one::

  $ curl -X GET -H "CINP-VERSION: 0.9" -v http://127.0.0.1:8888/api/v1/Car/Car:Meteor:
  *   Trying 127.0.0.1...
  * Connected to 127.0.0.1 (127.0.0.1) port 8888 (#0)
  > GET /api/v1/Car/Car:Meteor: HTTP/1.1
  > Host: 127.0.0.1:8888
  > User-Agent: curl/7.47.0
  > Accept: */*
  > CINP-VERSION: 0.9
  >
  < HTTP/1.1 403 FORBIDDEN
  < Server: gunicorn/19.4.5
  < Date: Wed, 06 Sep 2017 03:12:30 GMT
  < Connection: close
  < Access-Control-Expose-Headers: Method, Type, Cinp-Version, Count, Position, Total, Multi-Object, Object-Id
  < Cinp-Version: 0.9
  < Access-Control-Allow-Origin: *
  < Content-Type: application/json;charset=utf-8
  < Content-Length: 29
  <
  * Closing connection 0
  {"message": "Not Authorized"}

The Permissions of the Cars do not allow us to GET/UPDATE/DELETE/CALL for car
that does not belong to us, so let's login as the Bob user.  This demo app has
a static function on the Session object to check username and password and create
a session::

  $ curl -X CALL -H "CINP-VERSION: 0.9" -d '{ "username": "bob", "password": "bob" }' -v http://127.0.0.1:8888/api/v1/User/Session\(login\)
  *   Trying 127.0.0.1...
  * Connected to 127.0.0.1 (127.0.0.1) port 8888 (#0)
  > CALL /api/v1/User/Session(login) HTTP/1.1
  > Host: 127.0.0.1:8888
  > User-Agent: curl/7.47.0
  > Accept: */*
  > CINP-VERSION: 0.9
  > Content-Length: 40
  > Content-Type: application/x-www-form-urlencoded
  >
  * upload completely sent off: 40 out of 40 bytes
  < HTTP/1.1 200 OK
  < Server: gunicorn/19.4.5
  < Date: Wed, 06 Sep 2017 03:05:30 GMT
  < Connection: close
  < Access-Control-Allow-Origin: *
  < Multi-Object: False
  < Cinp-Version: 0.9
  < Verb: CALL
  < Cache-Control: no-cache
  < Access-Control-Expose-Headers: Method, Type, Cinp-Version, Count, Position, Total, Multi-Object, Object-Id
  < Content-Type: application/json;charset=utf-8
  < Content-Length: 32
  <
  * Closing connection 0
  "ysGdBiFBtqdlkCFMzOwCHZPlIqvvUo"

That gives us a session token.  Let's try again with the Get (note you will
need to replace the AUTH-TOKEN with what you got from login)::

  $ curl -X GET -H "CINP-VERSION: 0.9" -H "AUTH-ID: bob" -H "AUTH-TOKEN: ysGdBiFBtqdlkCFMzOwCHZPlIqvvUo" -v http://127.0.0.1:8888/api/v1/Car/Car:Meteor:
  *   Trying 127.0.0.1...
  * Connected to 127.0.0.1 (127.0.0.1) port 8888 (#0)
  > GET /api/v1/Car/Car:Meteor: HTTP/1.1
  > Host: 127.0.0.1:8888
  > User-Agent: curl/7.47.0
  > Accept: */*
  > CINP-VERSION: 0.9
  > AUTH-ID: bob
  > AUTH-TOKEN: ysGdBiFBtqdlkCFMzOwCHZPlIqvvUo
  >
  < HTTP/1.1 403 FORBIDDEN
  < Server: gunicorn/19.4.5
  < Date: Wed, 06 Sep 2017 03:14:03 GMT
  < Connection: close
  < Access-Control-Expose-Headers: Method, Type, Cinp-Version, Count, Position, Total, Multi-Object, Object-Id
  < Cinp-Version: 0.9
  < Access-Control-Allow-Origin: *
  < Content-Type: application/json;charset=utf-8
  < Content-Length: 29
  <
  * Closing connection 0
  {"message": "Not Authorized"}

We are still not permitted b/c we asked for a car that does not belong to us, let's
try another::

  $ curl -X GET -H "CINP-VERSION: 0.9" -H "AUTH-ID: bob" -H "AUTH-TOKEN: ysGdBiFBtqdlkCFMzOwCHZPlIqvvUo" -v http://127.0.0.1:8888/api/v1/Car/Car:Commuter:
  *   Trying 127.0.0.1...
  * Connected to 127.0.0.1 (127.0.0.1) port 8888 (#0)
  > GET /api/v1/Car/Car:Commuter: HTTP/1.1
  > Host: 127.0.0.1:8888
  > User-Agent: curl/7.47.0
  > Accept: */*
  > CINP-VERSION: 0.9
  > AUTH-ID: bob
  > AUTH-TOKEN: ysGdBiFBtqdlkCFMzOwCHZPlIqvvUo
  >
  < HTTP/1.1 200 OK
  < Server: gunicorn/19.4.5
  < Date: Wed, 06 Sep 2017 03:15:30 GMT
  < Connection: close
  < Verb: GET
  < Multi-Object: False
  < Cinp-Version: 0.9
  < Access-Control-Expose-Headers: Method, Type, Cinp-Version, Count, Position, Total, Multi-Object, Object-Id
  < Access-Control-Allow-Origin: *
  < Cache-Control: no-cache
  < Content-Type: application/json;charset=utf-8
  < Content-Length: 197
  <
  * Closing connection 0
  {"name": "Commuter", "model": "/api/v1/Car/Model:4:", "cost": 500.0, "created": "2017-09-06T00:46:25.654209+00:00", "updated": "2017-09-06T00:46:25.654185+00:00", "owner": "/api/v1/User/User:bob:"}

Now we can see the car, let's sell it to Sally.  We do that by calling the sell
action on that car::

  $ curl -X CALL -H "CINP-VERSION: 0.9" -H "AUTH-ID: bob" -H "AUTH-TOKEN: ysGdBiFBtqdlkCFMzOwCHZPlIqvvUo" -d '{ "to": "/api/v1/User/User:sally:" }' -v http://127.0.0.1:8888/api/v1/Car/Car:Commuter:\(sell\)
  > CALL /api/v1/Car/Car:Commuter:(sell) HTTP/1.1
  > Host: 127.0.0.1:8888
  > User-Agent: curl/7.47.0
  > Accept: */*
  > CINP-VERSION: 0.9
  > AUTH-ID: bob
  > AUTH-TOKEN: ysGdBiFBtqdlkCFMzOwCHZPlIqvvUo
  > Content-Length: 36
  > Content-Type: application/x-www-form-urlencoded
  >
  * upload completely sent off: 36 out of 36 bytes
  < HTTP/1.1 200 OK
  < Server: gunicorn/19.4.5
  < Date: Wed, 06 Sep 2017 03:18:04 GMT
  < Connection: close
  < Verb: CALL
  < Multi-Object: False
  < Cinp-Version: 0.9
  < Access-Control-Expose-Headers: Method, Type, Cinp-Version, Count, Position, Total, Multi-Object, Object-Id
  < Access-Control-Allow-Origin: *
  < Cache-Control: no-cache
  < Content-Type: application/json;charset=utf-8
  < Content-Length: 0
  <
  * Closing connection 0

Now we can try getting the car's detail::

  $ curl -X GET -H "CINP-VERSION: 0.9" -H "AUTH-ID: bob" -H "AUTH-TOKEN: ysGdBiFBtqdlkCFMzOwCHZPlIqvvUo" -v http://127.0.0.1:8888/api/v1/Car/Car:Commuter:
  *   Trying 127.0.0.1...
  * Connected to 127.0.0.1 (127.0.0.1) port 8888 (#0)
  > GET /api/v1/Car/Car:Commuter: HTTP/1.1
  > Host: 127.0.0.1:8888
  > User-Agent: curl/7.47.0
  > Accept: */*
  > CINP-VERSION: 0.9
  > AUTH-ID: bob
  > AUTH-TOKEN: ysGdBiFBtqdlkCFMzOwCHZPlIqvvUo
  >
  < HTTP/1.1 403 FORBIDDEN
  < Server: gunicorn/19.4.5
  < Date: Wed, 06 Sep 2017 03:19:54 GMT
  < Connection: close
  < Access-Control-Expose-Headers: Method, Type, Cinp-Version, Count, Position, Total, Multi-Object, Object-Id
  < Cinp-Version: 0.9
  < Access-Control-Allow-Origin: *
  < Content-Type: application/json;charset=utf-8
  < Content-Length: 29
  <
  * Closing connection 0
  {"message": "Not Authorized"}

sure enough we don't own the car anymore, so we can't see it.


Python
------

First install the CInP python library

::

  pip3 install cinp

Now launch your python3 interpreture of choice, and let's try a few things out::

  In [1]: from cinp.client import CInP

  In [2]: conn = CInP( 'http://127.0.0.1', '/api/v1/', 8888 )

Now that we are connected, First let's Describe try a Describe::

  In [3]: conn.describe( '/api/v1/' )
  Out[3]:
  {'multi-uri-max': 100,
   'doc': '',
   'models': [],
   'namespaces': ['/api/v1/User/', '/api/v1/Car/'],
   'name': 'root',
   'path': '/api/v1/',
   'api-version': '1.0'}

Let's List the Cars::

   In [4]: conn.list( '/api/v1/Car/Car' )
   Out[4]:
   (['/api/v1/Car/Car:Commuter:',
     '/api/v1/Car/Car:Meteor:',
     '/api/v1/Car/Car:Meteor2:',
     '/api/v1/Car/Car:Planet_Hopper:',
     '/api/v1/Car/Car:Red_Beast:',
     '/api/v1/Car/Car:Smasher:',
     '/api/v1/Car/Car:Star_Chaser:',
     '/api/v1/Car/Car:Star_Hopper:'],
    {'total': 8, 'count': 8, 'position': 0})

There is a List of all the cars, let's get some detail on one::

  In [5]: conn.get( '/api/v1/Car/Car:Meteor:' )
  WARNING:root:cinp: Not Authorized
  ---------------------------------------------------------------------------
  NotAuthorized                             Traceback (most recent call last)
  <stack trace>

The Permissions of the Cars do not allow us to GET/UPDATE/DELETE/CALL for car
that does not belong to us, so let's login as the Bob user.  This demo app has
a static function on the Session object to check username and password and create
a session::

  In [6]: conn.call( '/api/v1/User/Session(login)', { 'username': 'bob', 'password': 'bob'} )
  Out[6]: 'NQduEzUEbRwnRyvpfWMZwsUnwTGJwe'

That gives us a session token.  Now we tell the CInP to remember the auth creds, and
try again with the Get (note you will need to replace the AUTH-TOKEN with what you
got from login)::

  In [7]: conn.setAuth( 'bob', 'NQduEzUEbRwnRyvpfWMZwsUnwTGJwe' )

  In [8]: conn.get( '/api/v1/Car/Car:Meteor:' )
  WARNING:root:cinp: Not Authorized
  ---------------------------------------------------------------------------
  NotAuthorized                             Traceback (most recent call last)
  <stack trace>

We are still not permitted b/c we asked for a car that does not belong to us, let's
try another::

  In [9]: conn.get( '/api/v1/Car/Car:Commuter:' )
  Out[9]:
  {'cost': 500.0,
   'updated': '2017-09-06T03:42:51.389253+00:00',
   'created': '2017-09-06T03:42:51.389282+00:00',
   'name': 'Commuter',
   'model': '/api/v1/Car/Model:4:',
   'owner': '/api/v1/User/User:bob:'}

Now we can see the car, let's sell it to Sally.  We do that by calling the sell
action on that car::

  In [10]: conn.call( '/api/v1/Car/Car:Commuter:(sell)', { 'to': '/api/v1/User/User:sally:' } )

Now we can try getting the car's detail::

  In [11]: conn.get( '/api/v1/Car/Car:Commuter:' )
  WARNING:root:cinp: Not Authorized
  ---------------------------------------------------------------------------
  NotAuthorized                             Traceback (most recent call last)
  <stack trace>

sure enough we don't own the car anymore, so we can't see it.
