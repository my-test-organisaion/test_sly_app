import os
from dotenv import load_dotenv
import supervisely as sly
from supervisely.app.widgets import Text, Container


load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

arg1 = os.environ.get("arg1.value")
arg2 = os.environ.get("arg2.value")
arg3 = os.environ.get("arg3.value")
arg4 = os.environ.get("arg4.checked")
arg5 = os.environ.get("arg5.value")
arg6 = os.environ.get("arg6.value")

layout = Container(
    widgets=[
        Text("Hello World"),
        Text(arg1),
        Text(arg2),
        Text(arg3),
        Text(arg4),
        Text(arg5),
        Text(arg6),
    ]
)

app = sly.Application(layout=layout)
