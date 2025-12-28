FROM python:3.13-slim

ARG UID=1000
ARG GID=1000
ENV LANG=C.UTF-8 DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN groupadd --force --gid $GID app \
    && useradd --non-unique --home-dir /opt/app --create-home --uid $UID --gid $GID --comment "Application" app

# Install wkhtmltopdf and dependencies
ARG TARGETARCH
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    ca-certificates \
    fontconfig \
    libjpeg62-turbo \
    libxrender1 \
    xfonts-75dpi \
    xfonts-base \
    && case ${TARGETARCH} in \
         "amd64")  WKHTML_ARCH=amd64  ;; \
         "arm64")  WKHTML_ARCH=arm64  ;; \
         *)        echo "Unsupported architecture: ${TARGETARCH}" && exit 1 ;; \
       esac \
    && wget -q https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/wkhtmltox_0.12.6.1-3.bookworm_${WKHTML_ARCH}.deb -O /tmp/wkhtmltox.deb \
    && apt-get install -y /tmp/wkhtmltox.deb \
    && rm /tmp/wkhtmltox.deb \
    && apt-get remove -y wget \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/app

# Copy requirements first for better caching
COPY --chown=app:app requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=app:app main.py ./

# Copy test files (optional, only needed for testing in container)
COPY --chown=app:app test_*.py pytest.ini ./

USER app

EXPOSE 9090

CMD ["python3", "-m", "main"]
