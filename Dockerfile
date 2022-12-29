FROM python:3.11

ARG UID=1000
ARG GID=1000
ENV LANG=C.UTF-8 DEBIAN_FRONTEND=noninteractive

RUN groupadd --force --gid $GID app \
    && useradd --non-unique --home-dir /opt/app --create-home --uid $UID --gid $GID --comment "Application" app

RUN apt-get update && apt-get install -y wkhtmltopdf

WORKDIR /opt/app
COPY --chown=app:app ./ ./

RUN pip install --no-cache-dir -r requirements.txt

USER app

CMD python3 -m main
