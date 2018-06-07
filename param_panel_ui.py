from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
import re
from custom_widgets import Common_button, Plain_button
from kivy.uix.image import Image
import webbrowser, os, sys
from kivy.properties import ObjectProperty
from par_values import Values
from kivy.uix.videoplayer import VideoPlayer
from mixins import Change_mixin


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
        self.dynwids=[]
        self.apply_changes(changes, self.dynwids)
        



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
        self.orientation = 'vertical'
        self.size_hint_y= 0.6
        self.configure()
        class ids:
            #emptyclass
            pass
    
    def configure(self):
        self.add_widget(Label(size_hint_y=0.05))
        self.topbox = BoxLayout(orientation='vertical')
        self.ids.main_preview = self.topbox
        #we don't need references to number subscripted widgets_ they are named

        #add the preview checkbox#########################################################################
        self.topbox_1=BoxLayout(orientation='horizontal', size_hint_y=0.1)#, padding_top="10dp")
        self.topbox_1.add_widget(Label(size_hint_x=0.5))
        preview_checkbox = CheckBox(active=False, size_hint_x=0.01)    
        self.ids.preview_checkbox = preview_checkbox
        self.topbox_1.add_widget(self.ids.preview_checkbox)

        # add the preview label
        preview_label = Label(size_hint_x=0.4, text="[ref=preview]Preview: [/ref]", markup=True, font_size="20dp", halign='left')
        self.ids.preview_label = preview_label
        self.topbox_1.add_widget(self.ids.preview_label)
        self.topbox_1.add_widget(Label(size_hint_x=0.5))
        ##################################################################################################



        # add the image_information label#################################################################
        self.topbox_2 = BoxLayout(orientation='horizontal', size_hint_y=.1)
        image_information = Label(size_hint_y=0.005, text='', color=(.6, .6, .6, 1), font_size="15dp")
        self.ids.image_information = image_information
        self.topbox_2.add_widget(self.ids.image_information)
        ##################################################################################################

        #add the image_panel##############################################################################
        self.topbox_3 = BoxLayout(orientation='vertical')
        x = Label(size_hint_y=.05)#just for adjusting proportions
        image_panel = Image(source='none.png')
        self.ids.image_panel = image_panel
        self.topbox_3.add_widget(x)
        self.topbox_3.add_widget(self.ids.image_panel)
        ##################################################################################################


        #add the panels###################################################################################
        self.topbox_4 = BoxLayout(size_hint_y=.1, orientation='horizontal')

        self.topbox_4.add_widget(Label(size_hint_x=.4))

        previous_button = Plain_button(size_hint_x=.2, text='<')
        next_button = Plain_button(size_hint_x=.2, text='>')

        self.ids.previous_button = previous_button
        self.ids.next_button = next_button

        self.topbox_4.add_widget(self.ids.previous_button)
        self.topbox_4.add_widget(self.ids.next_button)
        self.topbox_4.add_widget(Label(size_hint_x=.4))


        self.topbox.add_widget(self.topbox_1)
        self.topbox.add_widget(self.topbox_2)
        self.topbox.add_widget(self.topbox_3)
        self.topbox.add_widget(self.topbox_4)
        self.add_widget(self.topbox)


    def change_status(self, obj):
        obj.active=False if obj.active is True else True



class Info_and_preview(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        #global_defs for input widgets
        self.quantity=Values.quantity
        self.search_term=Values.search_term
        self.list_search=Values.list_search
        self.def_path=Values.def_path

        self.textboxes=[]
        self.dropdowns=[]
        self.preview_panel=None

        self.setall()
        self.produce_user_interface()
    
    def setall(self):
        """set all the widgets"""

        language= [('spinner', 
                            {'values':Values.language
                            }),
                    ('label',{'text':'Language: '})
                    ]

        img_type= [('spinner', 
                            {'values':Values.image_type
                            }),
                    ('label',{'text':'Image type: '})
                    ]
        
        vid_type= [('spinner',
                        {'values': Values.video_type
                        }),
                    ('label',{'text': 'Video type: '})
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
        ####################RIGHT LAYOUT QUERY PROPERTIES################################
        ######     "note: " in QUERY DECLARATIONS we reference 'TextInput' object
        ######     as "Input" and Label as 'Label'
        numeric_input= Values.numeric_value #re.compile('^[0-9]+$')
        
        common_size_hint_x_lab = 0.25 #common size for label
        common_size_hint_x_inp = 0.75 #common size for textinputwidget
        common_size_hint_y=0.1
        dynamic_button_size=0.15
        count = 2
        quantity_panel=[(
            'Input', 
            {'hint_text':'default is 100imgs, max rate: 5000 imgs/hr',
            'bind':{'text':lambda *_: self.checkinput(0, self.quantity,numeric_input)},
            'size_hint_x':common_size_hint_x_inp
                }),
            ('Label',
            {'text':'Quantity:',
            'size_hint_x': common_size_hint_x_lab}), 
            ]

        ################## RIGHT LAYOUT QUERY PROPERTIES #########################################

        fetch= Values.fetch_values  #re.compile('^[\w\ ]+$')
        image_search=[(
            'Input',
            {'hint_text':'Fetch Imgs e.g cars',
            'bind':{'text':lambda *_: self.checkinput(1, None, fetch, Type='word')},
            'size_hint_x':common_size_hint_x_inp
            }),
            ('Label',

            {'text': 'Fetch: ',
            'size_hint_x':common_size_hint_x_lab,
            }),
        ]

        multi_search=Values.multi_search#name multisearch
        multisearch=[(
            'Input',
            {'hint_text':'separate using ","',
            'bind':{'text':lambda *_: self.checkinput(2, None, multi_search, Type='word_list')},
            'size_hint_x':common_size_hint_x_inp
            }),
            ('Label',
            {'text': 'Multisearch: ', 
            'size_hint_x':common_size_hint_x_lab})
        ]

        output_path=Values.output_path
        output=[(
            'Input',
            {'hint_text': 'Write output path',
            'text': self.def_path,
            'bind':{'text':lambda *_: self.checkinput(3, None, output_path, Type='path')},
            'size_hint_x':common_size_hint_x_inp-(count*dynamic_button_size),
            }),
            ('Label',
            {'text': 'Output',
            'size_hint_x': (common_size_hint_x_lab)}),
            ('Add', [(Common_button, {'size_hint_x': dynamic_button_size, 
                                    'font_size': '10dp',
                                    'text': 'Settings'}),
                    (Common_button, {'size_hint_x': dynamic_button_size,
                                'font_size':'10dp',
                                'text': 'Browse..'})
                    ])
        ]   

        #################################################################################
        
        
        ########### QUERY INSTANCE DECLARATIONS #######################################
         #all dropdown instances
        self.dropdowns=[dropdown_holder(quality),
                        dropdown_holder(img_type),
                        dropdown_holder(language),
                        dropdown_holder(category),
                        dropdown_holder(order),
                        dropdown_holder(orien),
                        dropdown_holder(colors),
                        ]
        
        #dropdown vids used for type video
        self.dropdowns_vid=[self.dropdowns[0],
                        dropdown_holder(vid_type),
                        self.dropdowns[2],
                        self.dropdowns[3],
                        self.dropdowns[4],
                        self.dropdowns[5],
                        ]
        
        #dropdown imgs used for downloading both types
        self.dropdowns_bth=[self.dropdowns[0],
                        self.dropdowns[1],
                        self.dropdowns_vid[1],
                        self.dropdowns[2],
                        self.dropdowns[3],
                        self.dropdowns[4],
                        self.dropdowns[5],
                        self.dropdowns[6]
                    ]
        
        self.spinners= [x.ids.spin for x in self.dropdowns]

        #all textbox instances
        self.textboxes = [Img_query_holder(quantity_panel, size_hint_y=common_size_hint_y), 
                    Img_query_holder(image_search, size_hint_y=common_size_hint_y),
                    Img_query_holder(multisearch, size_hint_y=common_size_hint_y),
                    Img_query_holder(output, size_hint_y=common_size_hint_y),]
        
        
        #All dynamically added widget instances
        ################################################################################


        

        self.left_layout = BoxLayout(size_hint_x=0.5, orientation='vertical')
        self.right_layout = BoxLayout(size_hint_x=0.5, orientation='vertical')

        self.left_layout_drop = BoxLayout(orientation='vertical', size_hint_y=0.8)


        ###########FIX DROPDOWN INSTANCES OF LEFT LAYOUT##################
        
        for widget in self.dropdowns:
          self.left_layout_drop.add_widget(widget)  
        
        #############  RIGHT PANEL QUERY HOLDERS ############################################
        self.right_layout.add_widget(self.textboxes[1])
        self.right_layout.add_widget(self.textboxes[2])
        self.right_layout.add_widget(self.textboxes[0])
        self.right_layout.add_widget(self.textboxes[3])

        ############# RIGHT PANEL PREVIEW HOLDER ############################################
        
        self.preview_panel=Preview_panel()
        self.display_parent=self.preview_panel.ids.main_preview
        self.image_panel=self.preview_panel.ids.image_panel
        self.cur_panel='img' #store current panel information
        self.video_panel = VideoPlayer(source='none.mp4')#source='magic.mp4')

        self.right_layout.add_widget(self.preview_panel)
        ############link button#########################3

        ###########FIX QUERY WIDGETS OF LEFT LAYOUT ############################

        self.left_layout.add_widget(self.left_layout_drop)
        #123123123 searchpoint
       
        self.fetch_btn = Common_button(size_hint_y=0.2,
                text='Fetch!', font_size="20dp",
                )

        self.left_layout.add_widget(self.fetch_btn)
        
        self.right_layout.add_widget(Label(text='Source: [ref=link]Pixabay.com[/ref]',
                                    color=(0.15,0.15,0.15,1),
                                    font_size='20dp',
                                    size_hint_y="0.08",
                                    markup=True,on_ref_press=lambda *_:self.open_new_browser())) #not gonna change for eternity

        
        self.add_widget(self.left_layout)
        self.add_widget(Label(size_hint_x=0.07))
        self.add_widget(self.right_layout)
        
        
    
    def open_new_browser(self):
        webbrowser.open('https://pixabay.com')
    
    def checkinput(self, Instance, property, pattern, Type='range'):
        #Available checking types: 
        #1)range 2)path   3)word 4)list words
        print("The instance is: ", Instance)
        
        #pattern is the regex pattern
        #text is what the text widget contains
        #Instance is a number referring to the instance number in self.textboxes
        #global def are the instance variables reffering to the default value of widgets


        #####Code starts here
        if self.textboxes:
            Instance=self.textboxes[Instance].items['Input']
            text=Instance.text

            if Type=='range':
                self.filter_realtime_input(pattern, text, Instance, 'quantity')
            elif Type=='word':
                self.filter_realtime_input(pattern, text, Instance, 'search_term')
            elif Type=='word_list':
                self.filter_realtime_input(pattern, text, Instance, 'list_search')
            elif Type=='path':
                self.filter_realtime_input(pattern, text, Instance, 'def_path')


    def filter_realtime_input(self, pattern, text, Instance, global_def):
        if pattern.match(text):
            setattr(self, global_def, text)
        else:
            if text=='':
                setattr(self, global_def, getattr(Values, global_def))
            else:
                print("The text is: ", text)
                Instance.text=getattr(self, global_def)

    # def test(self, *ignore):
    #         if self.cur_panel=='img':
    #             self.display_parent.remove_widget(self.image_panel)
    #             self.display_parent.add_widget(self.video_panel)
    #             self.cur_panel='vid'
    #         else:
    #             self.display_parent.remove_widget(self.video_panel)
    #             self.display_parent.add_widget(self.image_panel)
    #             self.cur_panel='img'

    def produce_user_interface(self):
        self.interface={
            'dropdowns': self.dropdowns,
            'dropdowns_vid':self.dropdowns_vid,
            'dropdowns_bth':self.dropdowns_bth,
            'spinners': self.spinners,
            'textboxes': [inst.items['Input'] for inst in  self.textboxes],
            'prvw_chkbx': self.preview_panel.ids.preview_checkbox,
            'prvw_label': self.preview_panel.ids.preview_label,
            'img_display': self.preview_panel.ids.image_panel,
            'vid_display': self.video_panel,
            'pre_butn': self.preview_panel.ids.previous_button,
            'nxt_butn': self.preview_panel.ids.next_button,
            'save_btn': (self.textboxes[3].dynwids)[0],
            'brws_btn': (self.textboxes[3].dynwids)[1],
            'drpdwn_par': self.dropdowns[0].parent,
            'display_par':self.preview_panel.ids.image_panel.parent,
            'image_info':self.preview_panel.ids.image_information,
            'prev_btn': self.preview_panel.ids.previous_button,
            'next_btn': self.preview_panel.ids.next_button,
            'settings': (self.textboxes[3].dynwids)[0],#settings button
            'fetch_btn': self.fetch_btn
        }

        
        
        