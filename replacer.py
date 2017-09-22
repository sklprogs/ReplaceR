#!/usr/bin/python3

import shared as sh
import sharedGUI as sg
import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('replacer','./locale')

product = 'ReplaceR'
version = '1.0'
globs   = {'dic':'dic.txt','file':'in.txt','file_w':'out.txt'}



class Commands:
    
    def open_dic(self,*args):
        sh.Launch(target=globs['dic']).default()
        sg.Message (func    = 'Commands.open_dic'
                   ,level   = _('INFO')
                   ,message = _('Press OK to reload the dictionary now.')
                   )
        objs.reset()
        objs.dic()
        
    def open_input(self,*args):
        sh.Launch(target=globs['file']).default()
        
    def apply2file(self,*args):
        text = sh.ReadTextFile(file=globs['file']).get()
        if text:
            text = objs.apply().apply(text=text)
            sh.WriteTextFile (file       = globs['file_w']
                             ,AskRewrite = False
                             ).write(text)
            sh.Launch(target=globs['file_w']).default()
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
        self.obj = sg.objs.new_top(Maximize=0)
        self.title()
        self.buttons()
        self.bindings()
        
    def buttons(self):
        sg.Button (parent_obj = self.obj
                  ,action     = Commands().open_dic
                  ,text       = _('Modify the dictionary')
                  ,side       = 'top'
                  ,TakeFocus  = True
                  )
                 
        sg.Button (parent_obj = self.obj
                  ,action     = Commands().open_input
                  ,text       = _('Modify the input file')
                  ,side       = 'top'
                  )
        
        sg.Button (parent_obj = self.obj
                  ,action     = Commands().apply2file
                  ,text       = _('Write the output file')
                  ,side       = 'top'
                  )
                 
        self.watch_btn = sg.Button (parent_obj = self.obj
                                   ,action     = self.toggle_watch
                                   ,text       = _('Start clipboard watch')
                                   ,side       = 'top'
                                   )
                                   
        sg.Button (parent_obj = self.obj
                  ,action     = self.close
                  ,text       = _('Quit')
                  ,side       = 'top'
                  )
    
    def toggle_watch(self,*args):
        if self.WatchActive:
            self.WatchActive = False
            self.watch_btn.title(_('Start clipboard watch'))
            self.watch_btn.widget.config(fg='black')
        else:
            self.WatchActive = True
            self.watch_btn.title(_('Stop clipboard watch'))
            self.watch_btn.widget.config(fg='red')
        
    def focus_next(self,event,*args): # If this does not work, set 'takefocus=1'
        event.widget.tk_focusNext().focus()
        return 'break'
        
    def focus_prev(self,event,*args): # If this does not work, set 'takefocus=1'
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

    def show(self,*args):
        self.obj.show()

    def close(self,*args):
        self.obj.close()
        
    def title(self,arg=None):
        if not arg:
            arg = sh.List(lst1=[product,version]).space_items()
        self.obj.title(arg)



class Objects:
    
    def __init__(self):
        self._menu = None
        self.reset()
        
    def reset(self):
        self._dic = self._apply = self._watch = None
    
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
                           ,message = _('The condition "%s" is not observed!') % (len(self.orig) + ' == ' + len(self.transl))
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
