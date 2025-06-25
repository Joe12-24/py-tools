-- =======================================================================================
-- ---           Script v10.6: Controller for macOS (Robust Path-Switching)        ---
-- --- Action: Fixes the "Where is Electron?" error by using the precise file path ---
-- ---         of the original application to ensure a reliable switch-back.       ---
-- =======================================================================================

-- --- 配置 (Configuration) ---
property vdiAppName : "桌面云客户端"
property minSeconds : 5 -- 4 分钟
property maxSeconds : 5 -- 9 分钟

-- --- 主逻辑 (Main Logic) ---
repeat
    set waitTime to random number from minSeconds to maxSeconds
    log "Anti-Lock script (v10.6) is running... Next action in " & (waitTime as integer) & " seconds."
    delay waitTime
    
    -- **v10.6 新增逻辑：路径精确定位与切换**
    try
        if application vdiAppName is running then
            
            -- 1. 记录当前最前端应用程序的【文件路径】
            tell application "System Events"
                set originalFrontAppProcess to first application process whose frontmost is true
                set originalFrontApp to application file of originalFrontAppProcess
                set originalFrontAppName to name of originalFrontAppProcess
            end tell
            
            if originalFrontAppName is not vdiAppName then
                log "Current app is '" & originalFrontAppName & "'. Preparing for robust quick-switch..."
            else
                log "VDI app is already frontmost. No switch needed."
            end if
            
            -- 2. 快速激活目标并执行无害操作
            tell application "System Events"
                tell process vdiAppName
                    set frontmost to true
                    delay 0.2
                    key code 111 -- F15 key press
                    log "Action SUCCESS: Sent F15 key press to '" & vdiAppName & "'."
                end tell
            end tell
            
            -- 3. 如果原始应用不是云桌面，则通过【文件路径】精确切回
            if originalFrontAppName is not vdiAppName then
                tell application (originalFrontApp as text) -- 使用文件路径激活
                    activate
                    log "Switched back to '" & originalFrontAppName & "' using its file path."
                end tell
            end if
            
        else
            log "Action SKIPPED: Application '" & vdiAppName & "' is not running."
        end if
        
    on error errorMessage
        log "An ERROR occurred: " & errorMessage
        -- 如果出错，尝试用最后记录的应用切回，增加保障
        try
            if originalFrontApp is not missing then
                tell application (originalFrontApp as text) to activate
            end if
        end try
    end try
end repeat
