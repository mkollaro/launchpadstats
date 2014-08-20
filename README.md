Stackalytics CLI
================

Get the Stackalytics data and create CSV tables out of them. The CSV output
uses `;` as a delimiter.

Each section in the configuration file corresponds to a table name, which can
have a certain table type and overwrite the default values. Currently
implemented table types are *group-metrics* and *user-metrics*.

## Examples:

With the *group-metrics* table type (specified in the default `config.ini`
file):

    $ stackalyticscli --table-name group-summary
    metric/release; havana; juno; icehouse
    drafted_blueprint_count; 2; 1; 0
    completed_blueprint_count; 1; 1; 1
    filed_bug_count; 53; 50; 45
    resolved_bug_count; 9; 6; 7
    sum; 65; 58; 53

Example with the *user-metrics* table type:

    $ stackalyticscli --table-name user-metrics-havana
    user/metric; drafted_blueprint_count; completed_blueprint_count; filed_bug_count; resolved_bug_count; commit_count; reviews (-2, -1, +1, +2, A)
    mkollaro; 1; 0; 3; 1; 9; (0, 6, 12, 0, 0)
    psedlak; 0; 1; 0; 0; 9; (0, 9, 19, 0, 0)
    afazekas; 1; 0; 48; 8; 82; (2, 57, 83, 439, 66)


## Usage

For more information, look into the `config.ini` table.

    usage: stackalyticscli [-h] [-v] [-c CONFIG] [-t TABLE_NAME]

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
