@echo off

python3 -m pip install --upgrade pip
python3 -m venv .env
.env\Scripts\activate.bat
python3 -m pip install -U pip setuptools
pip install -r requirements.txt
