@echo off
call "..\..\py_res_helper_venv\Scripts\activate"
 
python app.py

@REM echo Running the first function...
@REM python -c "import res_script; res_script.process_file()"

@REM pause

@REM echo Running the second function...
@REM python -c "import res_script; res_script.merge_pdfs()"
