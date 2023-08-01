import json
import os
from pathlib import Path
from dotenv import load_dotenv
import supervisely as sly
from supervisely.app.widgets import Text, Container, Button, Checkbox, ReloadableArea, Field, InputNumber, OneOf, Switch, Card, Image


load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

# text_1 = Text("Hello World")
# text_2 = Text("I'm Subapp")
# text_3 = Text("hello, I'm updated 2")
# times_clicked = 0
# reload_n = 0

# texts = [text_1, text_2, text_3]
# button = Button("Button")
# checkbox_text = Text("Not Checked")
# checkbox = Checkbox(checkbox_text)

# reload = ReloadableArea(content=text_1)
# reload_field = Field(reload, "reloadable")
# reload_btn = Button("change reloadable widget")

# layout = Container(widgets=[*texts, button, checkbox, reload_field, reload_btn])

# app = sly.Application(layout=layout)

# text_1.text = "Changed"

# @button.click
# def on_click():
#     global texts
#     global times_clicked
#     times_clicked += 1
#     for i in range(10):
#         for j, text in enumerate(texts):
#             text.text = f"text_{j+1}_changed_{i+1}_clicked_{times_clicked}"


# @checkbox.value_changed
# def checkbox_changed_cb(value):
#     # checkbox_text.text = "Checked" if value else "Not Checked"
#     print("zxc")


# @reload_btn.click
# def reload_btn_cb():
#     global reload_n
#     if reload_n == 0:
#         reload.set_content = text_2
#         reload_n = 1
#     else:
#         reload.set_content = text_1
#         reload_n = 0
#     reload.reload()


# btn1 = Button("Button 1")
# text1 = Text("Text 1")

# layout = Container(widgets=[btn1, text1])

# app = sly.Application(layout=layout)

# @btn1.click
# def btn1_cb():
#     n = 1000000000000
#     for i in range(n):
#         x = i * i
#         if x % 1000000000000 == 0:
#             text1.text = str(i)

# add_node_btn = Button("Add Node")

# input_number = InputNumber()

# on = Text("on")
# off = Text("off")

# switch = Switch(off_content=off, on_content=on)
# one_of = OneOf(switch)

# nodes = [
#     NodesFlow.Node(
#         id="node_1",
#         name="Node 1",
#         options=[
#             NodesFlow.Node.Option(
#                 name="option_1",
#                 widget=Checkbox("Option 1")
#             ),
#             NodesFlow.Node.Option(
#                 name="option_2",
#                 widget=input_number
#             )
#         ],
#         inputs=[
#             NodesFlow.Node.Input("input_1", "Input 1"),
#             NodesFlow.Node.Input("input_2", "Input 2")
#         ],
#         outputs=[
#             NodesFlow.Node.Output("output_1", "Output 1"),
#         ]
#     ),
#     NodesFlow.Node(
#         id="node_2",
#         name="Node 2",
#         options=[
#             NodesFlow.Node.Option(
#                 name="option_1",
#                 widget=switch
#             ),
#             NodesFlow.Node.Option(
#                 name="option_2",
#                 widget=one_of
#             )
#         ],
#         inputs=[
#             NodesFlow.Node.Input("input_1", "Input 1"),
#             NodesFlow.Node.Input("input_2", "Input 2")
#         ],
#         outputs=[
#             NodesFlow.Node.Output("output_1", "Output 1"),
#         ]
#     )
# ]

# zxc_btn = Button("zxc")
# @zxc_btn.click
# def zxc_btn_cb():
#     print(input_number.get_value())

# nodes_flow = NodesFlow(nodes=nodes)

# print(json.dumps(nodes_flow.get_json_state(), indent=2))

# layout = Container(widgets=[add_node_btn, nodes_flow, zxc_btn])


# button = Button("change widget")

# reloadable_widgets = [
#     Text("Text 1"),
#     Checkbox("Checkbox 1"),
#     Field(content=InputNumber(), title="Field with InputNumber"),
# ]

# current_widget_idx = 0
# reloadable = ReloadableArea(content=reloadable_widgets[current_widget_idx])

# stop_btn = Button("stop app", button_type="danger")

# @button.click
# def change_widget():
#     global current_widget_idx
#     current_widget_idx = (current_widget_idx + 1) % len(reloadable_widgets)
#     reloadable.set_content(reloadable_widgets[current_widget_idx])
#     reloadable.reload()


# layout = Container(widgets=[button, reloadable, stop_btn])

# app = sly.Application(layout=layout)

# @stop_btn.click
# def stop_app():
#     app.stop()

# inpnum = InputNumber()

# layout = Container(widgets=[inpnum])

# app = sly.Application(layout=layout)

# @inpnum.value_changed
# def inpnum_cb(value):
#     print(value)


btn = Button("download local")
btn2 = Button("download url")

static_dir = Path("subapp/src/static")
local_img_url = "/static/flower.jpg"
img_url = "https://img.freepik.com/free-photo/close-up-delicate-pink-flower_23-2147623042.jpg?w=2000"


app = sly.Application(layout=Container(widgets=[btn, btn2]), static_dir=static_dir)

def download(url: str):
    if url.startswith("http"):
        path = sly.fs.download(url, r"C:\Users\User\Supervisely\test_app\subapp\src\saved\img.jpg")
        return path
    else:
        static_dir = Path(app.get_static_dir())
        filepath = url.lstrip("/").removeprefix("static/")
        path = static_dir.joinpath(filepath).absolute()
        return path

@btn.click
def btn_cb():
    path = download(local_img_url)
    print(path)

@btn2.click
def btn2_cb():
    path = download(img_url)
    print(path)