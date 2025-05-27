#!/bin/bash

PIDS=$(netstat -tulnp | grep :8002 | awk "{print \$7}" | cut -d"/" -f1)
if [ -n "$PIDS" ]; then
    kill -9 $PIDS
fi
nohup uvicorn app:app --host 0.0.0.0 --port 8002 --reload > uvicorn.log 2>&1 &
