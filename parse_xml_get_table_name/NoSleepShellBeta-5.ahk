#SingleInstance Force
#Persistent
SetWorkingDir %A_ScriptDir%

Menu, Tray, Icon
Menu, Tray, Tip, Anti-Lock Controller
Menu, Tray, Add, Start Anti-Lock Script, StartScript
Menu, Tray, Add, Stop Anti-Lock Script, StopScript
Menu, Tray, Add
Menu, Tray, Add, Exit Controller, ExitApp
Menu, Tray, Default, Start Anti-Lock Script

scriptTitle := "AntiLockScript"
ps1Path := "C:\\Path\\To\\AntiLockScript.ps1"
ideaPath := "C:\\Program Files\\JetBrains\\IntelliJ IDEA 2024.1\\bin\\idea64.exe"
browserPath := "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
navicatPath := "C:\\Program Files\\Navicat\\navicat.exe"

alreadyLaunched := false  ; 全局变量

; 自动启动
GoSub, AutoStart
return

AutoStart:
    Gosub, StartScript
return

StartScript:
    if (!alreadyLaunched) {
        if FileExist(ideaPath)
            Run, %ideaPath%

        if FileExist(browserPath)
        {
            Run, %browserPath%
            Sleep, 3000
            WinWaitActive, ahk_exe chrome.exe,, 5
            if !ErrorLevel
                Send ^+t
        }

        if FileExist(navicatPath)
            Run, %navicatPath%

        alreadyLaunched := true
    }

    Run, powershell.exe -NoExit -Command "$Host.UI.RawUI.WindowTitle = '%scriptTitle%'; & { Start-Sleep -Milliseconds 300; . '%ps1Path%' }"
    
    TrayTip, Anti-Lock Script, Script launched., 1
return

^!s::
    Gosub, StartScript
return

^!q::
StopScript:
    RunWait, taskkill /FI "WINDOWTITLE eq %scriptTitle%" /T /F, , Hide
    TrayTip, Anti-Lock Script, Stopped., 1
return

ExitApp:
    ExitApp
