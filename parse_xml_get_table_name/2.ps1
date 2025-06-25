# =======================================================================================
# ---      Script v21.0: The Definitive Edition (for Windows)                       ---
# --- Action: This definitive version solves the root "Add-Type" error by           ---
# ---         intelligently checking if the type already exists before attempting   ---
# ---         to load it. This ensures stability across all environments.           ---
# =======================================================================================

# =======================================================================================
# --- Part 1: Definitive One-Time Initialization ---
# =======================================================================================

# --- Check if the Win32 type needs to be defined ---
# This `if` block is the CORE FIX. It prevents the "TYPE_ALREADY_EXISTS" error.
if (-not ([System.Management.Automation.PSTypeName]'Win32').Type) {
    Write-Host "Initializing Win32 API for the first time..." -ForegroundColor Cyan
    $cSharpCode = @"
    using System;
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
}

# --- WScript Shell Object ---
$WShell = New-Object -ComObject WScript.Shell
Write-Host "--- Anti-Lock Script v21.0 (The Definitive Edition) Started ---" -ForegroundColor Green

# =======================================================================================
# --- Part 2: USER CONFIGURATION ---
# =======================================================================================
$vdiWindowTitle = "¶ÀÏí×ÀÃæ - [»¥ÁªÍø178¶Î]"
$minSeconds = 1
$maxSeconds = 2
$actionsConfig = @{
    useMouseClick  = $true
    useF15Key      = $true
    useNumberKeys  = $true
    useDeleteKey   = $true
    useSpacebarKey = $true
}

# =======================================================================================
# --- Part 3: MAIN SCRIPT LOOP ---
# =======================================================================================
while ($true) {
    $waitTime = Get-Random -Minimum $minSeconds -Maximum ($maxSeconds + 1)
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Script is active. Next action in $waitTime seconds."
    Start-Sleep -Seconds $waitTime
    
    $vdiProcess = Get-Process | Where-Object { $_.MainWindowTitle -eq $vdiWindowTitle } | Select-Object -First 1
    if ($null -eq $vdiProcess) {
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] ERROR: Cannot find VDI window. Retrying..." -ForegroundColor Red
        # continue
    }
    
    $vdiHWnd = $vdiProcess.MainWindowHandle
    $originalHWnd = [Win32]::GetForegroundWindow()
    [Win32]::SetForegroundWindow($vdiHWnd)
    Start-Sleep -Milliseconds 400

    $enabledActions = New-Object System.Collections.ArrayList
    if ($actionsConfig.useMouseClick)  { $null = $enabledActions.Add("MouseClick") }
    if ($actionsConfig.useF15Key)      { $null = $enabledActions.Add("F15Key") }
    if ($actionsConfig.useNumberKeys)  { $null = $enabledActions.Add("NumberKey") }
    if ($actionsConfig.useDeleteKey)   { $null = $enabledActions.Add("DeleteKey") }
    if ($actionsConfig.useSpacebarKey) { $null = $enabledActions.Add("SpacebarKey") }

    if ($enabledActions.Count -gt 0) {
        $chosenAction = $enabledActions | Get-Random
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Performing action: $chosenAction" -ForegroundColor Cyan
        switch ($chosenAction) {
            "MouseClick" {
                $rect = $null; [Win32]::GetWindowRect($vdiHWnd, [ref]$rect) | Out-Null
                if ($rect.Right - $rect.Left -gt 100 -and $rect.Bottom - $rect.Top -gt 100) {
                    $x = Get-Random -Minimum ($rect.Left + 50) -Maximum ($rect.Right - 50); $y = Get-Random -Minimum ($rect.Top + 50) -Maximum ($rect.Bottom - 50)
                    [Win32]::SetCursorPos($x, $y); Start-Sleep -Milliseconds 50
                    [Win32]::mouse_event(2, 0, 0, 0, [System.UIntPtr]::Zero); Start-Sleep -Milliseconds 100
                    [Win32]::mouse_event(4, 0, 0, 0, [System.UIntPtr]::Zero)
                    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] SUCCESS: Performed Mouse Click." -ForegroundColor Green
                } else { Write-Host "SKIPPED: Window is too small." -ForegroundColor Yellow }
            }
            "F15Key"      { $WShell.SendKeys("{F15}"); Write-Host "[$(Get-Date -Format 'HH:mm:ss')] SUCCESS: Sent F15 key." -ForegroundColor Green }
            "NumberKey"   { $num = Get-Random -Minimum 1 -Maximum 10; $WShell.SendKeys($num); Write-Host "[$(Get-Date -Format 'HH:mm:ss')] SUCCESS: Sent Number '$num'." -ForegroundColor Green }
            "DeleteKey"   { $WShell.SendKeys("{BS}"); Write-Host "[$(Get-Date -Format 'HH:mm:ss')] SUCCESS: Sent Backspace." -ForegroundColor Green }
            "SpacebarKey" { $WShell.SendKeys(" "); Write-Host "[$(Get-Date -Format 'HH:mm:ss')] SUCCESS: Sent Spacebar." -ForegroundColor Green }
        }
    } else { Write-Host "SKIPPED: No actions were enabled." -ForegroundColor Yellow }
    
    if ($originalHWnd -ne $vdiHWnd -and $originalHWnd -ne [IntPtr]::Zero) {
        [Win32]::SetForegroundWindow($originalHWnd)
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Switched back to previous window."
    }
}
