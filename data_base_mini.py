import constant
import datetime

def read_name_task_and_user_id():
    for name_task, id_user in constant.name_task_and_user_id.items():
        constant.temp_i += 1
        if(((str(name_task.lower())) == str(constant.name_task_y).lower()) and (str(id_user.lower())) == constant.temp_user_id):
            return True
        elif(constant.temp_i == len(constant.name_task_and_user_id)):
            return False
    constant.temp_i = 0

def calculation_time(time_from_user, date_now):
    temp_year = time_from_user[0:4]
    temp_months = time_from_user[5:7]
    temp_day = time_from_user[8:10]
    temp_hour = time_from_user[11:13]
    temp_min = time_from_user[14:16]
    temp_second = time_from_user[17:19]

    full_date = datetime.datetime(int(temp_year), int(temp_months), int(temp_day), int(temp_hour), int(temp_min), int(temp_second))

    if(date_now > full_date):
        return 'ERROR_TIME'
    else:
        delta = full_date - date_now
        delta = int(delta.seconds)

        return delta