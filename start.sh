#!/bin/bash

python -m uvicorn main:app --host 127.0.0.1 --port 8000 &
python -m streamlit run front.py --server.address 0.0.0.0 --server.port 3000 --server.headless true &

wait -n
exit 1