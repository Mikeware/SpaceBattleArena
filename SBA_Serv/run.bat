@ECHO OFF
IF "%2"=="" (
 python.exe SBA_Serv.py -c %1
) ELSE (
 python.exe SBA_Serv.py -c %1 -2 %2
)