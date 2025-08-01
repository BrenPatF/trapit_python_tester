﻿'''*************************************************************************************************
Name: maincolgroup.py                  Author: Brendan Furey                       Date: 08-Oct-2022

Component script in the 'Trapit - Python Unit Testing' module, which facilitates unit testing in
Oracle PL/SQL following 'The Math Function Unit Testing design pattern', as described here: 

    https://brenpatf.github.io/2023/06/05/the-math-function-unit-testing-design-pattern.html

GitHub project for Python:

    https://github.com/BrenPatF/trapit_python_tester

At the heart of the design pattern there is a language-specific unit testing driver function. This
function reads an input JSON scenarios file, then loops over the scenarios making calls to a
function passed in as a parameter from the calling script. The passed function acts as a 'pure'
wrapper around calls to the unit under test. It is 'externally pure' in the sense that it is
deterministic, and interacts externally only via parameters and return value. Where the unit under
test reads inputs from file the wrapper writes them based on its parameters, and where the unit
under test writes outputs to file the wrapper reads them and passes them out in its return value.
Any file writing is reverted before exit.

The driver function accumulates the output scenarios containing both expected and actual results
in an object, from which a JavaScript function writes the results in HTML and text formats.

In testing of non-JavaScript programs, the results object is written to a JSON file to be passed
to the JavaScript formatter. In Python, the entry-point API, test_format, calls test_unit to write
the JSON file, then calls the JavaScript formatter, format-external-file.js.

The table shows the driver scripts for the relevant package: There are two examples of use, with
main and test drivers, and a test driver for the test_unit function.
====================================================================================================
|  Main/Test       |  Unit Module |  Notes                                                         |
|==================================================================================================|
|  mainhelloworld  |              |  Hello World program implemented as a pure function to allow   |
|  testhelloworld  |  helloworld  |  for unit testing as a simple edge case                        |
|------------------|--------------|----------------------------------------------------------------|
| *maincolgroup*   |  utils_cg    |  Simple file-reading and group-counting module, with logging   |
|  testcolgroup    |  colgroup    |  to file. Example of testing impure units, and failing test    |
|------------------|--------------|----------------------------------------------------------------|
|  testtrapit      |  trapit      |  Unit test package with test driver utility, and test script   |
|                  |              |  that uses the utility to test itself                          |
====================================================================================================

This file is the driver script for a simple file-reading and group-counting module, with logging to 
file.

To run from root folder:

$ py examples/colgroup/maincolgroup.py

*************************************************************************************************'''
import sys, os
import colgroup as cg

ROOT = os.path.dirname(__file__) + '/'

(input_file, delim, col) = ROOT + 'fantasy_premier_league_player_stats.csv', ',', 6

grp = cg.ColGroup(input_file, delim, col)

grp.pr_list('(as is)', grp.list_as_is())

grp.pr_list('key', grp.sort_by_key())

grp.pr_list('value (lambda)', grp.sort_by_value_lambda())
