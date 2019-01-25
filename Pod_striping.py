import datetime, json
from netlab.client import Client

def pod_striping(pod_base=None,parent_pod=None,pod_numbers=32,pod_name_base=None,filename="./pc_clone_spec.json",
        set1="pc_clone_spec1",set2="pc_clone_spec2",set3="pc_clone_spec3",replacement=False):
    #argument usage/definitions
    #pod_base is used to decipher which pod # for the specific set
    #parent_pod is the pod to be cloned
    #pod_numbers is the number of pods to clone out
    #pod numbers will be added in the cloning step from the range utilizing the pod_base
    #pod_name_base is the string that is re-used by all pods
    #filename specifies a json file that contains the pc_clone_specs
    #example pod_name_base="Cyber_Patriots_State_Silver/MiddleSchool_Pod-%02d"
    #replacement is used to define if it is replacing an existing pod set, if true removes old pods


    #begin clone specs easier to edit the clone specs settings below than here
    #easier to manipulate clone specs
    with open(filename, 'r') as f:
        pc_specs=json.load(f)

    pc_clone_specs1 = pc_specs[set1][0]
    pc_clone_specs2 = pc_specs[set2][0]
    pc_clone_specs3 = pc_specs[set3][0]

    #end variable to change

    #pod_set is the range of pod destinations to be cloned to
    pod_set=range(pod_base+1,pod_base+(pod_numbers+1))

    tapi = Client()

    if replacement:
        #Tack Pods Offline
        for pod in pod_set:
            print("taking pod "+str(pod)+" offline")
            tapi.pod_state_change(pod_id=pod,state='OFFLINE')
        #Remove Pods

        for pod in pod_set:
                print("removing pod "+str(pod))
                tapi.pod_remove_task(pod_id=pod,remove_vms='DISK')

    #Creating new pods


    for pod in pod_set[::3]:
        print("Creating pod %02d"%(pod-pod_base))
        print("cloning to host vh id "+str(pc_clone_specs1['clone_vh_id']))
        tapi.pod_clone_task(source_pod_id=parent_pod,clone_pod_id=pod,clone_pod_name=pod_name_base%(pod-pod_base),
        pc_clone_specs=pc_clone_specs1)
    for pod in pod_set[1::3]:
        print("Creating pod %02d"%(pod-pod_base))   
        print("cloning to host vh id "+str(pc_clone_specs2['clone_vh_id']))
        tapi.pod_clone_task(source_pod_id=parent_pod,clone_pod_id=pod,clone_pod_name=pod_name_base%(pod-pod_base),
        pc_clone_specs=pc_clone_specs2)
    for pod in pod_set[2::3]:
        print("Creating pod %02d"%(pod-pod_base))
        print("cloning to host vh id "+str(pc_clone_specs3['clone_vh_id']))
        tapi.pod_clone_task(source_pod_id=parent_pod,clone_pod_id=pod,clone_pod_name=pod_name_base%(pod-pod_base),
        pc_clone_specs=pc_clone_specs3)



    #Bringing new pods online
    for pod in pod_set:
            print("taking pod "+str(pod)+" online")


