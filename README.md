RESTTest
========
Framework for testing RESTful APIs
----------------------------------
The RESTTest allows you to test your APIs using a non-programatic or GUI based approach (which are the more conventional ways of testing internal APIs). With RESTTest, all  tests are specified in JSON, so it can also be used by non-programmers.

Note: As of now it only supports internal APIs, but future versions will support OAuth and hence external APIs as well. The RESTTest was mainly created to test internal RESTful APIs that don't require authentication of the actual REST calls.

#General Concepts
* ###TestSuite:
 A TestSuite is collection of TestCases. The idea is to group related 'test cases' together. Global variables that need to be shared across the test cases can be declared as part of the test suite.


* ###TestCase:
 A TestCase contains one or more TestSteps. You can declare **globals** variables to be re-used across test steps. For a more complete list of all the options, please see -


```
{
   "name":"Test Case X",
   "globals":{
      "variables":{
        "base_api_url":"https://example/api/v1",
        "api_key":"xxxx"
      }
   },
   "testSteps":[
      {
         ...
      },
      {
         ...
      }
    ]
 ```

* ###TestStep:
  All of the action in RESTTest takes place in a TestStep**
For a more complete list of all the options, please see.
A TestStep contains the following -

- **API invocation** - As part of the API invocation, you are expected to supply the following minimal params -
  - URL
  - URL params
  - HTTP methods - get, put, post, delete

- A series of assert statements specified as part of an **AssertMap**
- Post step assignments

Example of a TestStep:

  ```
  testSteps: [
       "name":"Name of TestStep",
  		"apiUrl":"http://example/api/v1/helloworld/print",
         "assertMap":
         [
             {
                "message":"Hello World!",
             }
         ]
  ]
  ```

#Pre-reqs/Dependencies
* requests - pip install requests

#Installation
Clone the repo and get started!
The main class is testapi.py

#RESTTest Invocation Patterns
- Run the default test case -

  ```python apirunner.py```

  This will look for the default test case, ***test_case.json***
- Run a specific test case - use the command line option ***--tc=<file_name>***

  e.g. invoke a test case specified in the file "test_case.json"

  ```python apirunner.py --tc=test_case.json```

- Run the default test suite
- Run a specific test suite

#Other command line options
- Adjust the log output or details
  RESTTest support varying levels of logs - DEBUG, INFO, WARN, ERROR. You can
  specify the level using the command line option ***--log=<LEVEL>***

  e.g. run the API with INFO level

  ```python apirunner.py  --log=INFO```

- Just dump the JSON output

#Intepreting the results
All the results are directed to the console by default. You can control the level of output by specifying the --log command line option. You can direct the output to a file using the --opfile command line option.

#TestCase options
- **Skipping tests**

#TestStep options

#Organizing the tests

#TODO
- Support for HTTP headers
- Support of OAuth/authentication
- More logical operators for the asserts - e.g. ne, gt, lt etc
- Tabular summary
- Support for simple datatypes - lists, integers, strings etc

