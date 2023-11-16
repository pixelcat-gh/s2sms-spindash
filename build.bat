@ECHO OFF

IF EXIST s2.o DEL s2.o
IF EXIST s2.sym DEL s2.sym
IF EXIST s2.sms DEL s2.sms

ECHO Assembling...
wla_dx_binaries_latest\wla-z80 -vo src\s2.asm s2.o

IF %ERRORLEVEL% NEQ 0 GOTO assemble_fail
IF NOT EXIST s2.o GOTO assemble_fail

ECHO Linking...
wla_dx_binaries_latest\wlalink -rs link.txt s2.sms
IF %ERRORLEVEL% NEQ 0 GOTO link_fail

ECHO ==========================
ECHO Build Success.
ECHO ==========================

IF EXIST s2.o DEL s2.o
IF EXIST s2.sym DEL s2.sym

START "C:\Program Files\blastem-win32-0.6.2\blastem.exe" s2.sms

GOTO end

:assemble_fail
ECHO Error while assembling.
GOTO fail
:link_fail
ECHO Error while linking.
:fail

ECHO ==========================
ECHO Build failure.
ECHO ==========================

:end