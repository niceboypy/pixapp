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
from param_panel_ui import Info_and_preview 
from api_panel_ui import Integrated_api_bar
from custom_behaviour import Behaviour
from mixins import Fetch_mixin
import os

from par_values import Values
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
        



class PixApp(App):
    def build_config(self, config):
        self.myconfig = config
        config.setdefaults('General', {'path': Values.def_path})
        config.setdefaults('General', {'quantity':Values.quantity})
        config.setdefaults('General', {'lang':Values.language[0]})

    def build_settings(self, settings):

        #allowed values for type field below:
        #bool, numeric, string, path, title
        settings.add_json_panel("Settings", self.config, data="""
            [
            {"type": "string",
            "title": "Default Path",
            "section": "General",
            "key": "path"
                },
            {"type": "numeric",
            "title": "Default file quantity to fetch",
            "section": "General",
            "key": "quantity"
                },
            {"type": "string",
            "title": "Language used for search",
            "section": "General",
            "key": "lang"
                }
            ]""")
        
    def build(self):
        config = PixApp.get_running_app().config
        update_path=config.getdefault("General", "path", Values.def_path)
        update_quantity=config.getdefault("General", "quantity", Values.quantity)
        update_language=config.getdefault("General", "lang", Values.language[0])

        #The values are updated before anything that uses the default values are touched
        #during the instantiation of the Integration() panel
        self.update_values(update_path, 
                          update_quantity,
                          update_language
                          )

        main = Integration(orientation='vertical')
        main.paramholder.get('settings').bind(on_press=lambda*_: self.open_settings())
        return main
    
    def update_values(self, *objs):
        path, quantity, language = objs

        #"Two type of update techniques"
        #"Spin values in a list and just override the default values"
        def override(value_to_rplc, newvalue, Path=False):
            if Path:
                if os.path.exists(newvalue):
                    setattr(Values, value_to_rplc, newvalue)
                else:
                    try:
                        os.makedirs(newvalue)
                    except:
                        #may be permission denied
                        pass
                    else:
                        setattr(Values, value_to_rplc, newvalue)
                return None
            setattr(Values, value_to_rplc, newvalue)

        def spin_update(value_to_rplc, newvalue):
            """spin the list to update default values"""
            list_values = getattr(Values, value_to_rplc) 
            if (len(newvalue) > 2): newvalue=newvalue[:2]
            if newvalue in list_values:
                index = list_values.index(newvalue)
                list_values[0], list_values[index]=list_values[index], list_values[0]
                setattr(Values, value_to_rplc, list_values)

        override('def_path', path, Path=True)
        override('quantity', quantity)
        spin_update('language', language)
        

if __name__ == '__main__':
    PixApp().run()