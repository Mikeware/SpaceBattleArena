@echo off
del /Q bin\SBAServer.zip
mkdir bin
cd SBA_Serv
python compile.py py2exe
cd ..