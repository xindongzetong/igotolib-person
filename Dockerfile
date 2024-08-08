FROM python:3.9

LABEL authors="SHI"

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

RUN apt-get clean && apt-get update && apt-get install -y memcached

ENTRYPOINT ["/bin/bash", "./run.sh"]