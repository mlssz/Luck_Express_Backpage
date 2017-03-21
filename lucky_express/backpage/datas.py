"""
datas.py store the data of user

rental data include:
    channel
    position_x
    position_y
    orders:
        order - bidders

lessee data include:
    channel
    position_x
    position_y
"""
from threading import Lock
from collections import namedtuple

RentalDataItem = namedtuple("RentalDataItem", ["position_x", "position_y", "channel", "orders"])
LesseeDataItem = namedtuple("LesseeDataItem", ["position_x", "position_y", "channel"])

class BaseDataManager():
    "Base Data Manager."

    def __init__(self, lock, datas):
        self.lock = lock
        self.datas = datas

    def getData(self, uid):
        with self.lock:
            item = self.datas.get(uid, None)

        return item

    def putData(self, uid, item):
        with self.lock:
            self.datas[uid] = item

    def deleteData(self, uid):
        with self.lock:
            item = self.datas.pop(uid, None)

        return item

    def listData(self):
        with self.lock:
            data_iterator = self.datas.items()
        return data_iterator

    def clearData(self):
        with self.lock:
            self.datas.clear()

class RentalDataManager(BaseDataManager):
    "Data Manager of datas of rentals."
    lock = Lock()
    datas = dict() # uid : item

    def __init__(self):
        super(RentalDataManager, self).__init__(self.lock, self.datas)

    def update(self, uid, position=None, channel=None, orders=[]):
        item = self.getData(uid)
        if item is None:
            return item

        px, py = (item.position_x, item.position_y) if position is None else position
        channel = item.channel if channel is None else channel
        orders = item.orders if len(orders) <= 0 else orders
        return self.add(uid, px, py, channel, orders)

    def add(self, uid, px, py, channel, orders=[]):
        item = RentalDataItem(px, py, channel, orders)
        self.putData(uid, item)

        return item

class LesseeDataManager(BaseDataManager):
    "Data Manager of datas of Lessee."
    lock = Lock()
    datas = dict() # uid : item

    def __init__(self):
        super(LesseeDataManager, self).__init__(self.lock, self.datas)

    def update(self, uid, position=None, channel=None):
        item = self.getData(uid)
        if item is None:
            return item

        px, py = (item.position_x, item.position_y) if position is None else position
        channel = item.channel if channel is None else channel
        return self.add(uid, px, py, channel)

    def add(self, uid, px, py, channel):
        item = LesseeDataItem(px, py, channel)
        self.putData(uid, item)

        return item

LesseeDM = LesseeDataManager()
RentalDM = RentalDataManager()
