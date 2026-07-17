# Minimal, readable image for the hello-world sample app.
FROM python:3.12-slim

WORKDIR /app
COPY app.py .

ENV PORT=8080
EXPOSE 8080

# Run as a non-root user (the app writes nothing to disk).
USER 1000

CMD ["python", "app.py"]
