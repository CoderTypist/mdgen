import re
from typing import List

def _get_name(line: str, num_omit: int) -> str:
    
    line = line.strip()
    
    # omit leading characters
    # ex: 'def ' -> 4
    # ex: 'class ' -> 5
    line = line[num_omit:]

    # match up to the first '('
    m = re.match(r'.*(?=\()', line)
    if m:
        return m.group(0).strip()
    else:
        return None
        
        
def get_function_name(line: str) -> str:
    if (name := _get_name(line, 4)):
        return name
    else:
        raise Exception('Cannot extract function name')


def get_class_name(line: str) -> str:
    
    # if the class inherits from another class
    if (name := _get_name(line, 6)):
        return name
    
    # if the class does not inherit from another class
    line = line.strip()
    # omit the leading 'class ' and trailing ':'
    return line[6:-1]
    

def get_body(line: str) -> List:
    
    line = line.strip()

    m = re.search(r"\(.*\)", line)

    if m:
        
        param_body = m.group(0)
        
        # remove leading '(' and trailing ')'
        param_body = param_body[1:-1]
        
        # if only '' remains
        if not param_body:
            return None
        
        # get individual parameters
        params = param_body.split(',')
        params = [_.strip() for _ in params]
        return params        
        
    else:
        raise Exception('Cannot extract params')
    
def get_return_type(line: str) -> str:
    
    line = line.strip()
    
    ret_type = None
    ret_index = -1
    
    try:
        ret_index = line.index('->')
    except ValueError:
        pass
    
    if -1 != ret_index:
        ret_type = line[ret_index+2:-1].strip()
    
    return ret_type


def wprint(out_file, line: str, end='\n'):
    
    print(line, end=end) 
    
    if out_file:
        out_file.write(line+end)

 
def print_table(out, col_name: str, col_vals: List[str]) -> None:
    
    wprint(out, f'|{col_name}|description|')
    wprint(out, '|---|---|')
    
    for val in col_vals:
        wprint(out, f'|{val}|XXX|')
    
    wprint(out, '')
    
    
def mdgen(file_path: str, out: str=None):
    
    re_class = re.compile('class ')
    re_def = re.compile('def ')
    
    # yes, 'with open()' is better
    # but 'with open()' couldn't do what I needed
    
    f_in = open(file_path, 'r')
    f_out = None
    
    if out:
        f_out = open(out, 'w')   
            
    while (line := f_in.readline()):
        
        line = line.strip()
        line = line.replace('_', '\_')
        
        # class
        m_class = re_class.match(line)
        if m_class and m_class.group(0):
            
            class_name = get_class_name(line)
            wprint(f_out, f'## {class_name}')
            wprint(f_out, f'_{line}_')
            wprint(f_out, '\nXXX\n')
            
            if (extends := get_body(line)):
                print_table(f_out, 'extends', extends)            
            
        # function (def)
        m_def = re_def.match(line)
        if m_def and m_def.group(0):
            
            # get function name
            fun_name = get_function_name(line)
            
            wprint(f_out, f'## {fun_name}()')
            wprint(f_out, f'_{line}_')
            wprint(f_out, '\nXXX\n')
            
            # get function parameters
            if (params := get_body(line)):
                print_table(f_out, 'param', params)
                
            # get return type
            wprint(f_out, '__returns:__ ', end='')
            
            if (ret_type := get_return_type(line)):
                
                if '_None_' == ret_type:
                    wprint(f_out, '_None_')
                else:
                    wprint(f_out, f'_{ret_type}_:&nbsp; XXX')
            else:
                wprint(f_out, '_None_')
                
    f_in.close()
    
    if f_out:
        f_out.close()
                         