FROM python

RUN apt-get update -y && \
    apt-get update -y && \
    apt-get install cron ntpdate -y 

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENV APP_ENV=production

RUN ntpdate -B -q time.nist.gov

EXPOSE 8080

ADD start.sh /

CMD ./start.sh; python /app/app.py