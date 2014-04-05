import logging
import argparse
from testcase import ApiTestCaseRunner

def parse_cmdln_args():
    parser = argparse.ArgumentParser(description='Process command line args')
    parser.add_argument('--log', help='log help', default='INFO')
    parser.add_argument(
        '--test_case', help='test_case help', default='test_case.json')

    args = parser.parse_args()
    return (args.log.upper(), args.test_case)

if (__name__ == '__main__'):
    log_level, test_case = parse_cmdln_args()
    print log_level, test_case
    logging.basicConfig()
    logger = logging.getLogger('ApiTestCaseRunner')
    logger.setLevel(log_level)
    print log_level
    test_runner = ApiTestCaseRunner(logger)
    test_runner.run_test_case(test_case)
    test_runner.display_report()
