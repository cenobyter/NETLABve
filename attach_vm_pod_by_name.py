from netlab.client import Client

#attatch_vm_pd_by_name is designed to change out the vms attatched to a pod based on the name instead of various ID numbers used by netlab
#currently this is designed to replace all vms in a pod, as a single vm is easy enough to replace through the gui
#however it could easily be reworked to do a sing vm and strip out the for loop to another function
#this would require pl_index to be known ahead of time.
def attatch_vm_pod_by_name(pod_name=None,vm_name=None):
    tapi=Client()
    #initialize variables to be used
    all_vms=tapi.vm_inventory_list()
    vms_to_add=[]
    #cycle through all vm's and add the matching vms into the array
    for vm in all_vms:
        if vm_name in vm['vm_name']:
            vms_to_add.append(vm)
    #tracker is used to index the correct pc inside a pod
    tracker=1
    #searach for pod based on name and store pod id
    for pod in tapi.pod_list():
        if pod_name == pod['pod_name']:
            update_pod_id=pod['pod_id']
    #nasty safety net that doesn't work
    if update_pod_id !=  None:
        #run through all matching vm's and assign them to the corrrect pc_id to be used for the pod.
        for vm_to_add in vms_to_add:
            #grab pc id of the needed vm from the existing pod
            pcid=tapi.pod_pc_get(pod_id=update_pod_id,pl_index=tracker)['pc_id']
            #echo to user
            print("adding vm "+vm_to_add['vm_name']+" to pod "+str(update_pod_id)+" at index "+str(tracker))
            #long line doing the actual work
            tapi.pod_pc_update(pc_id=pcid,vm_id=vm_to_add['vm_id'],pc_os_id=vm_to_add['pc_os_id'],pc_type='AVMI',
                vm_snapshot='GOLDEN_MASTER',pc_online=True,vm_shutdown_pref='SHUTDOWN',vm_auto_display=True, 
                vm_auto_network=True, vm_auto_settings=True, vm_sanity_checks=True)
            tracker+=1