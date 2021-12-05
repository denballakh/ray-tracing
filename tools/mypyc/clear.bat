@echo off

rem Project root is two level up
pushd "../../"

del /s "*.pyd"
rmdir /s /q ".mypy_cache/" 2>nul
rmdir /s /q "build/" 2>nul

popd
pause
