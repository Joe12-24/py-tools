@echo off
setlocal enabledelayedexpansion

:: === 配置路径 ===
set DATAX_HOME=C:\Your\Path\To\DataX
set JOB_DIR=datax_jobs
set LOG_DIR=logs

:: === 创建日志目录（如果不存在） ===
if not exist %LOG_DIR% (
    mkdir %LOG_DIR%
)

echo ================================
echo 🚀 批量执行 DataX 任务开始！
echo DataX目录: %DATAX_HOME%
echo 任务目录: %JOB_DIR%
echo 日志目录: %LOG_DIR%
echo ================================
echo.

:: === 遍历 JSON 任务文件 ===
for %%F in (%JOB_DIR%\*.json) do (
    set "JOB_NAME=%%~nF"
    echo ▶ 执行任务: %%F
    python "%DATAX_HOME%\bin\datax.py" "%%F" > "%LOG_DIR%\!JOB_NAME!.log" 2>&1

    if !errorlevel! neq 0 (
        echo ❌ 任务失败: %%F，请查看日志: %LOG_DIR%\!JOB_NAME!.log
    ) else (
        echo ✅ 任务完成: %%F
    )
    echo -------------------------------------
)

echo ✅ 所有任务执行完毕！
pause
