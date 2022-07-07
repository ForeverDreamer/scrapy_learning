FROM python:3.7.3-alpine3.9

RUN apk --no-cache add py-pip

COPY . /www
WORKDIR /www/pps_web
RUN pip install -r requirements.txt


EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]