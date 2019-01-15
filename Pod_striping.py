#variables to change

#pod_base is used to decipher which pod # for the specific set
pod_base=53000

#parent_pod is the pod to be cloned
parent_pod=153

#number of pods to clone out
pod_numbers=33


#pod numbers will be added in the cloning step from the range utilizing the pod_base
pod_name_base="Cyber_Patriots_State_Silver/MiddleSchool_Pod-%02d"


#begin clone specs easier to edit the clone specs settings below than here

#109
pc_clone_spec1 = {'clone_role': 'NORMAL',
                   'clone_storage_alloc': 'ONDEMAND',
                   'clone_type': 'LINKED',
                   'clone_vh_id': 2,
                   'source_snapshot': 'GOLDEN_MASTER',
                   'clone_snapshot': 'GOLDEN_MASTER',
                   'clone_datastore': 'LOCAL109'}
#113
pc_clone_spec2 = {'clone_role': 'NORMAL',
                   'clone_storage_alloc': 'ONDEMAND',
                   'clone_type': 'LINKED',
                   'clone_vh_id': 3,
                   'source_snapshot': 'GOLDEN_MASTER',
                   'clone_snapshot': 'GOLDEN_MASTER',
                   'clone_datastore': 'LOCAL113'}
#114
pc_clone_spec3 = {'clone_role': 'NORMAL',
                   'clone_storage_alloc': 'ONDEMAND',
                   'clone_type': 'LINKED',
                   'clone_vh_id': 1,
                   'source_snapshot': 'GOLDEN_MASTER',
                   'clone_snapshot': 'GOLDEN_MASTER',
                   'clone_datastore': 'LOCAL114'}

#easier to manipulate clone specs

pc_clone_specs3 = pc_clone_spec2
pc_clone_specs1 = pc_clone_spec3
pc_clone_specs2 = pc_clone_spec1

#end variable to change

#pod_set is the range of pod destinations to be cloned to
pod_set=range(pod_base+1,pod_base+(pod_numbers+1))

tracker=1

#Tack Pods Offline
for pod in pod_set:
    if tracker==4:
        tracker=1
    print("taking pod "+str(pod)+" offline")
    tapi.pod_state_change(pod_id=pod,state='OFFLINE')
    tracker+=1

tracker=1

#Remove Pods

for pod in pod_set:
    if tracker==4:
        tracker=1
    if tracker==1:
        print("removing pod "+str(pod))
        tapi.pod_remove_task(pod_id=pod,remove_vms='DISK')
    if tracker==2:
        print("removing pod "+str(pod))
        tapi.pod_remove_task(pod_id=pod,remove_vms='DISK')
    if tracker==3:
        print("removing pod "+str(pod))
        tapi.pod_remove_task(pod_id=pod,remove_vms='DISK')

    tracker+=1

tracker=1

#Creating new pods


for pod in pod_set:
    print("Creating pod %02d"%(pod-pod_base))
    if tracker==4:
        tracker=1
    if tracker==1:
        print("cloning to host vh id "+str(pc_clone_specs1['clone_vh_id']))
        tapi.pod_clone_task(source_pod_id=parent_pod,clone_pod_id=pod,clone_pod_name=pod_name_base%(pod-pod_base),pc_clone_specs=pc_clone_specs1)
    if tracker==2:
        print("cloning to host vh id "+str(pc_clone_specs2['clone_vh_id']))
        tapi.pod_clone_task(source_pod_id=parent_pod,clone_pod_id=pod,clone_pod_name=pod_name_base%(pod-pod_base),pc_clone_specs=pc_clone_specs2)
    if tracker==3:
        print("cloning to host vh id "+str(pc_clone_specs3['clone_vh_id']))
        tapi.pod_clone_task(source_pod_id=parent_pod,clone_pod_id=pod,clone_pod_name=pod_name_base%(pod-pod_base),pc_clone_specs=pc_clone_specs3)
    tracker+=1


#Bringing new pods online

tracker=1

for pod in pod_set:
    if tracker==4:
        tracker=1
    if tracker==1:
        print("taking pod "+str(pod)+" online")
        tapi.pod_state_change(pod_id=pod,state='ONLINE')
    if tracker==2:
        print("taking pod "+str(pod)+" online")
        tapi.pod_state_change(pod_id=pod,state='ONLINE')
    if tracker==3:
        print("taking pod "+str(pod)+" online")
        tapi.pod_state_change(pod_id=pod,state='ONLINE')
    tracker+=1

