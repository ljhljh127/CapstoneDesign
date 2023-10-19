FROM tiangolo/uvicorn-gunicorn:python3.9

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["sh", "-c", "nohup python3 gRPCserver.py & uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]
