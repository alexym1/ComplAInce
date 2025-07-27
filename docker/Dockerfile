FROM python:3.11.11 AS builder

RUN pip install pipx
RUN pipx install poetry

COPY . .

RUN ${HOME}/.local/bin/poetry install
RUN ${HOME}/.local/bin/poetry build -f wheel


FROM python:3.11.11-slim AS production

RUN apt-get update && apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder dist/complaince-0.1.0-py3-none-any.whl /tmp/pkg/
RUN pip install /tmp/pkg/complaince-0.1.0-py3-none-any.whl
RUN rm -rf /tmp/pkg/*

WORKDIR /opt/sources/python/exposition/complaince

ENV LANG=en_US.UTF-8
ENV LC_CTYPE=en_US.UTF-8

CMD ["uvicorn", "complaince.exposition.complaince_api:app", "--host", "0.0.0.0"]
