$task_name = "snapshot_restore"
$python_path = Get-Command python.exe | Select-Object -ExpandProperty Path
$exe_path = (Get-Item ".\$($task_name).py").FullName

try {
  $does_task_exist = Get-ScheduledTask -TaskName $task_name
  if ($does_task_exist) {
    $null = Unregister-ScheduledTask -TaskName $task_name -Confirm:$false
  }
} catch {
  # pass
}


$task = New-ScheduledTask -Action (New-ScheduledTaskAction -Execute $python_path -Argument $exe_path) -Trigger (New-ScheduledTaskTrigger -AtStartup)
Register-ScheduledTask -TaskName $task_name -InputObject $task
