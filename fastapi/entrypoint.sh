#!/usr/bin/env bash
exec uvicorn src.main:app --reload --host 0.0.0.0 --port 8080
