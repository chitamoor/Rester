import json
import requests
import re
import logging

# TODO
# - Aggregate results and print summary
#    - Clean up output
# - Other command line options
#   - just dump output
#   - dump to an output file
#   - Add short and long command line option
# - Documentation - borrow concepts from - https://docs.python.org/2/library/unittest.html

# - Define modes of operation
#   - Run an individual test case
#   - Run a test suite
#   - Pass cmd line args to both test cases and test suites


class JsonWrapper(object):

    def __init__(self, d):
        for key, value in d.items():
            if isinstance(value, (list, tuple)):
                setattr(
                    self, key, [JsonWrapper(x) if isinstance(x, dict) else x for x in value])
            else:
                setattr(self, key, JsonWrapper(value)
                        if isinstance(value, dict) else value)

    def __getattr__(self, name):
        levels = name.split(".")
        if len(levels) > 1:
            curr_level = levels.pop(0)
            return getattr(self.__dict__[curr_level], '.'.join(levels))
        else:
            return self.__dict__[name]

    def __setattr__(self, key, value):
        self.__dict__[key] = JsonWrapper(value) if isinstance(value, dict) else value

    def items(self):
        return self.__dict__


class ApiTestCaseRunner:

    def __init__(self, logger):
        self.logger = logger
        self._variables = {}
        self._globalAssertMaps = {}
        self._test_cases = []
        self._pattern = re.compile(r'\{(\w+)\}')

    # def run_test_suite(testSuiteFile, configFile):
    #     if (configFile):
    #         processConfig(parseJsonFile(configFile))
    #     }
    #     def testSuite = parseJsonFile(testSuiteFile)
    #     testSuite.tests.each {
    #         runTestCase(new File(it))
    #     }
    #     displayReport();

    def run_test_case(self, test_case_file):
        test_case = self._process_test_suite(test_case_file)
        self._test_cases.append(test_case)
        self._process_config(test_case)

    def display_report(self):
        self.logger.info("\n\n ############################ TEST RESULTS ############################")
        for test_case in self._test_cases:
            self.logger.info('\n\n ===> TestCase  name : %s, status : %s', test_case.name, "Passed" if test_case.passed == True else "Failed!")
            for test_step in test_case.testSteps:
                self.logger.info('\n     ====> Test Step name : %s, status : %s, message : %s', test_step.name, test_step.result.status, test_step.result.message)

    def _process_test_suite(self, test_case_file):
        with open(test_case_file) as file:
            self.logger.info('Processing test suite %s', test_case_file)
            json_data = json.load(file)
            return JsonWrapper(json_data)

    def _process_config(self, test_case):
        for key, value in test_case.globals.variables.items().items():
            self._process_variable(key, value)
        self._execute_test_case(test_case)

    def _execute_test_case(self, test_case):
        skip_all_aubsequent_tests = False
        test_case.passed = True
        for test_step in test_case.testSteps:
            self.logger.debug('Test Case Name : %s', test_step.name)
            test_case.passed = True
            if not skip_all_aubsequent_tests:
                if hasattr(test_step, 'skip') and test_step.skip == True:
                    self.logger.info('\n=======> Skipping test case !!!')
                    test_step.result = {
                        "status": True, "message": "Skipped!!!"}
                else:
                    self._execute_test_step(test_case, test_step)

    def _execute_test_step(self, test_case, test_step):
        try:
            self.logger.debug(
                '\n=======> Executing TestStep : %s ', test_step.name)

            method = test_step.method if hasattr(
                test_step, 'method') else "get"

            params = {}
            if hasattr(test_step, 'params') and test_step.params is not None:
                self.logger.debug('Found params')
                for key, value in test_step.params.items().items():
                    params[key] = self._evaluate_expression(value)

            self.logger.debug(
                'Evaluated URL : %s', self._evaluate_expression(test_step.apiUrl))
            json_response = self._get_api_json_response(
                self._evaluate_expression(test_step.apiUrl), method, params, True)
            if json_response is None:
                return "Invalid JSON response or Error code"

            if hasattr(test_step, "assertMap"):
                self.logger.debug('Evaluating assertMaps')
                for key, value in test_step.assertMap.items().items():
                    self.logger.debug("key : %s, value : %s", key, value)
                    json_eval_expr = getattr(json_response, key, '')
                    if json_eval_expr != value:
                        assert_message = 'Assert Failed!!! for key : %s, json_eval_expr : %s,\
                        assert_msg : %s', key, json_eval_expr, value
                        self.logger.error('%s', assert_message)
                        test_step.result = {
                            "status": False, "message": assert_message}
                    else:
                        assert_message = 'Assert Passed! for key : %s, json_eval_expr : %s,\
                        assert_msg : %s', key, json_eval_expr, value
                        test_step.result = {"status": True, "message": assert_message}

            if test_case.passed == True:
                test_case.passed = test_step.result.status

        except Exception as inst:
            self.logger.error('Exception : %s', inst)
            self.logger.error('ERROR !!! TestStep %s Failed to execute !!!  %s \
                        \n !!! Will ignore all assignment statements as part of TestStep', test_step.name, inst)
            test_step.result = {"status": False, "message": inst}

    def _get_api_json_response(self, api_url, method, params, dump_response):
        self.logger.debug(
            '\n Invoking REST Call... api_url: %s, method: %s : ', api_url, method)
        allowed_methods = ["get", "post", "put", "delete"]
        if method in allowed_methods:
            json_response = getattr(requests, method)(api_url, params=params)
        # if method == 'get':
        #     json_response = requests.get(api_url, params=params)
        # elif method == 'post':
        #     json_response = requests.post(api_url, params=params)
        else:
            self.logger.error('undefined HTTP method!!! %s', method)

        if dump_response:
            self.logger.info('JSON response -  %s' + json.dumps(
                json_response.json(), sort_keys=True, indent=2))

        if json_response.status_code is 200:
            return JsonWrapper(json_response.json())
        else:
            return None

    def _process_variable(self, key, value):
        if self._variables.get(key, ''):
            self.logger.warn('WARN!!! Variable : %s Already defined!!!', key)

        self._variables[key] = self._evaluate_expression(value)

        # for key, value in config_section.globals._variables.items():
        #       print key, value

        # configSection.globals.assertMaps.each {
        #     log.debug "Assert Map Name: ${it.name}"
        #     log.debug "Assert Map : ${it.assertMap}"
        #     if (globalAssertMaps["${it.name}"]) {
        #         log.warn("WARN !!!AssertMap '\${it.name}' already found.")
        #     }
        #     def name = _evaluate_expression(it.name, globalAssertMaps)
        #     globalAssertMaps["${name}"] = it.assertMap
        # }

    def _evaluate_expression(self, expression):
        self.logger.debug('_evaluate_expression : %s', expression)

        result = self._pattern.sub(
            lambda var: self._variables[var.group(1)], expression)
        return result
