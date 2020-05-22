FROM liaojl/website:v0.1.5

ADD requirements.txt /requirements.txt

RUN pip3 install -r /requirements.txt

ENV PYTHONPATH=/cpchain-website

WORKDIR /cpchain-website
