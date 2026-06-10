from mangum import Mangum

from webex_a2a_hello_world.app import app

handler = Mangum(app, lifespan="off")
