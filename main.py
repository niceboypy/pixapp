#!/usr/bin/env python3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.base import EventLoop
from kivy.config import Config
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from custom_widgets import Common_button, Flexible_Input, Plain_button
from param_panel_ui import Info_and_preview#dropdown_holder, Img_query_holder, Img_search_preview
from api_panel_ui import Integrated_api_bar
from custom_behaviour import Behaviour
from mixins import Fetch_mixin

from kivy.uix.spinner import Spinner
from kivy.uix.bubble import Bubble
Config.set('input', 'mouse', 'mouse, disable_multitouch')
from kivy.clock import Clock

# from kivy.uix.button import Button
# from kivy.storage.jsonstore import JsonStore

# on_press: Clock.schedule_once(lambda *_: setattr(api_input, 'focus', True), 0.1)

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


class Integration(BoxLayout, Behaviour):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.padding="10dp"

        self.progress = ProgressBar(max=100, size_hint_y=0.01)
        self.apiholder = Apiholder(size_hint_y= .2)#contain self.interface
        self.paramholder = Paramholder(size_hint_y= 1)#contain self.interface

        self.add_widget(self.progress)
        self.add_widget(self.apiholder)
        self.add_widget(self.paramholder)

        self.add_behaviour()

class Apiholder(BoxLayout, Fetch_mixin):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.integrated_api_bar=Integrated_api_bar()
        self.interface=self.integrated_api_bar.interface

        self.add_widget(self.integrated_api_bar)


class Paramholder(BoxLayout, Fetch_mixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Info_and_preview=Info_and_preview()
        self.interface = self.Info_and_preview.interface
        self.add_widget(self.Info_and_preview)
        



class pixapp(App):
    def build(self):
        
        return Integration(orientation='vertical')

if __name__ == '__main__':
    pixapp().run()