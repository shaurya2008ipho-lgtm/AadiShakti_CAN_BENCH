@echo off
python -m venv .venv
call .venv\Scripts\activate
python -m pip install -r requirements.txt
start "Aadi CAN Mock" cmd /k "call .venv\Scripts\activate && python python_can\mock_node.py"
start "Aadi CAN Dashboard" cmd /k "call .venv\Scripts\activate && python dashboard\app.py"
