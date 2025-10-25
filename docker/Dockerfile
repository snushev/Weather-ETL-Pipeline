FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml /app/

RUN uv pip install --system -e .

COPY . /app/

CMD ["python", "main.py"]
