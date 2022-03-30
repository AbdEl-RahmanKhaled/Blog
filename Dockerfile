FROM python:3.8

RUN mkdir -p /usr/src/blog

COPY . /usr/src/blog

WORKDIR /usr/src/blog

RUN pip install --no-cache-dir -r ./requirements.txt

ENV PRIVET_KEY=d"jango-insecure-73^7k)g32y4#^&k%#vh#^7-ip(xo3ttg^0)lsmdiy7kd7k^k+"
ENV DB_HOST="db_server"
ENV DB_USER="postgres"
ENV DB_PASS="admin"

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]
