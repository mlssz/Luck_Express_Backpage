"""
This file defines function which used to do loop job.
"""
import datetime

from django.utils import timezone
from rest_framework.renderers import JSONRenderer

from backpage.datas import RentalDM, LesseeDM
from backpage.models import Orders, Lessee
from backpage.utils import compute_distance
from backpage.serializers import OrderSerializer

def boardcast_orders(distance=5000):
    # not timeout(15 minuts) and not be accepted
    now = timezone.now()
    valid_orders = Orders.objects.exclude(
        starttime__gte=now
    ).filter(
        starttime__gte=now - datetime.timedelta(minutes=15),
        lessee__isnull=True,
        status__in=[0,1,2,6]
    )
    lessees = list(LesseeDM.listData())

    for item in lessees:
        try:
            l = Lessee.objects.get(id=item[0])
            l_orders = valid_orders.filter(trucktype=l.truck.car_type)
            l_position = (item[1].position_x, item[1].position_y)
            orders_tuple = ((o, compute_distance(l_position, (o.startplacex, o.startplacey)))
                           for o in l_orders)
            orders_tuple = list(filter(lambda x: 0<=x[1]<=distance, orders_tuple))
            l_orders = (ot[0] for ot in orders_tuple)

            data = OrderSerializer(l_orders, many=True).data
            for i in range(len(data)):
                data[i]["starttime"] = data[i]["starttime"][:-1]
                data[i]["rental"]["account"] = data[i]["rental"].pop("id")
                data[i]["distance"] = orders_tuple[i][1]

            item[1].channel.send({
                "text": JSONRenderer().render({"action": 1, "orders": data}).decode()
            })
        except Lessee.DoesNotExist:
            LesseeDM.deleteData(item[0])
            print("Dose not found lessee {}".format(item[0]))
        except Exception as err:
            print(err)
