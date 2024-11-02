#!/bin/bash
uvicorn backed.phonebook.main:app --host 0.0.0.0 --port $PORT