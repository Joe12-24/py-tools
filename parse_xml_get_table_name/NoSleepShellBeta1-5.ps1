# =======================================================================================
# ---      Ultimate Anti-Lock Script v5.1 (Custom Sleep Duration from Filename)      ---
# =======================================================================================

# --- Part 1: Configuration ---
$enableConsoleLog = $true
$enableActivityLog = $true
$promptForShutdown = $true
$shutdownDialogTimeoutSeconds = 600
$targetUrl = "http://portal.mycompany.internal"

# --- Part 2: Core API Definition ---
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
$vk_F15 = 0x7E

# --- Part 3: Logging Function ---
$activityLogFile = "$PSScriptRoot\activity_log.txt"
function Write-Log($message, $color = 'Gray') {
    $logEntry = "[$(Get-Date -Format 's')] $message"
    if ($enableConsoleLog) { Write-Host $logEntry -ForegroundColor $color }
    if ($enableActivityLog) {
        try { $logEntry | Add-Content -Path $activityLogFile -Encoding utf8 } catch {
            Write-Host "[$(Get-Date -Format 's')] CRITICAL: Failed to write to log file!" -ForegroundColor Red
        }
    }
}

try {
    $desktopPath = [Environment]::GetFolderPath("Desktop")
    $targetFile = Join-Path $desktopPath "moveRandomInput.txt"
    if (-not (Test-Path $targetFile)) {
        New-Item -Path $targetFile -ItemType File -Force | Out-Null
        Write-Log "Created file: $targetFile" -Color Cyan
    } else {
        Clear-Content -Path $targetFile
        Write-Log "File exists, cleared content: $targetFile" -Color Cyan
    }
    Start-Process -FilePath "notepad.exe" -ArgumentList "`"$targetFile`""
    Start-Sleep -Seconds 2

    Write-Log "--- SCRIPT SESSION STARTED (v5.1) ---"
    $networkSimulationEnabled = $targetUrl -ne "http://portal.mycompany.internal"
    if (-not $networkSimulationEnabled) {
        Write-Log "NOTICE: Network simulation is DISABLED. Edit `$targetUrl` to enable it." -color Yellow
    }

    $shutdownEnabled = $false
    $shutdownTime = $null
    $sleepSeconds = 180
    $scriptBaseName = [System.IO.Path]::GetFileNameWithoutExtension($MyInvocation.MyCommand.Path)

    if ($scriptBaseName.Contains("-")) {
        $parts = $scriptBaseName.Split('-')
        $hoursString = $parts[-1]
        $shutdownHoursDouble = 0.0
        if ([double]::TryParse($hoursString, [ref]$shutdownHoursDouble) -and $shutdownHoursDouble -gt 0) {
            $shutdownEnabled = $true
            $shutdownTime = (Get-Date).AddHours($shutdownHoursDouble)
            $sleepSeconds = [math]::Round($shutdownHoursDouble * 3600 / 20)  # 20 cycles per session
            Write-Log "Shutdown enabled for $shutdownHoursDouble hours. Sleep per loop: $sleepSeconds sec" -Color Green
        }
    }

    $WShell = New-Object -ComObject WScript.Shell
    while ($true) {
        if ($shutdownEnabled -and ((Get-Date) -ge $shutdownTime)) {
            Write-Log "Reached scheduled shutdown time." -color Cyan
            if ($promptForShutdown) {
                Write-Log "Showing shutdown prompt..." -color Cyan
                Add-Type -AssemblyName System.Windows.Forms
                $form = New-Object Windows.Forms.Form
                $form.Text = 'Shutdown Confirmation'
                $form.Size = '400,180'
                $form.TopMost = $true
                $label = New-Object Windows.Forms.Label
                $label.Text = "Shutdown in $shutdownDialogTimeoutSeconds seconds"
                $label.Dock = 'Top'
                $form.Controls.Add($label)
                $cancel = New-Object Windows.Forms.Button
                $cancel.Text = "Cancel Shutdown"
                $cancel.Dock = 'Bottom'
                $cancel.Add_Click({ $form.Tag = 'Cancel'; $form.Close() })
                $form.Controls.Add($cancel)
                $timer = New-Object Windows.Forms.Timer
                $timer.Interval = 1000
                $timer.Add_Tick({ $shutdownDialogTimeoutSeconds--; $label.Text = "Shutdown in $shutdownDialogTimeoutSeconds seconds"; if ($shutdownDialogTimeoutSeconds -le 0) { $form.Close() } })
                $timer.Start()
                $form.ShowDialog() | Out-Null
                if ($form.Tag -eq 'Cancel') {
                    Write-Log "User cancelled shutdown." -Color Yellow
                    break
                }
                $performShutdown = $true
            } else {
                $performShutdown = $true
            }
            if ($performShutdown) {
                Write-Log "Initiating shutdown in 60 seconds." -Color Green
                shutdown /s /t 60 /c "Scheduled Anti-Lock Shutdown"
                break
            }
        }

        [Win32]::MoveMouse(1, 1); Start-Sleep -Milliseconds 50; [Win32]::MoveMouse(-1, -1)
        if ($networkSimulationEnabled) {
            try {
                Invoke-WebRequest -Uri $targetUrl -UseBasicParsing -TimeoutSec 10 | Out-Null
                Write-Log "Activity: Simulated network request."
            } catch {
                Write-Log "Network Error: $($_.Exception.Message)" -Color Red
            }
        }

        Write-Log "Sleeping $sleepSeconds seconds before next input..."
        Start-Sleep -Seconds $sleepSeconds

        try {
            $WShell.AppActivate("moveRandomInput.txt") | Out-Null
            Start-Sleep -Milliseconds 400
            $chars = [char[]](48..57 + 65..90 + 97..122)
            $count = Get-Random -Minimum 10 -Maximum 21
            for ($i = 0; $i -lt $count; $i++) {
                $WShell.SendKeys((Get-Random -InputObject $chars))
                Start-Sleep -Milliseconds 100
            }
            $WShell.SendKeys(" ")
            $WShell.SendKeys("^{s}")
            Write-Log "Typed $count characters + space + saved."
        } catch {
            Write-Log "Input error: $($_.Exception.Message)" -Color Red
        }
    }

} catch {
    Write-Log "FATAL ERROR: $($_.Exception.Message)" -Color Red
    "[$(Get-Date)] $($_.Exception.ToString())" | Out-File "$PSScriptRoot\error_log.txt" -Append -Encoding utf8
} finally {
    Write-Log "--- SCRIPT SESSION ENDED ---"
    Write-Host "\n--- Script ended. ---"
    pause
}
