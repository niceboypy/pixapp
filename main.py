#!/usr/bin/env python3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.base import EventLoop
from kivy.config import Config
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.label import Label

from param_panel_ui import param_holder
from api_panel_ui import Integrated_api_bar

Config.set('input', 'mouse', 'mouse, disable_multitouch')
from kivy.uix.spinner import Spinner

# from kivy.uix.button import Button
# from kivy.storage.jsonstore import JsonStore


# tips 
# user_data = JsonStore("user_data.json")
# on_press: Clock.schedule_once(lambda *_: setattr(api_input, 'focus', True), 0.1)

class Flexible_Input(TextInput):
    def on_touch_down(self, touch):
        super(Flexible_Input,self).on_touch_down(touch)
        if touch.button == 'right':
            pos = self.to_local(*self._long_touch_pos, relative=False)
            self._show_cut_copy_paste(
                pos, EventLoop.window, mode='copy')


class Integration(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.add_widget(Apiholder(size_hint_y= .3))
        self.add_widget(Paramholder(size_hint_y= 1))


class Apiholder(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Integrated_api_bar())


class Paramholder(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation='horizontal'
        change = [('spinner', 
                    {'values':('uno', 'dos', 'tres', 'quadro', 'sinco')
                    }
                  )
                ]
        self.left_layout = BoxLayout(size_hint_x=0.5, orientation='vertical')
        self.right_layout = BoxLayout(size_hint_x=0.5, orientation='vertical')

        self.left_layout.add_widget(param_holder(change))
        self.left_layout.add_widget(param_holder(change))
        self.left_layout.add_widget(param_holder(change))
        self.left_layout.add_widget(param_holder(change))
        self.left_layout.add_widget(param_holder(change))
        self.left_layout.add_widget(param_holder(change))

        self.right_layout.add_widget(Label(text='somethinghere', size_hint_x=0.5))

        self.add_widget(self.left_layout)
        self.add_widget(self.right_layout)




        
        



class pixapp(App):
    def build(self):
        
        return Integration(orientation='vertical')

if __name__ == '__main__':
    pixapp().run()