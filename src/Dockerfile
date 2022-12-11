FROM python:slim-buster

WORKDIR .
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

WORKDIR /app
COPY . .
ENV FLASK_APP=src/app.py
ENV PYTHONPATH="/app:${PYTHONPATH}"

WORKDIR /app
CMD [ "python3", "-m" , "uvicorn", "src.app:app", "--host=0.0.0.0", "--port=5052"]
EXPOSE 5052