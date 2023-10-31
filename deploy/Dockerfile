FROM python:3.8-slim-buster

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=myapp
ENV FLASK_ENV=prod
ENV HOST=0.0.0.0
ENV PORT=5000
ENV SECRET=secret

CMD ["python", "server.py"]
