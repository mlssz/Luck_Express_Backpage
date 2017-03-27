from backpage.models import (
    Orders,
    User,
    Truck,
    Rental,
    Lessee,
)
from django.utils import timezone
import random
import time, datetime

def work(num):
    nowtime = timezone.now()
    not_timeout = nowtime - datetime.timedelta(minutes=2)
    in_distant1 = (30.317715, 120.342891)
    in_distant2 = (30.313715, 120.342891)
    car_type = 2
    status = [0, 1]

    try:
        rental = Rental.objects.get(id=2)
    except Rental.DoesNotExist:
        rental = User(account="1", name="rental", user_type=1, token="123")
        rental.save()
        rental = Rental(id=rental, position_x=30.317636, position_y=120.342755)
        rental.save()

    # orders

    for i in range(num):
        ors = Orders(rental=rental, starttime=not_timeout, trucktype=car_type,
                                startplacex=in_distant1[0], startplacey=in_distant1[1],
                                status = status[0], startplace="a", fee=random.randrange(200), score=random.randrange(5), remark="remark")
        ors.save()
        ors.starttime = not_timeout
        ors.save()
        ors = Orders(rental=rental, starttime=not_timeout, trucktype=car_type,
                                startplacex=in_distant2[0], startplacey=in_distant2[1],
                                status = status[1], startplace="a", fee=random.randrange(200), score=random.randrange(5), remark="remark")
        ors.save()
        ors.starttime = not_timeout
        ors.save()
