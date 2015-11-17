FROM python:2.7
RUN pip install git+https://github.com/chitamoor/Rester.git@master
ADD rester/examples examples
