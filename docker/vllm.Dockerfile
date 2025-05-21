FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

RUN apt update && apt install -y git python3 python3-pip && pip3 install --upgrade pip
RUN pip install vllm

EXPOSE 8000

# CMD ["python3", "-m", "vllm.entrypoints.openai.api_server", "--model", "t-tech/T-lite-it-1.0", "--port", "8000"]
# CMD ["sh", "-c", "python3 -m vllm.entrypoints.openai.api_server --model $MODEL_NAME --port 8000 --dtype=half"]
# CMD ["sh", "-c", "python3 -m vllm.entrypoints.openai.api_server \
#   --model $MODEL_NAME \
#   --port 8000 \
#   --dtype=half \
#   --enable-lora \
#   --lora-modules poetry=/app/data/lora-poetry"]

# CMD ["sh", "-c", "python3 -m vllm.entrypoints.openai.api_server \
#   --model $MODEL_NAME \
#   --port 8000 \
#   --dtype=half \
#   --enable-lora \
#   --lora-modules poetry=/app/data/lora-poetry2,pushkin=/app/data/lora-poetry-pushkin"]

  # CMD ["sh", "-c", "python3 -m vllm.entrypoints.openai.api_server \
  # --model $MODEL_NAME \
  # --port 8000 \
  # --dtype=half \
  # --enable-lora \
  # --lora-modules 'poetry=/app/data/lora-poetry2,pushkin=/app/data/lora-poetry-pushkin'"]

  # CMD ["sh", "-c", "python3 -m vllm.entrypoints.openai.api_server \
  # --model $MODEL_NAME \
  # --port 8000 \
  # --dtype=half \
  # --enable-lora \
  # --lora-modules '[{\"name\": \"poetry\", \"path\": \"/app/data/lora-poetry2\", \"base_model_name\": \"t-tech/T-lite-it-1.0\"}, {\"name\": \"pushkin\", \"path\": \"/app/data/lora-poetry-pushkin\", \"base_model_name\": \"t-tech/T-lite-it-1.0\"}]'"]

# CMD ["sh", "-c", "python3 -m vllm.entrypoints.openai.api_server \
#   --model $MODEL_NAME \
#   --port 8000 \
#   --dtype=half \
#   --enable-lora \
#   --lora-modules '{\"name\": \"poetry\", \"path\": \"/app/data/lora-poetry2\", \"base_model_name\": \"t-tech/T-lite-it-1.0\"}' \
#   --lora-modules '{\"name\": \"pushkin\", \"path\": \"/app/data/lora-poetry-pushkin\", \"base_model_name\": \"t-tech/T-lite-it-1.0\"}'"]


CMD ["sh", "-c", "python3 -m vllm.entrypoints.openai.api_server \
  --model $MODEL_NAME \
  --port 8000 \
  --dtype=half \
  --enable-lora \
  --lora-modules poetry=/app/data/lora-poetry2 pushkin=/app/data/lora-poetry-pushkin"]