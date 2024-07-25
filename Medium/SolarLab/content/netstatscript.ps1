# Obtener todas las conexiones y puertos de escucha con sus PIDs
$netstatOutput = netstat -ano | Select-String "LISTENING"

# Crear una lista para almacenar los resultados
$result = @()

foreach ($line in $netstatOutput) {
    $parts = $line.ToString().Split()
    $port = $parts[1]
    $pid = $parts[-1]
    
    $process = Get-Process -Id $pid -ErrorAction SilentlyContinue
    
    if ($process) {
        $processOwner = (Get-WmiObject Win32_Process -Filter "ProcessId = $pid").GetOwner()
        $username = $processOwner.User
        $domain = $processOwner.Domain
        $username = if ($username) { "$domain\$username" } else { "N/A" }
    } else {
        $username = "N/A"
    }

    $result += [PSCustomObject]@{
        Port = $port
        PID = $pid
        ProcessName = if ($process) { $process.Name } else { "N/A" }
        UserName = $username
    }
}

$result | Format-Table -AutoSize | Out-File -FilePath "res.txt"
