FROM python:3.9-slim
WORKDIR /app
RUN pip install flask requests jsonschema
COPY . .
CMD ["python", "main.py"]