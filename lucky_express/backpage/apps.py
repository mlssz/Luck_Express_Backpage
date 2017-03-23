from django.apps import AppConfig

from backpage.utils import setInterval
from backpage.loop_jobs import boardcast_orders

class BackpageConfig(AppConfig):
    name = 'backpage'

BOARDCAST = True

def toggle_boardcast():
    global BOARDCAST
    BOARDCAST = False

def _boardcast_orders():
    boardcast_orders()
    return BOARDCAST

setInterval(1, _boardcast_orders, [])
