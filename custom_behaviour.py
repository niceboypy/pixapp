import kivy
from kivy.uix.videoplayer import VideoPlayer
from par_values import Values
import os
from custom_widgets import save_dialog
from kivy.uix.popup import Popup

class Behaviour:

    def add_behaviour(self):
        #behaviour for top 3 left radio buttons #search id in the file: #23D$
        self.add_search_type_behaviour(self.apiholder, self.paramholder)
        
        #behaviour for browsing button#search id:
        self.add_browser_behaviour(self.paramholder)

        #behaviour for preview panel
        self.add_preview_behaviour(self.apiholder, self.paramholder)

    ####################### BEHAVIOUR FOR RADIO BUTTONS: #23D$ ############################
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
        from_parent = paramholder.get('drpdwn_par')

        extra_dropdown = paramholder.get('dropdowns')[6]
        display_par = paramholder.get('display_par')
        image_panel = paramholder.get('img_display')
        video_panel = VideoPlayer()#source='magic.mp4')


        Bind(img_sel_lab, on_ref_press =  lambda *_: self.switch('add',sch_typ_pan, img_sel_chkbx, extra_dropdown, from_parent, video_panel, display_par, image_panel))
        Bind(vid_sel_lab, on_ref_press =  lambda *_: self.switch('remove',sch_typ_pan, vid_sel_chkbx, extra_dropdown, from_parent, image_panel, display_par, video_panel))
        Bind(bth_sel_lab, on_ref_press =  lambda *_: self.switch('add',sch_typ_pan, bth_sel_chkbx, extra_dropdown, from_parent))
    
    def switch(self, action, panel, obj, rmv_widgt, from_parent, replc_pan=None, from_dis_par=None, with_pan=None):
        panel.setstatus(obj)
        if action =='remove':
            from_parent.remove_widget(rmv_widgt)
            try:
                from_dis_par.remove_widget(replc_pan)
                from_dis_par.add_widget(with_pan)
            except: 
                pass
            
        else:
            try:
                from_parent.add_widget(rmv_widgt)
                from_dis_par.remove_widget(replc_pan)
                from_dis_par.add_widget(with_pan)

                print("Try run")
            except:
                print("Exception")
    ###############################################################################################

    ########################## BEHAVIOUR FOR BROWSER BUTTON #24D$ #####################################################################
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
        
    ######################### BEHAVIOUR FOR PREVIEW PANEL #################################
    def add_preview_behaviour(self, apiholder, paramholder):
        
        self.curindex=-1
        self.image_list=[]

        def yield_list(path):
            """yield items in path"""
            for i in os.listdir(path):
                yield i
        
        def create_list(Type='img'):
            """create a new list on every list_size_item preview"""
            list_size=13 #the list size to be generated
            for i in range(list_size):
                try:
                    x = next(self.gen_obj)
                except:
                    return None
                else:
                    if Type=='img':
                        if (x.endswith('.jpg') or x.endswith('.png')):
                            self.image_list.append(x)
                        elif (x.endswith('.svg')):
                            self.image_list.append(os.path.join(os.getcwd(),'no_svg.png'))
            
            # denotes if list contains items
            if self.image_list:
                return True
            else:
                return False


        image_dir = paramholder.get('textboxes')[3]
        image_display = paramholder.get('img_display')

        self.prev_dir = image_dir.text # save the value of previous directory - to   
                                       # check against the output path 
                                       # to form a list

        self.image_info = paramholder.get('image_info')
        self.image_info.text='Preview images on output path'

        prev_btn = paramholder.get('prev_btn')
        next_btn = paramholder.get('next_btn')
        display = paramholder.get('img_display')
        prvw_chkbox = paramholder.get('prvw_chkbx')
        prvw_label = paramholder.get('prvw_label')

        img_sel_chkbox = apiholder.get('img_sel_chkbx')
        vid_sel_chkbox = apiholder.get('vid_sel_chkbx')

        def select_behaviour(*objs):
            """callback on preview selection, selects image and 
                video preview behaviour"""

            img_sel_chkbox, prvw_chkbox, image_display, prev_btn, next_btn, image_dir = objs
            image_dir.text = image_dir.text if os.path.exists(image_dir.text) else Values.def_path

            # create a new generator object on every press of
            # preview reference label, this is the only thing
            # that updates the directory
            #because the directory is traversed using a generator object
            self.gen_obj = yield_list(image_dir.text)


            def getitem(image_dir, inrfac):
                # self.curdir = image_dir 
                nonlocal image_display
                if os.path.exists(image_dir):  
                    #check if the path has changed
                    #if yes, reset all the values
                    #create new generator for the path
                    #and set the list values 
                    if image_dir != self.prev_dir:
                        self.gen_obj = yield_list(image_dir)
                        self.image_list=[]
                        create_list(Type='img')
                        print("The image list is: ", self.image_list)
                        self.curindex=-1

                    self.prev_dir = image_dir

                if self.image_list:
                    try:
                        # try getting image from the
                        # list currently in existence
                        self.curindex += inrfac
                        if self.curindex < 0: self.curindex = 0
                        cur_image = self.image_list[self.curindex]
                        self.prev_image = cur_image
                    except:
                        #if that's an index error
                        try:
                            # see if the list can be extended since
                            # only list item(see in create_list function)
                            # elements can are added to the list at a time to save
                            # memory overhead
                            create_list(Type='img')
                            cur_image = self.image_list[self.curindex]
                            self.curindex += inrfac
                            print("The extended list is: ", self.image_list)
                        except IndexError:

                            if self.curindex > (len(self.image_list)-1):
                                self.curindex = len(self.image_list) -1 
                            elif self.curindex < 0:
                                self.curindex = 0
                            cur_image = self.image_list[self.curindex]

                    if not os.path.exists(cur_image):
                        #if the image found is not a path
                        #then, update the information label
                        #that displays image name above the preview display
                        self.image_info.text=cur_image
                        #then make it into a path and return the value
                        return os.path.join(self.prev_dir, cur_image)
                    else:
                        #return cur_image as one of the condition images
                        #condition images-> e.g. images that represent a state
                        #e.g. invalid=none.png, no_svg.png
                        self.image_info.text=''
                        return cur_image
                else:
                    self.image_info.text='No Images Found'
                    return 'none.png'


            def getprev(image_dir):
                return getitem(image_dir, -1)
            
            def getnext(image_dir):
                return getitem(image_dir, 1)

            if img_sel_chkbox.active:
                #we create a new list
                if create_list(Type='img'):
                    if prvw_chkbox.active:
                        prvw_chkbox.active=False
                        image_display.source='none.png'
                        prev_btn.bind(on_press=lambda *_: None)
                        next_btn.bind(on_press=lambda *_: None)
                        self.image_info.text='Preview images on output path'
                        print("No binding completed,")
                    else:
                        prvw_chkbox.active = True
                        #code to recontinue from previously left spot
                        if self.image_list:
                            if self.curindex <0: self.curindex=0
                            self.image_info.text = self.image_list[self.curindex]
                            if not os.path.exists(image_dir.text):
                                image_dir.text = Values.def_path
                            if os.path.exists(self.image_list[self.curindex]):
                                image_display.source = self.image_list[self.curindex]
                            else:
                                image_display.source = os.path.join(image_dir.text, self.image_list[self.curindex])
                            
                        #rebind buttons to traverse
                        next_btn.bind(on_press=lambda*_: setattr(image_display, 'source', getnext(image_dir.text)))
                        prev_btn.bind(on_press=lambda*_: setattr(image_display, 'source', getprev(image_dir.text)))
                else:
                    self.image_info.text = 'No images found'
                    image_display.source='none.png'
                    prev_btn.bind(on_press=lambda *_: None)
                    next_btn.bind(on_press=lambda *_: None)

        
        prvw_label.bind(on_ref_press=lambda*_: select_behaviour(img_sel_chkbox,
                                prvw_chkbox,image_display, prev_btn, next_btn,
                                image_dir))

    ###############################################################################################