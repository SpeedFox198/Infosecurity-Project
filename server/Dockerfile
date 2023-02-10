FROM python:3.10-slim
RUN apt update && apt install -y libmagic1 tesseract-ocr
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD ["hypercorn", "app:sio_app", "-c", "config.toml"]