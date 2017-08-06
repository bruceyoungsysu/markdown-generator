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
    def __init__(self,handler,blocks):
        self.type = ''
        self.handler = handler
        self.condition = []
        self.blocks = blocks
    def apply_sub(self,condition,self.blocks):
        for block in self.blocks:
            self.handler.sub(condition,block)
    def add_condition(self,cond):
        self.condition.append(cond)
       
    def apply(self,start_block,end_block,self.blocks):
        self.handler.start(self.type,start_block)
        self.handler.end(self.type,end_block)
        for condition in self.condition:
            self.apply_sub(condition,self.blocks)
   
   
class file_rules(Rules):#apply each handler to each corresponding blocks.Rule is a detector.
    def __init__(self,handler,blocks):
        Rules.__init__(self,handler,blocks)
        self.start_block = self.blocks[0]
        self.end_block = self.blocks[-1]
          
class title_rules(Rules):
    def __init__(self,handler,blocks):
        Rules.__init__(self,handler,blocks)
        self.start_block = self.title_block(blocks)
        self.end_block = self.title_block(blocks)
    def title_match(self,blocks):
        for block in blocks:
            if re.match('t|Tiltle:',block):
                return block
            
class body_rules(Rules):
    def __init__(self,handler,blocks):
        Rules.__init__(self,handler,blocks)
        self.type = 'body'
        self.condition = []
        self.start_block = self.body_match(self.blocks)
        self.end_block = self.blocks[-1]
        
    def body_match(self,blocks):
        block = blocks.next()
        while not re.match('t|Title:',block):
            block = blocks.next()
        block = blocks.next()
        return block
        
class url_rules(Rules):
    def __init__(self,handler):
        Rules.__init__(self,handler)
        #self.condition = ['url']
        self.type = 'url'
        

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
    def sub_url(self,block):
        pattern = 'http:\\www.[0-9a-zA-Z]+.com'
        for item in re.finditer(pattern,block):
            if item != None:
                repl = '<a herf = %s></a>' %item
                re.sub(item,repl,string)

def __main__():
    