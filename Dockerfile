FROM ghcr.io/astral-sh/uv:python3.13-alpine

# Copy files (check .dockerignore for exclusions)
ADD . /app
COPY crontab/root /var/spool/cron/crontabs/

# Set working directory
WORKDIR /app

# Install dependencies
RUN uv sync --locked

# Run cron daemon in foreground
# This is necessary to keep the container running
CMD ["crond", "-f"]