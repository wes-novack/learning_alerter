FROM python:3.8

WORKDIR /opt/learning_alerter/

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT [ "python", "./main.py" ]