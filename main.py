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

from param_panel_ui import dropdown_holder, Img_query_holder, Img_preview_holder
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

    def on_touch_down(self, touch):
        super(Flexible_Input,self).on_touch_down(touch)
        if touch.button == 'right':
            pos = super(Flexible_Input,self).to_local(*self._long_touch_pos, relative=True)
            self._show_cut_copy_paste(
                pos, EventLoop.window, mode='copy')
            


class Integration(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
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
        self.orientation='horizontal'
        change = [('spinner', 
                    {'values':('uno', 'dos', 'tres', 'quadro', 'sinco')
                    }
                  )
                ]
        self.left_layout = BoxLayout(size_hint_x=0.5, orientation='vertical')
        self.right_layout = BoxLayout(size_hint_x=0.5, orientation='vertical')

        self.left_layout.add_widget(dropdown_holder(change))
        self.left_layout.add_widget(dropdown_holder(change))
        self.left_layout.add_widget(dropdown_holder(change))
        self.left_layout.add_widget(dropdown_holder(change))
        self.left_layout.add_widget(dropdown_holder(change))
        

        minimum_height=[(
            'Input', 
            {'hint_text':'leave for default'}),
            ('Label',
            {'text':'Minimum width: '})
            ]

        quantity_panel=[(
            'Input', 
            {'hint_text':'max: 5000 imgs/hr'}),
            ('Label',
            {'text':'Quantity (def. 100): '})
            ]

        image_search=[(
            'Input',
            {'hint_text':'Fetch Imgs e.g cars'}),
            ('Label',
            {'text': 'Fetch: '}),
        ]

        multisearch=[(
            'Input',
            {'hint_text':'separate using ","'}),
            ('Label',
            {'text': 'Multisearch: '})
        ]


        
        self.left_layout.add_widget(Img_query_holder())
        self.left_layout.add_widget(Img_query_holder(minimum_height))
        self.left_layout.add_widget(Img_query_holder(quantity_panel))

        self.right_layout.add_widget(Img_query_holder(image_search, size_hint_y=0.15))
        self.right_layout.add_widget(Img_query_holder(multisearch, size_hint_y=0.15))
        self.right_layout.add_widget(Img_preview_holder(size_hint_y=0.8))
        

        self.add_widget(self.left_layout)
        self.add_widget(self.right_layout)
        self.add_widget(Label(size_hint_x=0.01))



class pixapp(App):
    def build(self):
        
        return Integration(orientation='vertical')

if __name__ == '__main__':
    pixapp().run()