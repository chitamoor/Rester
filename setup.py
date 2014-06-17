from setuptools import setup

setup(name='Rester',
    version='0.5.0',
    author='Rajeev Chitamoor',
    author_email='rajeev@chitamoor.com',
    url='https://github.com/chitamoor/rester',
    license='LICENSE.txt',
    packages=['rester'],
    entry_points={
        'console_scripts':['apirunner = rester.apirunner:run']
    },
    test_suite="test",
    description='Rest API Testing',
    long_description=open('README').read(),
    install_requires=["requests"],
)
