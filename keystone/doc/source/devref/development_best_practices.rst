..
      Copyright 2011-2012 OpenStack Foundation
      All Rights Reserved.

      Licensed under the Apache License, Version 2.0 (the "License"); you may
      not use this file except in compliance with the License. You may obtain
      a copy of the License at

          http://www.apache.org/licenses/LICENSE-2.0

      Unless required by applicable law or agreed to in writing, software
      distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
      WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
      License for the specific language governing permissions and limitations
      under the License.

==============
Best Practices
==============

Setting up Keystone
===================

Get your development environment set up according to
:doc:`development.environment`. It is recommended that you install
Keystone into a virtualenv.


Configuring Keystone
====================

Keystone requires a configuration file. There is a sample configuration file
that can be used to get started:

.. code-block:: bash

    $ cp etc/keystone.conf.sample etc/keystone.conf

The defaults are enough to get you going, but you can make any changes if
needed.


Running Keystone
================

To run the Keystone Admin and API server instances, use:

.. code-block:: bash

    $ uwsgi --http 127.0.0.1:35357 --wsgi-file $(which keystone-wsgi-admin)

This runs Keystone with the configuration the etc/ directory of the project.
See :doc:`../configuration` for details on how Keystone is configured. By default,
Keystone is configured with SQL backends.


Initializing Keystone
=====================

Before using keystone, it is necessary to create the database tables and ensures
the database schemas are up to date, perform the following:

.. code-block:: bash

    $ keystone-manage db_sync

If the above commands result in a ``KeyError``, or they fail on a
``.pyc`` file with the message, ``You can only have one Python script per
version``, then it is possible that there are out-of-date compiled Python
bytecode files in the Keystone directory tree that are causing problems. This
can occur if you have previously installed and ran older versions of Keystone.
These out-of-date files can be easily removed by running a command like the
following from the Keystone root project directory:

.. code-block:: bash

    $ find . -name "*.pyc" -delete

Initial Sample Data
-------------------

There is an included script which is helpful in setting up some initial sample
data for use with keystone:

.. code-block:: bash

    $ ADMIN_PASSWORD=s3cr3t tools/sample_data.sh

Once run, you can see the sample data that has been created by using the
`python-openstackclient`_ command-line interface:

.. code-block:: bash

    $ export OS_USERNAME=admin
    $ export OS_PASSWORD=s3cr3t
    $ export OS_PROJECT_NAME=admin
    $ export OS_USER_DOMAIN_ID=default
    $ export OS_PROJECT_DOMAIN_ID=default
    $ export OS_IDENTITY_API_VERSION=3
    $ export OS_AUTH_URL=http://localhost:5000/v3
    $ openstack user list

The `python-openstackclient`_ can be installed using the following:

.. code-block:: bash

    $ pip install python-openstackclient

Interacting with Keystone
=========================

You can also interact with keystone through its REST API. There is a Python
keystone client library `python-keystoneclient`_ which interacts exclusively
through the REST API, and a command-line interface `python-openstackclient`_
command-line interface.

.. _`python-keystoneclient`: https://git.openstack.org/cgit/openstack/python-keystoneclient
.. _`python-openstackclient`: https://git.openstack.org/cgit/openstack/python-openstackclient

Building the Documentation
==========================

The documentation is generated with Sphinx using the tox command. To create HTML
docs and man pages:

.. code-block:: bash

    $ tox -e docs

The results are in the ``doc/build/html`` and ``doc/build/man`` directories
respectively.


Generating a new Sample Config File
===================================

Keystone's sample configuration file ``etc/keystone.conf.sample`` is automatically
generated based upon all of the options available within Keystone. These options
are sourced from the many files around Keystone as well as some external libraries.

The sample configuration file will be updated as the end of the development
cycle approaches. Developers should *NOT* generate the config file and propose
it as part of their patches, this will cause unnecessary conflicts.

To generate a new sample configuration to see what it looks like, run:

.. code-block:: bash

    $ tox -egenconfig -r

The tox command will place an updated sample config in ``etc/keystone.conf.sample``.

If there is a new external library (e.g. ``oslo.messaging``) that utilizes the
``oslo.config`` package for configuration, it can be added to the list of libraries
found in ``config-generator/keystone.conf``.


Release Notes
=============

The Keystone team uses `reno <https://docs.openstack.org/developer/reno/usage.html>`_
to generate release notes. These are important user-facing documents that must
be included when a user-facing change is performed. A release note should be
included in the same patch the work is being performed.

For more information on how and when to create release notes, see the
`project-team-guide <https://docs.openstack.org/project-team-guide/release-management.html#how-to-add-new-release-notes>`_.

Testing Keystone
================

Running Tests
-------------

Before running tests, you should have ``tox`` installed and available in your
environment (in addition to the other external dependencies in
:doc:`development.environment`):

.. code-block:: bash

    $ pip install tox

.. NOTE::

    You may need to perform both the above operation and the next inside a
    python virtualenv, or prefix the above command with ``sudo``, depending on
    your preference.

To execute the full suite of tests maintained within Keystone, simply run:

.. code-block:: bash

    $ tox

This iterates over multiple configuration variations, and uses external
projects to do light integration testing to verify the Identity API against
other projects.

.. NOTE::

    The first time you run ``tox``, it will take additional time to build
    virtualenvs. You can later use the ``-r`` option with ``tox`` to rebuild
    your virtualenv in a similar manner.

To run tests for one or more specific test environments (for example, the most
common configuration of Python 2.7 and PEP-8), list the environments with the
``-e`` option, separated by spaces:

.. code-block:: bash

    $ tox -e py27,pep8

See ``tox.ini`` for the full list of available test environments.

Running with PDB
~~~~~~~~~~~~~~~~

Using PDB breakpoints with tox and testr normally doesn't work since the tests
just fail with a BdbQuit exception rather than stopping at the breakpoint.

To run with PDB breakpoints during testing, use the ``debug`` tox environment
rather than ``py27``. Here's an example, passing the name of a test since
you'll normally only want to run the test that hits your breakpoint:

.. code-block:: bash

    $ tox -e debug keystone.tests.unit.test_auth.AuthWithToken.test_belongs_to

For reference, the ``debug`` tox environment implements the instructions
here: https://wiki.openstack.org/wiki/Testr#Debugging_.28pdb.29_Tests

Disabling Stream Capture
~~~~~~~~~~~~~~~~~~~~~~~~

The stdout, stderr and log messages generated during a test are captured and
in the event of a test failure those streams will be printed to the terminal
along with the traceback. The data is discarded for passing tests.

Each stream has an environment variable that can be used to force captured
data to be discarded even if the test fails: `OS_STDOUT_CAPTURE` for stdout,
`OS_STDERR_CAPTURE` for stderr and `OS_LOG_CAPTURE` for logging. If the value
of the environment variable is not one of (True, true, 1, yes) the stream will
be discarded. All three variables default to 1.

For example, to discard logging data during a test run:

.. code-block:: bash

    $ OS_LOG_CAPTURE=0 tox -e py27

Test Structure
--------------

Not all of the tests in the ``keystone/tests/unit`` directory are strictly unit
tests. Keystone intentionally includes tests that run the service locally and
drives the entire configuration to achieve basic functional testing.

For the functional tests, an in-memory key-value store or in-memory SQLite
database is used to keep the tests fast.

Within the tests directory, the general structure of the backend tests is a
basic set of tests represented under a test class, and then subclasses of those
tests under other classes with different configurations to drive different
backends through the APIs.

For example, ``test_backend.py`` has a sequence of tests under the class
:class:`~keystone.tests.unit.test_backend.IdentityTests` that will work with
the default drivers as configured in this project's etc/ directory.
``test_backend_sql.py`` subclasses those tests, changing the configuration by
overriding with configuration files stored in the ``tests/unit/config_files``
directory aimed at enabling the SQL backend for the Identity module.

:class:`keystone.tests.unit.test_v2_keystoneclient.ClientDrivenTestCase`
uses the installed python-keystoneclient, verifying it against a temporarily
running local keystone instance to explicitly verify basic functional testing
across the API.

Testing Schema Migrations
-------------------------

The application of schema migrations can be tested using SQLAlchemy Migrate’s
built-in test runner, one migration at a time.

.. WARNING::

    This may leave your database in an inconsistent state; attempt this in
    non-production environments only!

This is useful for testing the *next* migration in sequence (both forward &
backward) in a database under version control:

.. code-block:: bash

    $ python keystone/common/sql/migrate_repo/manage.py test \
    --url=sqlite:///test.db \
    --repository=keystone/common/sql/migrate_repo/

This command references to a SQLite database (test.db) to be used. Depending on
the migration, this command alone does not make assertions as to the integrity
of your data during migration.


Writing Tests
-------------

To add tests covering all drivers, update the base test class in
``test_backend.py``.

.. NOTE::

    The structure of backend testing is in transition, migrating from having
    all classes in a single file (test_backend.py) to one where there is a
    directory structure to reduce the size of the test files. See:

        - :mod:`keystone.tests.unit.backend.role`
        - :mod:`keystone.tests.unit.backend.domain_config`

To add new drivers, subclass the ``test_backend.py`` (look towards
``test_backend_sql.py`` for examples) and update the
configuration of the test class in ``setUp()``.


Further Testing
---------------

devstack_ is the *best* way to quickly deploy Keystone with the rest of the
OpenStack universe and should be critical step in your development workflow!

You may also be interested in either the
`OpenStack Continuous Integration Infrastructure`_ or the
`OpenStack Integration Testing Project`_.

.. _devstack: https://docs.openstack.org/developer/devstack/
.. _OpenStack Continuous Integration Infrastructure: https://docs.openstack.org/infra/system-config
.. _OpenStack Integration Testing Project: https://git.openstack.org/cgit/openstack/tempest


LDAP Tests
----------

LDAP has a fake backend that performs rudimentary operations.  If you
are building more significant LDAP functionality, you should test against
a live LDAP server.  Devstack has an option to set up a directory server for
Keystone to use.  Add ldap to the ``ENABLED_SERVICES`` environment variable,
and set environment variables ``KEYSTONE_IDENTITY_BACKEND=ldap`` and
``KEYSTONE_CLEAR_LDAP=yes`` in your ``localrc`` file.

The unit tests can be run against a live server with
``keystone/tests/unit/test_ldap_livetest.py`` and
``keystone/tests/unit/test_ldap_pool_livetest.py``. The default password is
``test`` but if you have installed devstack with a different LDAP password,
modify the file ``keystone/tests/unit/config_files/backend_liveldap.conf`` and
``keystone/tests/unit/config_files/backend_pool_liveldap.conf`` to reflect your
password.

.. NOTE::
    To run the live tests you need to set the environment variable
    ``ENABLE_LDAP_LIVE_TEST`` to a non-negative value.


"Work in progress" Tests
------------------------

Work in progress (WIP) tests are very useful in a variety of situations
including:

* During a TDD process they can be used to add tests to a review while
  they are not yet working and will not cause test failures. (They should
  be removed before the final merge.)
* Often bug reports include small snippets of code to show broken
  behaviors. Some of these can be converted into WIP tests that can later
  be worked on by a developer. This allows us to take code that can be
  used to catch bug regressions and commit it before any code is
  written.

The :func:`keystone.tests.unit.utils.wip` decorator can be used to mark a test
as WIP. A WIP test will always be run. If the test fails then a TestSkipped
exception is raised because we expect the test to fail. We do not pass
the test in this case so that it doesn't count toward the number of
successfully run tests. If the test passes an AssertionError exception is
raised so that the developer knows they made the test pass. This is a
reminder to remove the decorator.

The :func:`~keystone.tests.unit.utils.wip` decorator requires that the author
provides a message. This message is important because it will tell other
developers why this test is marked as a work in progress. Reviewers will
require that these messages are descriptive and accurate.

.. NOTE::
    The :func:`~keystone.tests.unit.utils.wip` decorator is not a replacement for
    skipping tests.

.. code-block:: python

    @wip('waiting on bug #000000')
    def test():
        pass

.. NOTE::
   Another strategy is to not use the wip decorator and instead show how the
   code currently incorrectly works. Which strategy is chosen is up to the
   developer.


Developing ``doctor`` checks
============================

As noted in the section above, keystone's management CLI provides various tools
for administrating OpenStack Identity. One of those tools is called
``keystone-manage doctor`` and it is responsible for performing health checks
about the deployment. If ``keystone-manage doctor`` detects a symptom, it
will provide the operator with suggestions to improve the overall health of the
deployment. This section is dedicated to documenting how to write symptoms for
``doctor``.

The ``doctor`` tool consists of a list of symptoms. Each symptom is something
that we can check against, and provide a warning for if we detect a
misconfiguration. The ``doctor`` module is located in
:py:mod:`keystone.cmd.doctor`. The current checks are based heavily on
inspecting configuration values. As a result, many of the submodules within the
``doctor`` module are named after the configuration section for the symptoms
they check. For example, if we want to ensure the ``keystone.conf [DEFAULT]
max_token_size`` option is properly configured for whatever ``keystone.conf
[token] provider`` is set to, we can place that symptom in a module called
:py:mod:`keystone.cmd.doctor.tokens`. The symptom will be loaded by
importing the ``doctor`` module, which is done when ``keystone-manage doctor``
is invoked from the command line. When adding new symptoms, it's important to
remember to add new modules to the ``SYMPTOM_MODULES`` list in
:py:mod:`keystone.cmd.doctor.__init__`. Doing that will ensure ``doctor``
discovers properly named symptoms when executed.

Now that we know symptoms are organized according to configuration sections,
and how to add them, how exactly do we write a new symptom? ``doctor`` will
automatically discover new symptoms by inspecting the methods of each symptom
module (i.e. ``SYMPTOM_MODULES``). If a method declaration starts with
``def symptom_`` it is considered a symptom that ``doctor`` should check for,
and it should be run. The naming of the symptom, or method name, is extremely
important since ``doctor`` will use it to describe what it's doing to whoever
runs ``doctor``. In addition to a well named method, we also need to provide a
complete documentation string for the method. If ``doctor`` detects a symptom,
it will use the method's documentation string as feedback to the operator. It
should describe why the check is being done, why it was triggered, and possible
solutions to cure the symptom. For examples of this, see the existing symptoms
in any of ``doctor``'s symptom modules.

The last step is evaluating the logic within the symptom. As previously stated,
``doctor`` will check for a symptom if methods within specific symptom modules
make a specific naming convention. In order for ``doctor`` to suggest feedback,
it needs to know whether or not the symptom is actually present. We accomplish
this by making all symptoms return ``True`` when a symptom is present. When a
symptom evaluates to ``False``, ``doctor`` will move along to the next symptom
in the list since. If the deployment isn't suffering for a specific symptom,
``doctor`` should not suggest any actions related to that symptom (i.e. if
you have your cholesterol under control, why would a physician recommend
cholesterol medication if you don't need it).

To summarize:

- Symptoms should live in modules named according to the most relevant
  configuration section they apply to. This ensure we keep our symptoms
  organized, grouped, and easy to find.
- When writing symptoms for a new section, remember to add the module name to
  the ``SYMPTOM_MODULES`` list in :py:mod:`keystone.cmd.doctor.__init__`.
- Remember to use a good name for the symptom method signature and to prepend
  it with ``symptom_`` in order for it to be discovered automatically by
  ``doctor``.
- Symptoms have to evaluate to ``True`` in order to provide feedback to
  operators.
- Symptoms should have very thorough documentation strings that describe the
  symptom, side-effects of the symptom, and ways to remedy it.

For examples, feel free to run ``doctor`` locally using ``keystone-manage`` and
inspect the existing symptoms.

Database Migrations
===================

Starting with Newton, keystone supports upgrading both with and without
downtime. In order to support this, there are three separate migration
repositories (all under ``keystone/common/sql/``) that match the three phases
of an upgrade (schema expansion, data migration, and schema contraction):

``expand_repo``
    For additive schema modifications and triggers to ensure data is kept in
    sync between the old and new schema until the point when there are no
    keystone instances running old code.

``data_migration_repo``
    To ensure new tables/columns are fully populated with data from the old
    schema.

``contract_repo``
    Run after all old code versions have been upgraded to running the new code,
    so remove any old schema columns/tables that are not used by the new
    version of the code. Drop any triggers added in the expand phase.

All migrations are required to have a migration script in each of these repos,
each with the same version number (which is indicated by the first three digits
of the name of the script, e.g. ``003_add_X_table.py``). If there is no work to
do in a specific phase, then include a no-op migration to simply ``pass`` (in
fact the ``001`` migration in each of these repositories is a no-op migration,
so that can be used as a template).

.. NOTE::

    Since rolling upgrade support was added part way through the Newton cycle,
    some migrations had already been added to the legacy repository
    (``keystone/common/sql/migrate_repo``). This repository is now closed and
    no new migrations should be added (except for backporting of previous
    placeholders).

In order to support rolling upgrades, where two releases of keystone briefly
operate side-by-side using the same database without downtime, each phase of
the migration must adhere to following constraints:

These triggers should be removed in the contract phase. There are further
restrictions as to what can and cannot be included in migration scripts in each
phase:

Expand phase:
    Only additive schema changes are allowed, such as new columns, tables,
    indices, and triggers.

    Data insertion, modification, and removal is not allowed.

    Triggers must be created to keep data in sync between the previous release
    and the next release. Data written by the previous release must be readable
    by both the previous release and the next release. Data written by the next
    release must be readable by both the next release and the previous release.

    In cases it is not possible for triggers to maintain data integrity across
    multiple schemas, writing data should be forbidden using triggers.

Data Migration phase:
    Data is allowed to be inserted, updated, and deleted.

    No schema changes are allowed.

Contract phase:
    Only contractive schema changes are allowed, such as dropping or altering
    columns, tables, indices, and triggers.

    Data insertion, modification, and removal is not allowed.

    Triggers created during the expand phase must be dropped.

For more information on writing individual migration scripts refer to
`SQLAlchemy-migrate`_.

.. _SQLAlchemy-migrate: https://git.openstack.org/cgit/openstack/sqlalchemy-migrate


Filtering responsibilities between controllers and drivers
==========================================================

Keystone supports the specification of filtering on list queries as part of the
v3 identity API. By default these queries are satisfied in the controller
class when a controller calls the ``wrap_collection`` method at the end of a
``list_{entity}`` method.  However, to enable optimum performance, any driver
can implement some or all of the specified filters (for example, by adding
filtering to the generated SQL statements to generate the list).

The communication of the filter details between the controller level and its
drivers is handled by the passing of a reference to a Hints object,
which is a list of dicts describing the filters. A driver that satisfies a
filter must delete the filter from the Hints object so that when it is returned
to the controller level, it knows to only execute any unsatisfied
filters.

The contract for a driver for ``list_{entity}`` methods is therefore:

* It MUST return a list of entities of the specified type
* It MAY either just return all such entities, or alternatively reduce the
  list by filtering for one or more of the specified filters in the passed
  Hints reference, and removing any such satisfied filters. An exception to
  this is that for identity drivers that support domains, then they should
  at least support filtering by domain_id.

Entity list truncation by drivers
=================================

Keystone supports the ability for a deployment to restrict the number of
entries returned from ``list_{entity}`` methods, typically to prevent poorly
formed searches (e.g. without sufficient filters) from becoming a performance
issue.

These limits are set in the configuration file, either for a specific driver or
across all drivers.  These limits are read at the Manager level and passed into
individual drivers as part of the Hints list object. A driver should try and
honor any such limit if possible, but if it is unable to do so then it may
ignore it (and the truncation of the returned list of entities will happen at
the controller level).

Identity entity ID management between controllers and drivers
=============================================================

Keystone supports the option of having domain-specific backends for the
identity driver (i.e. for user and group storage), allowing, for example,
a different LDAP server for each domain. To ensure that Keystone can determine
to which backend it should route an API call, starting with Juno, the
identity manager will, provided that domain-specific backends are enabled,
build on-the-fly a persistent mapping table between Keystone Public IDs that
are presented to the controller and the domain that holds the entity, along
with whatever local ID is understood by the driver.  This hides, for instance,
the LDAP specifics of whatever ID is being used.

To ensure backward compatibility, the default configuration of either a
single SQL or LDAP backend for Identity will not use the mapping table,
meaning that public facing IDs will be the unchanged. If keeping these IDs
the same for the default LDAP backend is not required, then setting the
configuration variable ``backward_compatible_ids`` to ``False`` will enable
the mapping for the default LDAP driver, hence hiding the LDAP specifics of the
IDs being used.


Translated responses
====================

The Keystone server can provide error responses translated into the language in
the ``Accept-Language`` header of the request. In order to test this in your
development environment, there's a couple of things you need to do.

1. Build the message files. Run the following command in your keystone
   directory:

.. code-block:: bash

   $ python setup.py compile_catalog

This will generate .mo files like keystone/locale/[lang]/LC_MESSAGES/[lang].mo

2. When running Keystone, set the ``KEYSTONE_LOCALEDIR`` environment variable
   to the keystone/locale directory. For example:

.. code-block:: bash

    $ KEYSTONE_LOCALEDIR=/opt/stack/keystone/keystone/locale uwsgi --http 127.0.0.1:35357 --wsgi-file $(which keystone-wsgi-admin)


Now you can get a translated error response:

.. code-block:: bash

 $ curl -s -H "Accept-Language: zh" http://localhost:5000/notapath | python -mjson.tool
 {
     "error": {
         "code": 404,
         "message": "\u627e\u4e0d\u5230\u8cc7\u6e90\u3002",
         "title": "Not Found"
     }
 }


Caching Layer
=============

The caching layer is designed to be applied to any ``manager`` object within Keystone
via the use of the ``on_arguments`` decorator provided in the ``keystone.common.cache``
module.  This decorator leverages `dogpile.cache`_ caching system to provide a flexible
caching backend.

It is recommended that each of the managers have an independent toggle within the config
file to enable caching.  The easiest method to utilize the toggle within the
configuration file is to define a ``caching`` boolean option within that manager's
configuration section (e.g. ``identity``).  Once that option is defined you can
pass function to the ``on_arguments`` decorator with the named argument ``should_cache_fn``.
In the ``keystone.common.cache`` module, there is a function called ``should_cache_fn``,
which will provide a reference, to a function, that will consult the global cache
``enabled`` option as well as the specific manager's caching enable toggle.

    .. NOTE::
        If a section-specific boolean option is not defined in the config section specified when
        calling ``should_cache_fn``, the returned function reference will default to enabling
        caching for that ``manager``.

Example use of cache and ``should_cache_fn`` (in this example, ``token`` is the manager):

.. code-block:: python

    from keystone.common import cache
    SHOULD_CACHE = cache.should_cache_fn('token')

    @cache.on_arguments(should_cache_fn=SHOULD_CACHE)
    def cacheable_function(arg1, arg2, arg3):
        ...
        return some_value

With the above example, each call to the ``cacheable_function`` would check to see if
the arguments passed to it matched a currently valid cached item.  If the return value
was cached, the caching layer would return the cached value; if the return value was
not cached, the caching layer would call the function, pass the value to the ``SHOULD_CACHE``
function reference, which would then determine if caching was globally enabled and enabled
for the ``token`` manager.  If either caching toggle is disabled, the value is returned but
not cached.

It is recommended that each of the managers have an independent configurable time-to-live (TTL).
If a configurable TTL has been defined for the manager configuration section, it is possible to
pass it to the ``cache.on_arguments`` decorator with the named-argument ``expiration_time``.  For
consistency, it is recommended that this option be called ``cache_time`` and default to ``None``.
If the ``expiration_time`` argument passed to the decorator is set to ``None``, the expiration
time will be set to the global default (``expiration_time`` option in the ``[cache]``
configuration section.

Example of using a section specific ``cache_time`` (in this example, ``identity`` is the manager):

.. code-block:: python

    from keystone.common import cache
    SHOULD_CACHE = cache.should_cache_fn('identity')

    @cache.on_arguments(should_cache_fn=SHOULD_CACHE,
                        expiration_time=CONF.identity.cache_time)
    def cachable_function(arg1, arg2, arg3):
        ...
        return some_value

For cache invalidation, the ``on_arguments`` decorator will add an ``invalidate`` method
(attribute) to your decorated function.  To invalidate the cache, you pass the same arguments
to the ``invalidate`` method as you would the normal function.

Example (using the above cacheable_function):

.. code-block:: python

    def invalidate_cache(arg1, arg2, arg3):
        cacheable_function.invalidate(arg1, arg2, arg3)

.. WARNING::
    The ``on_arguments`` decorator does not accept keyword-arguments/named arguments.  An
    exception will be raised if keyword arguments are passed to a caching-decorated function.

.. NOTE::
    In all cases methods work the same as functions except if you are attempting to invalidate
    the cache on a decorated bound-method, you need to pass  ``self`` to the ``invalidate``
    method as the first argument before the arguments.

.. _`dogpile.cache`: http://dogpilecache.readthedocs.org/


dogpile.cache based MongoDB (NoSQL) backend
-------------------------------------------

The ``dogpile.cache`` based MongoDB backend implementation allows for various MongoDB
configurations, e.g., standalone, a replica set, sharded replicas, with or without SSL,
use of TTL type collections, etc.

Example of typical configuration for MongoDB backend:

.. code-block:: python

    from dogpile.cache import region

    arguments = {
        'db_hosts': 'localhost:27017',
        'db_name': 'ks_cache',
        'cache_collection': 'cache',
        'username': 'test_user',
        'password': 'test_password',

        # optional arguments
        'son_manipulator': 'my_son_manipulator_impl'
    }

    region.make_region().configure('keystone.cache.mongo',
                                   arguments=arguments)

The optional `son_manipulator` is used to manipulate custom data type while its saved in
or retrieved from MongoDB. If the dogpile cached values contain built-in data types and no
custom classes, then the provided implementation class is sufficient. For further details, refer
http://api.mongodb.org/python/current/examples/custom_type.html#automatic-encoding-and-decoding

Similar to other backends, this backend can be added via Keystone configuration in
``keystone.conf``::

    [cache]
    # Global cache functionality toggle.
    enabled = True

    # Referring to specific cache backend
    backend = keystone.cache.mongo

    # Backend specific configuration arguments
    backend_argument = db_hosts:localhost:27017
    backend_argument = db_name:ks_cache
    backend_argument = cache_collection:cache
    backend_argument = username:test_user
    backend_argument = password:test_password

This backend is registered in ``keystone.common.cache.core`` module. So, its usage
is similar to other dogpile caching backends as it implements the same dogpile APIs.
