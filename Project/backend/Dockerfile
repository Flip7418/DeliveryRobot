FROM python:3.9

ENV PYTHONUNBUFFERED=1 \
    COLUMNS=200 \
    TZ=Asia/Almaty

ADD ./app/requirements.txt \
    /app/

RUN apt update \
    && apt install -y apt-utils \
# Set timezone
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
# Upgrade pip
    && pip install --upgrade pip setuptools wheel \
# Add project dependencies
    && pip install \
    --no-cache-dir -Ur /app/requirements.txt \
    && apt clean


COPY ./app /app

WORKDIR /app
CMD ["./entrypoint.sh"]
