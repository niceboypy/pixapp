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
        video_panel = VideoPlayer(source='soapbubble.mp4')


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

    ##########################BEHAVIOUR FOR BROWSER BUTTON #24D$ #####################################################################
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
            nonlocal output_fld
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
        
        