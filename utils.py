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
    Currently only works in Linux
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
    input: file path    
    returns : blocks
    '''
    f2 = open(file_path,'a')
    f2.write('\n')
    f2.close()
    f = open(file_path,'r')
    lines = f.readlines()

    f.close()
    block = []
    blocks = []
    for line in lines:
        
        if line.rstrip():
            line = line
            block.append(line)
            
        elif block:
            blocks.append(''.join(block))
            block = []
            
    if lines[-1].strip():
        blocks.append(lines[-1])
    
    return blocks

def Create_file(file_path,blocks):
    ''''
    Create the html file after convet.
    input: output file path and generated blocks.
    output: html file.
    ''''
    dir_path,file_name=os.path.split(file_path)
    # detect the system used?
    html_path=dir_path+r'\new.html'
    f = open(html_path,'w')
    f.writelines(blocks)
    f.close()
    
def replace_block(new_block,block,blocks):
    '''
    replace the old block to new block in blocks
    input: blocks before replacement, block in blocks need to be replaced, new block to replace block.
    output: blocks afeter replacement    
    '''
    try :
        block_index = blocks.index(block)
        blocks.insert(block_index,new_block)
        blocks.remove(block)
    except:
        return 'error'

def replace_pattern(start_pattern,end_pattern,normal_pattern,new_pattern,block):
    '''replace the special patterns different from head and end like quote, code block, etc
    input: the start pattern in html, the end pattern in html, the major pattern in the middle of block
    output: new block with all marks replaced by html tags
    methods:
    replace_start : replace the start of whole block for special tag
    replace_end : replace the end of whole block for special tag
    replace_normal : replace the other markers with universal tag    
    '''
    lines = block.split('\n')
    #print len(lines)
    #print lines
    def replace_start(start_pattern,normal_pattern,lines):
        Tag = 'True'
        count = 0
        
        while Tag and count< len(lines):
            if  re.match(normal_pattern,lines[count]):
                Tag = 'False'
                lines[count] = re.sub(normal_pattern,start_pattern,lines[count],1)
                break
            else:
                count += 1      
        return lines
        
    def replace_end(end_pattern,normal_pattern,new_pattern,lines):
        Tag = 'True'
        count = -1
        while Tag and abs(count)<= len(lines):
            if  re.match(normal_pattern,lines[count]) or len(lines) == 1:
                Tag = 'False'
                lines[count] = lines[count].replace(normal_pattern,new_pattern)+ end_pattern
                break
            else:
                count -= 1
                
        return lines
        
    def replace_normal(new_pattern,normal_pattern,lines):
        new_lines = []
        for line in lines:
            if re.match(normal_pattern,line):
                line = re.sub(normal_pattern,new_pattern,line)
            new_lines.append(line)
        return new_lines
    #print len(lines)
    #print lines
    lines = replace_start(start_pattern,normal_pattern,lines)

    lines = replace_end(end_pattern,normal_pattern,new_pattern,lines)

    lines= replace_normal(new_pattern,normal_pattern,lines)
    
    return ''.join(lines)