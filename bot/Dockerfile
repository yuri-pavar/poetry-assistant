# FROM python:3.10

# WORKDIR /app
# COPY bot/requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY bot/ .

# CMD ["python", "bot.py"]


FROM python:3.10

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
