FROM python:3.9.5-slim

WORKDIR /app

RUN pip install poetry==1.3.1
RUN poetry config virtualenvs.create false

COPY pyproject.toml ./
COPY poetry.lock ./
RUN poetry --version
RUN poetry install --no-interaction --no-ansi

COPY src ./src
COPY scripts ./scripts
COPY migrations ./migrations

ENV PYTHONPATH="$PYTHONPATH:/app/src"

CMD ["bash", "./scripts/cmd.sh"]
