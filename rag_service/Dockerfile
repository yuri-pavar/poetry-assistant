FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

WORKDIR /app

RUN apt update && apt install -y python3 python3-pip git && pip3 install --upgrade pip

COPY rag_service ./rag_service
COPY data ./data
COPY rag_service/requirements.txt .

RUN pip install -r requirements.txt

CMD ["uvicorn", "rag_service.main:app", "--host", "0.0.0.0", "--port", "8100"]