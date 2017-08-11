# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 17:40:04 2017

@author: bruyang
"""

import argparse
import re
import os

def CommandParser():
    '''
    Parse the user input command especially txt file path.
    returns : txt file path.
    '''
    parser = argparse.ArgumentParser(discription = 'Please input a valid TxT file for conversion.')
    parser.add_argument('file_path',type = str)
    args = parser.parse_args()
    
    txt_path = args.file_path
    
    if not os.existspath(txt_path):
        raise UserWarning('Please input a valid path!') # distingush between file and folder?
        
    return txt_path

def FileParser(file_path): #parse a txt file to blocks.
    '''
    parse the txt file to seperate blocks. Each block is like a paragraph.
    returns : generator of blocks
    '''
    f = open(file_path,'r')
    lines = f.readlines()
    f.close()
    block = []
    blocks = []
    for line in lines:
        if line.strip():
            block.append(line)
        elif block:
            blocks.append(''.join(block))
    return blocks
   
   
   
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
        #for block in blocks:
            #match content with re module.
        pass
        
class TextParser(Parser):
    def __init__(self,handler):
        Parser.__init__(self)
        self.handler = handler
        
    def ParseText(self):
        for rule in self.rules:
            rule.apply()
        for setting in self.settings:
            setting.apply()
                
    def Gen_file(self,blocks):
        for rule in self.rules:
            blocks = rule.apply(blocks)
        return blocks


class Rules: #Rules applied to each block of text.
    def __init__(self,handler,blocks):
        self.type = ''
        self.handler = handler
        self.condition = []
        self.blocks = blocks
        
    def apply_sub(self,condition):
        for block in self.blocks:
            self.handler.sub(condition,block)
    def add_condition(self,cond):
        self.condition.append(cond)
       
    def apply(self,blocks):
               
        new_start = self.handler.start(self.type,blocks[self.start_num])
        new_end = self.handler.end(self.type,blocks[self.end_num])        
        repl = []
        for item in blocks:
            if item  == blocks[self.start_num]:
                repl.append(new_start)
            elif item == blocks[self.end_num]:
                repl.append(new_end)
            else: 
                repl.append(item)
        
        for condition in self.condition:
            for block in blocks:
                self.apply_sub(condition,block)
        blocks = repl
        
        return blocks

   
class file_rules(Rules):#apply each handler to each corresponding blocks.Rule is a detector.
    def __init__(self,handler,blocks):
        Rules.__init__(self,handler,blocks)
        self.type = 'file'
        self.start_num = 0
        self.end_num = -1
          
class title_rules(Rules):
    def __init__(self,handler,blocks):
        Rules.__init__(self,handler,blocks)
        self.start_num = self.title_match(blocks)
        self.end_num = self.title_match(blocks)
        self.type = 'title'
    def title_match(self,blocks):
        for block in blocks:
            if re.match('t|Tiltle:',block):
                return blocks.index(block)
            
class body_rules(Rules):
    def __init__(self,handler,blocks):
        Rules.__init__(self,handler,blocks)
        self.type = 'body'
        self.condition = []
        self.start_block = self.body_match(self.blocks)
        self.end_num = -1
        
    def body_match(self,blocks):
        for block in blocks:
            while re.match('t|Title:',block):
                return blocks.index(block) + 1
        
class url_rules(Rules):
    def __init__(self,handler,blocks):
        Rules.__init__(self,handler,blocks)
        #self.condition = ['url']
        self.type = 'url'
        

class Handler(): #how to handle each section.
    def callfuction(self,preflix,name,*args):
        method = getattr(self,preflix+name,None)
        if callable(method):return method(*args)
            
    def start(self,name,block):
        return self.callfuction('start_',name,block)
        
        
    def end(self,name,block):
        return self.callfuction('end_',name,block)
        
    def sub(self,name,pattern,block):
        block = self.callfuction('sub_',name,block)
        
class HTML_handler(Handler):
    def start_file(self,block):        
        return '<html>'+block
        
    def end_file(self,block):
        return block + '</html>'
    def start_title(self,block):
        return '<head><title>' +block
    def end_title(self,block):
        return block + '</title></head>'
    def start_body(self,block):
        return '<body>'+block
    def end_body(self,block):
        return block + '</body>'
    def sub_url(self,block):
        pattern = 'http:\\www.[0-9a-zA-Z]+.com'
        for item in re.finditer(pattern,block):
            if item != None:
                repl = '<a herf = %s></a>' %item
                re.sub(item,repl,block)

def main():
    #file_path = CommandParser()
    file_path = "./test.txt"
    g=FileParser(file_path)
    handler = HTML_handler()
    parser = TextParser(handler)
    candi = []
    for typename in candi:
        method = typename + '_rules'        
        if callable(method):
            typename + 'rules' = method(handler,g)
            parser.AddRule()
    filerules = file_rules(handler,g)
    titlerules = title_rules(handler,g)

    parser.AddRule(filerules)
    parser.AddRule(titlerules)
    
    print parser.Gen_file(g)
    print g
    
    
if __name__ == '__main__':
    main()
    