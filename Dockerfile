FROM python:3.11-slim-bookworm
WORKDIR /app
RUN apt-get update && apt-get install -y git
COPY common-requirements.txt requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"
CMD ["python", "-m", "katiba_chat.entrypoints.gradio_app"]
