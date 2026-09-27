FROM python:3.13-slim AS builder

WORKDIR /build

COPY pyproject.toml README.md LICENSE ./
COPY src ./src

RUN python -m pip wheel --no-cache-dir --wheel-dir /wheels .


FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HOST=0.0.0.0 \
    PORT=2480 \
    DATABASE=/data/inventory.sqlite \
    TIEFKUEHLLISTE_CONFIG=/config/config.yaml

RUN groupadd --gid 10001 tiefkuehlliste \
    && useradd --uid 10001 --gid tiefkuehlliste --no-create-home --shell /usr/sbin/nologin tiefkuehlliste \
    && install -d -o tiefkuehlliste -g tiefkuehlliste \
        /data /config /usr/local/var/tiefkuehlliste.app-instance

COPY --from=builder /wheels /wheels
RUN python -m pip install --no-cache-dir /wheels/*.whl \
    && rm -rf /wheels

USER tiefkuehlliste

VOLUME ["/data"]
EXPOSE 2480

CMD ["tiefkuehlliste"]
