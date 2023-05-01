FROM python:3.10

ADD main.py .
ADD requirements.txt .

EXPOSE 2244

RUN pip install -r requirements.txt

CMD ["python", "./main.py", "aisquared/dlite-v1-124m"]