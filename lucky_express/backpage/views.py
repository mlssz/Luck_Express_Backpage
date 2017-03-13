import math, functools
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from backpage.serializers import LesseeSerializer
from backpage.models import Lessee, Rental

degree = math.pi / 180

class NearLesseesList(APIView):
    """
    List all near lessees
    """
    def is_near_lessee(self, limit, distance) -> "bool":
        """Compare value of limit and the distance between render and lessee."""

        return 0 <= distance <= limit

    def compute_distance(self, rental: "Rental", lessee: "Lessee") -> "float":
        """Compute distance between rental and lessee."""
        x1, y1 = rental.position_x, rental.position_y
        x2, y2 = lessee.position_x, lessee.position_y

        distance = 6378.138 * 2 * math.asin(math.sqrt(
            math.pow(math.sin((x1 * degree -x2 * degree) / 2), 2)
            + math.cos(x1 * degree) * math.cos(x2 * degree)
            * math.pow(math.sin((y1 * degree - y2 * degree) / 2), 2)
        )) * 1000

        return distance

    def get_object(self, pk):
        """Get object and check the permissions of user."""
        obj = get_object_or_404(Rental, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, pk, format=None):
        """find all lessees near the rental."""
        rental = self.get_object(pk)

        car_type = int(request.GET.get("cartype", 2))
        position_x = request.GET.get("positionx", None)
        position_y = request.GET.get("positiony", None)
        limit = float(request.GET.get("limit", 20))
        rental.position_x = rental.position_x if position_x is None else float(position_x)
        rental.position_y = rental.position_y if position_y is None else float(position_y)

        lessee_tuple = ((l, self.compute_distance(rental, l))
                        for l in Lessee.objects.filter(truck__car_type=car_type))
        lessee_tuple = list(filter(lambda x: self.is_near_lessee(limit, x[1]), lessee_tuple))
        lessees = (lt[0] for lt in lessee_tuple)

        data = LesseeSerializer(lessees, many=True).data
        for i in range(len(data)):
            data[i]["user"] = data[i].pop("id")
            data[i]["distance"] = lessee_tuple[i][1]

        return Response(data)
