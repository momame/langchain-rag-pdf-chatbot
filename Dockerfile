FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PROVIDER=groq

# Build the vector index into the image so the container starts ready.
# Needs the PDF in the build context, or: docker build --build-arg PDF_URL=https://... .
ARG PDF_URL
RUN PDF_URL=$PDF_URL python -c "import vector"

EXPOSE 7860
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
