

# =======================================================================================
# ---      Ultimate Anti-Lock Script v5.0 (Timed & Switchable Shutdown)             ---
# --- Features:                                                                       ---
# --- 1. NEW: Custom shutdown dialog with a countdown timer. Defaults to shutting   ---
# ---    down if no action is taken.                                                ---
# --- 2. NEW: Switch ($promptForShutdown) to enable or disable the shutdown prompt. ---
# --- 3. Unified logging, decimal hours support, and robust error handling.         ---
# =======================================================================================

# --- Part 1: Configuration ---
# ---------------------------------------------------------------------------------------
# --- Logging Switches ---
# Set to $true to show detailed, timestamped activity logs in the console window.
$enableConsoleLog = $true
# Set to $true to write detailed, timestamped activity logs to "activity_log.txt".
$enableActivityLog = $true

# --- Shutdown Behavior Switches (NEW IN V5.0) ---
# Set to $true to show a confirmation dialog before shutting down.
# Set to $false to initiate shutdown immediately when the time is reached, without any prompt.
$promptForShutdown = $true
# How many seconds the shutdown confirmation dialog should wait before proceeding automatically.
$shutdownDialogTimeoutSeconds = 600


# --- Network Simulation ---
# IMPORTANT: Change this to a real internal company URL to enable network simulation!
$targetUrl = "http://portal.mycompany.internal"


# --- Part 2: Core API Definition (MUST BE AT THE TOP) ---
# ---------------------------------------------------------------------------------------
$cSharpCode = @"
using System;
using System.Runtime.InteropServices;
public class Win32 {
    private const int INPUT_MOUSE = 0; private const int INPUT_KEYBOARD = 1; private const uint KEYEVENTF_KEYUP = 0x0002; private const uint MOUSEEVENTF_MOVE = 0x0001;
    [StructLayout(LayoutKind.Sequential)] public struct MOUSEINPUT { public int dx; public int dy; public uint mouseData; public uint dwFlags; public uint time; public IntPtr dwExtraInfo; }
    [StructLayout(LayoutKind.Sequential)] public struct KEYBDINPUT { public ushort wVk; public ushort wScan; public uint dwFlags; public uint time; public IntPtr dwExtraInfo; }
    [StructLayout(LayoutKind.Explicit)] public struct INPUT { [FieldOffset(0)] public int type; [FieldOffset(4)] public MOUSEINPUT mi; [FieldOffset(4)] public KEYBDINPUT ki; }
    [DllImport("user32.dll", SetLastError = true)] private static extern uint SendInput(uint nInputs, INPUT[] pInputs, int cbSize);
    public static void MoveMouse(int dx, int dy) { INPUT[] i = new INPUT[1]; i[0].type = INPUT_MOUSE; i[0].mi.dx = dx; i[0].mi.dy = dy; i[0].mi.dwFlags = MOUSEEVENTF_MOVE; SendInput(1, i, Marshal.SizeOf(typeof(INPUT))); }
    public static void SendKey(ushort k) { INPUT[] i = new INPUT[2]; i[0].type = INPUT_KEYBOARD; i[0].ki.wVk = k; i[1].type = INPUT_KEYBOARD; i[1].ki.wVk = k; i[1].ki.dwFlags = KEYEVENTF_KEYUP; SendInput(2, i, Marshal.SizeOf(typeof(INPUT))); }
}
"@
Add-Type -TypeDefinition $cSharpCode
$vk_F15 = 0x7E # Note: F15 key press is disabled in main loop to prevent mouse issues.


# --- Part 3: Main Script Logic with Full Error Handling ---
# ---------------------------------------------------------------------------------------
# Define log file path
$activityLogFile = "$PSScriptRoot\activity_log.txt"

# --- Unified Logging Function ---
function Write-Log($message, $color = 'Gray') {
    # Create the timestamped log entry
    $logEntry = "[$(Get-Date -Format 's')] $message" # 's' format is like '2025-06-24T23:30:00'

    # Output to console if enabled
    if ($enableConsoleLog) {
        Write-Host $logEntry -ForegroundColor $color
    }

    # Write to file if enabled
    if ($enableActivityLog) {
        try {
            $logEntry | Add-Content -Path $activityLogFile -Encoding utf8
        } catch {
            Write-Host "[$(Get-Date -Format 's')] CRITICAL: Failed to write to log file!" -ForegroundColor Red
        }
    }
}

try {

    # Define file path
    $desktopPath = [Environment]::GetFolderPath("Desktop")
    $targetFile = Join-Path $desktopPath "moveRandomInput.txt"

    # --- 创建文件（如果不存在） ---
    if (-not (Test-Path $targetFile)) {
        New-Item -Path $targetFile -ItemType File -Force | Out-Null
        Write-Log "Created file: $targetFile" -Color Cyan
    } else {
        Clear-Content -Path $targetFile
        Write-Log "File exists, cleared content: $targetFile" -Color Cyan
    }

    # Open file with notepad explicitly (so we can identify it later)
    Start-Process -FilePath "notepad.exe" -ArgumentList "`"$targetFile`""
    Start-Sleep -Seconds 2
    # --- Write initial log entry ---
    Write-Log "--- SCRIPT SESSION STARTED (v5.0) ---"
    
    # --- Intelligent Feature Detection ---
    $networkSimulationEnabled = $true
    if ($targetUrl -eq "http://portal.mycompany.internal") {
        $networkSimulationEnabled = $false
        Write-Log "NOTICE: Network simulation is DISABLED. Edit `$targetUrl` to enable it." -color Yellow
    }

    # --- Parse filename on startup to set shutdown task ---
    $shutdownEnabled = $false
    $shutdownTime = $null
    $startTime = Get-Date
    $scriptBaseName = [System.IO.Path]::GetFileNameWithoutExtension($MyInvocation.MyCommand.Path)

    if ($scriptBaseName.Contains("-")) {
        $parts = $scriptBaseName.Split('-')
        $hoursString = $parts[-1]
        $shutdownHoursDouble = 0.0
        if ([double]::TryParse($hoursString, [ref]$shutdownHoursDouble) -and $shutdownHoursDouble -gt 0) {
            $shutdownEnabled = $true
            $shutdownTime = $startTime.AddHours($shutdownHoursDouble)
            Write-Log "Shutdown enabled for $shutdownHoursDouble hours. Scheduled time: $($shutdownTime.ToString('yyyy-MM-dd HH:mm:ss'))" -color Green
            Write-Log "Shutdown prompt enabled: $promptForShutdown" -color Cyan
        }
    }
    
    # --- Main Loop ---
    Write-Host "`nPress Ctrl+C in this window to stop the script at any time."
    $WShell = New-Object -ComObject WScript.Shell
    while ($true) {
        # Step 1: Check for shutdown
        if ($shutdownEnabled -and ((Get-Date) -ge $shutdownTime)) {
            Write-Log "Reached scheduled shutdown time." -color Cyan
            
            $performShutdown = $false
            
            if ($promptForShutdown) {
                # --- NEW V5.0: Custom Timed Dialog Box ---
                Write-Log "Displaying timed confirmation dialog ($($shutdownDialogTimeoutSeconds)s)..." -color Cyan
                Add-Type -AssemblyName System.Windows.Forms
                
                $userCancelled = $false
                $countdown = $shutdownDialogTimeoutSeconds

                $form = New-Object System.Windows.Forms.Form
                $form.Text = 'Shutdown Confirmation'
                $form.Size = New-Object System.Drawing.Size(400, 180)
                $form.StartPosition = 'CenterScreen'
                $form.TopMost = $true

                $label = New-Object System.Windows.Forms.Label
                $label.Location = New-Object System.Drawing.Point(20, 20)
                $label.Size = New-Object System.Drawing.Size(360, 60)
                $label.Font = New-Object System.Drawing.Font('Arial', 10)
                $label.Text = "The script has run for its scheduled duration.`nComputer will shut down in $countdown seconds."
                $form.Controls.Add($label)

                $cancelButton = New-Object System.Windows.Forms.Button
                $cancelButton.Location = New-Object System.Drawing.Point(140, 90)
                $cancelButton.Size = New-Object System.Drawing.Size(120, 30)
                $cancelButton.Text = 'Cancel Shutdown'
                $cancelButton.DialogResult = [System.Windows.Forms.DialogResult]::Cancel
                $cancelButton.add_Click({ $script:userCancelled = $true; $form.Close() })
                $form.Controls.Add($cancelButton)
                
                $timer = New-Object System.Windows.Forms.Timer
                $timer.Interval = 1000 # 1 second
                $timer.add_Tick({
                    $script:countdown--
                    $label.Text = "The script has run for its scheduled duration.`nComputer will shut down in $countdown seconds."
                    if ($countdown -le 0) {
                        $timer.Stop()
                        $form.Close()
                    }
                })
                $timer.Start()

                # Show the form and wait for it to be closed (by button or timer)
                $form.ShowDialog() | Out-Null
                
                # Cleanup
                $timer.Stop(); $timer.Dispose(); $form.Dispose()

                if ($userCancelled) {
                    Write-Log "User CANCELLED the shutdown." -color Yellow
                } else {
                    Write-Log "Dialog timed out or was closed. Proceeding with shutdown." -color Green
                    $performShutdown = $true
                }

            } else { # --- No prompt, direct shutdown ---
                Write-Log "Direct shutdown initiated as per configuration (no prompt)." -color Green
                $performShutdown = $true
            }

            if ($performShutdown) {
                Write-Log "Initiating shutdown in 60 seconds." -color Green
                shutdown /s /t 60 /c "Shutdown initiated by Anti-Lock script."
            }
            
            break # Exit the main while loop
        }

        # Step 2: Perform anti-lock activities
        try { 
            [Win32]::MoveMouse(1, 1); Start-Sleep -Milliseconds 50; [Win32]::MoveMouse(-1, -1)
            Write-Log "Activity: Mouse jiggled."
        } catch {}
        
        # NOTE: F15 key press is intentionally disabled to prevent mouse click issues.
        # try { [Win32]::SendKey($vk_F15); Write-Log "Activity: F15 key sent." } catch {}
        
        if ($networkSimulationEnabled) {
            try { 
                $null = Invoke-WebRequest -Uri $targetUrl -UseBasicParsing -TimeoutSec 15
                Write-Log "Activity: Network traffic sent successfully."
            } catch { 
                Write-Log "Network Error: Failed to access URL. ($($_.Exception.Message))" -color Red
            }
        }
    
        # Step 3: Wait
        $sleepSeconds = Get-Random -Minimum 50 -Maximum 241
        Write-Log "Waiting for $sleepSeconds seconds..."
        Start-Sleep -Seconds $sleepSeconds
        try {
            # Send the F15 key. This is a non-intrusive key.
            $WShell.SendKeys("{F15}")
            Write-Log "Activity: Sent {F15} key press." -Color Cyan
            
            
						# Bring Notepad window with our file to front
						$null = $WShell.AppActivate("moveRandomInput.txt") # Will activate Notepad window with this title
						Start-Sleep -Milliseconds 500

						# Send random characters
						$digits = [char[]](48..57)
						$lowercase = [char[]](97..122)
						$uppercase = [char[]](65..90)
						$chars = $digits + $lowercase + $uppercase

						$count = Get-Random -Minimum 10 -Maximum 21
						for ($i = 0; $i -lt $count; $i++) {
						    $randomChar = Get-Random -InputObject $chars
						    try {
						        $Wshell.SendKeys($randomChar)
						        Start-Sleep -Milliseconds 100
						    } catch {}
						}
                        # 输入一个空格
                        $WShell.SendKeys(" ")
						# Save the file (Ctrl+S)
						$Wshell.SendKeys("^{s}")
						Write-Log "Activity: Wrote $count random chars to moveRandomInput.txt"
						
        } catch {
            Write-Log "ERROR: Failed to send key press. Details: $($_.Exception.Message)" -Color Red
        }
    }

} catch {
    # --- Fatal Error Handling Block ---
    $errorMessageText = "A FATAL ERROR OCCURRED! See error_log.txt for details."
    Write-Log $errorMessageText -color Red
    
    $errorLogFile = "$PSScriptRoot\error_log.txt"
    $fullErrorMessage = "Timestamp: $(Get-Date)`nError Details:`n$($_.Exception.ToString())`n`n"
    $fullErrorMessage | Out-File -FilePath $errorLogFile -Append -Encoding utf8

} finally {
    Write-Log "--- Initiating cleanup (finally block) ---" -Color Cyan

    try {
        # Ensure $WShell is defined
        if (-not $WShell) {
            $WShell = New-Object -ComObject WScript.Shell
        }

        # Try saving the file again
        try {
            $WShell.AppActivate("moveRandomInput.txt") | Out-Null
            Start-Sleep -Milliseconds 500
            $WShell.SendKeys("^{s}")
            Write-Log "Final Save: Sent Ctrl+S to Notepad." -Color Cyan
        } catch {
            Write-Log "WARNING: Failed to activate/save Notepad. $($_.Exception.Message)" -Color Yellow
        }

        # Close Notepad
        $processes = Get-Process notepad -ErrorAction SilentlyContinue
        foreach ($p in $processes) {
            try {
                if ($p.MainWindowTitle -like "*moveRandomInput.txt*") {
                    Stop-Process -Id $p.Id -Force
                    Write-Log "Closed Notepad process: PID $($p.Id)" -Color Yellow
                }
            } catch {
                Write-Log "WARNING: Failed to close Notepad: $($_.Exception.Message)" -Color Red
            }
        }

        Start-Sleep -Milliseconds 800

        # Delete the file
        if (Test-Path $targetFile) {
            Remove-Item -Path $targetFile -Force
            Write-Log "Deleted file: $targetFile" -Color Cyan
        }

    } catch {
        Write-Log "ERROR during cleanup: $($_.Exception.Message)" -Color Red
    }

    Write-Log "--- SCRIPT SESSION ENDED ---"
    # 不再提示用户按任意键，直接退出
}
