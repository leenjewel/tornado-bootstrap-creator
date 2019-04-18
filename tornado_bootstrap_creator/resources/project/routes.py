
from {{ package }}.handler import *

routes = (
    (r"^[/]?$", IndexHandler),
    (r"^/index[/]?$", IndexHandler),
    (r"^/login[/]?$", LoginHandler),
    (r"^/logout[/]?$", LogoutHandler),
    {% for route, handler in routes.items() %}
    (r"^{{ route }}[/]?$", {{ handler }}),
    {% endfor %}
)