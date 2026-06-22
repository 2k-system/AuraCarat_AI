@echo off

echo [%date% %time%]: START
echo [%date% %time%]: Creating conda env with python 3.12
/anaconda3/Scripts/activate.bat

echo [%date% %time%]: Activate env
conda create -p venv python=3.12 -y
conda activate ./venv

echo [%date% %time%]: Installing requirements
pip install -r requirements.txt

echo [%date% %time%]: END
