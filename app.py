import falcon.asgi
import logging

from api.operation import Operation
from api.docs import Docs

logging.basicConfig(
    level=2,
    format="%(asctime)-15s %(levelname)-8s %(message)s"
)

def create_app():

    app = falcon.asgi.App(middleware=[])

    operation = Operation()
    docs = Docs()

    app.add_route('/operations', operation, suffix='operations')
    app.add_route('/docs', docs, suffix='docs')
    app.add_route('/template', docs, suffix='template')

    return app

app = create_app()