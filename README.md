<img src="png/mountains.png">

> The Math Function Unit Testing design pattern, implemented in Python

:detective:

This module supports a new design pattern for unit testing that can be applied in any language, and is here implemented in Python. The module name is derived from 'TRansactional API Testing' (TRAPIT), and the 'unit' should be considered to be a transactional unit (this is not micro-testing).

The module supplies a simple utility for unit testing Python programs based on the 'Math Function Unit Testing design pattern'. The utility provides a generic driver program for unit testing, with test data read from an input JSON file, results written to an output JSON file, and all specific test code contained in a callback function passed to the generic driver function. A separate JavaScript module is used to parse the results JSON and format them in HTML and plain text.

There is a blog post on scenario selection in unit testing that may be of interest:

- [Unit Testing, Scenarios and Categories: The SCAN Method](https://brenpatf.github.io/jekyll/update/2021/10/17/unit-testing-scenarios-and-categories-the-scan-method.html)

# In This README...
[&darr; Background](#background)<br />
[&darr; Usage](#usage)<br />
[&darr; API](#api)<br />
[&darr; Installation](#installation)<br />
[&darr; Unit Testing](#unit-testing)<br />
[&darr; See Also](#see-also)<br />
[&darr; License](#license)<br />

## Background
[&uarr; In This README...](#in-this-readme)<br />

On March 23, 2018 I made the following presentation at the Oracle User Group conference in Dublin:

[Database API Viewed As A Mathematical Function: Insights into Testing](https://www.slideshare.net/brendanfurey7/database-api-viewed-as-a-mathematical-function-insights-into-testing)

The first section was summarised as:
<blockquote>Developing a universal design pattern for testing APIs using the concept of a 'pure' function as a wrapper to manage the 'impurity' inherent in database APIs</blockquote>

Although the presentation focussed on database testing the design pattern is clearly quite general.

The main features of the design pattern are:

- The unit under test is viewed from the perspective of a mathematical function having an `extended signature`, comprising any actual parameters and return value, together with other inputs and outputs of any kind
- A wrapper function is constructed based on this conceptual function, and the wrapper function is `externally pure`, while internally handling impurities such as file I/O
- The wrapper function performs the steps necessary to test the UUT in a single scenario
- It takes all inputs of the extended signature as a parameter, creates any test data needed from them, effects a transaction with the UUT, and returns all outputs as a return value
- Any test data, and any data changes made by the UUT, are reverted before return
- The wrapper function specific to the UUT is called within a loop over scenarios by a library test driver module
- The library test driver module reads data for all scenarios in JSON format, with both inputs to the UUT and the expected outputs, and metadata records describing the specific data structure
- The module takes the actual outputs from the wrapper function and merges them in alongside the expected outputs to create an output results object
- This output results object is processed by a JavaScript module to generate the results formatted as a summary page, with a detail page for each scenario, in both HTML and text versions

At a high level the design pattern:

- takes an input file containing all test scenarios with input data and expected output data for each scenario
- creates a results object based on the input file, but with actual outputs merged in
- uses the results object to generate unit test results files formatted in HTML and/or text

<img src="png/Math_Function_UT_DP_-_HL_Flow.png">
<br />

The Math Function Unit Testing design pattern is centred around the idea of a `pure` wrapper function that maps from `extended` input parameters to an `extended`  return value, with both sides using a generic nested object structure.

<img src="png/Math_Function_UT_DP_-_Mapping.png">
<br />

Here is a diagram illustrating the concept of the `externally pure` wrapper function:
<br /><br />
<img src="png/Math_Function_UT_DP_-_Wrapper.png">
<br /><br />
The JavaScript Trapit module supports the full process for testing JavaScript programs, and, for non-JavaScript programs, performs the formatting step by reading in the results object from a JSON file materialized by the external program. 

The current Python project illustrates how this works in unit testing external programs, and there are also examples using Oracle and Powershell.
<br /><br />
Advantages of the design pattern include:

- Writing the unit test wrapper function is the only programming required for the specific unit test, with unit test driver, assertion and formatting all centralized in library packages
- Once the unit test wrapper function is written for one scenario, no further programming is required to handle additional scenarios, facilitating good scenario coverage
- The formatted results show exactly what the program does in terms of data inputs and outputs
- All unit test programs can follow a single, straightforward pattern with minimal programming
- The JavaScript Trapit module can be used to process results files generated from any language as JSON files, as in the current Python project

## Usage
[&uarr; In This README...](#in-this-readme)<br />
[&darr; General Usage](#general-usage)<br />
[&darr; Example 1 - colgroup](#example-1---colgroup)<br />
[&darr; Example 2 - hello_world](#example-2---hello_world)<br />

In this section we show how to use the package for unit testing, first in general terms, then via two examples.

### General Usage
[&uarr; Usage](#usage)<br />
[&darr; Preliminary Steps](#preliminary-steps)<br />
[&darr; Unit Testing Process (General)](#unit-testing-process-general)<br />
[&darr; Unit Test Documentation](#unit-test-documentation)<br />

#### Preliminary Steps
[&uarr; General Usage](#general-usage)<br />

In order to use the design pattern for unit testing, the following preliminary steps are required: 
- Create a JSON file containing the input test data including expected return values in the required format. The input JSON file essentially consists of two objects: 
  - `meta`: inp and out objects each containing group objects with arrays of field names
  - `scenarios`: scenario objects containing inp and out objects, with inp and out objects containing, for each group defined in meta, an array of input records and an array of expected output records, respectively, records being in delimited fields format
- Create a unit test script containing the wrapper function and a 1-line main section calling the Trapit library function, passing in the wrapper as a callback function. The wrapper function should call the unit under test passing the appropriate parameters and return its outputs, with the following signature:

  - Input parameter: 3-level list with test inputs as an object with groups as properties having 2-level arrays of record/field as values: {GROUP: [[String]], ...}
                        
  - Return Value:    2-level list with test outputs as an object with groups as properties having an array of records as delimited fields strings as value: {GROUP: [String], ...}

This wrapper function may need to write inputs to, and read outputs from, files or tables, but should be `externally pure` in the sense that any changes made are rolled back before returning, including any made by the unit under test, and should be `essentially` deterministic.

The diagram shows the flows between input and output files:

- Input JSON file (yellow)
- Output JSON file (yellow)
- Formatted unit test reports (blue)

and the four code components, where the design pattern centralizes as much code as possible in the library packages:

- JavaScript Trapit library package for formatting results (dark green)
- External (Python) library package for unit testing (light green)
- Specific (Python) test package (tan)
- Unit under test (Python) (rose)

<img src="png/Math_Function_UT_DP_-_External.png">

#### Unit Testing Process (General)
[&uarr; General Usage](#general-usage)<br />

Once the preliminary steps are executed, the script (testuut.py, say) can be executed as follows:

```py
$ py [path]/testuut.py
```

The output results files are processed by a JavaScript program that has to be installed separately, as described in the [Installation](#installation) section. The JavaScript program produces listings of the results in HTML and/or text format in a subfolder named from the unit test title. 

To run the processor, go to the npm trapit package folder after placing the output JSON files, trapit_py_out.json, in a new (or existing) folder, python, within the subfolder externals and run:

```
$ node externals/format-externals python
```

This outputs to screen the following summary level report (for both examples described below), as well as writing the formatted results files to the subfolders indicated:
```
Unit Test Results Summary for Folder ./externals/python
=======================================================
 File                 Title        Inp Groups  Out Groups  Tests  Fails  Folder     
--------------------  -----------  ----------  ----------  -----  -----  -----------
*colgroup_out.json    Col Group             3           4      5      1  col-group  
 helloworld_out.json  Hello World           0           1      1      0  hello-world

1 externals failed, see ./externals/python for scenario listings
colgroup_out.json
```

The running of the python unit test, and its Javascript formatting can easily be automated, as in the following Powershell script in the examples folder:
```ps
$ ./Run-Examples.ps1
```
This example script runs both example unit tests and then the Javascript formatter, assuming a hard-coded npm root folder, and writes the summary to a file python.log.

#### Unit Test Documentation
[&uarr; General Usage](#general-usage)<br />

In documenting our unit testing it may be helpful to divide into four sections: The unit testing process; wrapper function design and code; scenario category analysis; unit test results. The heading structure might look as follows:

- Unit Testing Process
- Unit Test Wrapper Function
  - Wrapper Function Signature Diagram
  - Input JSON File
  - Wrapper Function Code
- Scenario Category ANalysis (SCAN)
  - Simple Category Sets
  - Composite Category Sets
  - Scenario Category Mapping
- Unit Test Results
  - Results Summary
  - Unit Test Report: Title

### Example 1 - colgroup
[&uarr; Usage](#usage)<br />
[&darr; Unit Testing Process - colgroup](#unit-testing-process---colgroup)<br />
[&darr; Unit Test Wrapper Function - colgroup](#unit-test-wrapper-function---colgroup)<br />
[&darr; Scenario Category ANalysis (SCAN) - colgroup](#scenario-category-analysis-scan---colgroup)<br />
[&darr; Unit Test Results - colgroup](#unit-test-results---colgroup)<br />

This example is a python class with a constructor function that reads in a CSV file and counts instances of distinct values in a given column. The constructor function appends a timestamp and call details to a log file. The class has methods to list the value/count pairs in several orderings. 

There is a main script that shows how the class might be called outside of unit testing, run from the module root folder:
```py
$ py examples/colgroup/maincolgroup.py
```
with output to console:
```
Counts sorted by (as is)
========================
Team         #apps
-----------  -----
team_name_2      1
team_name_1      1
West Brom     1219
Swansea       1180
Blackburn       33
Bolton          37
Chelsea       1147
Arsenal        534
Everton       1147
Tottenham     1288
Fulham        1209
QPR           1517
Liverpool     1227
Sunderland    1162
Man City      1099
Man Utd       1231
Newcastle     1247
Stoke City    1170
Wolves          31
Aston Villa    685
Wigan         1036
Norwich       1229
West Ham      1126
Reading       1167
...
```
and to log file, fantasy_premier_league_player_stats.csv.log:
```
Sun Sep 23 2018 13:29:07: File ./examples/colgroup/fantasy_premier_league_player_stats.csv, delimiter ',', column 6
```

The example illustrates how a wrapper function can handle `impure` features of the unit under test:
- Reading input from file
- Writing output to file

...and also how the JSON input file can allow for nondeterministic outputs giving rise to deterministic test outcomes:
- By using regex matching for strings including timestamps
- By using number range matching and converting timestamps to epochal offsets (number of units of time since a fixed time)

#### Unit Testing Process - colgroup
[&uarr; Example 1 - colgroup](#example-1---colgroup)<br />

To run the unit test program from the module root folder:

```py
$ py examples/colgroup/testcolgroup.py
```

The output result file is processed by a JavaScript program as explained in the `General Usage` section above. It outputs to screen a summary level report (for both examples), as well as writing the listings of the results in HTML and/or text format in a subfolder named from the unit test title, as specified in the input JSON file.

The section `Unit Testing Process (General)`, above, shows how to combine the running of the python script and the JavaScript formatter in a single powershell script.

#### Unit Test Wrapper Function - colgroup
[&uarr; Example 1 - colgroup](#example-1---colgroup)<br />
[&darr; WF Signature Diagram - colgroup](#wf-signature-diagram---colgroup)<br />
[&darr; Input JSON File - colgroup](#input-json-file---colgroup)<br />
[&darr; Wrapper Function Code - colgroup](#wrapper-function-code---colgroup)<br />

##### WF Signature Diagram - colgroup
[&uarr; Unit Test Wrapper Function - colgroup](#unit-test-wrapper-function---colgroup)<br />

The JSON input file contains `meta` and `scenarios` properties, as mentioned above, with structure reflecting the (extended) inputs and outputs of the unit under test. I like to make a diagram of the input and output groups, which for this example is:

<img src="png/Math_Function_UT_DP_-_JSD-CG.png">

##### Input JSON File - colgroup
[&uarr; Unit Test Wrapper Function - colgroup](#unit-test-wrapper-function---colgroup)<br />

An easy way to generate a starting point for the input JSON file is to use a powershell utility [Powershell Utilites module](https://github.com/BrenPatF/powershell_utils) to generate a template file with a single scenario with placeholder records from simple CSV files. The CSV files, `colgroup_inp.csv`, containing input group, field pairs, and the second, `colgroup_out.csv`, the same for output for the JSON structure diagram above would look like this:

<img src="png/Input_CSV_Files_colGroup.png">

The powershell utility can be run from a powershell window like this:

```powershell
Import-Module TrapitUtils
Write-UT_Template 'colgroup' '|'
```

This generates a JSON template file, colgroup_temp.json.

The template is then updated with test data for 5 scenarios (showing just the first one here):

```json
{ "meta": {
    "title": "Col Group",
    "inp": {
        "Log": [
            "Line"
        ],
        "Scalars": [
            "Delimiter",
            "Column#"
        ],
        "Lines": [
            "Line"
        ]
    },
    "out": {
        "Log": [
            "#Lines",
            "Date Offset",
            "Text"
        ],
        "listAsIs": [
            "#Instances"
        ],
        "sortByKey": [
            "Key",
            "Value"
        ],
        "sortByValue": [
            "Key",
            "Value"
        ]
    }
},
"scenarios" : { 
   "Col 1/3; 2 duplicate lines; double-delimiter; 1-line log": 
   {
    "active_yn" : "Y",
    "inp": {
       "Log": [
       ],
       "Scalars": [
            ",|2"
        ],
        "Lines": [
            "0,1,Cc,3",
            "00,1,A,9",
            "000,1,B,27",
            "0000,1,A,81"
        ]
    },
    "out": {
        "Log": [
            "1|IN [0, 2000]|LIKE /.*: File ./examples/colgroup/ut_group.csv, delimiter ',', column 2/"
        ],
        "listAsIs": [
            "3"
        ],
        "sortByKey": [
            "A|2",
            "Bx|1",
            "Cc|1"
        ],
        "sortByValue": [
            "B|1",
            "Cc|1",
            "A|2"
        ]
    }
},
...3 more scenarios
}}
```

Notice the syntax for the expected values for the second and third fields in the 3-field output record for the log group. This specifies matching against a numeric range and a regular expression, respectively, as follows:

- Date Offset: "IN [0, 2000]" - the datetime offset in microseconds must be between 0 and 2000 microseconds from the datetime at the start of execution
- Text: "LIKE /.\*: File ./examples/colgroup/ut_group.csv, delimiter ',', column 2/" - the line of text written must match the regular expression betwen the '/' delimiters, allowing us to ignore the precise timestamp for testing purposes, but still to display it for information


##### Wrapper Function Code - colgroup
[&uarr; Unit Test Wrapper Function - colgroup](#unit-test-wrapper-function---colgroup)<br />

The text box below shows the entire specific unit test code for this example (short isn't it? &#128513;) containing the pure wrapper function, purely_wrap_unit, and the one line main section calling the library function, trapit.test_unit.

```py
import sys, os
from datetime import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import trapit, colgroup as cg

ROOT = os.path.dirname(__file__) + '/'
DELIM = '|'
INPUT_JSON,             OUTPUT_JSON,                INPUT_FILE,            LOG_FILE                  = \
ROOT + 'colgroup.json', ROOT + 'colgroup_out.json', ROOT + 'ut_group.csv', ROOT + 'ut_group.csv.log'
GRP_LOG,   GRP_SCA,   GRP_LIN, GRP_LAI,    GRP_SBK,     GRP_SBV       = \
'Log',     'Scalars', 'Lines', 'listAsIs', 'sortByKey', 'sortByValue'

def from_CSV(csv, col):
    return csv.split(DELIM)[col]
def join_tuple(t):
    return t[0] + DELIM + str(t[1])
def setup(inp):
    with open(INPUT_FILE, 'w') as infile:
        infile.write('\n'.join(inp[GRP_LIN]))
    if (len(inp[GRP_LOG]) > 0):
        with open(LOG_FILE, 'w') as logfile:
            logfile.write('\n'.join(inp[GRP_LOG]) + '\n')
    return cg.ColGroup(INPUT_FILE, from_CSV(inp[GRP_SCA][0], 0), from_CSV(inp[GRP_SCA][0], 1))
def teardown():
    os.remove(INPUT_FILE)
    os.remove(LOG_FILE)

def purely_wrap_unit(inp_groups):
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
        GRP_LOG : [str((len(lines_array) - 1)) + DELIM + str(diffDate) + DELIM + text],
        GRP_LAI : [str(len(col_group.list_as_is()))],
        GRP_SBK : list(map(join_tuple, col_group.sort_by_key())),
        GRP_SBV : list(map(join_tuple, col_group.sort_by_value_lambda()))
    }
trapit.test_unit(INPUT_JSON, OUTPUT_JSON, purely_wrap_unit)
```

#### Scenario Category ANalysis (SCAN) - colgroup
[&uarr; Example 1 - colgroup](#example-1---colgroup)<br />
[&darr; Simple Category Sets - colgroup](#simple-category-sets---colgroup)<br />
[&darr; Composite Category Sets - colgroup](#composite-category-sets---colgroup)<br />
[&darr; Scenario Category Mapping - colgroup](#scenario-category-mapping---colgroup)<br />

This article, [Unit Testing, Scenarios and Categories: The SCAN Method](https://brenpatf.github.io/jekyll/update/2021/10/17/unit-testing-scenarios-and-categories-the-scan-method.html), explains how to derive unit test scenarios using a new approach called the SCAN method.

Following the method, in this section we identify the category sets for the problem, and tabulate the corresponding categories. We need to consider which category sets can be tested independently of each other, and which need to be considered in combination. We can then obtain a set of scenarios to cover all relevant combinations of categories.

##### Simple Category Sets - colgroup
[&uarr; Scenario Category ANalysis (SCAN) - colgroup](#scenario-category-analysis-scan---colgroup)<br />

###### MUL-LIN - Multiplicity of lines

Check works correctly with 0, 1 and multiple lines.

| Code | Description |
|:----:|:------------|
|   0  | None        |
|   1  | One         |
|   m  | Multiple    |

###### POS-KEY - Position of key column

Check works correctly when the key column is first, last or in the middle.

| Code | Description |
|:----:|:------------|
|   F  | First       |
|   L  | Last        |
|   M  | Middle      |

###### MUL-KEY - Multiplicity of key instances

Check works correctly with 1 and multiple key instances.

| Code | Description |
|:----:|:------------|
|   1  | One         |
|   m  | Multiple    |

###### MUL-COL - Multiplicity of file columns

Check works correctly with 1 and multiple columns in file.

| Code | Description |
|:----:|:------------|
|   1  | One         |
|   m  | Multiple    |

###### MUL-DEL - Multiplicity of delimiter character

Check works correctly with 1 and multiple delimiter character.

| Code | Description |
|:----:|:------------|
|   1  | One         |
|   m  | Multiple    |

###### SIZ - Size of key

Check works correctly with short and long key values.

| Code | Description |
|:----:|:------------|
|   S  | Short       |
|   L  | Long        |

###### LOG  - Log file existence

Check works correctly when there is already a log file and when there isn't.

| Code | Description                              |
|:----:|:-----------------------------------------|
|   N  | No - file does not exist at time of call |
|   Y  | No - file exists at time of call         |

###### ORD-SAM  - Ordering same by key and by value?

Check ordering methods work when order of output records same by key and value and when differs.

| Code | Description                              |
|:----:|:-----------------------------------------|
|   N  | Order by key differs from order by value |
|   Y  | Order by key same as order by value      |

##### Composite Category Sets - colgroup
[&uarr; Scenario Category ANalysis (SCAN) - colgroup](#scenario-category-analysis-scan---colgroup)<br />

In this section we need to consider which simple category sets need to be considered in combination with others. In fact, in this case, all the category sets other than `Multiplicity of lines` are independent of each other, and have a very simple dependence on `Multiplicity of lines`: There has to be at least one line in the file to test the other category sets, and multiple lines to test a couple of them. 

As `Position of key column` has three categories, we can test these with multiple lines, as well as testing the zero-lines edge case and the 1-line case. The possible combinations of these two category sets can then be the basis for our scenarios, and we can just enumerate the other categories within them.

###### MUL-LK - Multiplicity of lines and key instances

Check works correctly with 0, 1 and multiple lines, and for multiple lines all three categories of `Position of key column`.

| MUL-LIN | POS-KEY | Description                         |
|:-------:|:-------:|:------------------------------------|
|    0    |    -    | Lines: None; Key column: NA         |
|    1    |    F    | Lines: 1; Key column: First         |
|    m    |    F    | Lines: Multiple; Key column: First  |
|    m    |    L    | Lines: Multiple; Key column: Last   |
|    m    |    M    | Lines: Multiple; Key column: Middle |

##### Scenario Category Mapping - colgroup
[&uarr; Scenario Category ANalysis (SCAN) - colgroup](#scenario-category-analysis-scan---colgroup)<br />

We now want to construct a set of scenarios based on the category sets identified, covering each individual category, and also covering combinations of categories that may interact. As discussed in the previous section, the possible combinations of the first two category sets form the basis for the category-level scenario set, with the remaining category sets enumerated in the additional columns.

| # | MUL-LIN | POS-KEY | MUL-KEY | MUL-COL | MUL-DEL | SIZ | LOG | ORD-SAM | Description                         |
|:--|:-------:|:-------:|:-------:|:-------:|:-------:|:---:|:---:|:-------:|:------------------------------------|
| 1 |    0    |    -    |    -    |    -    |    -    |  -  |  -  |    -    | Lines: None; Key column: NA         |
| 2 |    1    |    F    |    1    |    1    |    1    |  S  |  N  |    -    | Lines: 1; Key column: First         |
| 3 |    m    |    F    |    m    |    m    |    m    |  L  |  Y  |    N    | Lines: Multiple; Key column: First  |
| 4 |    m    |    L    |    m    |    m    |    m    |  L  |  Y  |    Y    | Lines: Multiple; Key column: Last   |
| 5 |    m    |    M    |    m    |    m    |    m    |  L  |  Y  |    N    | Lines: Multiple; Key column: Middle |
  
#### Unit Test Results - colgroup
[&uarr; Example 1 - colgroup](#example-1---colgroup)<br />
[&darr; Results Summary - colgroup](#results-summary---colgroup)<br />
[&darr; Unit Test Report: Col Group](#unit-test-report-col-group)<br />

##### Results Summary - colgroup
[&uarr; Unit Test Results - colgroup](#unit-test-results---colgroup)<br />

The results summary from the JavaScript test formatter was (for both examples):
```
Unit Test Results Summary for Folder ./externals/python
=======================================================
 File                 Title        Inp Groups  Out Groups  Tests  Fails  Folder     
--------------------  -----------  ----------  ----------  -----  -----  -----------
*colgroup_out.json    Col Group             3           4      5      1  col-group  
 helloworld_out.json  Hello World           0           1      1      0  hello-world

1 externals failed, see ./externals/python for scenario listings
colgroup_out.json
```

You can review the HTML formatted unit test results for the program here:

- [Unit Test Report: Col Group](http://htmlpreview.github.io/?https://github.com/BrenPatF/trapit_python_tester\examples\colgroup\col-group/col-group.html)

The formatted results files, both text and HTML, are available in the `col-group` subfolder. The summary report showing scenarios tested, in text format, along with the detailed report for scenario 5, are copied below:

##### Unit Test Report: Col Group
[&uarr; Unit Test Results - colgroup](#unit-test-results---colgroup)<br />
```
Unit Test Report: Col Group
===========================

      #    Scenario                             Fails (of 4)  Status 
      ---  -----------------------------------  ------------  -------
      1    Lines: None; Key column: NA          0             SUCCESS
      2    Lines: 1; Key column: First          0             SUCCESS
      3    Lines: Multiple; Key column: First   0             SUCCESS
      4    Lines: Multiple; Key column: Last    0             SUCCESS
      5*   Lines: Multiple; Key column: Middle  1             FAILURE

Test scenarios: 1 failed of 5: FAILURE
======================================
```
Note the record #5 above marked with a '\*' indicating failure status. The detailed report for the fifth scenario, in text format, is copied below:
```
SCENARIO 5: Lines: Multiple; Key column: Middle {
=================================================
   INPUTS
   ======
      GROUP 1: Log {
      ==============
            #  Line      
            -  ----------
            1  Log line 1
      }
      =
      GROUP 2: Scalars {
      ==================
            #  Delimiter  Column#
            -  ---------  -------
            1  ;;         5      
      }
      =
      GROUP 3: Lines {
      ================
            #  Line                                                                         
            -  -----------------------------------------------------------------------------
            1  0;;1;;2;;3;;4;;12345678901234567890123456789012345678901234567890;;5;;6;;7;;8
            2  0;;1;;2;;3;;4;;abc;;5;;6;;7;;8                                               
            3  0;;1;;2;;3;;4;;12345678901234567890123456789012345678901234567890;;5;;6;;7;;8
      }
      =
   OUTPUTS
   =======
      GROUP 1: Log {
      ==============
            #  #Lines  Date Offset           Text                                                                                                                                                                                                           
            -  ------  --------------------  ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            1  2       IN [0,2000]: 480.149  LIKE /.*: File .*examples-colgroup-ut_group.csv, delimiter ';;', column 5/: 2021-11-20 16:14:04: File C:-Users-Brend-OneDrive-Script-pip-trapit-trapit-examples-colgroup-ut_group.csv, delimiter ';;', column 5
      } 0 failed of 1: SUCCESS
      ========================
      GROUP 2: listAsIs {
      ===================
            #   #Instances
            --  ----------
            1   3         
            1*  2         
      } 1 failed of 1: FAILURE
      ========================
      GROUP 3: sortByKey {
      ====================
            #  Key                                                 Value
            -  --------------------------------------------------  -----
            1  12345678901234567890123456789012345678901234567890  2    
            2  abc                                                 1    
      } 0 failed of 2: SUCCESS
      ========================
      GROUP 4: sortByValue {
      ======================
            #  Key                                                 Value
            -  --------------------------------------------------  -----
            1  abc                                                 1    
            2  12345678901234567890123456789012345678901234567890  2    
      } 0 failed of 2: SUCCESS
      ========================
} 1 failed of 4: FAILURE
========================
```

Note the record #1 above marked with a '\*' in 'GROUP 2: listAsIs', indicating a mismatch between expected and actual values. This is a deliberate error to illustrate the format when mismatches occur. Where the actual value differs from expected the actual record is listed below the expected, with the '\*' marker against the record number, and in the HTML report the record is coloured red. In fact the value '2' is correct and the expected value has been incorrectly set to '3'.

### Example 2 - hello_world
[&uarr; Usage](#usage)<br />
[&darr; Unit Testing Process - helloworld](#unit-testing-process---helloworld)<br />
[&darr; Unit Test Wrapper Function - helloworld](#unit-test-wrapper-function---helloworld)<br />
[&darr; Scenario Category ANalysis (SCAN) - helloworld](#scenario-category-analysis-scan---helloworld)<br />
[&darr; Unit Test Results - helloworld](#unit-test-results---helloworld)<br />

```py
def hello_world():
    return 'Hello World!'
```
This is a pure function form of Hello World program, returning a value rather than writing to screen itself. It is of course trivial, but has some interest as an edge case with no inputs and extremely simple JSON input structure and test code.

There is a main script that shows how the function might be called outside of unit testing, run from the module root folder:
```py
$ py examples/helloworld/mainhelloworld.py
```
with output to console:
```
Hello World!
```
#### Unit Testing Process - helloworld
[&uarr; Example 2 - hello_world](#example-2---hello_world)<br />

To run the unit test program from the module root folder:

```py
$ py examples/helloworld/testhelloworld.py
```

The output result file is processed by a JavaScript program as explained in the `General Usage` section above. It outputs to screen a summary level report (for both examples), as well as writing the listings of the results in HTML and/or text format in a subfolder named from the unit test title, as specified in the input JSON file.

The section `Unit Testing Process (General)`, above, shows how to combine the running of the python script and the JavaScript formatter in a single powershell script.

#### Unit Test Wrapper Function - helloworld
[&uarr; Example 2 - hello_world](#example-2---hello_world)<br />
[&darr; WF Signature Diagram - helloworld](#wf-signature-diagram---helloworld)<br />
[&darr; Input JSON File - helloworld](#input-json-file---helloworld)<br />
[&darr; Wrapper Function Code - helloworld](#wrapper-function-code---helloworld)<br />

##### WF Signature Diagram - helloworld
[&uarr; Unit Test Wrapper Function - helloworld](#unit-test-wrapper-function---helloworld)<br />

The JSON structure diagram for this trivial example is:

<img src="png/Math_Function_UT_DP_-_JSD-HW.png">

##### Input JSON File - helloworld
[&uarr; Unit Test Wrapper Function - helloworld](#unit-test-wrapper-function---helloworld)<br />

The input JSON file, showing empty input property in the meta and scenarios objects, is:

[&uarr; Input JSON File](#input-json-file-1)

```json
{ "meta": {
    "title": "Hello World",
    "inp": {},
    "out": {
        "Group": [
            "Greeting"
        ]
    }
},
"scenarios" : { 
   "Scenario": 
   {
    "inp": {},
    "out": {
        "Group": [
            "Hello World!"
        ]
    }
}
}}
```

##### Wrapper Function Code - helloworld
[&uarr; Unit Test Wrapper Function - helloworld](#unit-test-wrapper-function---helloworld)<br />

The text box below shows the entire specific unit test code for this example. In this trivial case, we can pass the pure wrapper function as a lambda expression.

```py
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import trapit, helloworld

ROOT = os.path.dirname(__file__) + '/'
INPUT_JSON = ROOT + 'helloworld.json'
OUTPUT_JSON = ROOT + 'helloworld_out.json'

trapit.test_unit(INPUT_JSON, OUTPUT_JSON, lambda  inp_groups: {'Group': [helloworld.hello_world()]})
```

#### Scenario Category ANalysis (SCAN) - helloworld
[&uarr; Example 2 - hello_world](#example-2---hello_world)<br />

With no input data, the set of input data category sets is of course empty 🙂.

#### Unit Test Results - helloworld
[&uarr; Example 2 - hello_world](#example-2---hello_world)<br />
[&darr; Results Summary - helloworld](#results-summary---helloworld)<br />
[&darr; Unit Test Report: Hello World](#unit-test-report-hello-world)<br />

##### Results Summary - helloworld
[&uarr; Unit Test Results - helloworld](#unit-test-results---helloworld)<br />

The results summary from the JavaScript test formatter was (for both examples):
```

Unit Test Results Summary for Folder ./externals/python
=======================================================
 File                 Title        Inp Groups  Out Groups  Tests  Fails  Folder     
--------------------  -----------  ----------  ----------  -----  -----  -----------
*colgroup_out.json    Col Group             3           4      5      1  col-group  
 helloworld_out.json  Hello World           0           1      1      0  hello-world

1 externals failed, see ./externals/python for scenario listings
colgroup_out.json
```

You can review the HTML formatted unit test results for the program here:

- [Unit Test Report: Col Group](http://htmlpreview.github.io/?https://github.com/BrenPatF/trapit_python_tester\examples\colgroup\col-group/col-group.html)

The formatted results files, both text and HTML, are available in the `hello-world` subfolder. Here is the full set of results in text format:

##### Unit Test Report: Hello World
[&uarr; Unit Test Results - helloworld](#unit-test-results---helloworld)<br />

```
Unit Test Report: Hello World
=============================
      #    Scenario  Fails (of 1)  Status 
      ---  --------  ------------  -------
      1    Scenario  0             SUCCESS
Test scenarios: 0 failed of 1: SUCCESS
======================================
SCENARIO 1: Scenario {
======================
   INPUTS
   ======
   OUTPUTS
   =======
      GROUP 1: Group {
      ================
            #  Greeting    
            -  ------------
            1  Hello World!
      } 0 failed of 1: SUCCESS
      ========================
} 0 failed of 1: SUCCESS
========================
```

## API
[&uarr; In This README...](#in-this-readme)<br />
[&darr; trapit.test_unit(inp_file, out_file, purely_wrap_unit)](#trapittest_unitinp_file-out_file-purely_wrap_unit)<br />

```py
import trapit
```

### trapit.test_unit(inp_file, out_file, purely_wrap_unit)
[&uarr; API](#api)<br />

The unit test driver utility function is called as effectively the main function of any specific unit test script. It reads the input JSON scenarios file, then loops over the scenarios making calls to a function passed in as a parameter from the calling script. The function acts as a `pure` wrapper around calls to the unit under test. It is `externally pure` in the sense that it is deterministic, and interacts externally only via parameters and return value. Where the unit under test reads inputs from file the wrapper writes them based on its parameters, and where the unit under test writes outputs to file the wrapper reads them and passes them out in its return value. Any file writing is reverted before exit. 

It has the following parameters:

- `inp_file`: JSON input file name
- `out_file`: JSON output file name
- `purely_wrap_unit`: wrapper function, which calls the unit under test passing the appropriate parameters and returning its outputs, with the following signature:
  - inp_groups: input groups object, a 3-level list with test inputs as an object with groups as properties having 2-level arrays of record/field as values: {GROUP: [[String]], ...}
  - Return Value: output groups object, a 2-level list with test outputs as an object with groups as properties having an array of records as delimited fields strings as value: {GROUP: [String], ...}

## Installation
[&uarr; In This README...](#in-this-readme)<br />
[&darr; Python Installation - pip](#python-installation---pip)<br />
[&darr; Javascript Installation - npm](#javascript-installation---npm)<br />

### Python Installation - pip
[&uarr; Installation](#installation)<br />

With [python](https://www.python.org/downloads/windows/) installed, run in a powershell or command window:

```py
$ py -m pip install trapit 
```

### Javascript Installation - npm
[&uarr; Installation](#installation)<br />

- [Trapit JavaScript Tester/Formatter - GitHub module](https://github.com/BrenPatF/trapit_nodejs_tester)

With [npm](https://npmjs.org/) installed, run from your npm installation folder:

```js
$ npm install trapit 
```

## Unit Testing
[&uarr; In This README...](#in-this-readme)<br />
[&darr; Unit Testing Process](#unit-testing-process)<br />
[&darr; Wrapper Function](#wrapper-function)<br />
[&darr; Scenario Category ANalysis (SCAN)](#scenario-category-analysis-scan)<br />
[&darr; Unit Test Results](#unit-test-results)<br />

In this section the unit testing API function trapit.test_unit is itself tested using the Math Function Unit Testing design pattern.

### Unit Testing Process
[&uarr; Unit Testing](#unit-testing)<br />

The unit test utility can be used to test itself following the same 'Math Function Unit Testing design pattern' that it facilitates for testing of general programs. The challenge in this case is in determining a suitable signature and specification for the wrapper function that has to represent unit testing of any program.

Unit testing is data-driven from the input file trapit_py.json and produces an output results file, trapit_py_out.json. This contains arrays of expected and actual records by group and scenario. 

To run the unit test program from the module root folder:

```py
$ py unit_test/testtrapit.py
```

The output result file is processed by a JavaScript program as explained in the `General Usage` section above. It outputs to screen a summary level report (including for both of the earlier examples), as well as writing the listings of the results in HTML and/or text format in a subfolder named from the unit test title, as specified in the input JSON file.

To run the processor, go to the npm trapit package folder after placing the output JSON files, trapit_py_out.json, in a new (or existing) folder, python, within the subfolder externals and run:

```js
$ node externals/format-externals python
```
This outputs to screen the following summary level report, as well as writing the formatted results files to the subfolders indicated:
```
Unit Test Results Summary for Folder ./externals/python
=======================================================
 File                 Title               Inp Groups  Out Groups  Tests  Fails  Folder            
--------------------  ------------------  ----------  ----------  -----  -----  ------------------
*colgroup_out.json    Col Group                    3           4      5      1  col-group         
 helloworld_out.json  Hello World                  0           1      1      0  hello-world       
 trapit_py_out.json   Python Unit Tester           7           6      3      0  python-unit-tester

1 externals failed, see ./externals/python for scenario listings
colgroup_out.json
```

The running of the python unit test, and its Javascript formatting can easily be automated, as in the following Powershell script in the unit_test folder:
```ps
$ ./Run-Ut.ps1
```
This script runs the unit test and then the Javascript formatter, assuming a hard-coded npm root folder, and writes the summary to a file, python.log.

### Wrapper Function
[&uarr; Unit Testing](#unit-testing)<br />
[&darr; Wrapper Function Signature Diagram](#wrapper-function-signature-diagram)<br />
[&darr; Input JSON File](#input-json-file)<br />
[&darr; Wrapper Function Code](#wrapper-function-code)<br />

The signature of the unit under test is: 

    trapit.test_unit(inp_file, out_file, purely_wrap_unit)

The parameters are input and output file names, and a function. The `extended` inputs and outputs required for the wrapper function include the contents of the input and output files.

#### Wrapper Function Signature Diagram
[&uarr; Wrapper Function](#wrapper-function)<br />

<img src="png/JSD_Python_test_unit_Screen.png">

As noted above, the inputs to the unit under test here include a function. This raises the interesting question as to how we can model a function in our test data. In fact the best way to do this seems to be to regard the function as a kind of black box, where we don't care about the interior of the function, but only its behaviour in terms of returning an output from an input. This is why we have the `Actual Values` group in the input side of the diagram above, as as well as on the output side. We can model any deterministic function in our test data simply by specifying input and output sets of values.

As we are using the trapit.test_unit API to test itself, we will have inner and outer levels for the calls and their parameters. The inner-level wrapper function passed in in the call to the unit under test by the outer-level wrapper function therefore needs simply to return the set of `Actual Values` records for the given scenario. In order for it to know which set to return, the scenarios need to be within readable scope, and we need to know which scenario to use. This is achieved by maintaining arrays containing a list of inner scenarios and a list of inner output groups, along with a nonlocal variable with an index to the current inner scenario that the inner wrapper increments each time it's called. This allows the output array to be extracted from the input parameter from the outer wrapper function.

#### Input JSON File
[&uarr; Wrapper Function](#wrapper-function)<br />

An easy way to generate a starting point for the input JSON file is to use a powershell utility [Powershell Utilites module](https://github.com/BrenPatF/powershell_utils) to generate a template file with a single scenario with placeholder records from simple CSV files (see the script test_unit.ps1 in the `test` subfolder). The CSV files, `test_unit_inp.csv`, containing input group, field pairs, and the second, `test_unit_out.csv`, the same for output for the JSON structure diagram above would look like this:

<img src="png/Input_CSV_Files_Trapit.png">

The powershell utility can be run from a powershell window like this:

```powershell
Import-Module TrapitUtils
Write-UT_Template 'test_unit' '|'
```

This generates a JSON template file, test_unit_temp.json. The template is then updated with test data for the four scenarios identified in the `Scenario Category Analysis` section.

#### Wrapper Function Code
[&uarr; Wrapper Function](#wrapper-function)<br />
[&darr; testtrapit.py](#testtrapitpy)<br />
[&darr; purely_wrap_unit](#purely_wrap_unit)<br />
[&darr; write_input_json](#write_input_json)<br />
[&darr; get_actuals](#get_actuals)<br />
[&darr; Small functions](#small-functions)<br />

The wrapper function has the structure shown in the diagram below, being defined in a driver script followed by a single line calling the test_unit API.

<img src="png/testtrapit_CSD.png">

##### testtrapit.py
[&uarr; Wrapper Function Code](#wrapper-function-code)<br />
The text box below shows the code for the driving script, with the wrapper function def line as a placeholder for later expansion.
```py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import trapit

ROOT = os.path.dirname(__file__) + '\\'
DELIM = '|'

INP_JSON,                OUT_JSON,                    INP_JSON_INNER,                OUT_JSON_INNER                = \
ROOT + 'trapit_py.json', ROOT + 'trapit_py_out.json', ROOT + 'trapit_py_inner.json', ROOT + 'trapit_py_out_inner.json'

TITLE,   DELIMITER,   ACTIVE_YN,   UNIT_TEST,   META,   SCENARIOS,   INP,   OUT,   EXP,   ACT = \
'title', 'delimiter', 'active_yn', 'Unit Test', 'meta', 'scenarios', 'inp', 'out', 'exp', 'act'

INP_FIELDS,     OUT_FIELDS,      INP_VALUES,     EXP_VALUES,        ACT_VALUES = \
'Input Fields', 'Output Fields', 'Input Values', 'Expected Values', 'Actual Values'

def purely_wrap_unit(inp_groups, # input groups object
                     scenario):  # scenario key

trapit.test_unit(INP_JSON, OUT_JSON, purely_wrap_unit)
```

##### purely_wrap_unit
[&uarr; Wrapper Function Code](#wrapper-function-code)<br />
This is the outer level unit test wrapper function, returning an object with the output group objects actual values from the unit under test for a single scenario. It defines several local functions, including an inner level wrapper function, purely_wrap_unit_inner (whose
bodies are shown later).
```py
def purely_wrap_unit(inp_groups): # input groups object

    def groups_from_group_field_pairs(group_field_lis): # group/field pairs list

    def groups_obj_from_gf_pairs(group_lis,        # groups list
                                 group_field_lis): # group/field pairs list

    def groups_obj_from_sgf_triples(sce,             # scenario
                                    group_lis,       # groups list
                                    sgf_triple_lis): # scenario/group/field triples list

    def purely_wrap_unit_inner(inp_groups_inner) # input groups object (inner level)

    def write_input_json():

    def get_actuals():

    out_group_lis, sce_inp_lis = write_input_json()
    sce_inp_ind = 0
    trapit.test_unit(INP_JSON_INNER, OUT_JSON_INNER, purely_wrap_unit_inner)
    return get_actuals()
```

##### write_input_json
[&uarr; Wrapper Function Code](#wrapper-function-code)<br />
This function writes out the inner level JSON file. It returns two objects: a list of (inner) output groups, and a list of (inner) scenarios; these are referenced in purely_wrap_unit_inner.
```py
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
```

##### get_actuals
[&uarr; Wrapper Function Code](#wrapper-function-code)<br />
This function extract the actual results from the JSON output file created by the inner level call to trapit.test_unit. It returns an object with output groups as keys and actual values lists as values for given scenario.
```py
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
```

##### Small functions
[&uarr; Wrapper Function Code](#wrapper-function-code)<br />
###### groups_from_group_field_pairs
This function returns a list of distinct groups from an input list of group/field pairs.
```py
def groups_from_group_field_pairs(group_field_lis): # group/field pairs list
    return list(dict.fromkeys([gf.split(DELIM)[0] for gf in group_field_lis]))
```
###### groups_obj_from_gf_pairs
This function returns an object with groups as keys and field lists as values, based on input lists of groups and group/field pairs.
```py
def groups_obj_from_gf_pairs(group_lis,        # groups list
                             group_field_lis): # group/field pairs list
    obj = {}
    for g in group_lis:
        gf_pairs = filter(lambda gf: gf[:len(g)] == g, group_field_lis)
        obj[g] = [gf[len(g) + 1:] for gf in gf_pairs]
    return obj

```
###### groups_obj_from_sgf_triples
This function returns an object with groups as keys and field lists as values for given scenario, based on input scenario and lists of groups and scenario/group/field triples
```py
def groups_obj_from_sgf_triples(sce,             # scenario
                                group_lis,       # groups list
                                sgf_triple_lis): # scenario/group/field triples list
    this_sce_pairs = list(filter(lambda g: g[:len(sce)] == sce, sgf_triple_lis))
    group_field_lis = [p[len(sce) + 1:] for p in this_sce_pairs]
    return groups_obj_from_gf_pairs(group_lis, group_field_lis)

```
###### purely_wrap_unit_inner
This function is the inner level unit test wrapper function, returning an object with the output group objects 'actual' values from unit under test, which is here trapit.test_unit. It returns the 'Actual Values' group values specified in the outer level for the given scenario, ignoring the (required) input groups parameter in this special case. It references two arrays held in the scope of the outer level wrapper function, and also an index into the scenarios list that has the same outer level scope.
```py
def purely_wrap_unit_inner(inp_groups_inner): # input groups object (inner level)
    nonlocal sce_inp_ind
    scenario_inner = sce_inp_lis[sce_inp_ind]
    sce_inp_ind += 1
    return groups_obj_from_sgf_triples(scenario_inner, out_group_lis, inp_groups[ACT_VALUES])
```

### Scenario Category ANalysis (SCAN)
[&uarr; Unit Testing](#unit-testing)<br />
[&darr; Simple Category Sets](#simple-category-sets)<br />
[&darr; Composite Category Sets](#composite-category-sets)<br />
[&darr; Scenario Category Mapping](#scenario-category-mapping)<br />

The art of unit testing lies in choosing a set of scenarios that will produce a high degree of confidence in the functioning of the unit under test across the often very large range of possible inputs.

A useful approach to this is to think in terms of categories of inputs, where we reduce large ranges to representative categories. Categories are chosen to explore the full range of potential behaviours of the unit under test.

In this section we identify the category sets for the problem, and tabulate the corresponding categories. We need to consider which category sets can be tested independently of each other, and which need to be considered in combination. We can then obtain a set of scenarios to cover all relevant combinations of categories.

#### Simple Category Sets
[&uarr; Scenario Category ANalysis (SCAN)](#scenario-category-analysis-scan)<br />
[&darr; SAF - Scenario active flag](#saf---scenario-active-flag)<br />
[&darr; MUL-0 - Multiplicity including zero](#mul-0---multiplicity-including-zero)<br />
[&darr; MUL-1 - Multiplicity excluding zero](#mul-1---multiplicity-excluding-zero)<br />
[&darr; INV - Invalidity Type](#inv---invalidity-type)<br />

In this section we identify some simple category sets to apply.

##### SAF - Scenario active flag
[&uarr; Simple Category Sets](#simple-category-sets)<br />

We want to check that active scenarios are processed while inactive ones are ignored.

| Code | Description       |
|:----:|:------------------|
|  Y   | Scenario active   |
|  N   | Scenario inactive |

##### MUL-0 - Multiplicity including zero
[&uarr; Simple Category Sets](#simple-category-sets)<br />

We want to check behaviour when there are 0, 1, or more than 1, records for each entity, for those entities where zero multiplicity makes sense.

| Code | Description     |
|:----:|:----------------|
|  0   | Zero values     |
|  1   | 1 value         |
|  m   | Multiple values |

This category set is applied to the following entities:

| Category Set | Description               |
|:------------:|:--------------------------|
| IGM          | Input group multiplicity  |
| OGM          | Output group multiplicity |
| IVM          | Input value multiplicity  |
| OVM          | Output value multiplicity |

##### MUL-1 - Multiplicity excluding zero
[&uarr; Simple Category Sets](#simple-category-sets)<br />

We want to check behaviour when there are 1, or more than 1, records for each entity, for those entities where zero multiplicity does not make sense.

| Code | Description     |
|:----:|:----------------|
|  1   | 1 value         |
|  m   | Multiple values |

This category set is applied to the following entities:

| Category Set | Description                       |
|:------------:|:----------------------------------|
| SCM          | Scenario multiplicity             |
| IFM          | Input field multiplicity          |
| OFM          | Output field multiplicity         |
| DCM          | Delimiter characters multiplicity |

##### INV - Invalidity Type
[&uarr; Simple Category Sets](#simple-category-sets)<br />

A unit test returns a status of Failure if any output group returns a status of Failure, which happens when the actual output set of records differs from the expected output set.

We can categorise types of invalidity by set cardinality differences (with E for expected set cardinality, and A for actual set cardinality). We want to check behaviour for each type of invalidity as well as the valid case.

| Code    | Description                                                 |
|:-------:|:------------------------------------------------------------|
|  VAL    | Same cardinalities and all records the same                 |
|  E=A    | Same cardinalities but at least one record differs in value |
|  E&gt;A | More records in expected set than in actual set             |
|  A&gt;E | More records in actual set than in expected set             |

#### Composite Category Sets
[&uarr; Scenario Category ANalysis (SCAN)](#scenario-category-analysis-scan)<br />
[&darr; IGM / OGM](#igm--ogm)<br />
[&darr; SCM / SAF ](#scm--saf-)<br />

The category sets considered can be treated as largely independent, with the exception that having zero multiplicity for both input and output groups doesn't make sense, and making a scenario inactive means nothing else can be tested within that scenario. Therefore we can take the following combinations of the category sets IGM, OGM as the basis of our scenario category mapping, and ensure that the combinations noted below of SCM and SAF are handled.

The Invalidity Type category set could be tested within the third scenario, but we'll add a fourth scenario for greater clarity.

##### IGM / OGM
[&uarr; Composite Category Sets](#composite-category-sets)<br />

Ensure the zero edge case for input groups and output groups are handled separately, and note that 0 for either group implies no fields are possible.

| IGM | OGM | IFM | OFM |
|:---:|:---:|:---:|:---:|
|  0  |  1  |  -  |     |
|  1  |  0  |     |  -  |
|  m  |  m  |     |     |

##### SCM / SAF 
[&uarr; Composite Category Sets](#composite-category-sets)<br />

Ensure that the inactive scenario category occurs within a multi-scenario situation, so that other categories can be simultaneously tested.

| SCM | SAF |
|:---:|:---:|
|  1  |  Y  |
|  m  |  N  |

#### Scenario Category Mapping
[&uarr; Scenario Category ANalysis (SCAN)](#scenario-category-analysis-scan)<br />

We now want to construct a set of scenarios based on the category sets identified, covering each individual category, and also covering combinations of categories that may interact.

In this case, the first four category sets may be considered as a single composite set with the combinations listed below forming the scenario keys, while the two SIZ categories are covered in the first two scenarios.

| #  | IGM | OGM | IVM | OVM | SCM | IFM | OFM | DCM | SAF | INV | Description                                                                |
|:---|:---:|:----|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:-------------------------------------------------------------------------------------|
| 1  |  0  |  1  |  -  |  0  |  1  |  -  |  1  |  1  |  Y  | VAL | Zero input groups, 1 of other entities where possible; active scenario; valid | 
| 2  |  1  |  0  |  1  |  -  |  1  |  1  |  -  |  1  |  Y  | VAL | Zero output groups, 1 of other entities where possible; active scenario; valid | 
| 3  |  m  |  m  |  m  |  m  |  m  |  m  |  m  |  m  |  N  | VAL | Multiple entities; one inactive scenario; all valid  | 
| 4  |  1  |  1  |  m  |  m  |  m  |  m  |  m  |  m  |  Y  |  *  | One input and output groups; multiple other entities; active scenarios; each type of invalid scenario | 

### Unit Test Results
[&uarr; Unit Testing](#unit-testing)<br />
[&darr; Results Summary](#results-summary)<br />
[&darr; Unit Test Report: Python Unit Tester](#unit-test-report-python-unit-tester)<br />

#### Results Summary
[&uarr; Unit Test Results](#unit-test-results)<br />

```
Unit Test Results Summary for Folder ./externals/python
=======================================================
 File                 Title               Inp Groups  Out Groups  Tests  Fails  Folder            
--------------------  ------------------  ----------  ----------  -----  -----  ------------------
*colgroup_out.json    Col Group                    3           4      5      1  col-group         
 helloworld_out.json  Hello World                  0           1      1      0  hello-world       
 trapit_py_out.json   Python Unit Tester           7           6      4      0  python-unit-tester

1 externals failed, see ./externals/python for scenario listings
colgroup_out.json
```

You can review the HTML formatted unit test results here:

- [Unit Test Report: Python Unit Tester](http://htmlpreview.github.io/?https://github.com/BrenPatF/trapit_python_tester/blob/main/unit_test/python-unit-tester/python-unit-tester.html)

#### Unit Test Report: Python Unit Tester
[&uarr; Unit Test Results](#unit-test-results)<br />
```
Unit Test Report: Python Unit Tester
====================================

      #    Scenario                                                                                               Fails (of 6)  Status 
      ---  -----------------------------------------------------------------------------------------------------  ------------  -------
      1    Zero input groups, 1 of other entities where possible; active scenario; valid                          0             SUCCESS
      2    Zero output groups, 1 of other entities where possible; active scenario; valid                         0             SUCCESS
      3    Multiple entities; one inactive scenario; all valid                                                    0             SUCCESS
      4    One input and output groups; multiple other entities; active scenarios; each type of invalid scenario  0             SUCCESS

Test scenarios: 0 failed of 4: SUCCESS
======================================
```
Here are the output results for the first scenario (slightly edited for brevity):

```
SCENARIO 1: Zero input groups, 1 of other entities where possible; active scenario; valid {
===========================================================================================
   INPUTS
   ======
      GROUP 1: Unit Test {
      ====================
            #  Title        Delimiter
            -  -----------  ---------
            1  Inner title  ;        
      }
      GROUP 2: Input Fields: Empty
      ============================
      GROUP 3: Output Fields {
      ========================
            #  Group           Field         
            -  --------------  --------------
            1  Output Group 1  Output Field 1
      }
      GROUP 4: Scenario {
      ===================
            #  Scenario          Active Y/N
            -  ----------------  ----------
            1  Inner scenario 1  Y         
      }
      GROUP 5: Input Values: Empty
      ============================
      GROUP 6: Expected Values {
      ==========================
            #  Scenario          Group           Row CSV         
            -  ----------------  --------------  ----------------
            1  Inner scenario 1  Output Group 1  Expected value 1
      }
      GROUP 7: Actual Values {
      ========================
            #  Scenario          Group           Row CSV       
            -  ----------------  --------------  --------------
            1  Inner scenario 1  Output Group 1  Actual value 1
      }
   OUTPUTS
   =======
      GROUP 1: Unit Test {
      ====================
            #  Title        Delimiter
            -  -----------  ---------
            1  Inner title  ;        
      } 0 failed of 1: SUCCESS
      ========================
      GROUP 2: Input Fields: Empty as expected: SUCCESS
      =================================================
      GROUP 3: Output Fields {
      ========================
            #  Group           Field         
            -  --------------  --------------
            1  Output Group 1  Output Field 1
      } 0 failed of 1: SUCCESS
      ========================
      GROUP 4: Input Values: Empty as expected: SUCCESS
      =================================================
      GROUP 5: Expected Values {
      ==========================
            #  Scenario          Group           Row CSV         
            -  ----------------  --------------  ----------------
            1  Inner scenario 1  Output Group 1  Expected value 1
      } 0 failed of 1: SUCCESS
      ========================
      GROUP 6: Actual Values {
      ========================
            #  Scenario          Group           Row CSV       
            -  ----------------  --------------  --------------
            1  Inner scenario 1  Output Group 1  Actual value 1
      } 0 failed of 1: SUCCESS
      ========================
} 0 failed of 6: SUCCESS
========================
```

## See Also
[&uarr; In This README...](#in-this-readme)<br />

- [Database API Viewed As A Mathematical Function: Insights into Testing](https://www.slideshare.net/brendanfurey7/database-api-viewed-as-a-mathematical-function-insights-into-testing)
- [Unit Testing, Scenarios and Categories: The SCAN Method](https://brenpatf.github.io/jekyll/update/2021/10/17/unit-testing-scenarios-and-categories-the-scan-method.html)
- [Trapit JavaScript Tester/Formatter - GitHub module](https://github.com/BrenPatF/trapit_nodejs_tester)
- [Trapit Python Tester - GitHub module](https://github.com/BrenPatF/trapit_python_tester)
- [Trapit Oracle Tester - GitHub module](https://github.com/BrenPatF/trapit_oracle_tester)
- [Powershell Utilities - GitHub module](https://github.com/BrenPatF/powershell_utils)
- [Trapit Python Tester - Python Package Index module](https://pypi.org/project/trapit/)
- [Timer Set Python Code Timer - GitHub module](https://github.com/BrenPatF/timerset_python)

## License
[&uarr; In This README...](#in-this-readme)<br />

MIT

