from backpage.models import (
    Orders,
    User,
    Truck,
    Rental,
    Lessee,
)
from django.utils import timezone
import time, datetime

def work():
    nowtime = timezone.now()
    not_timeout = nowtime - datetime.timedelta(minutes=2)
    timeout = nowtime - datetime.timedelta(minutes=17)
    timeup = nowtime + datetime.timedelta(minutes=2)
    in_distant1 = (30.317715, 120.342891)
    in_distant2 = (30.313715, 120.342891)
    out_distant = (99, 99)
    true_car_type = 2
    false_car_type = 1
    true_status = 1
    false_status = 3
    try:
        rental = Rental.objects.get(id=2)
    except Rental.DoesNotExist:
        rental = User(account="1", name="rental", user_type=1, token="123")
        rental.save()
        rental = Rental(id=rental, position_x=30.317636, position_y=120.342755)
        rental.save()
    try:
        lessee = Lessee.objects.get(id=999)
    except Lessee.DoesNotExist:
        lessee = User(id=999, account="1", name="lessee", user_type=2, token="ws123")
        lessee.save()
        lessee = Lessee(id=lessee, position_x=30.317636, position_y=120.342755)
        lessee.save()
        truck = Truck.objects.create(lessee=lessee, no="dsfa", car_type=2)

    # orders
    ors = Orders(rental=rental, starttime=not_timeout, trucktype=true_car_type,
                            startplacex=in_distant1[0], startplacey=in_distant1[1],
                            status = true_status, startplace="a", fee=12, score=0, remark="remark")
    ors.save()
    ors.starttime = not_timeout
    ors.save()
    ors = Orders(rental=rental, starttime=not_timeout, trucktype=true_car_type,
                            startplacex=in_distant2[0], startplacey=in_distant2[1],
                            status = true_status, startplace="a", fee=12, score=0, remark="remark")
    ors.save()
    ors.starttime = not_timeout
    ors.save()
    ors = Orders(rental=rental, starttime=timeout, trucktype=true_car_type,
                            startplacex=in_distant2[0], startplacey=in_distant2[1],
                            status = true_status, startplace="a", fee=12, score=0, remark="remark")
    ors.save()
    ors.starttime = timeout
    ors.save()
    ors = Orders(rental=rental, starttime=timeup, trucktype=true_car_type,
                            startplacex=in_distant2[0], startplacey=in_distant2[1],
                            status = true_status, startplace="a", fee=12, score=0, remark="remark")
    ors.save()
    ors.starttime = timeup
    ors.save()
    ors = Orders(rental=rental, starttime=not_timeout, trucktype=false_car_type,
                            startplacex=in_distant1[0], startplacey=in_distant1[1],
                            status = true_status, startplace="a", fee=12, score=0, remark="remark")
    ors.save()
    ors.starttime = not_timeout
    ors.save()
    ors = Orders(rental=rental, starttime=not_timeout, trucktype=true_car_type,
                            startplacex=out_distant[0], startplacey=out_distant[1],
                            status = true_status, startplace="a", fee=12, score=0, remark="remark")
    ors.save()
    ors.starttime = not_timeout
    ors.save()
    ors = ors = Orders(rental=rental, starttime=not_timeout, trucktype=true_car_type,
                            startplacex=in_distant1[0], startplacey=in_distant1[1],
                            status = false_status, startplace="a", fee=12, score=0, remark="remark")
    ors.save()
    ors.starttime = not_timeout
    ors.save()
