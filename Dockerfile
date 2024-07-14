FROM python:slim-bullseye

WORKDIR /fastapi_backend

COPY . /fastapi_backend

RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 80

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]