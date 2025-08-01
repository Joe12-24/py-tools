-- === CONFIGURATION ===
property enableConsoleLog : true
property enableActivityLog : true
property targetUrl : "http://portal.mycompany.internal"
property logFile : ((path to desktop folder as text) & "activity_log.txt")

-- === CHARACTER SET ===
property charset : "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

-- === LOGGING FUNCTION ===
on logMessage(msg)
	set timestamp to do shell script "date '+%Y-%m-%dT%H:%M:%S'"
	set fullMsg to "[" & timestamp & "] " & msg
	if enableConsoleLog then
		log fullMsg
	end if
	if enableActivityLog then
		try
			do shell script "echo " & quoted form of fullMsg & " >> " & quoted form of POSIX path of logFile
		end try
	end if
end logMessage

-- === RANDOM CHARACTER INPUT ===a
on typeRandomCharacters()
	-- 配置目标应用和窗口
	set targetApp to "TextMate"
	set targetWindowName to ""

	-- 激活应用
	tell application targetApp to activate
	delay 1

	tell application "System Events"
		tell process targetApp
			set frontmost to true
			
			-- 查找窗口并聚焦
			repeat with w in windows
				if name of w contains targetWindowName then
					set front window to w
					delay 0.5
					
					-- 主动点击窗口中心（确保焦点在编辑区）
					try
						set winBounds to bounds of w
						set xPos to item 1 of winBounds + 200
						set yPos to item 2 of winBounds + 200
						click at {xPos, yPos}
						delay 0.5
					end try
					
					exit repeat
				end if
			end repeat
			
			-- 输入随机字符
			set allChars to "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
			set charList to characters of allChars
			set inputCount to (random number from 10 to 20)
			
			repeat with i from 1 to inputCount
				set randIndex to (random number from 1 to (length of charList))
				set randChar to item randIndex of charList
				keystroke randChar
				delay 0.1
			end repeat
			keystroke space -- 输入空格
			delay 0.3
			keystroke "s" using command down -- ⌘+S
		end tell
	end tell
	
	logMessage("Activity: Typed random characters and saved in " & targetWindowName)
end typeRandomCharacters

-- 获取当前鼠标位置（x,y字符串）
on getMousePosition()
	try
		return do shell script "python3 -c 'from Quartz.CoreGraphics import CGEventCreate, CGEventGetLocation; loc = CGEventGetLocation(CGEventCreate(None)); print(f\"{int(loc.x)},{int(loc.y)}\")'"
	on error
		return "error"
	end try
end getMousePosition
on parseXY(posStr)
	set AppleScript's text item delimiters to ","
	set parts to text items of posStr
	set x to item 1 of parts as integer
	set y to item 2 of parts as integer
	return {x, y}
end parseXY
on abs(x)
	if x < 0 then
		return -x
	else
		return x
	end if
end abs

on isMouseMoved(p1, p2)
	set xy1 to parseXY(p1)
	set xy2 to parseXY(p2)
	set dx to abs((item 1 of xy1) - (item 1 of xy2))
	set dy to abs((item 2 of xy1) - (item 2 of xy2))
	if dx > 2 or dy > 2 then -- 可调：2像素以内算没动
		return true
	else
		return false
	end if
end isMouseMoved


property pauseTriggered : false
-- === MAIN SCRIPT ===
logMessage("--- SCRIPT SESSION STARTED ---")
if targetUrl is "http://portal.mycompany.internal" then
	logMessage("NOTICE: Network simulation is DISABLED.")
else
	logMessage("Network simulation ENABLED. Target: " & targetUrl)
end if

repeat



	-- Prevent sleep
	try
		do shell script "/usr/bin/caffeinate -u -t 5 &"
	end try
	
	-- Simulate network request
	if targetUrl is not "http://portal.mycompany.internal" then
		try
			do shell script "curl --max-time 10 " & quoted form of targetUrl & " > /dev/null 2>&1"
			logMessage("Activity: Simulated network request.")
		on error errMsg
			logMessage("Network Error: " & errMsg)
		end try
	end if
	

	set initialMousePos to getMousePosition()
	delay 1
	set laterMousePos to getMousePosition()

	if initialMousePos is "error" or laterMousePos is "error" then
		logMessage("WARNING: Failed to get mouse position, skipping mouse movement detection.")
	else
		if isMouseMoved(initialMousePos, laterMousePos) then
			logMessage("Mouse moved >2px detected. Pausing input.")
			set mouseMovedPause to true
		else
			-- 鼠标没动，取消暂停
			if mouseMovedPause then
				logMessage("Mouse stopped moving. Resuming input.")
			end if
			set mouseMovedPause to false
		end if
	end if
	
	-- 判断是否要输入随机字符
	if mouseMovedPause then
		logMessage("SKIPPED: Input paused due to mouse movement.")
	else
		try
			typeRandomCharacters()
		end try
	end if





-- 每轮循环开始前先判断是否命中特殊暂停时间
	set currentTime to do shell script "date +%H:%M:%S"
	logMessage("DEBUG: currentTime = " & currentTime)

	if currentTime ≥ "07:34:00" and currentTime < "07:34:45" and not pauseTriggered then
		set pauseTriggered to true
		logMessage("MATCHED: Between 07:34:00 and 07:34:45 - Sleeping 480 seconds.")
		delay 480
	else if not pauseTriggered then
		-- 正常模拟用户操作
		logMessage("Activity: Sent no-idle event via caffeinate.")
		logMessage("Activity: Typed random characters and saved in ...")

		-- 改进版 delay：拆分成小块，便于中途检查时间
		set totalSleep to (random number from 180 to 300)
		set slept to 0
		logMessage("Starting sleep loop for " & totalSleep & " seconds.")

		repeat while slept < totalSleep
			-- 检查是否进入 07:35~07:36 时间段
			set currentTime to do shell script "date +%H:%M:%S"
			if currentTime ≥ "07:35:00" and currentTime < "07:36:00" and not pauseTriggered then
				set pauseTriggered to true
				logMessage("INTERRUPT: Entered 07:35 time during sleep - switching to 900 second sleep.")
				delay 900
				exit repeat
			end if

			delay 10
			set slept to slept + 10
		end repeat
	end if


	
end repeat
