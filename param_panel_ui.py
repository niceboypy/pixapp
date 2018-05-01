from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.properties import ObjectProperty

class Change_mixin:
    def apply_changes(self, changes):
            #format of changes:
            #[('name', {'attribute', 'value'})]
        if changes: 
            for change in changes:
                for props in change[1].keys():
                    setattr(self.items[change[0]],
                            props,
                            change[1][props])


class Img_search_preview(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def change_status(self, obj):
        obj.active=False if obj.active is True else True
            

class Img_query_holder(BoxLayout, Change_mixin):
    #short for
    #image dimension info holder
    def __init__(self, changes=None, **kwargs):
        super().__init__(**kwargs)
        self.items = {
            'Input': self.ids.dim_input,
            'Label': self.ids.label,
            'place1':self.ids.place_label1,
            'place2':self.ids.place_label2,
        }

        self.apply_changes(changes)
    
    def print_text(self):
        print("I am here, ", self.ids.dim_input.text)



class dropdown_holder(BoxLayout, Change_mixin):
    spinner = ObjectProperty()
    def __init__(self, changes=None, **kwargs):
        super().__init__(**kwargs)
        self.items={
            'spinner':self.ids.spin,
            'label':self.ids.info_label
            # 'label':self.ids.lab
        }
        self.ids.spin.dropdown_cls.max_height=150

        self.apply_changes(changes)
    
class Info_and_preview(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        change= [('spinner', 
                            {'values':('uno', 'dos', 'tres', 'quadro', 'sinco')
                            }),
                    ('label',{'text':'narrow_heigh'})
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

        common_size_hint= 0.15
        image_search=[(
            'Input',
            {'hint_text':'Fetch Imgs e.g cars'}),
            ('Label',
            {'text': 'Fetch: ',
            'size_hint_x':common_size_hint,
            }),
        ]

        multisearch=[(
            'Input',
            {'hint_text':'separate using ","'}),
            ('Label',
            {'text': 'Multisearch: ', 
            'size_hint_x':common_size_hint})
        ]

        self.left_layout.add_widget(Img_query_holder())
        self.left_layout.add_widget(Img_query_holder(minimum_height))
        self.left_layout.add_widget(Img_query_holder(quantity_panel))
        self.right_layout.add_widget(Img_search_preview())

        self.add_widget(self.left_layout)
        self.add_widget(Label(size_hint_x=0.07))
        self.add_widget(self.right_layout)
        # self.add_widget(Label(size_hint_x=0.01))






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
