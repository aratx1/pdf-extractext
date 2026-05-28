#!/bin/sh
set -e

ollama serve &
PID=$!

echo "Waiting for Ollama to start..."
until ollama list > /dev/null 2>&1; do
  sleep 2
done
echo "Ollama is ready."

MODEL=${OLLAMA_MODEL:-llama3.2}
echo "Pulling model: $MODEL..."
ollama pull "$MODEL"
echo "Model pulled successfully."

wait $PID
