from django.test import TestCase
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser

from backpage.models import Rental, Lessee, User, Truck
from backpage.datas import LesseeDM, RentalDM

from channels import Group
from channels.tests import ChannelTestCase, HttpClient


class WebsocketTests(ChannelTestCase):

    rental_id = 1
    lessee_id = 1

    def setUp(self):
        RentalDM.clearData()
        LesseeDM.clearData()
        rental = User(account="1", name="rental", user_type=1, token="123")
        rental.save()
        # RentalDM.add(rental.id, 30.317636, 120.342755, "0")
        self.rental_id = rental.id

        Rental.objects.create(id=rental, position_x=30.317636, position_y=120.342755)
        lessee = User(account="2", name="lessee1", user_type=2, token="1111")
        lessee.save()
        # LesseeDM.add(lessee.id, 30.317379, 120.343004, "1")
        self.lessee_id = lessee.id
        lessee = Lessee(id=lessee, position_x=30.317379, position_y=120.343004, password="1", realname="1", ci="1")
        lessee.save()
        truck = Truck.objects.create(lessee=lessee, no="dsfa", car_type=2)

    def test_position_of_rental_receive_and_update(self):
        client = HttpClient()
        self.assertIsNone(RentalDM.getData(self.rental_id))

        client.send_and_consume('websocket.connect',
                                path='/{}/{}/'.format(self.rental_id, "123"))

        client.send_and_consume('websocket.receive',
                                text={"state": 99, "positionx": 99, "positiony": 99},
                                path='/{}/{}/'.format(self.rental_id, "123"))

        item = RentalDM.getData(self.rental_id)
        self.assertEqual(item.position_x,  99)
        self.assertEqual(item.position_y,  99)

    def test_position_of_lessee_receive_and_update(self):
        client = HttpClient()
        self.assertIsNone(LesseeDM.getData(self.lessee_id))

        client.send_and_consume('websocket.connect',
                                path='/{}/{}/'.format(self.lessee_id, "1111"))

        client.send_and_consume('websocket.receive',
                                text={"state": 99, "positionx": 99, "positiony": 99},
                                path='/{}/{}/'.format(self.lessee_id, "1111"))

        item = LesseeDM.getData(self.lessee_id)
        self.assertEqual(item.position_x,  99)
        self.assertEqual(item.position_y,  99)

    def test_position_of_rental_receive_and_update(self):
        client = HttpClient()
        self.assertIsNone(RentalDM.getData(self.rental_id))

        client.send_and_consume('websocket.connect',
                                path='/{}/{}/'.format(self.rental_id, "123"))

        client.send_and_consume('websocket.receive',
                                text={"state": 99, "positionx": 99, "positiony": 99},
                                path='/{}/{}/'.format(self.rental_id, "123"))

        item = RentalDM.getData(self.rental_id)
        self.assertEqual(item.position_x,  99)
        self.assertEqual(item.position_y,  99)

    def test_connnect_rental_disconnect(self):
        client = HttpClient()
        self.assertIsNone(RentalDM.getData(self.rental_id))

        client.send_and_consume('websocket.connect', path='/{}/{}/'.format(self.rental_id, "123"))

        self.assertEqual(RentalDM.getData(self.rental_id) is None,  False)
        self.assertEqual(list(RentalDM.listData())[0][0], self.rental_id)

        client.send_and_consume('websocket.disconnect', path='/{}/{}/'.format(self.rental_id, "123"))
        self.assertEqual(RentalDM.getData(self.rental_id) is None, True)

    def test_connnect_lessee_disconnect(self):
        client = HttpClient()
        self.assertIsNone(LesseeDM.getData(self.lessee_id))

        client.send_and_consume('websocket.connect', path='/{}/{}/'.format(self.lessee_id, "1111"))

        self.assertEqual(LesseeDM.getData(self.lessee_id) is None,  False)
        self.assertEqual(list(LesseeDM.listData())[0][0], self.lessee_id)

        client.send_and_consume('websocket.disconnect', path='/{}/{}/'.format(self.lessee_id, "1111"))
        self.assertEqual(RentalDM.getData(self.lessee_id) is None, True)

class NearLesseeTestCase(TestCase):
    rental_id = 1

    def setUp(self):
        RentalDM.clearData()
        LesseeDM.clearData()
        rental = User(account="1", name="rental", user_type=1, token="123")
        rental.save()
        RentalDM.add(rental.id, 30.317636, 120.342755, "0")
        self.rental_id = rental.id
        Rental.objects.create(id=rental, position_x=30.317636, position_y=120.342755)
        lessee = User(account="2", name="lessee1", user_type=2, token="1111")
        lessee.save()
        LesseeDM.add(lessee.id, 30.317379, 120.343004, "1")
        lessee = Lessee(id=lessee, position_x=30.317379, position_y=120.343004, password="1", realname="1", ci="1")
        lessee.save()
        truck = Truck.objects.create(lessee=lessee, no="dsfa", car_type=2)
        lessee = User(account="3", name="lessee2", user_type=2, token="1111")
        lessee.save()
        LesseeDM.add(lessee.id, 30.317715, 120.342891, "2")
        lessee = Lessee(id=lessee, position_x=30.317715, position_y=120.342891, password="1", realname="1", ci="1")
        lessee.save()
        truck = Truck.objects.create(lessee=lessee, no="dsfa", car_type=2)
        lessee = User(account="4", name="lessee3", user_type=2, token="1111")
        lessee.save()
        LesseeDM.add(lessee.id, 30.317734, 120.342562, "3")
        lessee = Lessee(id=lessee, position_x=30.317734, position_y=120.342562, password="1", realname="1", ci="1")
        lessee.save()
        truck = Truck.objects.create(lessee=lessee, no="dsfa", car_type=1)
        lessee = User(account="5", name="lessee4", user_type=2, token="1111")
        lessee.save()
        LesseeDM.add(lessee.id, 40.317379, 110.343004, "4")
        lessee = Lessee(id=lessee, position_x=40.317379, position_y=110.343004, password="1", realname="1", ci="1")
        lessee.save()
        truck = Truck.objects.create(lessee=lessee, no="dsfa", car_type=1)
        lessee = User(account="6", name="lessee5", user_type=2, token="1111")
        lessee.save()
        LesseeDM.add(lessee.id, 30.317379, 20.343004, "5")
        Lessee.objects.create(id=lessee, position_x=30.317379, position_y=20.343004, password="1", realname="1", ci="1")



    def test_get_near_lessees_list_success_with_query(self):
        response = self.client.get(
            "/rent/{}/near_lessees/?token=123&positionx=30.317636&positiony=120.342755&limit=40&cartype=2".format(self.rental_id))
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

    def test_get_near_lessees_list_success_without_query_and_data(self):
        RentalDM.deleteData(self.rental_id)
        response = self.client.get(
            "/rent/{}/near_lessees/?token=123&limit=40".format(self.rental_id))
        self.assertEqual(response.status_code, 200)
        stream = BytesIO(response.content)
        result = JSONParser().parse(stream)
        self.assertEqual(len(result), 0)

    def test_get_near_lessees_list_forbidden(self):
        response = self.client.get(
            "/rent/{}/near_lessees/?positoinx=30.317636&positiony=120.342755&limit=40".format(self.rental_id))
        self.assertEqual(response.status_code, 403)

    def test_get_near_lessees_list_not_found(self):
        response = self.client.get(
            "/rent/{}/near_lessees/?token=123&positoinx=30.317636&positiony=120.342755&limit=40".format(21343421))
        self.assertEqual(response.status_code, 404)
