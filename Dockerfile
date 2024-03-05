FROM python:3.12-alpine

RUN adduser -D -h / -s /bin/sh app_user

WORKDIR /home/app_user/outline-cli-app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

USER app_user

COPY . .

CMD ["sh"]