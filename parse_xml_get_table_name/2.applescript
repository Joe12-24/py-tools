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
			
			delay 0.3
			keystroke "s" using command down -- ⌘+S
		end tell
	end tell
	
	logMessage("Activity: Typed random characters and saved in " & targetWindowName)
end typeRandomCharacters



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
		logMessage("Activity: Sent no-idle event via caffeinate.")
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
	
	-- Random keystrokes + save
	try
		typeRandomCharacters()
	end try
	
	-- Sleep 2–4 minutes
	set sleepSecs to (random number from 10 to 11)
	logMessage("Sleeping for " & sleepSecs & " seconds.")
	delay sleepSecs
end repeat
