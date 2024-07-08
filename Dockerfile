FROM python:3.10.8

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

COPY api-flask-rest-firebase-adminsdk-6f0w1-319d793f16.json .

ENV FIREBASE_AUTH=api-flask-rest-firebase-adminsdk-6f0w1-319d793f16.json
ENV JWT_SECRET_KEY=flask-secret-jwt

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
