# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 17:40:04 2017

@author: bruyang
"""

import argparse
import os
import re

def CommandParser():
    '''
    Parse the user input command especially txt file path.
    returns : txt file path.
    '''
    parser = argparse.ArgumentParser(discription = 'Please input a valid TxT file for conversion.')
    parser.add_argument('file_path',type = str)
    args = parser.parse_args()
    
    txt_path = args.file_path
    
    if not existspath(txt_path):
        raise UserWarning('Please input a valid path!') # distingush between file and folder?
        
    return txt_path

def FileParser(file_path): #parse a txt file to blocks.
    '''
    parse the txt file to seperate blocks. Each block is like a paragraph.
    returns : generator of blocks
    '''
    f = os.open(file_path,'r')
    lines = f.readlines()
    f.close()
    block = []
    for line in lines:
        if line.strip():
            block.append(line)
        elif block:
            yield ''.join(block)
   
   
   
class Parser: #Parse each setting and rule to each block
    def __init__(self):
        self.rules = []
        self.settings = []
        
    def AddRule(self,Rule):
        self.rules.append(Rule)
    def AddSetting(self,Setting):
        self.settings.append(Setting)
                       
class SettingParser(Parser):
    def ParseSetting(self,blocks):
        for block in blocks:
            #match content with re module.
        pass
        
class TextParser(Parser):
    def __init__(self,handler):
        Parser.__init__(self)
        self.handler = handler
        
    def ParseText(self,blocks):
        for rule in self.rules:
            rule.apply(blocks)
        for setting in self.settings:
            setting.apply(blocks)
                
    def Gen_file(self,blocks):
        pass


class Rules: #Rules applied to each block of text.
    def __init__(self,handler):
        self.type = ''
        self.handler = handler
        self.condition = []
    '''    
    def apply(self,blocks):
        self.handler.start(self.type)
        self.handler.end(self.type)
        for condition in self.condition:
            self.handler.sub(self,condition,blocks)
   '''
   
class file_rules(Rules):#apply each handler to each corresponding blocks.Rule is a detector.
        
    def apply(self,blocks):
        blocks[0]=self.handler.start_file() + blocks[0]
        blocks[-1]=block[-1] + self.handler.start_file()
        
          
class title_rules(Rules):
        
    def apply(self,blocks):
        for block in blocks:
            if re.match('t|Tiltle:',block):
                block = self.handler.start_title() + block + self.handler.end_title()
                break
            
class body_rules(Rules):
    def __init__(self,handler):
        Rules.__init__(self,handler)
        #self.type = ''
        self.condition = []
        
    def apply(self,blocks):
        
class url_rules(Rules):
    def __init__(self,handler):
        Rules.__init__(self,handler)
        self.condition = []
        
    def apply(self, blocks):

class Handler(): #how to handle each section.
    def callfuction(self,preflix,name,*args):
        method = getattr(self,preflix+name,None)
        if callable(method):return method(*args):
            
    def start(self,name):
        self.callfuction('start_',name)
        
    def end(self,name):
        self.callfuction('end_',name)
        
    def sub(self,name,pattern,block):
        self.callfuction('sub_',name,item,block)
        
class HTML_handler(Handler):
    def start_file(self):
        yield '<html>'
    def end_file(self):
        yield '</html>'
    def start_title(self):
        yield '<head><title>'
    def end_title(self):
        yield '</title></head>'
    def start_body(self):
        yield '<body>'
    def end_body(self):
        yield '</body>'
    def sub_url(self,item,block):
        pattern = 'http:\\www.[0-9a-zA-Z]+.com'
        for item in re.finditer(pattern,block):
            if item != None:
                repl = '<a herf = %s></a>' %item
                re.sub(item,repl,string)
        