import datetime, random

def gen_data():
    start_date = datetime.datetime(2022, 10, 1, 1, 1, 1)
    end_date   = datetime.datetime(2030, 11, 30, 1, 1, 1)
    num_days   = (end_date - start_date).days
    rand_days   = random.randint(1, num_days)
    rand_hours  = random.randint(1, 24)
    rand_min  = random.randint(1, 60)
    random_date = start_date + datetime.timedelta(days=rand_days, hours=rand_hours, minutes=rand_min)
    return random_date.strftime("20%y-%m-%dT%H:%M:%S")

print(gen_data())
print(gen_data())