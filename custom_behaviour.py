import kivy
from kivy.uix.videoplayer import VideoPlayer
from par_values import Values
import os
from custom_widgets import save_dialog
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

import urllib.request as urlrequest
import json

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
                try:    
                    drpdwn_par.add_widget(dropdown)
                except:
                    #already has a parent
                    pass
        
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
                        #already has a parent
                        pass
                        
        self.prev_state = data_type

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

        stat_indicator =    (apiholder.get('img_sel_chkbx'), apiholder.get('vid_sel_chkbx'))
        api_inp_bar    =    apiholder.get('api_inp_bar')
        editor_choice  = apiholder.get('editor_choice')
        output_fld = paramholder.get('textboxes')[3]
        whole_dropdowns=    ([x.items['spinner'] for x in paramholder.get('dropdowns')],
                            [x.items['spinner'] for x in paramholder.get('dropdowns_vid')],
                            [x.items['spinner'] for x in paramholder.get('dropdowns_bth')])

        textboxes      =    paramholder.get('textboxes')
        
        self.img_par_list = ['quality', 'image_type', 'lang', 'category', 'order', 'orientation', 'colors']
        self.vid_par_list = ['quality', 'video_type', 'lang', 'category', 'order', 'orientation']
        self.bth_par_list = ['quality', 'image_type', 'video_type', 'lang', 'category', 'order', 'orientation', 'colors']
        self.parameter_structure = "&{}={}" #string used for parameter forming
        api_key = api_inp_bar.text

        fetch_btn.bind(on_press=lambda*_: self.fetch(api_inp_bar, output_fld,editor_choice, paramholder, textboxes, whole_dropdowns, stat_indicator))


    def fetch(self, api_bar,output_fld, editor_choice, paramholder, textboxes, whole_dropdowns,stat_indicator):
        # dropdowns, dropdowns_vid, dropdowns_bth = whole_dropdowns
        img_sel_chkbox, vid_sel_chkbox = stat_indicator
        

        api_key = api_bar.text
        self.type_base_url ={'img': Values.image_search.format(api_key),
                    'vid': Values.video_search.format(api_key)}

        if img_sel_chkbox.active: 
            parameters = [spinner.text for spinner in whole_dropdowns[0]]
            dwnld_type='img'
            parameter_keys=self.img_par_list
        elif vid_sel_chkbox.active:
            parameters = [spinner.text for spinner in whole_dropdowns[1]]
            dwnld_type='vid'
            parameter_keys=self.vid_par_list
        else:
            parameters = [spinner.text for spinner in whole_dropdowns[2]]
            dwnld_type='bth'
            parameter_keys=self.bth_par_list
        
        requests = self.form_requests(textboxes, parameters, parameter_keys, dwnld_type,editor_choice.active)
        
        if requests:
            #urllib.request = urlrequest
            file_numbering = 1 #simple numbering scheme
            path = os.path.join(output_fld.text, dwnld_type+str(file_numbering)+'.jpg')
            for request in requests['img']:
                
                json_result = urlrequest.urlopen(request).read().decode()
                json_result = json.loads(json_result)
                # for elements in json['hits']:
                    # print(elements)


                for urls in json_result['hits']:
                    image_url = urls['largeImageURL']
                

                try:
                    with open(path, 'xb') as something:
                        pass
                except FileExistsError:
                    #file already exists so assign a new name
                    pass



    def form_requests(self, text_values, parameters, parameter_keys, dwnld_type, editor_choice:"editor's choice image results"):
        """form the request url string and return them as lists"""

        image_parameters = [1,7]
        video_parameters = [2] #since this is lesser than image parameters , we use this

        _quantity= text_values[0].text
        quantity = int(Values.quantity) if (not _quantity) else int(_quantity) 
        
        search = text_values[1].text.strip().replace(' ', '+')
        multisearch = text_values[2].text

        requests = {'img': [], 'vid': []}
        base_params = {'img': '', 'vid': ''}
        
        #input error detection during fetch
        if (quantity < 3):
            custom_popup("Quantity must be at least 1", 'Error')
            return None

        if multisearch:
            search_terms = multisearch.strip().split(',')
            
            #stripping any further is of no use, because the user can enter
            #<some_words><comma><space><comma><space><comma>.... and so on, so, it has to be checked later

            search_terms = [terms.strip().replace(' ', '+') for terms in search_terms]
            if search != '':
                search_terms += [search]
        elif search:
            search_terms = [search]
        else:
            custom_popup('At least one search item must be specified', 'Error')
            return None
        
        search_terms = [items for items in search_terms if items != '']
        search_terms = list(set(search_terms)) #convert it into a unique list

        #alter any pornograhic search terms here
        #     TO DO                            #
        
        list_length = len(parameters)
        
        if dwnld_type == 'bth':
            for i in range(1,  list_length):
                if (parameters[i]!='any' and parameters[i]!='all'):
                    if i in video_parameters:
                        base_params['vid'] += self.parameter_structure.format(parameter_keys[i],parameters[i])
                    elif i in image_parameters:
                        base_params['img'] += self.parameter_structure.format(parameter_keys[i],parameters[i])
                    else:
                        base_params['img'] += self.parameter_structure.format(parameter_keys[i],parameters[i])
                        base_params['vid'] += self.parameter_structure.format(parameter_keys[i],parameters[i])

        else:
            for i in range(1, list_length):
                if (parameters[i]!='any' and parameters[i]!='all'):
                    base_params[dwnld_type] += self.parameter_structure.format(parameter_keys[i],parameters[i])


        #formulate the urls inaccording to quantity
        pagination_strings = self.get_condition(len(search_terms), quantity, dwnld_type)
        editor_choice = self.parameter_structure.format('editors_choice', 'true') if editor_choice else ''

        if base_params['img']:
            for search_term in search_terms:
                for pagination in pagination_strings:
                    requests['img'].append(self.type_base_url['img']+self.parameter_structure.format('q', search_term)+\
                                            base_params['img']+editor_choice+pagination)

        if base_params['vid']:
            for search_term in search_terms:
                for pagination in pagination_strings:
                    requests['vid'].append(self.type_base_url['vid']+self.parameter_structure.format('q', search_term)+\
                                            base_params['vid']+editor_choice+pagination)
        

    def get_condition(self, total_items, quantity, dwnld_type):
        """  specifies if the urls 
        are to be splitted, paginated, numbered, to satisfy the 
        quantity need to as far as possible"""

        #say there are 3 search terms, then the total quantity is to be
        #divided by 3 and the sum total of the results
        #is equal to the quantity
        #e.g. car, bike, would download 30 cars and 30 bike
        #images if the quantity is 60

        #dwnld_each describes how much each search_term image could 

        dwnld_each = int(quantity/total_items)+1        #download approximately the given quantity
        pagination_strings = []
        pagination_structure = '&page={}&per_page={}'

        print("The download each is: ", dwnld_each)
        print("The total items is: ", total_items)
        print("The quantity is: ", quantity)

        if (dwnld_each>200):

            #num_pages: number of pages to generate
            #per_page: allowed quantity to fetch per page
            per_page = 200
            num_pages = int(dwnld_each/per_page)
            curpage = 0 #next page number value after the for loop
            
            for i in range(1, num_pages+1):
                pagination_strings.append(pagination_structure.format(i, per_page))
                curpage = i+1
                dwnld_each -= per_page

            dwnld_each = 3 if dwnld_each < 3 else dwnld_each
            pagination_strings.append(pagination_structure.format(curpage, dwnld_each))

        else:
            #if search items are more than the number of downloads then, 
            #we gotta get the downloads equal to at least the number of search terms
            if total_items > dwnld_each:
                dwnld_each = total_items

            dwnld_each = 3 if dwnld_each<3 else dwnld_each
            pagination_strings.append(pagination_structure.format(1, dwnld_each))
        
        print("The pagination strings are: ", pagination_strings)
        
        return pagination_strings
    ###############################################################################################