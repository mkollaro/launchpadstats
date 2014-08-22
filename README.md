Stackalytics CLI
================

Get the Stackalytics data and create CSV or HTML tables out of them. The CSV
output uses `;` as a delimiter.

Each section in the configuration file corresponds to a table name, which can
have a certain table type and overwrite the default values. Currently
implemented table types are *group-metrics* and *user-metrics*.

## Examples:

With the *group-metrics* table type (specified in the default `config.ini`
file):

    $ launchpadstats --table-name group-summary
    metric/release; havana; juno; icehouse
    drafted_blueprint_count; 2; 1; 0
    completed_blueprint_count; 1; 1; 1
    filed_bug_count; 53; 50; 45
    resolved_bug_count; 9; 6; 7
    sum; 65; 58; 53

Example with the *user-metrics* table type:

    $ launchpadstats --table-name user-metrics-havana
    user/metric; drafted_blueprint_count; completed_blueprint_count; filed_bug_count; resolved_bug_count; commit_count; reviews (-2, -1, +1, +2, A)
    mkollaro; 1; 0; 3; 1; 9; (0, 6, 12, 0, 0)
    psedlak; 0; 1; 0; 0; 9; (0, 9, 19, 0, 0)
    afazekas; 1; 0; 48; 8; 82; (2, 57, 83, 439, 66)


## Usage

For more information, look into the `config.ini` table.

    usage: launchpadstats [-h] [-v] [-c CONFIG] [-t TABLE_NAME]

    Get Stackalytics data and create various types of tables out of them.

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         Show logging output
      -c CONFIG, --config CONFIG
                            Configuration file, by default use 'config.ini' in the
                            project directory
      -t TABLE_NAME, --table-name TABLE_NAME
                            Which section name in the config file to use, the
                            default value is 'DEFAULT'
      --output-format {csv,html}
                            What output format to use. Default is 'csv'.

## Configuration

Look into `config.ini` for an example.

### Table types
Currently implemented table types are *group-metrics* and *user-metrics*, which
you can specify in the `table-type` option.

* `group-metrics` -
Show the metrics of the group per release in columns. The *group* is defined as
the list of people passed in the `people` option.
One metric per line is shown, releases are columns.
Shows a sum of the metrics per release.

* `user-metrics` -
For each person in the `people` option, display a line with their
metrics (given in the `metrics` option), summed up in all the releases
specified in `releases`.


### Possible metrics
These are the values you can give to the option `metrics`.

* `email_count`
* `loc` - lines of code
* `commit_count`
* `drafted_blueprint_count`
* `completed_blueprint_count`
* `reviews` - shows in the format (-2, -1, +1, +2, A)
* `filed_bug_count`
* `resolved_bug_count`
* `patch_set_count`

### Other options
* option `people` - list of user IDs, which should be the same as the `user_id`
  parameter on the Stackalytics webpage, i.e.
  `http://stackalytics.com/?user_id=username`
* option `releases` - list of OpenStack releases, in lower case
  (e.g. havana,icehouse,juno,..)

The options given in the `DEFAULT` section can be used as short-cuts in other
options.
