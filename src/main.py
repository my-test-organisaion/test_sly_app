import os
from dotenv import load_dotenv
import supervisely as sly
from supervisely.app.widgets import Text, Container


load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

layout = Container(widgets=[Text("Hello World")])

app = sly.Application(layout=layout)
