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
        
        self.curindex=0
        self.image_list=[]

        def yield_list(path):
            """yield items in path"""
            for i in os.listdir(path):
                yield i
        
        def create_list(Type='img'):
            """create a new list on every list_size_item preview"""
            list_size=10
            for i in range(list_size):
                try:
                    x = next(self.gen_obj)
                    print('try executed')
                except:
                    print('except executed')
                    return None
                else:
                    print('finally executed')
                    if Type=='img':
                        if (x.endswith('.jpg') or x.endswith('.png')):
                            self.image_list.append(x)
                        elif (x.endswith('.svg')):
                            self.image_list.append(os.path.join(os.getcwd(),'no_svg.png'))



        image_dir = paramholder.get('textboxes')[3]
        image_display = paramholder.get('img_display')
        self.image_info = paramholder.get('image_info')
        prev_btn = paramholder.get('prev_btn')
        next_btn = paramholder.get('next_btn')
        display = paramholder.get('img_display')
        prvw_chkbox = paramholder.get('prvw_chkbx')
        prvw_label = paramholder.get('prvw_label')

        img_sel_chkbox = apiholder.get('img_sel_chkbx')
        vid_sel_chkbox = apiholder.get('vid_sel_chkbx')

        image_dir_path = image_dir.text if image_dir.text.strip() != '' else Values.def_path

        self.gen_obj = yield_list(image_dir_path)
        

        def select_behaviour(*objs):
            img_sel_chkbox, prvw_chkbox, image_display, prev_btn, next_btn, image_dir = objs

            if img_sel_chkbox.active:
                create_list(Type='img')
                if prvw_chkbox.active:
                    self.image_info.text=''            
                    prvw_chkbox.active=False
                    image_display.source='none.png'
                    prev_btn.bind(on_press=lambda *_: None)
                    next_btn.bind(on_press=lambda *_: None)
                else:
                    prvw_chkbox.active=True
                    create_list(Type='img')
                    if self.image_list:
                        try:
                            image_display.source=os.path.join(image_dir.text, self.image_list[self.curindex])
                            self.curindex += 1
                        except IndexError:
                            self.curindex-=1
                            if self.image_list:
                                #self.image_list[self.curindex]
                                return os.path.join(image_dir.text, self.image_list[self.curindex])
                            else:
                                return 'none.png'
                    else:
                        image_display.source='none.png'

                    
                    def getimagenext(image_dir):
                        
                        print("The list is: ", self.image_list)
                        print("The current index is: ", self.curindex)
                        try:
                            item = self.image_list[self.curindex]
                            if (os.path.exists(item)):
                                x = item
                            else:
                                x = os.path.join(image_dir.text, self.image_list[self.curindex])
                        except IndexError:
                            # if index is out of bound
                            # then reset to last element
                            self.curindex-=1
                            if self.image_list:
                                #self.image_list[self.curindex]
                                return os.path.join(image_dir.text, self.image_list[self.curindex])
                            else:
                                return 'none.png'
                        else:
                            self.curindex += 1
                            name = x.split(os.sep)[-1] #strip the directory out
                            self.image_info.text='' if 'svg' in name else name
                            return x
                        
                    def getimageprev(image_dir):
                        
                        print("The list is: ", self.image_list)
                        print("The current index is: ", self.curindex)
                        try:
                            if self.curindex<0: raise IndexError
                            item=self.image_list[self.curindex]
                            if(os.path.exists(item)):
                                x = item
                            else:
                                x = os.path.join(image_dir.text, self.image_list[self.curindex])
                        except IndexError:
                            self.curindex += 1
                            if self.image_list:
                                return os.path.join(image_dir.text, self.image_list[self.curindex])
                            else:
                                return 'none.png'
                        else:
                            self.curindex -=1
                            return x

                    next_btn.bind(on_press=lambda*_: setattr(image_display, 'source', getimagenext(image_dir)))
                    prev_btn.bind(on_press=lambda*_: setattr(image_display, 'source', getimageprev(image_dir)))

                    
        
        prvw_label.bind(on_ref_press=lambda*_: select_behaviour(img_sel_chkbox,
                                prvw_chkbox,image_display, prev_btn, next_btn,
                                image_dir))
        # next_btn.bind(on_press=lambda *_: setattr(image_display, 'source', next_file(self.files, image_dir_path)))

    ###############################################################################################