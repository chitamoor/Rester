RESTTest
========
Framework for testing RESTful APIs
----------------------------------
The RESTTest allows you to test your APIs using a non-programatic or GUI based approach (which are the more conventional ways of testing internal APIs). RESTTest is inspired by various unittesting frameworks like JUnit, unittest etc and is conceptually organized like those frameworks but is geared towards resting RESTful APIs. With RESTTest, all tests are specified in JSON, so it can also be used by non-programmers.

#So, why RESTTest?
Testing RESTful APIs generally involves two prediticable steps -

- Invoke the API end point
- Validate the response (JSON, XML etc)

Most testing tools available for testing RESTful APIs use some sort of a GUI based approach which doesn't lend itself towards re-use, better code organization, abstraction etc and some of the other benefits that are generally available with more programmatic frameworks like JUnit. Programmatically building test cases provides the highest level of flexibility and sophistication, but the downside to this approach is that it ends up with lots of fairly tedious and repetitive code. Conceptually, RESTTest is similar to existing unit testing frameworks, but it uses JSON (instead of a programming language) to implement/specify the actual tests. It can be used by programmers and non-programmers alike, but reap all the benefits of a unittesting framework.


Note: As of now RESTTest only supports APIs that don't require explicit authentication of calls, but future versions will support OAuth. The RESTTest was mainly created to test internal RESTful APIs that generally bypass the need for authentication of the calls. Also, RESTTest only supports validation of JSON responses/payloads.


#Assumptions
- RESTTest does not manage the life-cycle of the container/server that exposes the API endpoints. RESTTest assumes the API endpoints (to be tested) are up and avaliable. 
- Unlike other unittesting frameworks however, RESTTest does guarantee the order of execution of the **TestSteps** within a **TestCase**. For a better understanding of TestSteps and TestCases see the "General Concepts" section below. The **ordering** will come in hands if you want to test a series of API end-points (invoked in succession) that modify system state in a particular way.


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

  `python apirunner.py`

  This will look for the default test case, ***test_case.json***
- Run a specific test case - use the command line option ***--tc=<file_name>***

  e.g. invoke a test case specified in the file "test_case.json"

  `python apirunner.py --tc=test_case.json`

- Run the default test suite
- Run a specific test suite

#Other command line options
- Adjust the log output or details
  RESTTest support varying levels of logs - DEBUG, INFO, WARN, ERROR. You can
  specify the level using the command line option ***--log=<LEVEL>***

  e.g. run the API with INFO level

  `python apirunner.py  --log=INFO`

- Just dump the JSON output

#Intepreting the results
All the results are directed to the console by default. You can control the level of output by specifying the --log command line option. You can direct the output to a file using the --opfile command line option.

#TestCase options
- **Skipping tests**

#TestStep options

#Organizing the tests

#TODO
- Support for HTTP headers
- More logical operators for the asserts - e.g. ne, gt, lt etc
- Tabular summary
- Support for simple datatypes - lists, integers, strings etc
- Supoport for JSON schema validation
- Support for enums
- Support of OAuth/authentication
- YAML format for specifying the tests


