#this is only a very slightly modified version of a script provided by LucD on the vmware community forum
#link for that thread: https://communities.vmware.com/thread/473762
#this script will take a vm (or set of VM's) and remove the desired hardware from it
$vmname="My_VM"
$devicename="Device to Remove"
$vms=get-vm -name $vmname
Foreach ($vm in $vms){
    #set device to be removed (originally audio devices were the target)
    #for Kali VM's from the source audio device is a: “VirtualEnsoniq1371”
    $audio = $vm.ExtensionData.Config.Hardware.Device | Where-Object {$_.GetType().Name -eq $devicename}
    #create a new spec to apply
    $spec = New-Object VMware.Vim.VirtualMachineConfigSpec
    #create a device spec to use to remove HW device
    $dev = New-Object VMware.Vim.VirtualDeviceConfigSpec
    #configure device config to remove the device
    $dev.Device = $audio
    $dev.Operation = "remove"
    #set spec to apply changes in dev spec
    $spec.deviceChange += $dev
    #apply spec to VM
    $vm.ExtensionData.ReconfigVM($spec)
}