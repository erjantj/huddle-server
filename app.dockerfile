FROM python:3.6

ENV FLASK_ENV development
ENV FLASK_APP flaskr

WORKDIR /var/www

COPY requirements.txt /var/www
RUN pip install -r requirements.txt

EXPOSE 5000

CMD flask run -h 0.0.0.0 -p 5000