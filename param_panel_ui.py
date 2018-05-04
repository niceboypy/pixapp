from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.app import App
import re
import webbrowser, os, sys
from kivy.properties import ObjectProperty
from par_values import Values

class Change_mixin:
    def apply_changes(self, changes):
        if changes: 
            for change in changes:
                #     [(
                # 'Input', 
                # {'hint_text':'leave for default',
                # 'bind': {'on_text': self.checkinput()}
                # }),
                # ('Label',
                # {'text':'Minimum height: '})
                # ]
                # [('Add', (Button, [(Button, {properties})]  )]

                if change[0] != 'Add':
                    Cur_obj = self.items[change[0]]
                    for props in change[1].keys():
                        Cur_obj_properties = change[1][props]
                        if props=='bind':
                            Cur_obj.bind(**(change[1]['bind']))
                        else: 
                            setattr(Cur_obj,
                                    props,
                                    Cur_obj_properties)
                else:
                    parent = self.items['parent']
                    
                    for dynwid in change[1]:
                        self.dynwid= (dynwid[1][0](**(dynwid[1][1])))
                    
                    for dynwid in self.dynwid:
                        parent.add_widget(dynwid)

                    



class Img_search_preview(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    
            

class Img_query_holder(BoxLayout, Change_mixin):
    def __init__(self, changes=None, **kwargs):
        super().__init__(**kwargs)
        self.items = {
            'Input': self.ids.dim_input,
            'Label': self.ids.label,
            'parent': self.ids.dim_input.parent
        }
        
        self.apply_changes(changes)



class dropdown_holder(BoxLayout, Change_mixin):
    spinner = ObjectProperty()
    def __init__(self, changes=None, **kwargs):
        super().__init__(**kwargs)
        self.items={
            'spinner':self.ids.spin,
            'label':self.ids.info_label
        }
        self.ids.spin.dropdown_cls.max_height=150
        self.apply_changes(changes)

class Preview_panel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def change_status(self, obj):
        obj.active=False if obj.active is True else True



class Info_and_preview(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.quantity=Values.quantity
        self.search_term=Values.search_term
        self.list_search=Values.list_search
        self.setall()
    
    def setall(self):

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

        quality = [('spinner', 
                            {'values':Values.quality
                            }),
                    ('label',{'text':'Quality: '})
                    ]

        ####################LEFT LAYOUT QUERY PROPERTIES################################
        ######     "note: " in QUERY DECLARATIONS we reference 'TextInput' object
        ######     as "Input" and Label as 'Label'

        numeric_input= Values.numeric_value#re.compile('^[0-9]+$')
        
        quantity_panel=[(
            'Input', 
            {'hint_text':'max: 5000 imgs/hr',
            'bind':{'text':lambda *_: self.checkinput(0, self.quantity,numeric_input)},
                }),
            ('Label',
            {'text':'Quantity (def. 100): '}), 
            ]

        common_size_hint= 0.15 #common size for textinputwidget
        ####################################
        # 

        ################## RIGHT LAYOUT QUERY PROPERTIES #########################################

        fetch= Values.fetch_values#re.compile('^[\w\ ]+$')
        image_search=[(
            'Input',
            {'hint_text':'Fetch Imgs e.g cars',
            'bind':{'text':lambda *_: self.checkinput(1, None, fetch, Type='word')}
            }),
            ('Label',
            {'text': 'Fetch: ',
            'size_hint_x':common_size_hint,
            }),
        ]

        multi_search=Values.multi_search#name multisearch
        multisearch=[(
            'Input',
            {'hint_text':'separate using ","',
            'bind':{'text':lambda *_: self.checkinput(2, None, multi_search, Type='word_list')}
            }),
            ('Label',
            {'text': 'Multisearch: ', 
            'size_hint_x':common_size_hint})
        ]
        #################################################################################
        # 
        ########### QUERY INSTANCE DECLARATIONS #######################################
         #all dropdown instances
        self.dropdowns= [dropdown_holder(language),
                        dropdown_holder(img_type),
                        dropdown_holder(orien),
                        dropdown_holder(category),
                        dropdown_holder(colors),
                        dropdown_holder(order),
                        dropdown_holder(quality),
                        ]

        #all textbox instances
        self.textboxes = [Img_query_holder(quantity_panel), 
                    Img_query_holder(image_search, size_hint_y=0.07),
                    Img_query_holder(multisearch, size_hint_y=0.07)]
        
        #All dynamically added widget instances
        self.dynwids = []
        ################################################################################


        

        self.left_layout = BoxLayout(size_hint_x=0.5, orientation='vertical')
        self.right_layout = BoxLayout(size_hint_x=0.5, orientation='vertical')

        self.left_layout_drop = BoxLayout(orientation='vertical', size_hint_y=0.8)
        self.left_layout_quer = BoxLayout(orientation='vertical', size_hint_y=0.2)


        ###########FIX DROPDOWN INSTANCES OF LEFT LAYOUT##################
        for widget in self.dropdowns:
          self.left_layout_drop.add_widget(widget)  
        

        ###########FIX QUERY WIDGETS OF LEFT LAYOUT ############################
        self.left_layout_quer.add_widget(self.textboxes[0])

        self.left_layout.add_widget(self.left_layout_drop)
        self.left_layout.add_widget(self.left_layout_quer)
        self.left_layout.add_widget(Label(text='Image Source: [ref=link]Pixabay.com[/ref]',
                                    color=(0.1,0.1,0.1,1),
                                    font_size='20dp',
                                    size_hint_y="0.08",
                                    markup=True,on_ref_press=lambda *_:self.open_new_browser())) #not gonna change for eternity

        #############  RIGHT PANEL QUERY HOLDERS ############################################
        self.right_layout.add_widget(self.textboxes[1])
        self.right_layout.add_widget(self.textboxes[2])
        ############# RIGHT PANEL PREVIEW HOLDER ############################################
        self.right_layout.add_widget(Preview_panel())

        
        self.add_widget(self.left_layout)
        self.add_widget(Label(size_hint_x=0.07))
        self.add_widget(self.right_layout)
        # self.add_widget(Label(size_hint_x=0.01))
    
    def open_new_browser(self):
        webbrowser.open('https://pixabay.com')
    
    def checkinput(self, Instance, property, pattern, Type='range'):
        #Instance is a number referring to the instance number in self.textboxes
        #Available checking types: 
        #1)range 2)path   3)word 4)list words

        Instance=(self.textboxes[Instance].items)['Input']
        text=Instance.text

        if Type=='range':
            self.filter_realtime_input(pattern, text, Instance, 'quantity')
        elif Type=='word':
            print("Something")
            self.filter_realtime_input(pattern, text, Instance, 'search_term')
        elif Type=='word_list':
            print("The word_list text is: ", text)
            self.filter_realtime_input(pattern, text, Instance, 'list_search')


    def filter_realtime_input(self, pattern, text, Instance, global_def):
        if pattern.match(text):
            setattr(self, global_def, text)
        else:
            if text=='':
                setattr(self, global_def, getattr(Values, global_def))
            else:
                Instance.text=getattr(self, global_def)
                    




            