#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _

PRODUCT = 'ReplaceR'
VERSION = '1.1'
ICON = sh.objs.get_pdir().add('..','resources','replacer.gif')


class Menu:
    
    def __init__(self):
        self.WatchActive = False
        self.set_gui()
    
    def set_gui(self):
        title = sh.List(lst1=[PRODUCT,VERSION]).space_items()
        self.parent = sh.Top (title = title
                             ,icon = ICON
                             )
        self.set_buttons()
        self.set_bindings()
        
    def set_buttons(self):
        self.btn_dic = sh.Button (parent = self.parent
                                 ,text = _('Modify the dictionary')
                                 ,side = 'top'
                                 )
        self.btn_inp = sh.Button (parent = self.parent
                                 ,text = _('Modify the input file')
                                 ,side = 'top'
                                 )
        self.btn_apl = sh.Button (parent = self.parent
                                 ,text = _('Write the output file')
                                 ,side = 'top'
                                 )
        self.btn_wtc = sh.Button (parent = self.parent
                                 ,action = self.toggle_watch
                                 ,text = _('Start clipboard watch')
                                 ,side = 'top'
                                 )
        sh.Button (parent = self.parent
                  ,action = self.close
                  ,text = _('Quit')
                  ,side = 'top'
                  )
        self.btn_dic.focus()
    
    def toggle_watch(self,event=None):
        if self.WatchActive:
            self.WatchActive = False
            self.btn_wtc.set_title(_('Start clipboard watch'))
            self.btn_wtc.widget.config(fg='black')
        else:
            self.WatchActive = True
            self.btn_wtc.set_title(_('Stop clipboard watch'))
            self.btn_wtc.widget.config(fg='red')
        
    def focus_next(self,event=None):
        # If this does not work, set 'takefocus=1'
        event.widget.tk_focusNext().focus()
        return 'break'
        
    def focus_prev(self,event=None):
        # If this does not work, set 'takefocus=1'
        event.widget.tk_focusPrev().focus()
        return 'break'
    
    def set_bindings(self):
        sh.com.bind (obj = self.parent
                    ,bindings = ['<Control-q>','<Control-w>','<Escape>']
                    ,action = self.close
                    )
        sh.com.bind (obj = self.parent
                    ,bindings = '<Down>'
                    ,action = self.focus_next
                    )
        sh.com.bind (obj = self.parent
                    ,bindings = '<Up>'
                    ,action = self.focus_prev
                    )

    def show(self,event=None):
        self.parent.show()

    def close(self,event=None):
        self.parent.close()


if __name__ == '__main__':
    sh.com.start()
    Menu().show()
    sh.com.end()
