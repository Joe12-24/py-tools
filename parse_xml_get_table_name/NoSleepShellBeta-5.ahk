; 设置单例，防止多开
#SingleInstance Force
#Persistent
SetWorkingDir %A_ScriptDir%  ; 设置当前工作目录为脚本所在目录

; 显示托盘图标（去掉 #NoTrayIcon 以便看到图标）
Menu, Tray, Icon
Menu, Tray, Tip, Anti-Lock Controller
Menu, Tray, Add, Start Anti-Lock Script, StartScript
Menu, Tray, Add, Stop Anti-Lock Script, StopScript
Menu, Tray, Add
Menu, Tray, Add, Exit Controller, ExitApp

; 设置双击托盘图标默认执行“启动脚本”
Menu, Tray, Default, Start Anti-Lock Script

; -------------- 配置区（请修改为你的 PowerShell 脚本路径） --------------
scriptTitle := "AntiLockScript"
ps1Path := "C:\\Path\\To\\AntiLockScript.ps1"  ; 注意路径用双反斜杠

; ---------------- 下面是热键及函数 ----------------

^!s::  ; Ctrl+Alt+S 启动脚本
StartScript:
    ; 判断脚本是否已经运行（窗口标题匹配）
    if WinExist(scriptTitle)
    {
        TrayTip, Anti-Lock Script, Already running., 1
        return
    }
    ; 运行 PowerShell 脚本，设置窗口标题，隐藏窗口-NoExit后加 -WindowStyle Hidden 
    Run, powershell.exe -NoExit -Command "$Host.UI.RawUI.WindowTitle = '%scriptTitle%'; & { Start-Sleep -Milliseconds 300; . '%ps1Path%' }"
    TrayTip, Anti-Lock Script, Started successfully., 1
return

^!q::  ; Ctrl+Alt+Q 关闭脚本
StopScript:
    RunWait, taskkill /FI "WINDOWTITLE eq %scriptTitle%" /T /F, , Hide
    TrayTip, Anti-Lock Script, Stopped., 1
return

ExitApp:  ; 退出控制器
    ExitApp
