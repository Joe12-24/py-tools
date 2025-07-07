# =======================================================================================
# ---      Script v23.0: The Standard Library Final Edition (for Windows)           ---
# --- Action: This definitive version uses the industry-standard, most robust C#    ---
# ---         definition for the SendInput API to permanently fix the               ---
# ---         "MethodNotFound" error and provide the most reliable input simulation.---
# =======================================================================================

# =======================================================================================
# --- Part 1: Definitive One-Time Initialization ---
# =======================================================================================

# --- Check if the Win32 type needs to be defined ---
# This `if` block prevents the "Type already exists" error.
if (-not ([System.Management.Automation.PSTypeName]'Win32').Type) {
    Write-Host "Initializing Standard Win32 API for the first time..." -ForegroundColor Cyan
    # This is the industry-standard, robust C# definition for SendInput.
    $cSharpCode = @"
    using System;
    using System.Runtime.InteropServices;
    public class Win32 {
        [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
        [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);

        [DllImport("user32.dll", SetLastError = true)]
        private static extern uint SendInput(uint nInputs, INPUT[] pInputs, int cbSize);

        [StructLayout(LayoutKind.Sequential)]
        public struct MOUSEINPUT {
            public int dx; public int dy; public int mouseData; public int dwFlags; public int time; public IntPtr dwExtraInfo;
        }
        [StructLayout(LayoutKind.Sequential)]
        public struct KEYBDINPUT {
            public ushort wVk; public ushort wScan; public uint dwFlags; public int time; public IntPtr dwExtraInfo;
        }
        [StructLayout(LayoutKind.Sequential)]
        public struct HARDWAREINPUT {
            public int uMsg; public short wParamL; public short wParamH;
        }
        [StructLayout(LayoutKind.Explicit)]
        public struct INPUT {
            [FieldOffset(0)] public int type;
            [FieldOffset(4)] public MOUSEINPUT mi;
            [FieldOffset(4)] public KEYBDINPUT ki;
            [FieldOffset(4)] public HARDWAREINPUT hi;
        }
        
        public static void KeyPress(ushort keyCode) {
            INPUT[] inputs = new INPUT[2];
            
            inputs[0].type = 1; // 1 = Keyboard Input
            inputs[0].ki.wVk = keyCode;
            
            inputs[1].type = 1; // 1 = Keyboard Input
            inputs[1].ki.wVk = keyCode;
            inputs[1].ki.dwFlags = 0x0002; // KEYEVENTF_KEYUP
            
            SendInput(2, inputs, Marshal.SizeOf(typeof(INPUT)));
        }
    }
"@
    Add-Type -TypeDefinition $cSharpCode
}

Write-Host "--- Anti-Lock Script v23.0 (Standard Library Final) Started ---" -ForegroundColor Green

# =======================================================================================
# --- Part 2: USER CONFIGURATION ---
# =======================================================================================
$vdiWindowTitle = "¶ÀÏí×ÀÃæ - [»¥ÁªÍø178¶Î]"
$minSeconds = 1
$maxSeconds = 2
$actionsConfig = @{
    useF15Key      = $true
    useNumberKeys  = $true
    useDeleteKey   = $true
    useSpacebarKey = $true
}
# Virtual Key Codes for SendInput
$keyCodes = @{
    F15 = 0x7E; NUM_1 = 0x31; NUM_2 = 0x32; NUM_3 = 0x33; NUM_4 = 0x34; NUM_5 = 0x35;
    NUM_6 = 0x36; NUM_7 = 0x37; NUM_8 = 0x38; NUM_9 = 0x39; NUM_0 = 0x30;
    BACKSPACE = 0x08; SPACE = 0x20;
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
        continue
    }
    
    $vdiHWnd = $vdiProcess.MainWindowHandle
    $originalHWnd = [Win32]::GetForegroundWindow()
    [Win32]::SetForegroundWindow($vdiHWnd)
    Start-Sleep -Milliseconds 500

    $enabledActions = New-Object System.Collections.ArrayList
    if ($actionsConfig.useF15Key) { $null = $enabledActions.Add("F15Key") }
    if ($actionsConfig.useNumberKeys) { $null = $enabledActions.Add("NumberKey") }
    if ($actionsConfig.useDeleteKey) { $null = $enabledActions.Add("DeleteKey") }
    if ($actionsConfig.useSpacebarKey) { $null = $enabledActions.Add("SpacebarKey") }

    if ($enabledActions.Count -gt 0) {
        $chosenAction = $enabledActions | Get-Random
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Performing hardware-level action: $chosenAction" -ForegroundColor Cyan
        
        switch ($chosenAction) {
            "F15Key"      { [Win32]::KeyPress($keyCodes.F15); Write-Host "SUCCESS: Sent F15 key." -ForegroundColor Green }
            "NumberKey"   { $numKey = "NUM_" + (Get-Random -Minimum 0 -Maximum 10); [Win32]::KeyPress($keyCodes[$numKey]); Write-Host "SUCCESS: Sent Number key." -ForegroundColor Green }
            "DeleteKey"   { [Win32]::KeyPress($keyCodes.BACKSPACE); Write-Host "SUCCESS: Sent Backspace key." -ForegroundColor Green }
            "SpacebarKey" { [Win32]::KeyPress($keyCodes.SPACE); Write-Host "SUCCESS: Sent Spacebar key." -ForegroundColor Green }
        }
    } else { Write-Host "SKIPPED: No actions were enabled." -ForegroundColor Yellow }
    
    if ($originalHWnd -ne $vdiHWnd -and $originalHWnd -ne [IntPtr]::Zero) {
        [Win32]::SetForegroundWindow($originalHWnd)
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Switched back to previous window."
    }
}
