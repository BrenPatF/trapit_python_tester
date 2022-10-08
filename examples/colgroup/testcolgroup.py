'''*************************************************************************************************
Name: testcolgroup.py                  Author: Brendan Furey                       Date: 08-Oct-2022

Code component in the Trapit Python Tester module, which has a utility function for unit testing
with the Math Function Unit Testing design pattern, and some examples of use.

    GitHub: https://github.com/BrenPatF/trapit_python_tester

The design pattern involves the use of JSON files for storing test scenario and metadata, with an
input file including expected results, and an output file that has the actual results merged in.

The unit test driver utility function (trapit.test_unit) is called as effectively the main function
of any specific unit test script. It reads the input JSON scenarios file, then loops over the
scenarios making calls to a function passed in as a parameter from the calling script. The function
acts as a 'pure' wrapper around calls to the unit under test. It is 'externally pure' in the sense
that it is deterministic, and interacts externally only via parameters and return value. Where the
unit under test reads inputs from file the wrapper writes them based on its parameters, and where
the unit under test writes outputs to file the wrapper reads them and passes them out in its return
value. Any file writing is reverted before exit. 

The utility function comes with a unit test script that uses the utility to test itself; there are
also two examples, each with main script and unit test script.

Unit testing follows the Math Function Unit Testing design pattern, as described in:

    Trapit JavaScript Tester: https://github.com/BrenPatF/trapit_nodejs_tester#trapit

The above JavaScript project includes a utility to format the output JSON files as HTML pages and
plain text.
====================================================================================================
|  Main/Test       |  Unit Module |  Notes                                                         |
|==================================================================================================|
|  mainhelloworld  |              |  Hello World program implemented as a pure function to allow   |
|  testhelloworld  |  helloworld  |  for unit testing as a simple edge case                        |
|------------------|--------------|----------------------------------------------------------------|
|  maincolgroup    |  utils_cg    |  Simple file-reading and group-counting module, with logging   |
| *testcolgroup*   |  colgroup    |  to file. Example of testing impure units, and failing test    |
|------------------|--------------|----------------------------------------------------------------|
|  testtrapit      |  trapit      |  Unit test package with test driver utility, and test script   |
|                  |              |  that uses the utility to test itself                          |
====================================================================================================

This file is a unit test script for a simple file-reading and group-counting module, with logging to 
file. Note that this example has two deliberate errors to show how these are handled.

To run from root folder:

$ py examples/colgroup/testcolgroup.py

*************************************************************************************************'''
import sys, os
from datetime import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import trapit, colgroup as cg

ROOT = os.path.dirname(__file__) + '\\'
DELIM = '|'

INPUT_JSON,             OUTPUT_JSON,                INPUT_FILE,            LOG_FILE                  = \
ROOT + 'colgroup.json', ROOT + 'colgroup_out.json', ROOT + 'ut_group.csv', ROOT + 'ut_group.csv.log'

GRP_LOG,   GRP_SCA,   GRP_LIN, GRP_LAI,    GRP_SBK,     GRP_SBV       = \
'Log',     'Scalars', 'Lines', 'listAsIs', 'sortByKey', 'sortByValue'

def from_CSV(csv,  # string of delimited values
             col): # 0-based column index
    return csv.split(DELIM)[col]
def join_tuple(t): # 2-tuple
    return t[0] + DELIM + str(t[1])

def setup(inp): # input groups object
    with open(INPUT_FILE, 'w') as infile:
        infile.write('\n'.join(inp[GRP_LIN]))
    if (len(inp[GRP_LOG]) > 0):
        with open(LOG_FILE, 'w') as logfile:
            logfile.write('\n'.join(inp[GRP_LOG]) + '\n')
    return cg.ColGroup(INPUT_FILE, from_CSV(inp[GRP_SCA][0], 0), from_CSV(inp[GRP_SCA][0], 1))

def teardown():
    os.remove(INPUT_FILE)
    os.remove(LOG_FILE)

def purely_wrap_unit(inp_groups): # input groups object
    col_group   = setup(inp_groups)
    with open(LOG_FILE, 'r') as logfile:
        logstr = logfile.read()
    lines_array = logstr.split('\n')
    lastLine   = lines_array[len(lines_array) - 2]
    text       = lastLine
    date       = lastLine[0:19]
    logDate    = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    now        = datetime.now()
    diffDate   = (now - logDate).microseconds / 1000

    teardown()
    return {
        GRP_LOG : [str((len(lines_array) - 1)) + DELIM + str(diffDate) + DELIM + text.replace("\\", "-")],
        GRP_LAI : [str(len(col_group.list_as_is()))],
        GRP_SBK : list(map(join_tuple, col_group.sort_by_key())),
        GRP_SBV : list(map(join_tuple, col_group.sort_by_value_lambda()))
    }
trapit.test_unit(INPUT_JSON, OUTPUT_JSON, purely_wrap_unit)
