FROM python:3.14-alpine

RUN apk add --no-cache build-base

WORKDIR /app

COPY pyproject.toml ./
COPY rt_scheduling_simulator ./rt_scheduling_simulator
COPY rt_scheduling_frontend ./rt_scheduling_frontend

RUN pip install --upgrade pip && \
    pip install . && \
    pip show gunicorn && \
    python -m gunicorn --version

EXPOSE 5000

CMD ["python", "-m", "gunicorn", "-b", "0.0.0.0:5000", "rt_scheduling_frontend:create_app()"]
