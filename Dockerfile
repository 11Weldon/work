FROM python:3.12

WORKDIR /bil_app

COPY . /bil_app

RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 80

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]