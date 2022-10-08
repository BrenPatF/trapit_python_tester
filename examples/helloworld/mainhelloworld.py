'''*************************************************************************************************
Name: mainhelloworld.py                Author: Brendan Furey                       Date: 08-Oct-2022

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
| *mainhelloworld* |              |  Hello World program implemented as a pure function to allow   |
|  testhelloworld  |  helloworld  |  for unit testing as a simple edge case                        |
|------------------|--------------|----------------------------------------------------------------|
|  maincolgroup    |  utils_cg    |  Simple file-reading and group-counting module, with logging   |
|  testcolgroup    |  colgroup    |  to file. Example of testing impure units, and failing test    |
|------------------|--------------|----------------------------------------------------------------|
|  testtrapit      |  trapit      |  Unit test package with test driver utility, and test script   |
|                  |              |  that uses the utility to test itself                          |
====================================================================================================

This file is the driver script for a Hello World program implemented as a pure function to allow for
unit testing as a simple edge case.

To run from root folder:

$ py examples/helloworld/mainhelloworld.py

*************************************************************************************************'''
import helloworld as hw

print(hw.hello_world())
