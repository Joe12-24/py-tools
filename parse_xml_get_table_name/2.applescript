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
	tell application "System Events"
		repeat with i from 1 to (random number from 10 to 20)
			set randIndex to (random number from 1 to (length of charset))
			set randChar to character randIndex of charset
			keystroke randChar
			delay 0.1
		end repeat
		delay 0.2
		keystroke "s" using command down -- ⌘ + S
	end tell
	logMessage("Activity: Typed random characters and ⌘+S sent.")
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
	set sleepSecs to (random number from 40 to 180)
	logMessage("Sleeping for " & sleepSecs & " seconds.")
	delay sleepSecs
end repeat
