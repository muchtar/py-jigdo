@echo off

rem This file is distributed with jigdo-lite for Windows
rem Copyright 2002-2005 Richard Atterer, http://atterer.net/jigdo/

rem Most of the Windows versions of the various Unix utilities were
rem taken from MSYS, see http://www.mingw.org/msys.shtml
rem Many thanks to the MSYS people!

if not x%JIGDOPATH%==x goto hasrun
path jigdo-bin;%PATH%
set JIGDOPATH=yes
:hasrun

rem start rxvt -sl 2500 -fg Black -bg White -fn Courier-12 -tn jigdo-file -e sh jigdo-lite
sh jigdo-lite %1 %2 %3 %4 %5 %6 %7 %8 %9
pause
