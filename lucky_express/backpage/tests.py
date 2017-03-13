from django.test import TestCase
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser

from backpage.models import Rental, Lessee, User, Truck

class NearLesseeTestCase(TestCase):
    rental_id = 1

    def setUp(self):
        rental = User(account="1", name="rental", user_type=1, token="123")
        rental.save()
        self.rental_id = rental.id
        Rental.objects.create(id=rental, position_x=30.317636, position_y=120.342755)
        lessee = User(account="2", name="lessee1", user_type=2, token="1111")
        lessee.save()
        lessee = Lessee(id=lessee, position_x=30.317379, position_y=120.343004, password="1", realname="1", ci="1")
        lessee.save()
        truck = Truck.objects.create(lessee=lessee, no="dsfa", car_type=2)
        lessee = User(account="3", name="lessee2", user_type=2, token="1111")
        lessee.save()
        lessee = Lessee(id=lessee, position_x=30.317715, position_y=120.342891, password="1", realname="1", ci="1")
        lessee.save()
        truck = Truck.objects.create(lessee=lessee, no="dsfa", car_type=2)
        lessee = User(account="4", name="lessee3", user_type=2, token="1111")
        lessee.save()
        lessee = Lessee(id=lessee, position_x=30.317734, position_y=120.342562, password="1", realname="1", ci="1")
        lessee.save()
        truck = Truck.objects.create(lessee=lessee, no="dsfa", car_type=1)
        lessee = User(account="5", name="lessee4", user_type=2, token="1111")
        lessee.save()
        lessee = Lessee(id=lessee, position_x=40.317379, position_y=110.343004, password="1", realname="1", ci="1")
        lessee.save()
        truck = Truck.objects.create(lessee=lessee, no="dsfa", car_type=1)
        lessee = User(account="6", name="lessee5", user_type=2, token="1111")
        lessee.save()
        Lessee.objects.create(id=lessee, position_x=30.317379, position_y=20.343004, password="1", realname="1", ci="1")

    def test_get_near_lessees_list_success_with_query(self):
        response = self.client.get(
            "/rent/{}/near_lessees/?token=123&positoinx=30.317636&positiony=120.342755&limit=40&cartype=2".format(self.rental_id))
        self.assertEqual(response.status_code, 200)
        stream = BytesIO(response.content)
        result = JSONParser().parse(stream)
        print(result)
        self.assertEqual(len(result), 2)

    def test_get_near_lessees_list_success_without_query(self):
        response = self.client.get(
            "/rent/{}/near_lessees/?token=123&limit=40".format(self.rental_id))
        self.assertEqual(response.status_code, 200)
        stream = BytesIO(response.content)
        result = JSONParser().parse(stream)
        self.assertEqual(len(result), 2)

    def test_get_near_lessees_list_forbidden(self):
        response = self.client.get(
            "/rent/{}/near_lessees/?positoinx=30.317636&positiony=120.342755&limit=40".format(self.rental_id))
        self.assertEqual(response.status_code, 403)

    def test_get_near_lessees_list_not_found(self):
        response = self.client.get(
            "/rent/{}/near_lessees/?token=123&positoinx=30.317636&positiony=120.342755&limit=40".format(21343421))
        self.assertEqual(response.status_code, 404)
