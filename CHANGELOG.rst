0.6.0 2019-04-06
----------------

* Remove deprecated features, this renders this version incompatible
  with Quart 0.6.X releases - please use the 0.5.X Hypercorn releases.
* Bugfix accept bind definitions as a single string (alongside a list
  of strings).
* Add a LifespanTimeout Exception to better communicate the failure.
* Stop supporting Python 3.6, support only 3.7 or better.
* Add an SSL handshake timeout, fixing a potential DOS weakness.
* Pause reading during h11 pipelining, fixing a potential DOS weakness.
* Add the spec_version to the scope.
* Added check for supported ssl versions.
* Support ASGI 3.0, with ASGI 2.0 also supported for the time being.
* Support serving on insecure binds alongside secure binds, thereby
  allowing responses that redirect HTTP to HTTPS.
* Don't propagate access logs.

0.5.4 2019-04-06
----------------

* Bugfix correctly support the ASGI specification; headers an
  subprotocol support on WebSocket acceptance.
* Bugfix ensure the response headers are correctly built, ensuring
  they have lowercase names.
* Bugfix reloading when invocated as python -m hypercorn.
* Bugfix RESUSE -> REUSE typo.

0.5.3 2019-02-24
----------------

* Bugfix reloading on both Windows and Linux.
* Bugfix WebSocket unbounded memory usage.
* Fixed import from deprecated trio.ssl.

0.5.2 2019-02-03
----------------

* Bugfix ensure stream is not closed when reseting.

0.5.1 2019-01-29
----------------

* Bugfix mark the task started after the server starts.
* Bugfix ensure h11 connections are closed.
* Bugfix ensure h2 streams are closed/reset.

0.5.0 2019-01-24
----------------

* Add flag to control SSL verify mode (--verify-mode).
* Allow the SSL Verify Flags to be specified in the config.
* Add an official API for using Hypercorn programmatically::

    async def serve(app: Type[ASGIFramework], config: Config) -> None:

    asyncio.run(serve(app, config))
    trio.run(serve, app, config)

* Add the ability to bind to multiple sockets::

    hypercorn --bind '0.0.0.0:5000' --bind '[::]:5000' ...

* Bugfix default port is now 8000 not 5000,
* Bugfix ensure that h2c upgrade requests work.
* Support requests that assume HTTP/2.
* Allow the ALPN protocols to be configured.
* Allow the access logger class to be customised.
* Change websocket access logging to be after the handshake.
* Bugfix ensure there is no race condition in lifespan startup.
* Bugfix don't crash or log on SSL handshake failures.
* Initial working h2 Websocket support RFC 8441.
* Bugfix support reloading on Windows machines.

0.4.6 2019-01-01
----------------

* Bugfix EOF handling for websocket connections.
* Bugfix Introduce a random delay between worker starts on Windows.

0.4.5 (Not Released)
--------------------

An issue with incorrect tags lead to this being pulled from PyPI.

0.4.4 2018-12-28
----------------

* Bugfix ensure on timeout the connection is closed.
* Bugfix ensure Trio h2 connections timeout when idle.
* Bugfix flow window updates to connection window.
* Bugfix ensure ASGI framework errors are logged.

0.4.3 2018-12-16
----------------

* Bugfix ensure task cancellation works on Python 3.6
* Bugfix task cancellation warnings

0.4.2 2018-11-13
----------------

* Bugfix allow SSL setting to be configured in a file

0.4.1 2018-11-12
----------------

* Bugfix uvloop argument usage
* Bugfix lifespan not supported error
* Bugfix downgrade logging to warning for no lifespan support

0.4.0 2018-11-11
----------------

* Introduce a worker-class configuration option. Note that the ``-k``
  cli option is now mapped to ``-w`` to match Gunicorn. ``-k`` for the
  worker class and ``-w`` for the number of workers. Note also that
  ``--uvloop`` is deprecated and replaced with ``-k uvloop``.
* Add a trio worker, ``-k trio`` to run trio or neutral ASGI
  applications. This worker supports HTTP/1, HTTP/2 and
  websockets. Note trio must be installed, ideally via the Hypercorn
  ``trio`` extra requires.
* Handle application failures with a 500 response if no (partial)
  response has been sent.
* Handle application failures with a 500 HTTP or 1006 websocket
  response depending on upgrade acceptance.
* Bugfix a race condition establishing the client/server address.
* Bugfix don't create an unpickleable (on windows) ssl context in the
  master worker, rather do so in each worker. This should support
  multiple workers on windows.
* Support the ASGI lifespan protocol (with backwards compatibility to
  the provisional protocol for asyncio & uvloop workers).
* Bugfix cleanup all tasks on asyncio & uvloop workers.
* Adopt Black for code formatting.
* Bugfix h2 don't try to send negative or zero bytes.
* Bugfix h2 don't send nothing.
* Bugfix restore the single worker behaviour of being a single
  process.
* Bugfix Ensure sending doesn't error when the connection is closed.
* Allow configuration of h2 max concurrent streams and max header list
  size.
* Introduce a backlog configuration option.

0.3.2 2018-10-04
----------------

* Bugfix cope with a None loop argument to run_single.
* Add a new logo.

0.3.1 2018-09-25
----------------

* Bugfix ensure the event-loop is configured before the app is
  created.
* Bugfix import error on windows systems.

0.3.0 2018-09-23
----------------

* Add ability to specify a file logging target.
* Support serving on a unix domain socket or a file descriptor.
* Alter keep alive timeout to require a request to be considered
  active (rather than just data). This mitigates a HTTP/2 DOS attack.
* Improve the SSL configuration, including NPN protocols, compression
  suppression, and disallowed SSL versions for HTTP/2.
* Allow the h2 max inbound frame size to be configured.
* Add a PID file to be specified and used.
* Upgrade to the latest wsproto and h11 libraries.
* Bugfix propagate TERM signal to workers.
* Bugfix ensure hosting information is printed when running from the
  command line.

0.2.4 2018-08-05
----------------

* Bugfix don't force the ALPN protocols
* Bugfix shutdown on reload
* Bugfix set the default log level if std(out/err) is used
* Bugfix HTTP/1.1 -> HTTP/2 Upgrade requests
* Bugfix correctly handle TERM and INT signals
* Bugix loop usage and creation for multiple workers

0.2.3 2018-07-08
----------------

* Bugfix setting ssl from config files
* Bugfix ensure modules aren't set as config values
* Bugfix use the wsgiref datetime formatter (accurate Date headers).
* Bugfix query_string value ASGI conformance

0.2.2 2018-06-27
----------------

* Bugfix ensure that hypercorn as a command line (entry point) works.

0.2.1 2018-06-26
----------------

* Bugfix ensure CLI defaults don't override configuration settings.

0.2.0 2018-06-24
----------------

* Bugfix correct ASGI extension names & definitions
* Bugfix don't log without a target to log to.
* Bugfix allow SSL values to be loaded from command line args.
* Bugfix avoid error when logging with IPv6 bind.
* Don't send b'', rather no-op for performance.
* Support IPv6 binding.
* Add the ability to load configuration from python or TOML files.
* Unblock on connection close (send becomes a no-op).
* Bugfix send the close message only once.
* Bugfix correct scope client and server values.
* Implement root_path scope via config variable.
* Stop creating event-loops, rather use the default/existing.

0.1.0 2018-06-02
----------------

* Released initial alpha version.
