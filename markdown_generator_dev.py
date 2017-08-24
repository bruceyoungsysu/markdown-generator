# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 17:40:04 2017

@author: bruyang
"""

#import argparse
import re
#import os
import utils

       
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
        
    def ParseText(self,blocks):
        for rule in self.rules:
            blocks = rule.apply(blocks)
        for setting in self.settings:
            setting.apply()
        return blocks
         
    def Gen_file(self,blocks):
        for rule in self.rules:
            blocks = rule.apply(blocks)
            
        return blocks


class Rules: #Rules applied to each block of text.
    def __init__(self,handler,blocks):
        self.type = ''
        self.handler = handler
        self.condition = ['list','quote','url','br','head','code']
        self.blocks = blocks
        
    def apply_sub(self,condition):
        for block in self.blocks:
            self.handler.sub(condition,block)
    def add_condition(self,cond):
        self.condition.append(cond)
       
    def apply(self,blocks):
        if self.type not in self.condition:
            
            new_start = self.handler.start(self.type,blocks[self.start_num])
            new_end = self.handler.end(self.type,blocks[self.end_num])
            utils.replace_block(new_start,blocks[self.start_num],blocks)
            if self.type != 'title':
                utils.replace_block(new_end,blocks[self.end_num],blocks)

        else:
            for block in blocks:
                new_block = self.handler.sub(self.type,block)
                utils.replace_block(new_block,block,blocks)       
        return blocks

   
class file_rules(Rules):#apply each handler to each corresponding blocks.Rule is a detector.
    def __init__(self,handler,blocks):
        Rules.__init__(self,handler,blocks)
        self.type = 'file'
        self.start_num = 0 #using block itself instead of the number will induce to error when the orginal block is changed.
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
        self.start_num = self.body_match(self.blocks)
        self.end_num = -1
        
    def body_match(self,blocks):
        for block in blocks:
            while not re.match('t|Title:',block):
                return blocks.index(block)
        
class url_rules(Rules):
    def __init__(self,handler,blocks):
        Rules.__init__(self,handler,blocks)
        self.type = 'url'

class br_rules(Rules):
    def __init__(self,handler,blocks):
        Rules.__init__(self,handler,blocks)
        self.type = 'br'
        
class head_rules(Rules):
    def __init__(self,handler,blocks):
        Rules.__init__(self,handler,blocks)
        self.type = 'head'

class code_rules(Rules):
    def __init__(self,handler,blocks):
        Rules.__init__(self,handler,blocks)
        self.type = 'code'
        
class quote_rules(Rules):
    def __init__(self,handler,blocks):
        Rules.__init__(self,handler,blocks)
        self.type = 'quote'
        
class list_rules(Rules):
    def __init__(self,handler,blocks):
        Rules.__init__(self,handler,blocks)
        self.type = 'list'
 

class Handler(): #how to handle each section.
    def callfuction(self,preflix,name,*args):
        method = getattr(self,preflix+name,None)
        if callable(method):return method(*args)
            
    def start(self,name,block):
        return self.callfuction('start_',name,block)
        
        
    def end(self,name,block):
        return self.callfuction('end_',name,block)
        
    def sub(self,name,block):
        return self.callfuction('sub_',name,block)
        
        
class HTML_handler(Handler):
    def start_file(self,block):       
        return '<html>'+block
        
    def end_file(self,block):
        return block + '</html>'

    def start_title(self,block):
        return '<head><title>' +block +'</title></head>'

    def end_title(self,block):
        pass

    def start_body(self,block):
        return '<body>'+block

    def end_body(self,block):
        return block + '</body>'
        
    def sub_code(self,block):
        pattern = r'    |\t'
        
        for item in re.findall(pattern,block):
            if item != None:
                repl = '<pre>'
                repl_1 = '</pre>'
                block = block.replace(item,repl) + repl_1
        return block
                

    def sub_url(self,block):
        pattern = r'www.[0-9a-zA-Z]+.com'

        for item in re.findall(pattern,block): #other function to replace findall?
            if item != None:
                repl = '<a href = "http://%s">%s</a>' %(item,item)
                               
                block = block.replace(item,repl)
        return block

    def sub_br(self,block):
        pattern = r'\n'
        for item in re.findall(pattern,block):
            if item != None:
                repl = '<br>'
                block = block.replace(item,repl)
        return block

    def sub_head(self,block):
        pattern = '[#]{1,6}'
        for item in re.findall(pattern,block):
            if item != None:
                repl = '<h%s>' %(len(item))
                repl_1 = '</h%s>' %(len(item))
                block = block.replace(item,repl) + repl_1
        return block
        
    def sub_quote(self,block):
        pattern = r'>>'
        
        for item in re.findall(pattern,block):
            if item != None:
                if '<blockquote>' not in block:
                    repl = '<blockquote>'
                else:
                    repl = ''
                print repl
                block = block.replace(item,repl,1)
                repl_1 = '</blockquote>'
                if '</blockquote>' not in block:                
                    block += repl_1
        return block
        
    def sub_list(self,block):
        '''
        for line in block.split(r'\n'):
            Tag = 'True'
            if re.match('^/-'):
                if Tag == 'True':
                    line.replace('^/-','<ol>/n<li>')
                    line += '</li>'
                    Tag = 'False'
                else:
                    line.replace('^/-','<li>')
                    line += '</li>'
        '''
        start_pattern = '<ol>/n<li>'
        end_pattern = '</li>\n</ol>'
        normal_pattern = '^/-'
        new_pattern = '<li></li>'
        new_block = utils.replace_pattern(start_pattern,end_pattern,normal_pattern,new_pattern,block)
        return new_block
        

'''
def HTML_sort(in_list):
    out_list = []
    if 'body' in  in_list:
        in_list.pop('body')
        out_list.append('body')
'''        
        
def main():
    #file_path = CommandParser()
    file_path = "./test.txt"
    g=utils.FileParser(file_path)
    
    handler = HTML_handler()
    parser = TextParser(handler)
    candi = ['list','quote','code','head','br','url','title','body','file']
    #candi = ['url','file']
    for typename in candi:
        new_rule = eval(typename+'_rules')
        #if issubclass(new_rule,Rules):
        if callable(new_rule):
            rule  = new_rule(handler,g)
            parser.AddRule(rule)
        
    
    g = parser.Gen_file(g)
    print g
    utils.Create_file(file_path,g)
    #print g
    
    
if __name__ == '__main__':
    main()
    