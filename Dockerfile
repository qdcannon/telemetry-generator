# Generate workable requirements.txt from Poetry dependencies 
FROM python:3-slim as requirements 

#RUN apt-get install -y --no-install-recommends build-essential gcc 

RUN python -m pip install --no-cache-dir --upgrade poetry 

COPY pyproject.toml poetry.lock ./ 
RUN poetry export -f requirements.txt --without-hashes -o /src/requirements.txt 

#​ Final app image 
FROM python:3-slim as webapp 

#​ Switching to non-root user appuser 
#RUN adduser appuser 
WORKDIR /app
#USER appuser:appuser 

#​ Install requirements 
COPY --from=requirements /src/requirements.txt . 
RUN pip install --no-cache-dir --user -r requirements.txt

COPY ./src/telemetry_generator .

CMD ["python3", "main.py"]