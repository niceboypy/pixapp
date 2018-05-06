from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


class Common_button(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Flexible_Input(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
