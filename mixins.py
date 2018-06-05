class Change_mixin:
    def apply_changes(self, changes, opt=None):
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
                # ('Add', [(Button, {properties}),
                #           (Button, {properties1})]  )

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
                        print()
                        print("dynwin is: ", dynwid)
                        # time.sleep(10)
                        print()
                        self.dynwids.append(dynwid[0](**(dynwid[1])))
                    
                    for dynwid in self.dynwids:
                        parent.add_widget(dynwid)

class Fetch_mixin:
    def get(self, prop_2_fetch):
        return self.interface[prop_2_fetch]
