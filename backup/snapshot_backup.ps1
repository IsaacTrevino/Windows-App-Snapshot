$task_name = "snapshot_backup"

function Log-Message {
    param (
        [string]$message
    )
    Add-Content -Path ".\backup\$($task_name).log" -Value "$(Get-Date -Format "yyyy-MM-dd HH:mm:ss") - $message"
}

try {
    $python_path = Get-Command python.exe | Select-Object -ExpandProperty Path
    Log-Message "Python path: $python_path"
    
    $exe_path = (Get-Item (Resolve-Path ".\backup\$($task_name).py")).FullName
    Log-Message "Executable path: $exe_path"
    
    $does_task_exist = Get-ScheduledTask -TaskName $task_name
    if ($does_task_exist) {
        $null = Unregister-ScheduledTask -TaskName $task_name -Confirm:$false
        Log-Message "Unregistered existing task: $task_name"
    }
} catch {
    Log-Message "Error: $_"
}

try {
    $task = New-ScheduledTask -Action (New-ScheduledTaskAction -Execute $python_path -Argument $exe_path) -Trigger (New-ScheduledTaskTrigger -Once -At (Get-Date).AddSeconds(10)) -Principal (New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest)
    Register-ScheduledTask -TaskName $task_name -InputObject $task
    Log-Message "Registered new task: $task_name"
} catch {
    Log-Message "Error: $_"
}