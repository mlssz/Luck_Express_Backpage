"""Routing.py defines a routing scheme, which points to a list containing the routing settings."""

from channels.routing import route_class
from backpage.consumers import PositionsConsumer

channel_routing = [
    route_class(PositionsConsumer, path=r"^/(?P<pk>[0-9]+)/(?P<token>\w+)/?"),
]
