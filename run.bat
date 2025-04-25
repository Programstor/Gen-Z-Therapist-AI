@echo off
rem Activate the virtual environment
call .\.venv\Scripts\activate.bat

rem Run Streamlit app
python -m streamlit run app.py

rem Deactivate the virtual environment after the app finishes
deactivate
