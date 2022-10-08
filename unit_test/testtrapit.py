'''*************************************************************************************************
Name: testtrapit.py                    Author: Brendan Furey                       Date: 08-Oct-2022

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
| *testtrapit*     |  trapit      |  Unit test package with test driver utility, and test script   |
|                  |              |  that uses the utility to test itself                          |
====================================================================================================

This file is a unit test script for the trapit entry point function test_unit.

To run from root folder:

$ py unit_test/testtrapit.py

*************************************************************************************************'''
import sys, os, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import trapit

ROOT = os.path.dirname(__file__) + '\\'
DELIM = '|'

INP_JSON,                OUT_JSON,                    INP_JSON_INNER,                OUT_JSON_INNER                = \
ROOT + 'trapit_py.json', ROOT + 'trapit_py_out.json', ROOT + 'trapit_py_inner.json', ROOT + 'trapit_py_out_inner.json'

OUT_GROUP,       SCE_INP = \
'out_group_lis', 'sce_inp_lis'

TITLE,   DELIMITER,   ACTIVE_YN,   UNIT_TEST,   META,   SCENARIOS,   INP,   OUT,   EXP,   ACT = \
'title', 'delimiter', 'active_yn', 'Unit Test', 'meta', 'scenarios', 'inp', 'out', 'exp', 'act'

INP_FIELDS,     OUT_FIELDS,      INP_VALUES,     EXP_VALUES,        ACT_VALUES = \
'Input Fields', 'Output Fields', 'Input Values', 'Expected Values', 'Actual Values'

'''*************************************************************************************************

purely_wrap_unit: Outer level unit test wrapper function, returning an object with the output group
    objects actual values from unit under test for a single scenario

*************************************************************************************************'''
def purely_wrap_unit(inp_groups): # input groups object
    '''*************************************************************************************************

    groups_from_group_field_pairs: Returns a list of distinct groups from an input list of group/field
        pairs

    *************************************************************************************************'''
    def groups_from_group_field_pairs(group_field_lis): # group/field pairs list
        return list(dict.fromkeys([gf.split(DELIM)[0] for gf in group_field_lis]))

    '''*************************************************************************************************

    groups_obj_from_gf_pairs: Returns an object with groups as keys and field lists as values, based on
        input lists of groups and group/field pairs

    *************************************************************************************************'''
    def groups_obj_from_gf_pairs(group_lis,        # groups list
                                 group_field_lis): # group/field pairs list
        obj = {}
        for g in group_lis:
            gf_pairs = filter(lambda gf: gf[:len(g)] == g, group_field_lis)
            obj[g] = [gf[len(g) + 1:] for gf in gf_pairs]
        return obj

    '''*************************************************************************************************

    groups_obj_from_sgf_triples: Returns an object with groups as keys and field lists as values for
        given scenario, based on input scenario and lists of groups and scenario/group/field triples

    *************************************************************************************************'''
    def groups_obj_from_sgf_triples(sce,             # scenario
                                    group_lis,       # groups list
                                    sgf_triple_lis): # scenario/group/field triples list
        this_sce_pairs = list(filter(lambda g: g[:len(sce)] == sce, sgf_triple_lis))
        group_field_lis = [p[len(sce) + 1:] for p in this_sce_pairs]
        return groups_obj_from_gf_pairs(group_lis, group_field_lis)

    '''*************************************************************************************************

    purely_wrap_unit_inner: Inner level unit test wrapper function, returning an object with the output
        group objects 'actual' values from the unit under test, which is here trapit.test_unit. It 
        returns the 'Actual Values' group values specified in the outer level for the given scenario,
        ignoring the (required) input groups parameter in this special case. It references two arrays
        held in the scope of the outer level wrapper function, and also an index into the scenarios list
        that has the same outer level scope

    *************************************************************************************************'''
    def purely_wrap_unit_inner(inp_groups_inner): # input groups object (inner level)
        nonlocal sce_inp_ind
        scenario_inner = sce_inp_lis[sce_inp_ind]
        sce_inp_ind += 1
        return groups_obj_from_sgf_triples(scenario_inner, out_group_lis, inp_groups[ACT_VALUES])

    '''*************************************************************************************************

    write_input_json: This function writes out the inner level JSON file. It returns two objects: a list
        of (inner) output groups, and a list of (inner) scenarios; these are referenced in 
        purely_wrap_unit_inner

    *************************************************************************************************'''
    def write_input_json():
        inp_group_field_lis = inp_groups[INP_FIELDS]
        inp_group_lis = groups_from_group_field_pairs(inp_group_field_lis)
        out_group_field_lis = inp_groups[OUT_FIELDS]
        out_group_lis = groups_from_group_field_pairs(out_group_field_lis)
        title, delimiter = inp_groups[UNIT_TEST][0].split(DELIM)

        meta = {TITLE:     title,
                DELIMITER: delimiter,
                INP:       groups_obj_from_gf_pairs(inp_group_lis, inp_group_field_lis),
                OUT:       groups_obj_from_gf_pairs(out_group_lis, out_group_field_lis)
        }
        scenarios = {}
        sce_inp_lis = []
        for s_row in inp_groups['Scenario']:
            sce, active_yn = s_row.split(DELIM)
            if active_yn == 'Y':
                sce_inp_lis.append(sce)
            sce_inp = groups_obj_from_sgf_triples(sce, inp_group_lis, inp_groups[INP_VALUES])
            sce_out = groups_obj_from_sgf_triples(sce, out_group_lis, inp_groups[EXP_VALUES])
            scenarios[sce] = {
                ACTIVE_YN: active_yn,
                INP:       sce_inp,
                OUT:       sce_out
            }
        inp_json_obj = {
            META:       meta,
            SCENARIOS:  scenarios
        }
        with open(INP_JSON_INNER, 'w') as inp_f:
            json.dump(inp_json_obj, inp_f, indent=4) 
        return [out_group_lis, sce_inp_lis]
    '''*************************************************************************************************

    get_actuals: This function extract the actual results from the JSON output file created by the inner
        level call to trapit.test_unit. It returns an object with output groups as keys and actual
        values lists as values for given scenario

    *************************************************************************************************'''
    def get_actuals():
        with open(OUT_JSON_INNER, encoding='utf-8') as out_f:
            out_json_obj = json.loads(out_f.read())
        meta, scenarios = out_json_obj[META], out_json_obj[SCENARIOS]
    
        g_unit_test = [meta[TITLE] + DELIM + meta[DELIMITER]]
    
        g_inp_fields, g_out_fields, g_inp_values, g_exp_values, g_act_values = [], [], [], [], []
        for g in meta[INP]:
            for i in meta[INP][g]:
                g_inp_fields.append(g + DELIM + i)
    
        for g in meta[OUT]:
            for i in meta[OUT][g]:
                g_out_fields.append(g + DELIM + i)
    
        for s in scenarios:
            for g in scenarios[s][INP]:
                for i in scenarios[s][INP][g]:
                    g_inp_values.append(s + DELIM + g + DELIM + i)
            for g in scenarios[s][OUT]:
                for i in scenarios[s][OUT][g][EXP]:
                    g_exp_values.append(s + DELIM + g + DELIM + i)
                for i in scenarios[s][OUT][g][ACT]:
                    g_act_values.append(s + DELIM + g + DELIM + i)
    
        os.remove(INP_JSON_INNER)
        os.remove(OUT_JSON_INNER)
        return {
            UNIT_TEST:  g_unit_test,
            INP_FIELDS: g_inp_fields,
            OUT_FIELDS: g_out_fields,      
            INP_VALUES: g_inp_values,     
            EXP_VALUES: g_exp_values,        
            ACT_VALUES: g_act_values
        }
    out_group_lis, sce_inp_lis = write_input_json()
    sce_inp_ind = 0
    trapit.test_unit(INP_JSON_INNER, OUT_JSON_INNER, purely_wrap_unit_inner)
    return get_actuals()

trapit.test_unit(INP_JSON, OUT_JSON, purely_wrap_unit)
