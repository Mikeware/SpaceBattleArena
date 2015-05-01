@ECHO OFF
IF "%2"=="" (
 SBA_Serv.exe -c %1
) ELSE (
 SBA_Serv.exe -c %1 -2 %2
)