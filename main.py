#!/usr/bin/env python3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.base import EventLoop
from kivy.config import Config
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar

from param_panel_ui import Info_and_preview#dropdown_holder, Img_query_holder, Img_search_preview
from api_panel_ui import Integrated_api_bar

from kivy.uix.spinner import Spinner
from kivy.uix.bubble import Bubble

Config.set('input', 'mouse', 'mouse, disable_multitouch')
from kivy.clock import Clock

# from kivy.uix.button import Button
# from kivy.storage.jsonstore import JsonStore

# on_press: Clock.schedule_once(lambda *_: setattr(api_input, 'focus', True), 0.1)

class Flexible_Input(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # def on_touch_down(self, touch):
        #     super(Flexible_Input,self).on_touch_down(touch)
        #     if touch.button == 'right':
        #         # pos = super().to_local(*self._long_touch_pos, relative=False)
        #         pos = self.parse(str(touch))
        #         self._show_cut_copy_paste(
        #             pos, EventLoop.window, mode='copy')

        # def parse(self, cordinfo):
        #     pos = cordinfo[cordinfo.rfind('pos'):]
        #     pos =[int(float(x.strip())) for x in pos[pos.find('(')+1: pos.find(')')].split(',')]
        #     return tuple(pos)

            # pos = cordinfo.split()[2]
            # pos = pos[pos.find('(')+1: pos.find(')')].split()
            # pos = tuple(float(x) for x in pos)
            # print(pos)


class Integration(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.padding="10dp"
        progress = ProgressBar(max=100, size_hint_y=0.01)

        self.add_widget(progress)
        self.add_widget(Apiholder(size_hint_y= .2))
        progress.value=50
        self.add_widget(Paramholder(size_hint_y= 1))


class Apiholder(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Integrated_api_bar())


class Paramholder(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Info_and_preview())
        



class pixapp(App):
    def build(self):
        
        return Integration(orientation='vertical')

if __name__ == '__main__':
    pixapp().run()