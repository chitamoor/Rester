import logging
import argparse
from testcase import ApiTestCaseRunner

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
    log_level, test_case, test_suite = parse_cmdln_args()
    print log_level, test_case, test_suite
    logging.basicConfig()
    logger = logging.getLogger('ApiTestCaseRunner')
    logger.setLevel(log_level)
    print log_level
    test_runner = ApiTestCaseRunner(logger)
    if test_case is not None:
        print "test case has been specified"
        test_runner.run_test_case(test_case)
    elif test_suite is not None:
        print "test suite has been specified"
        test_runner.run_test_suite(test_suite)
    else:
        print "running the default test case"
        test_runner.run_test_case(DEFAULT_TEST_CASE)
    test_runner.display_report()

if (__name__ == '__main__'):
    run()

