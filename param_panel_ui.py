from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.app import App
import webbrowser, os, sys
from kivy.properties import ObjectProperty
from par_values import Values

class Change_mixin:
    def apply_changes(self, changes):
        # print(changes)
        # import time
        # time.sleep(3)
        if changes: 
            for change in changes:
                print(r"%%%%%%%%%%%%%%%%%%%%%%%")
                print("Item taken: ", change)
                print("Item properties", change[1].keys())
                print(r"%%%%%%%%%%%%%%%%%%%%%%%")
                # import time
                # time.sleep(2)
                Cur_obj = self.items[change[0]]
                
                for props in change[1].keys():
                    Cur_obj_properties = change[1][props]
                    print("Item properties", props)
                    if props=='bind':
                        import time
                        print("The current object is: ", Cur_obj)
                        time.sleep(4)
                        Cur_obj.bind(on_text=lambda *_: print('something'),
                                on_text_validate=lambda *_: print("something that I have here"))#**(change[1][props]))
                    else: 
                        setattr(Cur_obj,
                                props,
                                Cur_obj_properties)



class Img_search_preview(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def change_status(self, obj):
        obj.active=False if obj.active is True else True
            

class Img_query_holder(BoxLayout, Change_mixin):
    def __init__(self, changes=None, **kwargs):
        super().__init__(**kwargs)
        self.items = {
            'Input': self.ids.dim_input,
            'Label': self.ids.label,
        }
        # print("The current object passed is: ", self.ids.dim_input)
        # import time
        # time.sleep(4)

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

        language= [('spinner', 
                            {'values':Values.language
                            }),
                    ('label',{'text':'language: '})
                    ]

        img_type= [('spinner', 
                            {'values':Values.image_type
                            }),
                    ('label',{'text':'Image type: '})
                    ]

        orien= [('spinner', 
                            {'values':Values.orientation
                            }),
                    ('label',{'text':'Orientation: '})
                    ]

        category= [('spinner', 
                            {'values':Values.category
                            }),
                    ('label',{'text':'Category: '})
                    ]

        colors= [('spinner', 
                            {'values':Values.colors
                            }),
                    ('label',{'text':'Colors: '})
                    ]

        order= [('spinner', 
                            {'values':Values.order
                            }),
                    ('label',{'text':'Order: '})
                    ]

        order= [('spinner', 
                            {'values':Values.order
                            }),
                    ('label',{'text':'Order: '})
                    ]
        

        self.left_layout = BoxLayout(size_hint_x=0.5, orientation='vertical')
        self.right_layout = BoxLayout(size_hint_x=0.5, orientation='vertical')

        self.left_layout_drop = BoxLayout(orientation='vertical', size_hint_y=0.7)
        self.left_layout_quer = BoxLayout(orientation='vertical', size_hint_y=0.3)

        self.left_layout_drop.add_widget(dropdown_holder(language))
        self.left_layout_drop.add_widget(dropdown_holder(img_type))
        self.left_layout_drop.add_widget(dropdown_holder(orien))
        self.left_layout_drop.add_widget(dropdown_holder(category))
        self.left_layout_drop.add_widget(dropdown_holder(colors))
        self.left_layout_drop.add_widget(dropdown_holder(order))


        minimum_height=[(
            'Input', 
            {'hint_text':'leave for default',
                }),
            # 'bind': {'on_text': self.checkinput()}
            ('Label',
            {'text':'Minimum height: '})
            ]
        
        minimum_width=[(
            'Input', 
            {'hint_text':'leave for default',
            'on_text': lambda *_: self.checkinput('width')}),
            ('Label',
            {'text':'Minimum width: '})
            ]
        
        # x= (minimum_height)
        
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

        self.left_layout_quer.add_widget(Img_query_holder(minimum_height))#[ref=preview]Preview: [/ref]
        self.left_layout_quer.add_widget(Img_query_holder(minimum_width))
        self.left_layout_quer.add_widget(Img_query_holder(quantity_panel))

        self.left_layout.add_widget(self.left_layout_drop)
        self.left_layout.add_widget(self.left_layout_quer)
        self.left_layout.add_widget(Label(text='Image Source: [ref=link]Pixabay.com[/ref]',
                                    color=(0.1,0.1,0.1,1),
                                    font_size='20dp',
                                    size_hint_y="0.08",
                                    markup=True,on_ref_press=lambda *_:self.open_new_browser())) #not gonna change for eternity
        self.right_layout.add_widget(Img_search_preview())

        self.add_widget(self.left_layout)
        self.add_widget(Label(size_hint_x=0.07))
        self.add_widget(self.right_layout)
        # self.add_widget(Label(size_hint_x=0.01))
    
    def open_new_browser(self):
        webbrowser.open('https://pixabay.com')
    
    def checkinput(self, check_values=None):
        print("I am in checkinput")
