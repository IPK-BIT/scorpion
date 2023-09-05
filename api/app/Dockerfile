FROM python:3.10

WORKDIR /code
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . /code/app
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload" ]