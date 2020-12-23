#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import shared    as sh
import sharedGUI as sg

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('replacer','../resources/locale')


class Menu:
    
    def __init__(self):
        self.values()
        self.gui()
        
    def values(self):
        self.WatchActive = False
    
    def gui(self):
        self.obj = sg.objs.new_top()
        self.buttons()
        self.bindings()
        
    def buttons(self):
        self.btn_dic = sg.Button (parent = self.obj
                                 ,text = _('Modify the dictionary')
                                 ,side = 'top'
                                 )
        self.btn_inp = sg.Button (parent = self.obj
                                 ,text = _('Modify the input file')
                                 ,side = 'top'
                                 )
        self.btn_apl = sg.Button (parent = self.obj
                                 ,text = _('Write the output file')
                                 ,side = 'top'
                                 )
        self.btn_wtc = sg.Button (parent = self.obj
                                 ,action = self.toggle_watch
                                 ,text = _('Start clipboard watch')
                                 ,side = 'top'
                                 )
        sg.Button (parent = self.obj
                  ,action = self.close
                  ,text = _('Quit')
                  ,side = 'top'
                  )
        self.btn_dic.focus()
    
    def toggle_watch(self,event=None):
        if self.WatchActive:
            self.WatchActive = False
            self.btn_wtc.title(_('Start clipboard watch'))
            self.btn_wtc.widget.config(fg='black')
        else:
            self.WatchActive = True
            self.btn_wtc.title(_('Stop clipboard watch'))
            self.btn_wtc.widget.config(fg='red')
        
    # If this does not work, set 'takefocus=1'
    def focus_next(self,event=None):
        event.widget.tk_focusNext().focus()
        return 'break'
        
    # If this does not work, set 'takefocus=1'
    def focus_prev(self,event=None):
        event.widget.tk_focusPrev().focus()
        return 'break'
    
    def bindings(self):
        sg.bind (obj = self.obj
                ,bindings = ['<Control-q>','<Control-w>','<Escape>']
                ,action = self.close
                )
        sg.bind (obj = self.obj
                ,bindings = '<Down>'
                ,action = self.focus_next
                )
        sg.bind (obj = self.obj
                ,bindings = '<Up>'
                ,action = self.focus_prev
                )

    def show(self,event=None):
        self.obj.show()

    def close(self,event=None):
        self.obj.close()


if __name__ == '__main__':
    sg.objs.start()
    Menu().show()
    sg.objs.end()
