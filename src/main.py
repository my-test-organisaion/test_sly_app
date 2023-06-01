import os
from dotenv import load_dotenv
import supervisely as sly
from supervisely.app.widgets import Button, Container, Button, Text


load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

team_id = sly.env.team_id()

api = sly.Api()

stop_button = Button("stop")
print_button = Button("print")

buttons = []
for i in range(50):
    b = Button(f"button {i}")
    b.loading = True
    buttons.append(b)

layout = Container(
    widgets=[Text("hello, I'm branch 3"), stop_button, print_button, *buttons]
)
app = sly.Application(layout=layout)

@stop_button.click
def b_stop():
    app.stop()
    for b in buttons:
        b.loading = False

@print_button.click
def b_print():
    print("print clicked")
