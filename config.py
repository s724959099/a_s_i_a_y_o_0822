from starlette.config import Config
import os

app_path = os.path.dirname(os.path.realpath(__file__))
# config = Config(os.path.join(app_path, '.env'))
config = Config('.env')
