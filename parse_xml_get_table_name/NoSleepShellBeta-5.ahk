; 设置单例，防止多开
#SingleInstance Force
#Persistent
SetWorkingDir %A_ScriptDir%  ; 设置当前工作目录为脚本所在目录

Menu, Tray, Icon
Menu, Tray, Tip, Anti-Lock Controller
Menu, Tray, Add, Start Anti-Lock Script, StartScript
Menu, Tray, Add, Stop Anti-Lock Script, StopScript
Menu, Tray, Add
Menu, Tray, Add, Exit Controller, ExitApp

Menu, Tray, Default, Start Anti-Lock Script

; 配置区
scriptTitle := "AntiLockScript"
ps1Path := "C:\\Path\\To\\AntiLockScript.ps1"  ; PowerShell 脚本路径（双反斜杠）

ideaPath := "C:\\Program Files\\JetBrains\\IntelliJ IDEA 2024.1\\bin\\idea64.exe"
browserPath := "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
navicatPath := "C:\\Program Files\\Navicat\\navicat.exe"

^!s::  ; Ctrl+Alt+S 启动脚本
StartScript:
    if WinExist(scriptTitle)
    {
        TrayTip, Anti-Lock Script, Already running., 1
        return
    }

    ; 启动 IDEA
    if FileExist(ideaPath)
        Run, %ideaPath%

    ; 启动浏览器
    if FileExist(browserPath) {
        Run, %browserPath%
        Sleep, 3000  ; 等待 3 秒，确保浏览器启动完成

        ; 激活浏览器窗口（可选：更精确匹配类名或标题）
        WinWaitActive, ahk_exe chrome.exe,, 5
        if ErrorLevel {
            TrayTip, Browser, Failed to activate Chrome., 1
        } else {
            Send ^+t  ; Ctrl+Shift+T
        }
    }


    ; 启动 Navicat
    if FileExist(navicatPath)
        Run, %navicatPath%

    ; 等待 60 秒
    Sleep, 60000

    ; 启动 PowerShell 脚本，设置窗口标题
    Run, powershell.exe -NoExit -Command "$Host.UI.RawUI.WindowTitle = '%scriptTitle%'; & { Start-Sleep -Milliseconds 300; . '%ps1Path%' }"

    TrayTip, Anti-Lock Script, Started after delay., 1
return

^!q::  ; Ctrl+Alt+Q 停止脚本
StopScript:
    RunWait, taskkill /FI "WINDOWTITLE eq %scriptTitle%" /T /F, , Hide
    TrayTip, Anti-Lock Script, Stopped., 1
return

ExitApp:
    ExitApp
