-- === CONFIGURATION ===
property logFile : ((path to desktop folder as text) & "activity_log.txt")
property enableConsoleLog : true
property enableActivityLog : true
property charset : "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

-- === LOGGING FUNCTION ===
on logMessage(msg)
	set timestamp to do shell script "date '+%Y-%m-%dT%H:%M:%S'"
	set fullMsg to "[" & timestamp & "] " & msg
	if enableConsoleLog then log fullMsg
	if enableActivityLog then
		try
			do shell script "echo " & quoted form of fullMsg & " >> " & quoted form of POSIX path of logFile
		end try
	end if
end logMessage

-- === TEXT INPUT ===
on typeRandomCharacters()
	set targetApp to "TextMate"
	tell application targetApp to activate
	delay 1
	
	tell application "System Events"
		tell process targetApp
			set frontmost to true
			try
				click at {300, 300}
				delay 0.5
			end try
			
			set allChars to characters of charset
			set inputCount to (random number from 10 to 20)
			repeat with i from 1 to inputCount
				set randIndex to (random number from 1 to (count of allChars))
				keystroke (item randIndex of allChars)
				delay 0.1
			end repeat
			keystroke space
			delay 0.3
			keystroke "s" using command down
		end tell
	end tell
	
	logMessage("Typed random characters.")
end typeRandomCharacters

-- === MOUSE UTILS ===
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
	if x < 0 then return -x
	return x
end abs

on isMouseMoved(p1, p2)
	if p1 = "error" or p2 = "error" then return true
	set xy1 to parseXY(p1)
	set xy2 to parseXY(p2)
	set dx to abs((item 1 of xy1) - (item 1 of xy2))
	set dy to abs((item 2 of xy1) - (item 2 of xy2))
	return dx > 2 or dy > 2
end isMouseMoved

-- === MAIN ===
logMessage("--- SCRIPT STARTED ---")

repeat
	set waitThreshold to (random number from 180 to 300)
	set accumulatedTime to 0
	set lastMousePos to getMousePosition()
	logMessage("New wait window: " & waitThreshold & "s")

	repeat while accumulatedTime < waitThreshold
		delay 5
		set currentTime to do shell script "date +%H:%M:%S"
		
		if currentTime ≥ "07:33:00" and currentTime < "07:34:00" then
			logMessage("IN TIME WINDOW 07:33~07:34. Pausing 480s.")
			delay 480
			exit repeat
		end if
		
		set newMousePos to getMousePosition()
		if isMouseMoved(lastMousePos, newMousePos) then
			logMessage("Mouse moved. Resetting accumulated time.")
			set accumulatedTime to 0
		else
			set accumulatedTime to accumulatedTime + 5
			logMessage("Mouse still. Accumulated idle: " & accumulatedTime & "s")
		end if
		set lastMousePos to newMousePos
	end repeat

	if accumulatedTime ≥ waitThreshold then
		try
			logMessage("No mouse movement for " & accumulatedTime & "s. Typing random text...")
			typeRandomCharacters()
		on error errMsg
			logMessage("ERROR typing: " & errMsg)
		end try
	end if
end repeat
