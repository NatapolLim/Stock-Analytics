FROM python:3.9-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install \
        --no-install-recommends \
        -y

RUN pip install \
    --no-cache-dir \
    --disable-pip-version-check \
    poetry~=1.6.1

# RUN pip wheel --use-pep517 "psutil (==5.9.6)"

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry config virtualenvs.create false \
    && poetry install \
        --no-root

# COPY ./src/configs ./configs
# COPY ./src/config.py .
# COPY ./src/pipeline_comps ./pipeline_comps
# COPY ./src/queries ./queries
# COPY ./src/utils ./utils

EXPOSE 8051

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT [ "streamlit", "run" , "0_Home.py", "--server.port=8501", "--server.address=0.0.0.0" ]

