FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /opt/app

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY --chown=web:web . .

RUN chmod +x app.sh

RUN echo "Содержимое директории /opt/app:" && ls -la /opt/app


CMD ["bash", "app.sh"]
