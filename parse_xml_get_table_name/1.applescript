-- =======================================================================================
-- ---           Script v10.4: Controller for macOS (Robust Syntax Edition)        ---
-- --- Action: A more stable and robust version to prevent syntax errors (-2741).  ---
-- ---         Uses simpler, step-by-step commands for maximum compatibility.      ---
-- =======================================================================================

-- --- 配置 (Configuration) ---
-- 您的云桌面应用程序的进程名 (The process name of your VDI app)
property vdiAppName : "桌面云客户端"

-- --- 动作间隔时间 (单位：秒) ---
property minSeconds : 5 -- 4 分钟 (4 minutes)
property maxSeconds : 10 -- 9 分钟 (9 minutes)

-- --- 主逻辑 (Main Logic) ---
repeat
    -- 生成随机等待时间
    set waitTime to random number from minSeconds to maxSeconds
    
    -- 为终端输出日志
    log "Anti-Lock script (v10.4) is running... Next action in " & (waitTime as integer) & " seconds."
    delay waitTime
    
    try
        -- 检查目标应用是否在运行
        if application vdiAppName is running then
            tell application "System Events"
                tell process vdiAppName
                    -- 检查应用是否有可见窗口
                    if (count of windows) is greater than 0 then
                        
                        -- 将窗口置顶并等待激活
                        set frontmost to true
                        delay 1
                        
                        -- **健壮性改进：分步获取窗口信息**
                        set frontWindow to the front window
                        
                        set windowPosition to position of frontWindow
                        set windowSize to size of frontWindow
                        
                        set x1 to item 1 of windowPosition
                        set y1 to item 2 of windowPosition
                        
                        set w to item 1 of windowSize
                        set h to item 2 of windowSize
                        
                        -- **健壮性改进：计算安全的点击区域**
                        set clickAreaLeft to x1 + 20
                        set clickAreaTop to y1 + 20
                        set clickAreaRight to x1 + w - 20
                        set clickAreaBottom to y1 + h - 20
                        
                        -- **健壮性改进：检查点击区域是否有效**
                        if clickAreaLeft < clickAreaRight and clickAreaTop < clickAreaBottom then
                            -- 在安全区域内生成随机坐标
                            set randomX to random number from clickAreaLeft to clickAreaRight
                            set randomY to random number from clickAreaTop to clickAreaBottom
                            
                            -- 执行点击并输出日志
                            click at {randomX, randomY}
                            log "Action SUCCESS: Clicked at {" & randomX & ", " & randomY & "} inside '" & vdiAppName & "'."
                        else
                            log "Action SKIPPED: Window is too small to click inside."
                        end if
                    else
                        log "Action SKIPPED: Application '" & vdiAppName & "' is running but has no open windows."
                    end if
                end tell
            end tell
        else
            log "Action SKIPPED: Application '" & vdiAppName & "' is not currently running."
        end if
    on error errorMessage
        log "An ERROR occurred: " & errorMessage
    end try
end repeat
