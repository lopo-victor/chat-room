FROM python:3.9-slim

WORKDIR /app

VOLUME /data

COPY . .

COPY ./data /data

RUN pip install fastapi uvicorn pydantic

CMD ["uvicorn", "userServer:app", "--host", "0.0.0.0", "--port", "8000"]


