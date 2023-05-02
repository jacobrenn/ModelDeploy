FROM nvidia/cuda:11.4.0-base-ubuntu-22.04

RUN apt update
RUN apt-get install -y python3 python3-pip

ADD main.py .
ADD requirements.txt .

EXPOSE 2244

RUN pip install -r requirements.txt

CMD ["python", "./main.py", "aisquared/dlite-v1-124m"]