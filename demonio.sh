#!/bin/bash

python3 DataCollector.py &&
python3 StoreDB.py &&
python3 Process.py
