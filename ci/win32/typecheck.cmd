REM script to run mypy type checker on this source tree.
pushd .
cd /D "%~dp0"
cd ..\..\
call .\venv\Scripts\activate
set PYTHONPATH=.\src\lockgate;%$PYTHONPATH%
python -m mypy ./src/lockgate ./unit_test/
popd