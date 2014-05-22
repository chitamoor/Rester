RESTTest
========
Framework for testing RESTful APIs
----------------------------------
RESTTest allows you to test your APIs using a non-programatic or non-GUI based approach (which are some of the more conventional ways of testing RESTFul APIs). RESTTest is inspired by various unit testing frameworks like JUnit, 'unittest' (python) etc and is conceptually organized like those frameworks but is geared towards testing RESTful API endpoints. With RESTTest, all tests are specified in JSON, so it can also be used by non-programmers as well. 

#So, why RESTTest?
Testing RESTful APIs generally involves two prediticable steps -

- Invoke the API end point
- Validate the response - headers, payload etc

Most testing tools available for testing RESTful APIs use some sort of a GUI based approach which doesn't lend itself towards re-use, better code organization, abstraction etc and some of the other benefits that are generally available with more programmatic frameworks like JUnit. Programmatically building test cases provides the highest level of flexibility and sophistication, but the downside to this approach is that it ends up with lots of fairly tedious and repetitive code. Conceptually, RESTTest is similar to existing unit testing frameworks, but it uses JSON (instead of a programming language) to implement/specify the actual tests. It can be used by programmers and non-programmers alike, but reap all the benefits of a unittesting framework.


Note: As of now RESTTest only supports APIs that don't require explicit authentication of calls, but future versions will support OAuth. The RESTTest was mainly created to test internal RESTful APIs that generally bypass the need for authentication of the calls. Also, RESTTest only supports validation of JSON responses.

#Practical uses of RESTTest
- Perform "integration" testing of internal and external RESTful API endpoints
- Examine and test complex response payloads 
- You can simply use RESTTest to dump and analyze API responses - headers, payload etc.

#Assumptions
- RESTTest does not manage the life-cycle of the container or the server that exposes the API endpoints. RESTTest assumes the API endpoints to be tested are up and avaliable.
- Unlike other unittesting frameworks however, RESTTest does guarantee the order of execution of the **TestSteps** within a **TestCase**. For a better understanding of TestSteps and TestCases see the "General Concepts" section below. The **ordering** will come in hands if you want to test a series of API end-points (invoked in succession) that modify system state in a particular way.


#General Concepts
* **TestSuite**:
 A *TestSuite* is collection of *TestCases*. The idea is to group related 'test cases' together.

```
{
   "test_cases":[
                 "test_case_1.json", 
                 "test_case_2.json"
                ]
}
```

* **TestCase**:
 A *TestCase* contains one or more *TestSteps*. You can declare **globals** variables to be re-used across test steps. For a more complete list of all the options, please see -


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
         ... each TestStep is specified in here
      },
      {
         ...  each TestStep is specified in here
      }
    ]
 ```

* **TestStep**:
  All of the action in RESTTest takes place in a **TestStep**.
For a more complete list of all the options, please see.

A TestStep contains the following -

- **API end point invocation** - As part of the API endpoint invocation, you are expected to supply the following minimal params -
  - URL
  - URL params
  - HTTP method - get, put, post, delete ('get' is used by default)

- A series of assert statements specified as part of an **AssertMap**
- Post step assignments

Example of a TestStep:

  ```
  testSteps: [
    {
       "name":"Name of TestStep",
  		   "apiUrl":"http://example/api/v1/helloworld/print",
       "assertMap":{
             "headers":{
                 "content-type":"application/json; charset=utf-8"
             }
             "payLoad":{
                "message":"Hello World!"
             }
       }
    }    
  ]
  ```

#Pre-reqs/Dependencies
* requests - pip install requests

#Installation
Clone the repo and get started!
The main class is testapi.py

#RESTTest command line options
- Run the default test case -

  `python apirunner.py`

  This will look for the default test case, ***test_case.json***
- Run a specific test case - use the command line option ***--tc=<file_name>***

  e.g. invoke a test case specified in the file "test_case.json"

  `python apirunner.py --tc=test_case.json`

- Run a specific test suite
  `python apirunner.py --ts=test_suite.json`

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

#Examples of API request invocations 
- Specify the HTTP headers as part of an API request 
 ```
  testSteps: [
    {
       "name":"Name of TestStep",
  		   "apiUrl":"http://example/api/v1/helloworld/print",
  		   "headers":{
            "content-type":"application/json;"
       },
       ....
    }    
  ]
  ```

- Specify the URL params as part of an API request 
  Two ways to specific URL params
  
  ```
  testSteps: [
    {
       "name":"Name of TestStep",
  		   "apiUrl":"http://example/api/v1/helloworld/print",
       "params":{
            "param_1":"value1", 
            "param_2":"value2"
       },
       ....
    }    
  ]
  ```


   ```
  testSteps: [
    {
       "name":"Name of TestStep",
  		   "apiUrl":"http://example/api/v1/helloworld/print?param_1=value1&param_2=value2",
       ....
    }    
  ]
  ```

# Re-using declarations
- Variables are declared in the "globals" section of the TestSuite
  ```
   "globals":{
      "variables":{
        "baseApiUrl":"https://api.prevoty.com",
        "api_key":"YOUR_KEY",
        "rule_key":"CONFIG_KEY"
      }
   },
   ... 
   ```
  

#TODO
- Create a package support and PyPi distributable
- Unit Tests
- Plenty of refactoring :-)
- Support for POSTing JSON payloads
- More logical operators checks for the asserts - e.g. ne, gt, lt etc
- Cleaner results summary (Tabular?)
- Support for simple datatypes - lists, integers, strings etc
- Supoport for JSON schema validation
- Support for enums
- Support for OAuth/authentication
- Experiment with YAML format for specifying the tests


