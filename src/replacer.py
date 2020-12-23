#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import skl_shared.shared as sh
from skl_shared.localize import _
import gui as gi

default_dic = '''Enter text here.	Введите текст здесь.
This file must be tab-delimited.	Оригинал и перевод в этом файле должны быть разделены табуляцией.
nice	красивая
hat	шляпа'''
default_r = 'You have a nice hat!'

share_dir = sh.Home(gi.PRODUCT.lower()).get_share_dir()
sh.Path(share_dir).create()
file_dic = os.path.join(share_dir,'dic.txt')
file_r = os.path.join(share_dir,'in.txt')
file_w = os.path.join(share_dir,'out.txt')

if not os.path.exists(file_dic):
    sh.WriteTextFile(file_dic).write(default_dic)
if not os.path.exists(file_r):
    sh.WriteTextFile(file_r).write(default_r)



class Commands:
    
    def open_dic(self,event=None):
        f = '[ReplaceR] replacer.Commands.open_dic'
        text = sh.ReadTextFile(file_dic).get()
        objs.get_txt().reset(text)
        objs.txt.show()
        text = objs.txt.get()
        if text:
            sh.WriteTextFile (file = file_dic
                             ,Rewrite = True
                             ).write(text=text)
            objs.reset()
            objs.get_dic()
        else:
            sh.com.rep_empty(f)
        
    def open_input(self,event=None):
        f = '[ReplaceR] replacer.Commands.open_input'
        text = sh.ReadTextFile(file_r).get()
        objs.get_txt().reset(text)
        objs.txt.show()
        text = objs.txt.get()
        if text:
            sh.WriteTextFile (file = file_r
                             ,Rewrite = True
                             ).write(text)
        else:
            sh.com.rep_empty(f)
        
    def apply2file(self,event=None):
        f = '[ReplaceR] replacer.Commands.apply2file'
        text = sh.ReadTextFile(file_r).get()
        if text:
            text = objs.get_apply().apply(text)
            sh.WriteTextFile (file = file_w
                             ,Rewrite = True
                             ).write(text)
            objs.get_txt_ro().reset(text)
            objs.txt_ro.show()
        else:
            sh.com.rep_empty(f)



class Menu:
    
    def __init__(self):
        self.gui = gi.Menu()
        self.set_bindings()
        
    def set_bindings(self):
        self.gui.btn_dic.action = Commands().open_dic
        self.gui.btn_inp.action = Commands().open_input
        self.gui.btn_apl.action = Commands().apply2file

    def show(self,event=None):
        self.gui.show()

    def close(self,event=None):
        self.gui.close()



class Objects:
    
    def __init__(self):
        self.menu = self.txt = self.txt_ro = None
        self.reset()
        
    def reset(self):
        self.dic = self.apply = self.watch = None
    
    def get_txt_ro(self):
        if not self.txt_ro:
            self.txt_ro = sh.TextBoxRO (title = _('Check text:')
                                       ,icon = gi.ICON
                                       )
        return self.txt_ro
    
    def get_txt(self):
        if not self.txt:
            self.txt = sh.TextBoxRW (title = _('Edit text:')
                                    ,icon = gi.ICON
                                    )
        return self.txt
    
    def get_watch(self):
        if not self.watch:
            self.watch = Watch()
        return self.watch
    
    def get_apply(self):
        if not self.apply:
            self.apply = Apply (orig = objs.get_dic().orig
                               ,transl = objs.dic.transl
                               )
        return self.apply
    
    def get_dic(self):
        if not self.dic:
            self.dic = sh.Dic (file = file_dic
                              ,Sortable = True
                              )
            self.dic.sort()
        return self.dic
        
    def get_menu(self):
        if not self.menu:
            self.menu = Menu()
        return self.menu



class Watch:
    
    def __init__(self):
        self.old = ''
    
    def watch(self):
        if objs.get_menu().gui.WatchActive:
            paste = sh.Clipboard(Silent=1).paste()
            if paste != self.old:
                text = objs.get_apply().apply(paste)
                sh.Clipboard().copy(text)
                self.old = paste
        sh.objs.get_root().widget.after(1000,self.watch)



class Apply:
    
    def __init__(self,orig,transl):
        self.orig = orig
        self.transl = transl
        self.Success = True
        self.check()
    
    def check(self):
        f = '[ReplaceR] replacer.Apply.check'
        if self.orig and self.transl:
            if len(self.orig) != len(self.transl):
                self.Success = False
                sub = '{} == {}'.format (len(self.orig)
                                        ,len(self.transl)
                                        )
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                sh.objs.get_mes(f,mes).show_warning()
        else:
            self.Success = False
            sh.com.rep_empty(f)
                          
    def apply(self,text):
        f = '[ReplaceR] replacer.Apply.apply'
        if self.Success:
            if text:
                for i in range(len(self.orig)):
                    text = text.replace(self.orig[i],self.transl[i])
                return text
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)


objs = Objects()


if __name__ == '__main__':
    f = '[ReplaceR] replacer.__main__'
    sh.com.start()
    objs.get_watch().watch()
    objs.get_menu().show()
    mes = _('Goodbye!')
    sh.objs.get_mes(f,mes,True).show_debug()
    sh.com.end()
