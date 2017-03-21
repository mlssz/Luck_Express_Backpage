import functools
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from backpage.serializers import LesseeSerializer
from backpage.models import Lessee, Rental

from backpage.datas import LesseeDM, RentalDM
from backpage.utils import compute_distance

class NearLesseesList(APIView):
    """
    List all near lessees
    """
    def is_near_lessee(self, limit, distance) -> "bool":
        """Compare value of limit and the distance between render and lessee."""

        return 0 <= distance <= limit

    def compute_distance(self, rental_position, lessee_id):
        lessee_item = LesseeDM.getData(lessee_id)
        if lessee_item is None:
            return -1

        return compute_distance(rental_position, (lessee_item.position_x, lessee_item.position_y))

    def get_object(self, pk):
        """Get object and check the permissions of user."""
        obj = get_object_or_404(Rental, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, pk, format=None):
        """find all lessees near the rental."""
        rental = self.get_object(pk)
        rental_item = RentalDM.getData(int(pk))

        car_type = int(request.GET.get("cartype", 2))
        position_x = request.GET.get("positionx", None)
        position_y = request.GET.get("positiony", None)
        limit = float(request.GET.get("limit", 20))

        if rental_item is None and (position_y is None or position_x is None):
            return Response([])

        px = rental_item.position_x if position_x is None else float(position_x)
        py = rental_item.position_y if position_y is None else float(position_y)

        lessee_tuple = ((l, self.compute_distance((px, py), l.id.id))
                        for l in Lessee.objects.filter(truck__car_type=car_type))
        lessee_tuple = list(filter(lambda x: self.is_near_lessee(limit, x[1]), lessee_tuple))
        lessees = (lt[0] for lt in lessee_tuple)

        data = LesseeSerializer(lessees, many=True).data
        for i in range(len(data)):
            data[i]["user"] = data[i].pop("id")
            data[i]["distance"] = lessee_tuple[i][1]

        return Response(data)
