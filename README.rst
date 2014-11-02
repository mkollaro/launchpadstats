LaunchpadStats
==============

Get the `Launchpad <https://launchpad.net/>`__ statistics trough
`Stackalytics <http://stackalytics.com/>`__ and create CSV or HTML
tables out of them. The CSV output uses ``;`` as a delimiter.

Each section in the configuration file corresponds to a table name - the
name can be anything and does not have any effect on the table
structure. A table can have a certain type and overwrite the default
values. Currently implemented table types are *group-metrics* and
*user-metrics*.

Examples
--------

With the *group-metrics* table type, using the example configuration
file provided:

::

    $ launchpadstats -c ./config.ini --table-name tableA
    metric/release; havana; icehouse; juno
    drafted_blueprint_count; 2; 0; 1
    completed_blueprint_count; 1; 1; 1
    filed_bug_count; 55; 45; 64
    resolved_bug_count; 9; 7; 10
    sum; 67; 53; 76

Example with the *user-metrics* table type:

::

    $ launchpadstats -c ./config.ini --table-name user-metrics-havana
    user/metric; drafted_blueprint_count; completed_blueprint_count; filed_bug_count; resolved_bug_count; commit_count; reviews (-2, -1, +1, +2, A)
    mkollaro; 1; 0; 3; 1; 9; (0, 6, 12, 0, 0)
    psedlak; 0; 1; 0; 0; 9; (0, 9, 19, 0, 0)
    afazekas; 1; 0; 48; 8; 82; (2, 57, 83, 439, 66)

Create a single HTML page with all the tables (each section is
considered a table, except the section *DEFAULT*):

::

    $ launchpadstats -c ./config.ini -o html > everything.html


Configuration
-------------

Look into ``config.ini`` for an example.

Table types
~~~~~~~~~~~

Currently implemented table types are *group-metrics* and
*user-metrics*, which you can specify in the ``table-type`` option.

-  ``group-metrics`` - Show the metrics of the group per release in
   columns. The *group* is defined as the list of people passed in the
   ``people`` option. One metric per line is shown, releases are
   columns. Shows a sum of the metrics per release.

-  ``user-metrics`` - For each person in the ``people`` option, display
   a line with their metrics (given in the ``metrics`` option), summed
   up in all the releases specified in ``releases``.

Possible metrics
~~~~~~~~~~~~~~~~

These are the values you can give to the option ``metrics``.

-  ``email_count``
-  ``loc`` - lines of code
-  ``commit_count``
-  ``drafted_blueprint_count``
-  ``completed_blueprint_count``
-  ``reviews`` - shows in the format (-2, -1, +1, +2, A)
-  ``filed_bug_count``
-  ``resolved_bug_count``
-  ``patch_set_count``

Other options
~~~~~~~~~~~~~

-  option ``people`` - list of user IDs, which should be the same as the
   ``user_id`` parameter on the Stackalytics webpage, i.e.
   ``http://stackalytics.com/?user_id=username``
-  option ``releases`` - list of OpenStack releases, in lower case (e.g.
   havana,icehouse,juno,..)
-  option ``description`` - shown in the output as a header (in html) or
   comment (in csv) before the table

The options given in the ``DEFAULT`` section can be used as short-cuts
in other options.
