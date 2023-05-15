import modules.scripts as scripts
from scripts.start import start as extStart
import gradio as gr
import os

from modules import script_callbacks


def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as ui_component:
        extStart()
        return [(ui_component, "BooruGrabber", "booru_grabber")]

script_callbacks.on_ui_tabs(on_ui_tabs)