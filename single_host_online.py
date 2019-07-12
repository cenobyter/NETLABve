
import datetime
from netlab.client import Client
tapi = Client()

#single_host_online is a function designed to take all pods online that utilize the specified host
#the core idea being that if you are bringing a host back from maintenace this function will take all
#pods utilizing that host online
#
#single_host_online requires one keyed argument "online_host" which is a string representing
#desired hosts ip address
#
def single_host_online(*,online_host):
    #import the PCType for use later in a sanity check
    from netlab.enums import PCType
    #for loop to run through all pods on the system
    for pod in tapi.pod_list():
        #assign the pc value to the first pc in the pod
        #this will be used to verify that the pod exists on the server
        pc = tapi.pod_pc_get(pod_id=pod['pod_id'],pl_index=1)
        #check to see that the vm exists and it exists on the specified host
        if pc['pc_type'] !=PCType.ABSENT and online_host == pc['vh_name']:
            #take pod online and provide console feedback on activity
            print('taking pod '+ str(pod['pod_id'])+' online')
            tapi.pod_state_change(pod_id=['pod_id'],state='ONLINE')
