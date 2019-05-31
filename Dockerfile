FROM python:3.7

WORKDIR /usr/src/app
ENV SUPER_USERNAME=admin
ENV SUPER_EMAIL=admin@io.pl
ENV SUPER_PASSWORD=pass1234
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000 8080 4352

CMD bash -c "sleep 20; python ./manage.py makemigrations search4recipes; python ./manage.py migrate; python ./manage.py initAdmin; python ./manage.py runserver 0.0.0.0:8000;"