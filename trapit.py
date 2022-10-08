'''*************************************************************************************************
Name: trapit.py                        Author: Brendan Furey                       Date: 08-Oct-2022

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
|  testcolgroup    |  colgroup    |  to file. Example of testing impure units, and failing test    |
|------------------|--------------|----------------------------------------------------------------|
|  testtrapit      | *trapit*     |  Unit test package with test driver utility, and test script   |
|                  |              |  that uses the utility to test itself                          |
====================================================================================================

This file contains the trapit entry point function test_unit
*************************************************************************************************'''
import json
INP, OUT, EXP, ACT = 'inp', 'out', 'exp', 'act'
'''*************************************************************************************************

 _out_groups: Local function embeds input expected and acttual lists of values by group with 'exp'
                 and 'act' key objects

*************************************************************************************************'''
def _out_groups(exp_obj,  # expected value object with lists keyed by group name
                act_obj): # actual value object with lists keyed by group name

    exp_act_obj = {}
    for o in exp_obj:
        exp_act_obj[o] = {
            EXP : exp_obj[o],
            ACT : act_obj[o]
        }
    return exp_act_obj

'''*************************************************************************************************

test_unit: Unit test driver function, called like this from a script that defines the function 
           purely_wrap_unit:

                test_unit(INP_JSON, OUT_JSON, purely_wrap_unit}

           This function reads metadata and scenario data from an input JSON file, calls a wrapper
           function passed as a parameter within a loop over scenarios, and writes an output JSON
           file based on the input file but with the actual outputs merged in. This can then be
           processed using the npm Trapit package to produce formatted test results.

           The driver function calls two functions:

           - purely_wrap_unit is a function passed in from the client unit tester that returns an 
           object with result output groups consisting of lists of delimited strings. It has two 
           parameters: (i) inp_groups: input groups object; (ii) sce: scenario (usually unused)
           - _out_groups is a local function that takes an input scenario object and the output from
           the function above and returns the complete output scenario with groups containing both
           expected and actual result lists
*************************************************************************************************'''
def test_unit(inp_file,          # input JSON file name
              out_file,          # output JSON file name
              purely_wrap_unit): # unit test wrapper function

    with open(inp_file, encoding='utf-8') as inp_f:
        inp_json_obj = json.loads(inp_f.read())
    
    meta, inp_scenarios = inp_json_obj['meta'], inp_json_obj['scenarios']
    
    out_scenarios = {}
    for s in inp_scenarios:
        if inp_scenarios[s].get('active_yn', 'Y') != 'N':
            out_scenarios[s] = {
                INP : inp_scenarios[s][INP],
                OUT : _out_groups(inp_scenarios[s][OUT], purely_wrap_unit(inp_scenarios[s][INP]))
            }
    out_json_obj = {'meta': meta, 'scenarios': out_scenarios}
    with open(out_file, 'w') as out_f:
        json.dump(out_json_obj, out_f, indent=4)
