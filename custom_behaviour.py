import kivy
from kivy.uix.videoplayer import VideoPlayer
from par_values import Values
import os
from custom_widgets import save_dialog
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class custom_popup:
    def __init__(self, msg, title):
        box = BoxLayout(orientation = 'vertical', padding = (10))
        box.add_widget(Label(text = msg, size_hint_y=.7))
        btn1 = Button(text = "OK", size_hint_y=.1)
        box.add_widget(btn1)

        popup = Popup(title=title, title_size= (30), 
                    title_align = 'center', content = box,
                    size_hint=(None, None), size=(400, 400),
                    auto_dismiss = True)

        btn1.bind(on_press = popup.dismiss)
        popup.open()

class Behaviour:

    def add_behaviour(self):
        #behaviour for top 3 left radio buttons #search id in the file: #23D$
        self.add_search_type_behaviour(self.apiholder, self.paramholder)
        
        #behaviour for browsing button#search id:
        self.add_browser_behaviour(self.paramholder)

        #behaviour for preview panel
        self.add_preview_behaviour(self.apiholder, self.paramholder)

        #fetch button behaviour
        self.add_fetch_behaviour(self.apiholder, self.paramholder)
    ###############################################################################################
    ####################### BEHAVIOUR FOR RADIO BUTTONS: #23D$ ####################################
    def add_search_type_behaviour(self, *objs):
        apiholder, paramholder = objs

        def Bind(obj, **kwargs):
            obj.bind(**kwargs)

        sch_typ_pan=apiholder.get('sch_typ_pan')
        img_sel_chkbx=apiholder.get('img_sel_chkbx')
        img_sel_lab=apiholder.get('img_sel_lab')

        vid_sel_chkbx=apiholder.get('vid_sel_chkbx')
        vid_sel_lab=apiholder.get('vid_sel_lab')

        bth_sel_chkbx=apiholder.get('bth_sel_chkbx')
        bth_sel_lab = apiholder.get('bth_sel_lab')

        drpdwn_par = paramholder.get('drpdwn_par') #from_parent is the dropdown parent
        display_par = paramholder.get('display_par') #parent for display parent

        #self.mapping provides the mapping for the img, vid or bth list
        self.mapping={
            'img': paramholder.get('dropdowns'),
            'vid': paramholder.get('dropdowns_vid'),
            'bth': paramholder.get('dropdowns_bth')
        }

        image_panel = paramholder.get('img_display')
        video_panel = paramholder.get('vid_display')
        self.image_info = paramholder.get('image_info')
        
        self.item_display = image_panel #current panel that we have at preview
        self.prev_state = 'img'         #initial state is always 'img'
        Bind(img_sel_lab, on_ref_press = lambda *_: self.switch('img',sch_typ_pan, img_sel_chkbx, drpdwn_par, display_par, image_panel, video_panel))
        Bind(vid_sel_lab, on_ref_press = lambda *_: self.switch('vid',sch_typ_pan, vid_sel_chkbx, drpdwn_par, display_par, image_panel, video_panel))
        Bind(bth_sel_lab, on_ref_press = lambda *_: self.switch('bth',sch_typ_pan, bth_sel_chkbx, drpdwn_par, display_par, image_panel, video_panel))


    def switch(self, data_type, panel, obj, drpdwn_par, display_par, image_panel, video_panel):
        """dynamically switch panels when the reference labels are pressed"""
        #from_parent is the parent of spinner_widget
        #from_dis_par is the parent of the display_widget 

        panel.setstatus(obj) #change which panel is active by setting the active property

        # if the previous dropdown list does not match the currently selected
        # dropdown list, only then change the panel, otherwise
        #user's click events will be ignored
        if self.prev_state != data_type:
            #remove all the dropdowns from the previous state
            for dropdown in self.mapping[self.prev_state]:
                drpdwn_par.remove_widget(dropdown)
            
            for dropdown in self.mapping[data_type]:
                drpdwn_par.add_widget(dropdown)
        
            if self.prev_state == 'img':
                display_par.remove_widget(image_panel)
                display_par.add_widget(video_panel)
            else:
                #if self.prev_state == 'vid' or 'bth'
                if data_type == 'img':
                    try:
                        display_par.remove_widget(video_panel)
                        display_par.add_widget(image_panel)
                    except:
                        import sys
                        print(sys.exc_info())
                        import time
                        time.sleep(10)
        self.prev_state = data_type

        print("The line has been executed")
        #getting ready for list formation dynamically, according to user changes to the type of image downloaded
        self.list_type = data_type
        self.item_list = []            #with_pan holds whatever panel is in the current display
        self.item_display  = image_panel if data_type == 'img' else video_panel  #set the panel to whichever panel the radio indicates
        self.image_info.text=''
    ###############################################################################################
    ###############################################################################################

    ###############################################################################################
    ########################## BEHAVIOUR FOR BROWSER BUTTON #24D$ #################################
    def add_browser_behaviour(self, *obj):
        paramholder, *_ = obj
        save_btn=paramholder.get('brws_btn')

        output_fld=paramholder.get('textboxes')[3]
        
        save_btn.bind(on_release=lambda*_: self.update_output_fld(output_fld))
    
    def update_output_fld(self, output_fld):

        def_path=output_fld.text
        # def_path = def_path if os.path.exists(def_path) else Values.def_path
        
        #change in file chooser dialog
        title = 'Save file in....'
        popup = save_dialog()

        def updatepopup(mainpopup, filechooser):
            # nonlocal output_fld
            selection=filechooser.dialogue.selection[0]#multi select is false, only one element
            if not os.path.isdir(selection):
                selection=os.path.dirname(selection)
            
            update_string=title+"  "+selection
            mainpopup.title=update_string
            output_fld.text = selection


        self.Popup = Popup(title=title,
                    content=popup,
                    size_hint=(0.9, 0.9))

        def retain_path(output_fld):
            output_fld.text=def_path
            self.Popup.dismiss()

        popup.dialogue.bind(selection=lambda*_:updatepopup(self.Popup, popup))

        popup.open_button.bind(on_press=lambda*_: self.Popup.dismiss())
        popup.cancel.bind(on_press=lambda*_: retain_path(output_fld))
        
        self.Popup.open()
    ###############################################################################################
        
    ###############################################################################################
    ######################### BEHAVIOUR FOR PREVIEW PANEL #25D$ ###################################

    def add_preview_behaviour(self, apiholder, paramholder):
        """add preview behaviour to preview panel"""
        self.curindex=-1
        self.item_list=[]#saves items(images or video files in a directory)
        self.prev_state = 'img'#the state always starts for displaying images
        self.list_type = 'img'
        

        #########################   PARAMETERS AND VARIABLES DEFINED ##########################################
        image_dir = paramholder.get('textboxes')[3]
        
        self.prev_dir = image_dir.text # save the value of previous directory - to   
                                       # check against the output path 
                                       # to form a list

        self.image_info.text='Preview items on output path'
        self.get_prev_func = lambda *_: None
        self.get_next_func = lambda *_: None
        self.prev_btn = paramholder.get('prev_btn')
        self.next_btn = paramholder.get('next_btn')
        self.buttons=(self.prev_btn, self.next_btn)
        display = paramholder.get('img_display')
        prvw_chkbox = paramholder.get('prvw_chkbx')
        prvw_label = paramholder.get('prvw_label')

        img_sel_chkbox = apiholder.get('img_sel_chkbx')
        vid_sel_chkbox = apiholder.get('vid_sel_chkbx')
        ######################################################################################################

        def yield_list(path):
            """yield items in path"""
            for i in os.listdir(path):
                yield i
        
        def create_list(Type='img'):
            """create a new list on every list_size_item preview"""
            list_size=10 #the list size to be generated
            for i in range(list_size):
                try:
                    item = next(self.gen_obj)
                except:
                    #ignore the exception
                    pass
                else:
                    if Type=='img':
                        if (item.endswith('.jpg') or item.endswith('.png')):
                            self.item_list.append(item)
                        elif (item.endswith('.svg')):
                            self.item_list.append(os.path.join(os.getcwd(),'no_svg.png'))
                    elif Type=='vid':
                        if (item.endswith('.mp4')):
                            self.item_list.append(item)
                    else:
                        if (item.endswith('.jpg') or item.endswith('.png') or item.endswith('.mp4')):
                            self.item_list.append(item)
                        elif (item.endswith('.svg')):
                            self.item_list.append(os.path.join(os.getcwd(),'no_svg.png'))
                        
            
            # denotes if list contains items
            if self.item_list:
                return True
            else:
                return False

        def select_behaviour(*objs):
            """callback on preview selection, selects image and 
                video preview behaviour"""

            img_sel_chkbox, prvw_chkbox, image_dir = objs
            image_dir.text = image_dir.text if os.path.exists(image_dir.text) else Values.def_path
            # create a new generator object on every press of
            # preview reference label, this is the only thing
            # that updates the directory
            #because the directory is traversed using a generator object
            self.gen_obj = yield_list(image_dir.text)

            def getitem(image_dir, inrfac):                
                #check if the path has changed
                #if yes, reset all the values
                #create new generator for the path
                #and set the list values
                if os.path.exists(image_dir):
                    
                    if image_dir != self.prev_dir:
                        self.gen_obj = yield_list(image_dir)
                        self.item_list=[]
                        create_list(Type=self.list_type)
                        self.curindex = -1
                    self.prev_dir = image_dir

                if self.item_list:
                    try:
                        # try getting image from the
                        # list currently in existence
                        self.curindex += inrfac
                        if self.curindex < 0: self.curindex = 0
                        cur_image = self.item_list[self.curindex]
                        self.prev_image = cur_image
                    except:
                        #if that's an index error
                        try:
                            # see if the list can be extended since
                            # only list item(see in create_list function)
                            # elements can are added to the list at a time to save
                            # memory overhead
                            create_list(Type=self.list_type)
                            cur_image = self.item_list[self.curindex]
                            self.curindex += inrfac
                        except IndexError:
                            if self.curindex > (len(self.item_list)-1):
                                self.curindex = len(self.item_list) -1 
                            elif self.curindex < 0:
                                self.curindex = 0
                            cur_image = self.item_list[self.curindex]

                    if not os.path.exists(cur_image):
                        # if the image found is not a path
                        # then, update the information label
                        # that displays image name above the preview display
                        self.image_info.text=cur_image
                        # then make it into a path and return the value
                        return os.path.join(self.prev_dir, cur_image)
                    else:
                        #return cur_image as one of the condition images
                        #condition images-> e.g. images that represent a state
                        #e.g. invalid=none.png, no_svg.png
                        self.image_info.text=''
                        return cur_image
                else:
                    self.image_info.text='No Items Found'
                    return 'none.png'

            def getprev(image_dir):
                return getitem(image_dir, -1)
            
            def getnext(image_dir):
                return getitem(image_dir, 1)
        
            def traverse(list_type=self.list_type):
                """Traverse through a directory"""
                print("The list type is: ", self.list_type)
                if create_list(Type=list_type):
                    if prvw_chkbox.active:
                        prvw_chkbox.active=False
                        if self.list_type=='img':
                            self.item_display.source='none.png'
                        elif self.list_type=='vid':
                            self.item_display.source='none.mp4'
                        self.image_info.text='Preview items on output path'
                        self.item_list=[]
                        self.curindex=-1

                        self.prev_btn.unbind(on_press=self.get_prev_func)
                        self.next_btn.unbind(on_press=self.get_next_func)
                        self.get_prev_func, self.get_next_func = lambda *_: None, lambda *_: None
                        self.prev_btn.bind(on_press = self.get_prev_func)
                        self.next_btn.bind(on_press = self.get_next_func)
                        
                    else:
                        prvw_chkbox.active = True
                        #code to recontinue from previously left spot
                        if self.item_list:
                            if self.curindex <0: self.curindex=0
                            self.image_info.text = self.item_list[self.curindex]
                            if not os.path.exists(image_dir.text):
                                image_dir.text = Values.def_path
                            if os.path.exists(self.item_list[self.curindex]):
                                self.item_display.source = self.item_list[self.curindex]
                            else:
                                self.item_display.source = os.path.join(image_dir.text, self.item_list[self.curindex])
                            
                        #rebind buttons to traverse
                        if self.list_type=='img':
                            self.next_btn.unbind(on_press=self.get_next_func)
                            self.prev_btn.unbind(on_press=self.get_prev_func)
                            #self.get_next_func=lambda*_: setattr(self.item_display, 'source', getnext(image_dir.text))
                            #self.get_prev_func=lambda*_: setattr(self.item_display, 'source', getprev(image_dir.text))
                            #self.prev_btn.bind(on_press=self.get_prev_func)
                            #self.next_btn.bind(on_press=self.get_next_func)
                        elif self.list_type=='vid':
                            self.next_btn.unbind(on_press=self.get_next_func)
                            self.prev_btn.unbind(on_press=self.get_prev_func)

                        self.get_next_func=lambda*_: setattr(self.item_display, 'source', getnext(image_dir.text))
                        self.get_prev_func=lambda*_: setattr(self.item_display, 'source', getprev(image_dir.text))
                        self.next_btn.bind(on_press=self.get_next_func)
                        self.prev_btn.bind(on_press=self.get_prev_func) 
                
                else:
                    self.image_info.text = 'No Items Found'
                    self.item_display.source='none.png'
                    self.prev_btn.bind(on_press=lambda *_: None)
                    self.next_btn.bind(on_press=lambda *_: None)

            if img_sel_chkbox.active:
                #we create a new list
                if self.prev_state=='vid':
                    self.item_list=[]
                self.prev_state='img'
                traverse()
            else:# vid_sel_chkbox.active:
                if self.prev_state=='img':
                    self.item_list=[]
                self.prev_state='vid'
                traverse()
            
                    

        
        prvw_label.bind(on_ref_press=lambda*_: select_behaviour(img_sel_chkbox,
                                prvw_chkbox, image_dir))

    ###############################################################################################
    
    ###############################################################################################
    ########################  BEHAVIOUR FOR PREVIEW PANEL #26D$ ###################################
    def add_fetch_behaviour(self, apiholder, paramholder):
        fetch_btn = paramholder.get('fetch_btn')
        stat_indicator = (apiholder.get('img_sel_chkbx'), apiholder.get('vid_sel_chkbx'))
        api_inp_bar= apiholder.get('api_inp_bar')
        fetch_btn.bind(on_press=lambda*_: self.fetch(api_inp_bar, paramholder, stat_indicator))
        self.spin_parameters = ['quality','image_type', 'language', 'category', 'order', 'orientation', 'colors']
        
    def fetch(self, api_bar, paramholder, stat_indicator):
        dropdowns = paramholder.get('spinners')
        textboxes = paramholder.get('textboxes')
        api_key = api_bar.text
        
        if stat_indicator[0].active:
            dwnld_type='img'
            spin_count = 7
        elif stat_indicator[1].active:
            dwnld_type='vid'
            spin_count = 6
        else:
            dwnld_type='bth'
            spin_count = 6

        text_values = [textboxes[i].text for i in range(3)]
        spin_values = [spinners.text for spinners in dropdowns]
        request_strings = self.form_requests(text_values, spin_values, dwnld_type, api_key, spin_count)



    def form_requests(self, text_values, spin_values, dwnld_type, api_key, spin_count):
        """form the request url string and return them as lists"""
        _quantity= text_values[0]
        quantity = int(Values.quantity) if (not _quantity) else int(_quantity) 
        search = text_values[1]
        multisearch = text_values[2]
        if dwnld_type == 'img':
            requests = [Values.image_search.format(api_key)]
        elif dwnld_type == 'vid':
            requests = [Values.video_search.format(api_key)]
        else:
            requests = [Values.image_search.format(api_key),
                        Values.video_search.format(api_key)]
        
        #input error detection during fetch
        if (quantity < 1):
            custom_popup("Quantity must be at least 1", 'Error')
            return None
        if multisearch:
            search_terms = multisearch.strip().split(',')
            if search:
                search_terms.append(search.strip())
        elif search:
            search_terms = [search.strip()]
        else:
            custom_popup('At least one search item must be specified', 'Error')
            return None
        
        param_string = ''#confirm that it is set to nothing
        for i in range(1, spin_count):
            #param_string is the string that contains all the parameter specifications
            #such as: &image_type=photo&language=en&category=art
            if (spin_values[i] != 'all' and spin_values[i] != 'any'):
                param_string += '&'+ self.spin_parameters[i]+'='+spin_values[i]

        print("The param string is: ", param_string)
            

        search_terms = [terms.strip() for terms in search_terms]

        


        # fetch_btn.bind(on_press=showusnowupdate)

    ###############################################################################################

        


