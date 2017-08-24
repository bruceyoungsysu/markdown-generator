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
    
    if not os.existspath(txt_path):
        raise UserWarning('Please input a valid path!') # distingush between file and folder?
        
    return txt_path

def FileParser(file_path): #parse a txt file to blocks.
    '''
    parse the txt file to seperate blocks. Each block is like a paragraph.
    returns : generator of blocks
    '''
    f2 = open(file_path,'a')
    f2.write('\n\n')
    f2.close()
    f = open(file_path,'r')
    lines = f.readlines()

    f.close()
    block = []
    blocks = []
    for line in lines:
        
        if line.rstrip():
            block.append(line)
            
        elif block:
            blocks.append(''.join(block))
            block = []
            
    if lines[-1].strip():
        blocks.append(lines[-1])
    
    return blocks

def Create_file(file_path,blocks):
    dir_path,file_name=os.path.split(file_path)
    # detect the system used?
    html_path=dir_path+r'\new.html'
    f = open(html_path,'w')
    f.writelines(blocks)
    f.close()
    
def replace_block(new_block,block,blocks):
    '''replace the old block to new block in blocks'''
    try :
        block_index = blocks.index(block)
        blocks.insert(block_index,new_block)
        blocks.remove(block)
    except:
        print 'error'

def replace_pattern(start_pattern,end_pattern,normal_pattern,new_pattern,block):
    '''replace the special patterns different from head and end like quote, code block, etc
    input: the start pattern in html, the end pattern in html, the major pattern in the middle of block
    output: new block with all marks replaced by html tags    
    '''
    lines = block.split(r'\n')
    def replace_start(start_pattern,normal_pattern,lines):
        Tag = 'True'
        count = 0
        while Tag:
            if  re.match(normal_pattern,lines[count]):
                Tag = 'False'
                lines[count].replace(normal_pattern,start_pattern)
                break
            else:
                count +=1
                continue
        return lines
    def replace_end(end_pattern,normal_pattern,lines):
        Tag = 'True'
        count = -1
        while Tag:
            if  re.match(normal_pattern,lines[count]):
                Tag = 'False'
                lines[count].replace(normal_pattern,end_pattern)
                break
            else:
                count -= 1
                continue
        return lines
        
    def replace_normal(new_pattern,normal_pattern,lines):
        for line in lines:
            re.sub(normal_pattern,new_pattern,line)
            return lines
    new_block = []
    lines = replace_start(start_pattern,normal_pattern,lines)
    lines = replace_end(end_pattern,normal_pattern,lines)
    lines= replace_normal(new_pattern,normal_pattern,lines)
    new_block.append(lines.join(r'\n'))    
    return new_block