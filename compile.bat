@echo off
echo CLEAN
del /Q bin\SBAServer.zip
del /Q bin\SpaceBattle.jar
rmdir /S /Q doc\client\java_doc

echo BUILDING SERVER
mkdir bin
cd SBA_Serv
python compile.py py2exe
cd ..

echo BUILDING CLIENT
cd java_client_src

rmdir /S /Q bin
javac -cp ..\bin\gson-2.2.jar -d bin src\ihs\apcs\spacebattle\*.java src\ihs\apcs\spacebattle\commands\*.java src\ihs\apcs\spacebattle\games\*.java src\ihs\apcs\spacebattle\networking\*.java src\ihs\apcs\spacebattle\util\*.java
cd bin
jar cf ..\..\bin\SpaceBattle.jar ihs
cd..

echo GENERATE DOCS
javadoc -public -sourcepath src -classpath "*;bin" -d ..\doc\client\java_doc -windowtitle "IHS AP CS Space Battle" -doctitle "IHS AP CS Space Battle" ihs.apcs.spacebattle ihs.apcs.spacebattle.commands ihs.apcs.spacebattle.games

cd..
