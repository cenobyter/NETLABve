def student_drop_removal(int class, str student_file_location):
    with open(student_file_location) as dropped_students:
        student_name= dropped_student.readline()
            for student in tapi.class_roster_list(cls_id=class): student_to_drop=student[‘acc_id’] if student[‘acc_full_name’]==student_name else None
                tapi.class_roster_remove(cls_id=class, acc_id=student_to_drop) if student_to_drop!= None else print(“student “+student_to_drop+” not found”)

