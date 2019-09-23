function Import-VappFolder{
    Param(
        [Parameter(Mandatory)]
        [string]$SourceFolder
        ,
        [Parameter(Mandatory)]
        [string]$Server
        ,
        [Parameter(Mandatory)]
        [string]$Storage
        ,
        [Parameter(Mandatory=$false)]
        [string]$DestinationFolder
        )

    $vmHost = Get-VMHost -Name $server

    $vmDataStore = Get-Datastore -Name $Storage

    if($DestinationFolder -ne ""){
        $vmFolder= Get-Folder -Name $DestinationFolder
    }
    Get-Childitem -Recurse -filter *.ov* $SourceFolder | Where-Object{$_.name -match ".ov[af]"} | foreach-object {
        #folder deployment (location) does not seem to work the way I want it to
        if($DestinationFolder -ne ""){
            Import-Vapp -Source $_.fullname -Datastore $vmDataStore -VMHost $vmHost -InventoryLocation $vmFolder -force
        }
        else{
            Import-Vapp -Source $_.fullname -Datastore $vmDataStore -VMHost $vmHost -force
        }
    }
}