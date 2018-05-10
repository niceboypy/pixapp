from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.boxlayout import BoxLayout
from par_values import Values
import os
from kivy.uix.button import Button




class Common_button(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Plain_button(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Flexible_Input(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class save_dialog(BoxLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation='vertical'
        widget_props={
            'size_hint_y': 0.8,
            'id':'filechooser',
            'path' :os.path.dirname(Values.def_path),
            'dirselect':True,
            'multiselect':False,
        }

        self.dialogue=FileChooserIconView(**widget_props)
        self.add_widget(self.dialogue)
        self.layout = BoxLayout(size_hint_y=0.1,
                                orientation='horizontal')
        self.open_button=Common_button(text='Open')
        self.cancel=Common_button(text='Cancel')

        self.layout.add_widget(self.open_button)
        self.layout.add_widget(self.cancel)
        self.add_widget(self.layout)
        
