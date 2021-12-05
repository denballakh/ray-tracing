@echo off

rem Project root is two level up
pushd "../../"

rem Name of project folder
set R=ray_tracing
set "files= "

rem List of files to compile:


set files=%files% %R%/geometry/point.py


echo Files to compile:
set out=%files: =&echo.%
echo.

call mypyc %files% || pause

rem Clearing caches:
rmdir /s /q ".mypy_cache/"
rmdir /s /q "build/"

popd
