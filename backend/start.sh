#!/bin/bash

sh -c ollama serve &> /dev/null &
sleep 5 && 
ollama pull llama3 &> /dev/null &
uvicorn app.main:app --host 0.0.0.0 --port 8080