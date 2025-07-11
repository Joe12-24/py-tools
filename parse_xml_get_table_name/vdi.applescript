

-- 打开 Safari 并访问目标网页
tell application "Safari"
    activate
    open location "https://10.176.163.108"
end tell

delay 3 -- 等待页面加载

-- Step 1：点击“重新登录”
do shell script "/opt/homebrew/bin/cliclick c:199,247"
delay 1.5

-- Step 2：点击“注销”
do shell script "/opt/homebrew/bin/cliclick c:184,254"
delay 1

-- Step 3：点击“确认注销”
do shell script "/opt/homebrew/bin/cliclick c:1020,513"
delay 1.5

-- Step 4：再次点击“重新登录”
do shell script "/opt/homebrew/bin/cliclick c:199,247"
delay 2

-- Step 5：点击用户名输入框并输入
do shell script "/opt/homebrew/bin/cliclick c:753,499"
delay 0.5
tell application "System Events"
    keystroke "CP_gaoju"
end tell
delay 0.5

-- Step 6：点击密码输入框并输入
do shell script "/opt/homebrew/bin/cliclick c:923,556"
delay 0.5
tell application "System Events"
    keystroke "Linkage@12345"
end tell
delay 0.5

-- Step 7：点击“用户协议”勾选框
-- do shell script "/opt/homebrew/bin/cliclick c:669,607"
-- delay 0.5

-- Step 8：点击“登录”按钮
do shell script "/opt/homebrew/bin/cliclick c:863,658"
delay 10

-- Step 9：点击“互联网178段”区域
do shell script "/opt/homebrew/bin/cliclick c:552,337"

-- 等待 6 秒
delay 3



-- 左击两次 (双击)，906,301
do shell script "/opt/homebrew/bin/cliclick c:906,301"
delay 0.3
do shell script "/opt/homebrew/bin/cliclick c:906,301"
delay 2

-- 点击 756,586
do shell script "/opt/homebrew/bin/cliclick c:756,586"
delay 0.5

-- 输入 763210
tell application "System Events"
    keystroke "763210"
end tell
delay 20

-- 点击 975,593
do shell script "/opt/homebrew/bin/cliclick c:975,593"
delay 1
-- 点击坐标 (274, 934)
do shell script "/opt/homebrew/bin/cliclick c:274,934"
delay 1

-- 点击坐标 (412, 268)
do shell script "/opt/homebrew/bin/cliclick c:412,268"
delay 1

set thePath to "D:\\Users\\User\\Desktop\\ddddddd-10.ps1"


tell application "System Events"
    repeat with i from 1 to length of thePath
        set theChar to character i of thePath
        keystroke theChar
        delay 0.1
    end repeat
    key code 36 -- 回车
end tell

