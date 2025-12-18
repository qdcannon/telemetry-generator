# Generate workable requirements.txt from Poetry dependencies 
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    build-essential \
    gcc \
    python3 \
    python3-pip


RUN python3 -m pip install --no-cache-dir --upgrade poetry

RUN poetry self add poetry-plugin-export

# Disable venvs inside container
RUN poetry config virtualenvs.create false

WORKDIR /app

#When I updgrade the streamer with PyPl modules uncomment the next two lines
COPY pyproject.toml poetry.lock .

#​ Install requirements 
COPY ./src/telemetry_generator .
RUN poetry export -f requirements.txt --without-hashes -o requirements.txt 

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "main.py"]