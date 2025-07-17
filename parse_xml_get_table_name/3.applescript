-- =======================================================================================
-- ---           Script v11.0: The Ultimate Configurable Edition                   ---
-- --- Action: Features a full configuration block to let the user choose which    ---
-- ---         actions to perform (clicks, F15, numbers, delete) and keeps the     ---
-- ---         robust quick-switch logic to minimize user disruption.              ---
-- =======================================================================================

-- =======================================================================================
-- --- Part 1: 用户配置区 (USER CONFIGURATION) ---
-- =======================================================================================

-- 1. 目标应用程序名称
property vdiAppName : "桌面云客户端"

-- 2. 动作间隔时间 (单位：秒)
property minSeconds : 15 -- 2 分钟
property maxSeconds : 60 -- 5 分钟

-- 3. 【核心】动作类型配置
-- 请将您想启用的动作设置为 true，不想用的设置为 false。
-- 您可以启用多个，脚本会从中随机选择一个执行。
property actionsConfig : {¬
    useMouseClick: false, ¬
    useF15Key: false, ¬
    useNumberKeys: true, ¬
    useDeleteKey: true ¬
}

-- =======================================================================================
-- --- Part 2: 主脚本逻辑 (MAIN SCRIPT LOGIC) ---
-- --- (您通常无需修改以下内容) ---
-- =======================================================================================
repeat
    set waitTime to random number from minSeconds to maxSeconds
    log "Anti-Lock script (v11.0) is running... Next action in " & (waitTime as integer) & " seconds."
    delay waitTime
    
    try
        if application vdiAppName is running then
            -- 1. 记录当前激活的应用路径，准备切回
            tell application "System Events"
                set originalFrontAppProcess to first application process whose frontmost is true
                set originalFrontApp to application file of originalFrontAppProcess
                set originalFrontAppName to name of originalFrontAppProcess
            end tell
            
            -- 2. 激活云桌面
            tell application "System Events" to set frontmost of process vdiAppName to true
            delay 0.3 -- 等待一小会儿确保激活成功
            
            -- 3. 从启用的动作中随机选择并执行
            tell application "System Events"
                tell process vdiAppName
                    
                    -- 创建一个启用了的动作列表
                    set enabledActions to {}
                    if useMouseClick of actionsConfig is true then set end of enabledActions to "MouseClick"
                    if useF15Key of actionsConfig is true then set end of enabledActions to "F15Key"
                    if useNumberKeys of actionsConfig is true then set end of enabledActions to "NumberKey"
                    if useDeleteKey of actionsConfig is true then set end of enabledActions to "DeleteKey"
                    
                    -- 如果列表不为空，则随机选一个执行
                    if (count of enabledActions) > 0 then
                        set chosenAction to some item of enabledActions
                        
                        if chosenAction is "MouseClick" then
                            -- 执行鼠标点击
                            set frontWindow to the front window
                            set {x1, y1} to position of frontWindow
                            set {w, h} to size of frontWindow
                            if x1 + 40 < x1 + w and y1 + 40 < y1 + h then
                                set randomX to random number from (x1 + 20) to (x1 + w - 20)
                                set randomY to random number from (y1 + 20) to (y1 + h - 20)
                                click at {randomX, randomY}
                                log "Action SUCCESS: Performed Mouse Click inside '" & vdiAppName & "'."
                            else
                                log "Action SKIPPED: Window too small for a safe click."
                            end if
                            
                        else if chosenAction is "F15Key" then
                            -- 按下 F15 (最安全)
                            key code 111
                            log "Action SUCCESS: Sent F15 key press."
                            
                        else if chosenAction is "NumberKey" then
                            -- 按下随机数字 1-9
                            set randomNumber to random number from 1 to 9
                            keystroke randomNumber
                            log "Action SUCCESS: Sent Number '" & randomNumber & "' key press."
                            
                        else if chosenAction is "DeleteKey" then
                            -- 按下 Delete (Backspace) 键
                            key code 51
                            log "Action SUCCESS: Sent Delete (Backspace) key press."
                        end if
                    else
                        log "Action SKIPPED: No actions were enabled in the configuration."
                    end if
                end tell
            end tell
            
            -- 4. 立即切回原始应用
            if originalFrontAppName is not vdiAppName then
                tell application (originalFrontApp as text) to activate
                log "Switched back to '" & originalFrontAppName & "'."
            end if
            
        else
            log "Action SKIPPED: Application '" & vdiAppName & "' is not running."
        end if
    on error errorMessage
        log "An ERROR occurred: " & errorMessage
        try
            if originalFrontApp is not missing then
                tell application (originalFrontApp as text) to activate
            end if
        end try
    end try
end repeat
keystroke "v" using {command down}