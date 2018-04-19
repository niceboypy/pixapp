#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

# import re as regex


# def check_match(string, exp):
#     print("The expression is: ", exp)
#     pattern = regex.compile(exp)

#     if pattern.match(string):
#         return True
#     else:
#         return False


class Apibar(BoxLayout):
    api_input_bar = ObjectProperty()
    toggle_visibility_button = ObjectProperty()
    original_text = '*'
    pass_view = False

    def print_text(self, size=None):
        try:
            #test radio buttons
            print("Test function printed", size.active)
        except:
            try:
                print("The function printed: ", size)
            except:
                pass
    
    def clear(self):
        self.api_input_bar.text = ''
        self.api_input_bar.focus = True

        
    def align_string(self,string=None):
        print("function executed")

        if string:
            string=string
        else:
            string = "Your API key"

        size = int(list(self.api_input_bar.size)[1])
        self.api_input_bar.hint_text= "{}{}".format(" "*(size-len(string)), string)
        self.api_input_bar.focus = True

    def save_key(self):
        #self.clean_key() TO-DO
        self.original_text = self.api_input_bar.text.strip()
        #self.store_key(somewhere) TO-DO

    def toggle_visibility(self):
        button = self.toggle_visibility_button
        button.text = "Show" if button.text is "Hide" else "Hide"
        self.pass_view = False if self.pass_view is True else True
        if self.pass_view:
            self.api_input_bar.password = False
        else:
            self.api_input_bar.password = True
            

        



class pixapp(App):
    def build(self):
        return Apibar()

if __name__ == '__main__':
    pixapp().run()