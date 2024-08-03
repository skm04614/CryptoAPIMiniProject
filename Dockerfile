FROM python:3.12-bullseye
LABEL authors="skm04614"

RUN pip install poetry \
    && poetry config virtualenvs.create false

WORKDIR /superix
COPY poetry.lock pyproject.toml ./
RUN poetry install

COPY app ./app

CMD ["poetry", "run", "python", "-m", "app.main"]
