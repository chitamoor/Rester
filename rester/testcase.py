import json
import requests
import re
import logging
import re


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
            #print "name : " + name
            return self.__dict__[name]

    def __setattr__(self, key, value):
        self.__dict__[key] = JsonWrapper(value) if isinstance(value, dict) else value


    def items(self):
        return self.__dict__

class JsonResponseWrapper(object):
    def __init__(self, json, headers):
        self.json_wrapper = JsonWrapper(json)
        self.headers = JsonWrapper(headers)


# Module level functions
def is_string(expression):
    #self.logger.debug(" _is_string : %s ", type(expression))
    return expression and (isinstance(expression, unicode) or isinstance(expression, str))


def is_number(expression):
    if is_string(expression):
        expression = expression.strip()
        num_format = re.compile("^[-+]?[0-9]*\.?[0-9]*$")
        return re.match(num_format, expression)

def check_for_logical_op(expression):
    if is_string(expression):
        #self.logger.debug("_check_for_logical_op : expression %s", expression)
        oprtr_regex = re.compile("-lt|-le|-gt|-ge|-eq|-ne")
        match = re.match(oprtr_regex, expression)
        if match:
            return match.group()


class ApiTestCaseRunner:

    def __init__(self, logger):
        self.logger = logger
        self._variables = {}
        self._globalAssertMaps = {}
        self._test_cases = []
        self._pattern = re.compile(r'\{(\w+)\}')

    def run_test_suite(self, test_suite_file_name):
        test_suite = self._process_test_file(test_suite_file_name)
        for test_case_file_name in test_suite.test_cases:
            print "test case : " + test_case_file_name
            self.run_test_case(test_case_file_name)

    def run_test_case(self, test_case_file_name):
        test_case = self._process_test_file(test_case_file_name)
        self._test_cases.append(test_case)
        self._process_config(test_case)

    def display_report(self):
        self.logger.info("\n\n ############################ TEST RESULTS ############################")
        for test_case in self._test_cases:
            print "\n\n ===> TestCase : {0}, status : {1}".format(test_case.name, "Passed" if test_case.passed == True else "Failed!")
            for test_step in test_case.testSteps:
                #self.logger.info('\n     ====> Test Step name : %s, status : %s, message : %s', test_step.name, test_step.result.status, test_step.result.message)
                print "\n\n     ====> Test Step : {0}".format(test_step.name)

                if hasattr(test_step, 'result'):
                    print "\n\n         ====> {0}!".format(test_step.result.message)

                if hasattr(test_step, 'assertResults'):
                    for assert_result in test_step.assertResults:
                        #self.logger.debug('\n assert_result : ' + str(assert_result))
                        print "\n        ---> {0}".format(assert_result['message'])

    def _process_test_file(self, test_file):
        with open(test_file) as file:
            self.logger.info('Processing test file %s', test_file)
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

            self.logger.debug('Test Step Name : %s', test_step.name)

            test_case.passed = True
            if not skip_all_aubsequent_tests:
                if hasattr(test_step, 'skip') and test_step.skip == True:
                    self.logger.info('\n=======> Skipping test case : ' + test_step.name + ' !')
                    test_step.result = {"status": True, "message": "Skipped"}
                else:
                    self._execute_test_step(test_case, test_step)

    def _execute_test_step(self, test_case, test_step):
        try:
            self.logger.debug(
                '\n=======> Executing TestStep : %s ', test_step.name)

            method = test_step.method if hasattr(
                test_step, 'method') else "get"

            # process and set up headers
            headers = {}
            if hasattr(test_step, 'headers') and test_step.headers is not None:
                self.logger.debug('Found Headers')
                for key, value in test_step.headers.items().items():
                    headers[key] = self._evaluate_expression(value)

            # process and set up params
            params = {}
            if hasattr(test_step, 'params') and test_step.params is not None:
                self.logger.debug('Found params')
                for key, value in test_step.params.items().items():
                    params[key] = self._evaluate_expression(value)

            self.logger.debug(
                'Evaluated URL : %s', self._evaluate_expression(test_step.apiUrl))
            json_response_wrapper = self._get_api_json_response_wrapper(
                self._evaluate_expression(test_step.apiUrl), method, headers, params, True)
            if json_response_wrapper is None:
                return "Invalid JSON response or Error code"

            if hasattr(test_step, "assertMap"):
                assertMap = test_step.assertMap
                if hasattr(assertMap, "headers"):
                    self.logger.debug('Evaluating Response headers : ' + str(json_response_wrapper.headers))
                    self._assert_element_list(test_step, json_response_wrapper.headers, test_step.assertMap.headers.items().items())

                if hasattr(assertMap, "payLoad"):
                    self.logger.debug('Evaluating Response Payload')
                    self._assert_element_list(test_step, json_response_wrapper.json_wrapper, test_step.assertMap.payLoad.items().items())

            if test_case.passed == True:
                test_case.passed = test_step.result.status

        except Exception as inst:
            self.logger.error('Exception : %s', inst)
            self.logger.error('ERROR !!! TestStep %s Failed to execute !!!  %s \
                        \n !!! Will ignore all assignment statements as part of TestStep', test_step.name, inst)
            test_step.result = {"status": False, "message": inst}

    def _assert_element_list(self, test_step, target_response, assert_list):
        self.logger.debug("Inside assert_element_list : " + str(target_response))

        test_step.assertResults = []

        for key, value in assert_list:
            self.logger.debug('key : %s, value : %s', key, value)

            json_eval_expr = getattr(target_response, key, '')

            if is_number(json_eval_expr):
                json_eval_expr = float(json_eval_expr)

            self.logger.debug('json_eval_expr : %s ', json_eval_expr)

            # Check for logical operators
            logic_ops = {'-gt':'>', '-ge':'>=', '-lt':'<', '-le':'<=', '-ne':'!=', '-eq':'=='}
            lg_op_expr = check_for_logical_op(value)
            if lg_op_expr:
                self.logger.debug("---> Found lg_op_expr : " + lg_op_expr)

            if lg_op_expr and logic_ops.has_key(lg_op_expr):
                final_lg_op = logic_ops[lg_op_expr]
                value_segs = value.split(lg_op_expr)
                rest_of_value_expr = ('').join(value_segs)
                value = rest_of_value_expr
                self.logger.debug("     -----> Rest of the expression : " + value)
            else:
                # - If no operators found then assume '=='
                final_lg_op = logic_ops['-eq']

            self.logger.debug("---> Final final_lg_op : " + final_lg_op)

            value = self._evaluate_expression(value)
            self.logger.debug(' ---> final evaluated expression  : %s and type %s ', value, type(value))

            # construct the logical assert expression
            assert_expr = 'json_eval_expr {0} value'.format(final_lg_op)
            assert_literal_expr = '"{0} {1} {2}"'.format(json_eval_expr, final_lg_op, value)

            self.logger.debug('     ---> Assert_expr : ' + assert_expr)

            assert_result = eval(assert_expr)

            self.logger.debug('assert evaluation result  : %s', assert_result)


            if not assert_result:
                assert_message = 'Assert Statement : {0}   ---> Fail!'.format(assert_literal_expr)
                self.logger.error('%s', assert_message)
                test_step.result = {"status": False, "message": assert_message}
                test_step.assertResults.append({"status": False, "message": assert_message})

            else:
                assert_message = 'Assert Statement : {0}  ----> Pass!'.format(assert_literal_expr)
                self.logger.info('%s', assert_message)
                test_step.result = {"status": True, "message": assert_message}
                test_step.assertResults.append({"status": True, "message": assert_message})


    def _get_api_json_response_wrapper(self, api_url, method, headers, params, dump_response):
        self.logger.debug(
            '\n Invoking REST Call... api_url: %s, method: %s : ', api_url, method)
        allowed_methods = ["get", "post", "put", "delete"]
        if method in allowed_methods:
            json_response = getattr(requests, method)(api_url, headers=headers, params=params)
        else:
            self.logger.error('undefined HTTP method!!! %s', method)

        if dump_response:
            self.logger.info('JSON response Headers -  %s' + str(json_response.headers))
            self.logger.info('JSON response -  %s' + json.dumps(
                json_response.json(), sort_keys=True, indent=2))

        if json_response.status_code is 200:
            #return JsonWrapper(json_response.json())
            return JsonResponseWrapper(json_response.json(), json_response.headers)
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
        self.logger.debug("_evaluate_expression : expression %s", str(expression))
        if not is_string(expression):
            return expression

        result = self._pattern.sub(
            lambda var: str(self._variables[var.group(1)]), expression)

        result = result.strip()
        self.logger.debug('_evaluate_expression : %s - result : %s', expression, result)

        if is_number(result):
            if result.isdigit():
                self.logger.debug('     _evaluate_expression is integer !!!')
                return int(result)
            else:
                self.logger.debug('     _evaluate_expression is float !!!')

                return float(result)

        return result


#TODO
# Support enums
# Support basic types
# Set up one more API examples

