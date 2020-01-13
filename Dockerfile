FROM python:3

ADD ./DNSProxy.py /
EXPOSE 6565

CMD [ "python", "./DNSProxy.py" ]
