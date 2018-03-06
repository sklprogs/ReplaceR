#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import shared as sh
import sharedGUI as sg
import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('replacer','./locale')

product = 'ReplaceR'
version = '1.0'
globs   = {'dic':'dic.txt','file':'in.txt','file_w':'out.txt'}



class Commands:
    
    def open_dic(self,event=None):
        text = sh.ReadTextFile(file=globs['dic']).get()
        objs.txt().reset_data()
        objs._txt.insert(text=text)
        objs._txt.show()
        text = objs._txt.get()
        if text:
            sh.WriteTextFile (file       = globs['dic']
                             ,AskRewrite = False
                             ).write(text=text)
            objs.reset()
            objs.dic()
        else:
            sh.log.append ('Commands.open_dic'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
        
    def open_input(self,event=None):
        text = sh.ReadTextFile(file=globs['file']).get()
        objs.txt().reset_data()
        objs._txt.insert(text=text)
        objs._txt.show()
        text = objs._txt.get()
        if text:
            sh.WriteTextFile (file       = globs['file']
                             ,AskRewrite = False
                             ).write(text=text)
        else:
            sh.log.append ('Commands.open_input'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
        
    def apply2file(self,event=None):
        text = sh.ReadTextFile(file=globs['file']).get()
        if text:
            text = objs.apply().apply(text=text)
            sh.WriteTextFile (file       = globs['file_w']
                             ,AskRewrite = False
                             ).write(text)
            objs.txt_ro().reset_data()
            objs._txt_ro.insert(text=text)
            objs._txt_ro.show()
        else:
            sh.log.append ('Commands.apply2file'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )



class Menu:
    
    def __init__(self):
        self.values()
        self.gui()
        
    def values(self):
        self.WatchActive = False
    
    def gui(self):
        self.obj = sg.objs.new_top()
        self.title()
        self.buttons()
        self.bindings()
        
    def buttons(self):
        button = sg.Button (parent = self.obj
                           ,action = Commands().open_dic
                           ,text   = _('Modify the dictionary')
                           ,side   = 'top'
                           )
        button.focus()
                 
        sg.Button (parent = self.obj
                  ,action = Commands().open_input
                  ,text   = _('Modify the input file')
                  ,side   = 'top'
                  )
        
        sg.Button (parent = self.obj
                  ,action = Commands().apply2file
                  ,text   = _('Write the output file')
                  ,side   = 'top'
                  )
                 
        self.watch_btn = sg.Button (parent = self.obj
                                   ,action = self.toggle_watch
                                   ,text   = _('Start clipboard watch')
                                   ,side   = 'top'
                                   )
                                   
        sg.Button (parent = self.obj
                  ,action = self.close
                  ,text   = _('Quit')
                  ,side   = 'top'
                  )
    
    def toggle_watch(self,event=None):
        if self.WatchActive:
            self.WatchActive = False
            self.watch_btn.title(_('Start clipboard watch'))
            self.watch_btn.widget.config(fg='black')
        else:
            self.WatchActive = True
            self.watch_btn.title(_('Stop clipboard watch'))
            self.watch_btn.widget.config(fg='red')
        
    # If this does not work, set 'takefocus=1'
    def focus_next(self,event=None):
        event.widget.tk_focusNext().focus()
        return 'break'
        
    # If this does not work, set 'takefocus=1'
    def focus_prev(self,event=None):
        event.widget.tk_focusPrev().focus()
        return 'break'
    
    def bindings(self):
        sg.bind (obj      = self.obj
                ,bindings = ['<Control-q>','<Control-w>','<Escape>']
                ,action   = self.close
                )
        sg.bind (obj      = self.obj
                ,bindings = '<Down>'
                ,action   = self.focus_next
                )
        sg.bind (obj      = self.obj
                ,bindings = '<Up>'
                ,action   = self.focus_prev
                )

    def show(self,event=None):
        self.obj.show()

    def close(self,event=None):
        self.obj.close()
        
    def title(self,arg=None):
        if not arg:
            arg = sh.List(lst1=[product,version]).space_items()
        self.obj.title(arg)



class Objects:
    
    def __init__(self):
        self._menu = self._txt = self._txt_ro = None
        self.reset()
        
    def reset(self):
        self._dic = self._apply = self._watch = None
    
    def txt_ro(self):
        if not self._txt_ro:
            top = sg.objs.new_top()
            sg.Geometry(parent=top).set('800x600')
            self._txt_ro = sg.TextBox (parent        = top
                                      ,SpecialReturn = False
                                      ,state         = 'disabled'
                                      )
            self._txt_ro.state = 'normal'
            self._txt_ro.title(_('Check text:'))
        return self._txt_ro
    
    def txt(self):
        if not self._txt:
            top = sg.objs.new_top()
            sg.Geometry(parent=top).set('800x600')
            self._txt = sg.TextBox (parent        = top
                                   ,SpecialReturn = False
                                   )
            self._txt.title(_('Edit text:'))
        return self._txt
    
    def watch(self):
        if not self._watch:
            self._watch = Watch()
        return self._watch
    
    def apply(self):
        if not self._apply:
            self._apply = Apply (orig   = objs.dic().orig
                                ,transl = objs._dic.transl
                                )
        return self._apply
    
    def dic(self):
        if not self._dic:
            self._dic = sh.Dic (file     = globs['dic']
                               ,Sortable = True
                               )
            self._dic.sort()
        return self._dic
        
    def menu(self):
        if not self._menu:
            self._menu = Menu()
        return self._menu



class Watch:
    
    def __init__(self):
        self.old = ''
    
    def watch(self):
        if objs.menu().WatchActive:
            paste = sg.Clipboard(Silent=1).paste()
            if paste != self.old:
                text = objs.apply().apply(paste)
                sg.Clipboard().copy(text)
                self.old = paste
        sg.objs.root().widget.after(1000,self.watch)



class Apply:
    
    def __init__(self,orig,transl):
        self.orig    = orig
        self.transl  = transl
        self.Success = True
        if self.orig and self.transl:
            if len(self.orig) != len(self.transl):
                self.Success = False
                sg.Message (func    = 'Apply.__init__'
                           ,level   = _('WARNING')
                           ,message = _('The condition "%s" is not observed!') \
                                      % (len(self.orig) + ' == ' \
                                        + len(self.transl)
                                        )
                           )
        else:
            self.Success = False
            sh.log.append ('Apply.__init__'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
                          
    def apply(self,text):
        if self.Success:
            if text:
                for i in range(len(self.orig)):
                    text = text.replace(self.orig[i],self.transl[i])
                return text
            else:
                sh.log.append ('Apply.apply'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Apply.apply'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )



objs = Objects()



if __name__ == '__main__':
    sg.objs.start()
    objs.watch().watch()
    objs.menu().show()
    sg.objs.end()
