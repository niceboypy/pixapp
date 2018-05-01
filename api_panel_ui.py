from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty



class Integrated_api_bar(BoxLayout):
    orientation='vertical'
    def __init__(self):
        super().__init__()
        self.add_widget(Apibar())
        self.add_widget(Search_type_panel())




class Apibar(BoxLayout):
    api_input_bar = ObjectProperty()
    toggle_visibility_button = ObjectProperty()
    original_text = '*'
    pass_view = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def clear(self):
        self.api_input_bar.text = ''
        self.api_input_bar.focus = True
        # @@%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% cut this block
        # string aligning algorithm in case padding does work
        # def align_string(self,string=None):
        #     print("function executed")
        #     if string:
        #         string=string
        #     else:
        #         string = 'key'#"Your API key"

        #     size = int(list(self.api_input_bar.size)[1])
        #     self.api_input_bar.hint_text= "{}{}".format(" "*(size-len(string)), string)
        #     self.api_input_bar.focus = True
        # @@%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    def save_key(self):
        #self.clean_key() TO-DO
        self.original_text = self.api_input_bar.text.strip()
        # user_data.put('user_key', self.original_text)
        #self.store_key(somewhere) TO-DO

    def toggle_visibility(self):
        button = self.toggle_visibility_button
        button.text = "Show" if button.text is "Hide" else "Hide"
        self.pass_view = False if self.pass_view is True else True
        if self.pass_view:
            self.api_input_bar.password = False
        else:
            self.api_input_bar.password = True


class Search_type_panel(BoxLayout):
    image_optn = ObjectProperty()
    video_optn = ObjectProperty()
    both_optn = ObjectProperty()
    editor_option = ObjectProperty()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.search_choices = [self.ids.image, 
                                self.ids.video,
                                self.ids.both]
        self.padding_left='20dp'

    def setstatus(self, obj=None):
        if obj is self.ids.editor_choice:
            ed_c = self.ids.editor_choice
            setattr(ed_c, 'active', True) if ed_c.active is False else setattr(ed_c, 'active', False)
            

        [setattr(radio, 'active', True) if radio is obj else \
        setattr(radio, 'active', False) for radio in self.search_choices]
        