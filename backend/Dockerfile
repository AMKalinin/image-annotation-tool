FROM ubuntu

RUN apt update && apt install python3.11 python3-pip -y

RUN pip install poetry

WORKDIR /app

COPY . /app

RUN poetry install

EXPOSE 8000

# CMD [ "poetry", "run", "./run.sh" ]