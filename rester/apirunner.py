from testcase import ApiTestCaseRunner
import argparse
import logging
import sys

DEFAULT_TEST_CASE = 'test_case.json'


def parse_cmdln_args():
    parser = argparse.ArgumentParser(description='Process command line args')
    parser.add_argument('--log', help='log help', default='INFO')
    parser.add_argument(
        '--tc', help='tc help')
    parser.add_argument(
        '--ts', help='ts help')

    args = parser.parse_args()
    return (args.log.upper(), args.tc, args.ts)


def run():
    log_level, test_case_file, test_suite_file = parse_cmdln_args()
    print log_level, test_case_file, test_suite_file
    logging.basicConfig()
    logger = logging.getLogger('rester')
    logger.setLevel(log_level)
    test_runner = ApiTestCaseRunner()
    if test_case_file is not None:
        print "test case has been specified"
        test_runner.run_test_case(test_case_file)
    elif test_suite_file is not None:
        print "test suite has been specified"
        test_runner.run_test_suite(test_suite_file)
    else:
        print "running the default test case"
        test_runner.run_test_case(DEFAULT_TEST_CASE)
    test_runner.display_report()
    return any((result.get('failed') for result in test_runner.results))

if (__name__ == '__main__'):
    run()

