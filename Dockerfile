# Generate workable requirements.txt from Poetry dependencies 
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    build-essential \
    gcc \
    python3 \
    python3-pip


RUN python -m pip install --no-cache-dir --upgrade poetry 

COPY pyproject.toml poetry.lock ./ 
RUN poetry export -f requirements.txt --without-hashes -o /src/requirements.txt 

#​ Switching to non-root user appuser 
#RUN adduser appuser 
WORKDIR /app
#USER appuser:appuser 

#​ Install requirements 
COPY ./src/telemetry_generator .

RUN pip install --no-cache-dir --user -r requirements.txt

CMD ["python3", "main.py"]