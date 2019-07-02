foreach($pod in $range){
    $thing= "pod-{0:d2}" -f $pod  
    if(($pod+2)%3 -eq 0){$hostname = “172.16.0.109”}
    if(($pod+1)%3 -eq 0){$hostname = “172.16.0.113”}
    if(($pod)%3 -eq 0){$hostname = “172.16.0.114”}

    $network_in=“BARC_$thing”+”_Inside”
    Write-output “creating network $network_in on host $hostname”

    
    New-VirtualSwitch -VMHost $hostname -Name $network_in
    New-VirtualPortGroup -name $network_in+"_pg" -VirtualSwitch $network_in

    $network_out=“BARC_$thing"+"_Outside”
    Write-output “creating network $network_out on host $hostname”

    New-VirtualSwitch -VMHost $hostname -Name $network_out
    New-VirtualPortGroup -name $network_out+"_pg" -VirtualSwitch $network_out

    Write-output “attaching BARC_2019_$thing* to $network_in”

    Get-vm “BARC_2019_$thing*” | Get-NetworkAdapter | Set-NetworkAdapter -NetworkName $network_in+"_pg"

    Get-vm “BARC_2019_$thing*” | get-snapshot | remove-snapshot
    Get-vm “BARC_2019_$thing*” | new-snapshot -name “GOLDEN_MASTER” -description "Correct Networking?"
    Write-output "attaching BARC_2019_Hidden_$thing* to $network_out"

    get-vm "BARC_2019_Hidden_$thing*" | Get-NetworkAdapter | Set-NetworkAdapter -NetworkName $network_out+"_pg"
    get-vm "BARC_2019_Hidden_$thing*host2" | Get-NetworkAdapter | Set-NetworkAdapter -NetworkName $network_in+"_pg"
    get-vm "BARC_2019_Hidden_$thing*" | Get-NetworkAdapter -name "Network Adapter 2" | Set-NetworkAdapter -NetworkName $network_in+"_pg"

    get-vm "BARC_2019_Hidden_$thing*" | get-snapshot | remove-snapshot
    get-vm "BARC_2019_Hidden_$thing*" | new-snapshot -name "GOLDEN_MASTER" -description "Correct Networking?"
}

