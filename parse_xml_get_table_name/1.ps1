# =======================================================================================
# ---           Script v15.0: The Pure Core Edition (for Windows)                   ---
# --- Action: A completely rewritten, ultra-robust version with the simplest      ---
# ---         possible syntax to eliminate all parsing and character errors.        ---
# =======================================================================================

# =======================================================================================
# --- Part 1: USER CONFIGURATION ---
# =======================================================================================

# 1. The EXACT title of your target VDI window.
$vdiWindowTitle = "¶ÀÏí×ÀÃæ - [»¥ÁªÍø178¶Î]"

# 2. Action Interval (in seconds)
$minSeconds = 5
$maxSeconds = 5

# 3. Action Type Configuration
$actionsConfig = @{
    useMouseClick = $true
    useF15Key     = $true
    useNumberKeys = $false
    useDeleteKey  = $false
}

# =======================================================================================
# --- Part 2: Win32 API Definitions (Do not modify) ---
# =======================================================================================
$cSharpCode = @"
using System;
using System.Text;
using System.Runtime.InteropServices;
public class Win32 {
    [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);
    [DllImport("user32.dll")] public static extern bool SetCursorPos(int X, int Y);
    [DllImport("user32.dll")] public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint cButtons, UIntPtr dwExtraInfo);
    public const uint MOUSEEVENTF_LEFTDOWN = 0x02;
    public const uint MOUSEEVENTF_LEFTUP = 0x04;
    [StructLayout(LayoutKind.Sequential)]
    public struct RECT { public int Left; public int Top; public int Right; public int Bottom; }
}
"@
Add-Type -TypeDefinition $cSharpCode -ErrorAction Stop

# =======================================================================================
# --- Part 3: MAIN SCRIPT LOGIC (Rewritten for absolute stability) ---
# =======================================================================================
Write-Host "--- Anti-Lock Script v15.0 (Pure Core) Started ---" -ForegroundColor Green
$WShell = New-Object -ComObject WScript.Shell

while ($true) {
    $waitTime = Get-Random -Minimum $minSeconds -Maximum ($maxSeconds + 1)
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Script is active. Next action in $waitTime seconds."
    Start-Sleep -Seconds $waitTime
    
    # Step 1: Find VDI window by scanning processes
    $vdiProcess = Get-Process | Where-Object { $_.MainWindowTitle -eq $vdiWindowTitle } | Select-Object -First 1
    
    if ($null -eq $vdiProcess) {
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] ERROR: Cannot find VDI window. Retrying..." -ForegroundColor Red
        continue
    }
    
    # Step 2: Prepare for quick-switch
    $vdiHWnd = $vdiProcess.MainWindowHandle
    $originalHWnd = [Win32]::GetForegroundWindow()
    
    # Step 3: Activate VDI window
    [Win32]::SetForegroundWindow($vdiHWnd)
    Start-Sleep -Milliseconds 400

    # Step 4: Choose and perform a random action
    $enabledActions = New-Object System.Collections.ArrayList
    if ($actionsConfig.useMouseClick) { $null = $enabledActions.Add("MouseClick") }
    if ($actionsConfig.useF15Key)     { $null = $enabledActions.Add("F15Key") }
    if ($actionsConfig.useNumberKeys) { $null = $enabledActions.Add("NumberKey") }
    if ($actionsConfig.useDeleteKey)  { $null = $enabledActions.Add("DeleteKey") }

    if ($enabledActions.Count -gt 0) {
        $chosenAction = $enabledActions | Get-Random
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Performing action: $chosenAction" -ForegroundColor Cyan
        
        switch ($chosenAction) {
            "MouseClick" {
                [Win32]::GetWindowRect($vdiHWnd, [ref]$rect) | Out-Null
                $width = $rect.Right - $rect.Left
                $height = $rect.Bottom - $rect.Top
                
                # Using nested 'if' for maximum compatibility
                if ($width -gt 100) {
                    if ($height -gt 100) {
                        $x = Get-Random -Minimum ($rect.Left + 50) -Maximum ($rect.Right - 50)
                        $y = Get-Random -Minimum ($rect.Top + 50) -Maximum ($rect.Bottom - 50)
                        [Win32]::SetCursorPos($x, $y)
                        Start-Sleep -Milliseconds 50
                        [Win32]::mouse_event(2, 0, 0, 0, [System.UIntPtr]::Zero) # Left Down
                        Start-Sleep -Milliseconds 100
                        [Win32]::mouse_event(4, 0, 0, 0, [System.UIntPtr]::Zero) # Left Up
                        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] SUCCESS: Performed Mouse Click." -ForegroundColor Green
                    } else {
                        Write-Host "SKIPPED: Window height is too small for a safe click." -ForegroundColor Yellow
                    }
                } else {
                    Write-Host "SKIPPED: Window width is too small for a safe click." -ForegroundColor Yellow
                }
            }
            "F15Key" {
                $WShell.SendKeys("{F15}")
                Write-Host "[$(Get-Date -Format 'HH:mm:ss')] SUCCESS: Sent F15 key." -ForegroundColor Green
            }
            "NumberKey" {
                $num = Get-Random -Minimum 1 -Maximum 10
                $WShell.SendKeys($num)
                Write-Host "[$(Get-Date -Format 'HH:mm:ss')] SUCCESS: Sent Number '$num'." -ForegroundColor Green
            }
            "DeleteKey" {
                $WShell.SendKeys("{BS}") # Backspace
                Write-Host "[$(Get-Date -Format 'HH:mm:ss')] SUCCESS: Sent Backspace." -ForegroundColor Green
            }
        }
    } else {
        Write-Host "SKIPPED: No actions were enabled in configuration." -ForegroundColor Yellow
    }
    
    # Step 5: Switch back to the original window
    if ($originalHWnd -ne $vdiHWnd -and $originalHWnd -ne [IntPtr]::Zero) {
        [Win32]::SetForegroundWindow($originalHWnd)
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Switched back to previous window."
    }
}
