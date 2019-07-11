from netlab.client import Client
import datetime

tapi = Client()

def student_drop_removal(Netlab_Class,student_file_location):
    with open(student_file_location) as dropped_students:
        student_name= dropped_students.readline()
        for student in tapi.class_roster_list(cls_id=Netlab_Class):
            student_to_drop=student['acc_id'] if student['acc_full_name']==student_name else None
            if student_to_drop!= None:
                tapi.class_roster_remove(cls_id=Netlab_Class, acc_id=student_to_drop)
            else:
                    print("student "+student_to_drop+" not found")

