FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

COPY api-flask-secret.json .

ENV FIREBASE_AUTH=api-flask-secret.json
ENV JWT_SECRET_KEY=flask-secret-jwt

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
