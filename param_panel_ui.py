from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.properties import ObjectProperty



class param_holder(BoxLayout):
    spinner = ObjectProperty()
    def __init__(self, changes=None, **kwargs):
        super().__init__(**kwargs)
        self.items={
            'spinner':self.ids.spin,
            # 'label':self.ids.lab
        }
        self.ids.spin.dropdown_cls.max_height=200

        if changes:
            self.apply_changes(changes)
    
    def apply_changes(self, changes):
        #format of changes:
        #[('name', {'attribute', 'value'})]
        for change in changes:
            for props in change[1].keys():
                setattr(self.items[change[0]],
                        props,
                        change[1][props])










# class Params:
#     #params is parameters ;-)
#     global_default_params = {
#         'parent':{
#             'orientation': 'vertical',
#         },
#         'widgets':{
#                 'label1':{
#                     'text': 'default',
#                     'size_hint': (.3, None)
                    
#                 },
#                 'spinner1':{
#                     'text_autoupdate': True,
#                     'values': ('test1', 'test2', 'test3',
#                             'test4', 'test5', 'test6', 
#                             'test7', 'test8', 'test9', 
#                             'test10'),
#                     'size_hint':(.7, None),
#                 },
#             },
#             #format: (any parent,parent_property, child, property_to_link)
#         'objects': [(Label, 'label1'), (Spinner, 'spinner1')]
#     }

#     def __init__(self, kwargs=global_default_params):
#         self.key = {}
#         self.update(kwargs)
        
#     def update(self, kwargs):
#         self.__dict__.update(kwargs)


# class label_dropdown(BoxLayout):
#     def __init__(self, attribute=Params(), **updates):
#         super().__init__()
#         [setattr(self, x, (attribute.parent)[x]) for x in attribute.parent.keys()]
#         self.__dict__.update(**(attribute.parent))
#         attribute.update(updates) #everything is updated here
#         self.make_single(attribute)

#     def make_single(self, attribute):
#         for widgt in attribute.objects:
#             import time
#             print("here")
            
#             self.add_widget(self.construct(widgt[0],**(attribute.widgets[widgt[1]])))
    
#     def construct(self, obj, **properties):
#         print("The object is: ", obj)
#         print("The properties are: ", properties)
#         return obj(**properties)


# class params_panel(BoxLayout):
#     def __init__(self):
#         super().__init__()
#         self.orientation = 'vertical'
#         self.add_widget(label_dropdown())
#         self.add_widget(label_dropdown())
    

# class picapp(App):
#     def build(self):
#         return params_panel()

# if __name__ == '__main__':
#     picapp().run()
