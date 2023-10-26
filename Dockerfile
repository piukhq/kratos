FROM docker.io/python:3.11 as requirements

WORKDIR /app
COPY pyproject.toml poetry.lock main.py settings.py vop.py amex_merchant_search.py amex_api.py givex*.py stonegate.py common_modules.py /app/
RUN pip install poetry==1.2.0b3
RUN poetry config virtualenvs.create false
RUN poetry export -f requirements.txt --output requirements.txt

FROM ghcr.io/binkhq/python:3.11
WORKDIR /app
COPY --from=requirements /app/ /app/
RUN pip install -r requirements.txt

ENTRYPOINT [ "linkerd-await", "--" ]
CMD [ "gunicorn", "--bind=0.0.0.0:6502", "--workers=2", "main:app" ]
