FROM python:3.12

ENV PROJECT_DIR=/chtuka

WORKDIR $PROJECT_DIR

COPY . $PROJECT_DIR

RUN pip install $PROJECT_DIR/Lib/operatorfacade --no-cache-dir

RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 81

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "81"]
