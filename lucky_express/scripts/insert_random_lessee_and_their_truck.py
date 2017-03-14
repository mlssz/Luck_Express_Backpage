"""
This script generate and insert data about lessees and their trucks.
"""
import random
from backpage.models import (
    User,
    Lessee,
    Truck
)

base_position_y = 30.319799
base_position_x = 120.338637

def generate_lessee_and_truck(car_type, count):
    """Generate lessee and the special type truck"""
    account = str(random.randrange(10000, 1000000))
    lessee = User(account=account, name="lessee{}".format(count), user_type=2, token=account)
    lessee.save()
    offset = random.uniform(-0.09, 0.09)
    lessee = Lessee(
        id=lessee,
        position_x= base_position_x + offset,
        position_y= base_position_y + offset,
        password="1",
        realname="name"+account,
        order_count = random.randrange(200),
        score = random.randrange(1, 6),
        ci="ci" + account
    )
    lessee.save()
    Truck.objects.create(lessee=lessee, no="浙A"+account[:5], car_type=car_type)

def work_start(num):
    per_num = num // 5
    count = 0

    for i in range(5):
        print("Generate type {}.".format(i))
        for j in range(per_num):
            generate_lessee_and_truck(i, count)
            count += 1

    print("Finish!")
