FROM python:3.12

WORKDIR /chtuka

COPY . /chtuka

COPY .venv/Lib/site-packages/operatorfacade /chtuka/operatorfacade
RUN pip install /chtuka/operatorfacade --no-cache-dir

RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 81

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "81"]
