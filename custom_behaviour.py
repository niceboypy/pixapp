import kivy
from kivy.uix.videoplayer import VideoPlayer

class Behaviour:

    def add_behaviour(self):
        self.add_search_type_behaviour(self.apiholder, self.paramholder)


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
    

