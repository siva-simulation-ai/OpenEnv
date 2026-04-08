FROM python:3.10

WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn pydantic

# Start FastAPI server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]