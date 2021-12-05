@echo off

rem Project root is two level up
pushd "../../"

rem Name of project folder
set R=ray_tracing
set "files= "

rem List of files to compile:
rem set files=%files% %R%/obstacle.py
rem set files=%files% %R%/draw.py
rem set files=%files% %R%/model.py
set files=%files% %R%/point.py
rem set files=%files% %R%/queue.py
set files=%files% %R%/ray.py


echo Files to compile:
set out=%files: =&echo.%
echo.

call mypyc %files% || pause

rem Clearing caches:
rmdir /s /q ".mypy_cache/"
rmdir /s /q "build/"

popd
