FROM python:alpine3.6.8
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["honcho" "start" "web" "worker" "cron"]