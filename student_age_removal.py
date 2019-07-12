from netlab.client import Client
from netlab.enums import AccountType
import datetime

tapi = Client()

def student_age_removal(max_day_age=365):
    """
    This function will remove student accounts that surpass a maximum day value
    by default this value is 365 days (or the standard year)
    this can be changed if the function is called with an integer representing the max day age
    """
    #specify today to be used for calculations
    today=datetime.datetime.today()
    #set the delta time for calculations
    delta_time = datetime.timedelta(days=max_day_age)
    
    
    for user in tapi.user_account_list(properties='all'):
        #verify user is a student before proceeding
        #verify that the last login value is not none, as this would result in a type error during removal
        #finally check if last login was before the value of today minus the delta time
        if user['acc_type'] == AccountType('S')\
            and tapi.user_account_get(acc_id=user['acc_id'], properties='all')['acc_last_login'] != None\
            and tapi.user_account_get(acc_id=user['acc_id'], properties='all')['acc_last_login'] < (today-delta_time):
                tapi.user_account_remove(acc_id=user['acc_id'])
