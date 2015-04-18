# -*- coding: utf-8 -*-
#!/usr/bin/env python
# fomular.py
num = 0             
string = ''
item = {}
flag = {}
data = []       #每一项
sign = []       #项的符号
coeff = []      #项的系数
variable = []   #项的变量
var = {}        #提取的变量（有顺序）
coe = []        #合并的参数（有顺序，与提取的变量对应）
#提取项和项的符号
with open('fomular.txt','r') as file:
    str = ''
    while str != '\'':
        str = file.read(1)
        if str in ['[']:
            str = file.read(1)
            if str in ['+', '-']:
                flag[(num+1)] = str
                str = file.read(1)
            else:
                flag[(num+1)] = '+'
        if str in [' ', ',']:
            continue
        if str in ['+', '-', ']']:
            num = num + 1
            item[num] =string
            string = ''
        else:
            string = string + str
        if str == ']':
            data.append(item)
            sign.append(flag)
            item = {}
            flag = {}
            num = 0
        if str in ['+', '-']:
            flag[(num+1)] = str

#提取项的系数和变量
for x in data:
    item = {}
    flag = {}
    num = 0
    for y in x:
        ss = ''
        string = ''
        flag_temp = 0
        for z in x[y]:
            if flag_temp == 1:
                if z in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    string = string + z
                else:
                    if z == '*':
                        string = string + '*'
                    elif z == ')':
                        if(ss[-1] == '*'):
                            l = len(ss)
                            ss = ss[0: (l - 1)] + ')'
                        else:
                            ss = ss + ')'
                    flag_temp = 0
            else:
                if z in ['u', 'm', 'p']:
                    flag_temp = 1
                    string = string + z
                else:
                    ss = ss + z
        if(ss[-1] == '*'):
            l = len(ss)
            ss = ss[0: (l - 1)]
        if(string[-1] == '*'):
            l = len(string)
            string = string[0: (l - 1)]
        item[y] = string
        flag[y] = ss
    coeff.append(flag)
    variable.append(item)

#同变量合并系数
num = 0
for x in variable:
    for y in x:
        if x[y] not in var:
            num = num  + 1
            var[(x[y])] = num
print len(var)
for row in range(len(variable)):
    item = {}
    for num in variable[row]:
        if var[( variable[row][num] )] not in item:
            item[( var[( variable[row][num] )] )] = sign[row][num] + coeff[row][num]
        else:
            item[( var[( variable[row][num] )] )] += sign[row][num] + coeff[row][num]
    coe.append(item)
    
var_temp = var
var = {}
for x in var_temp:
    var[var_temp[x]] = x

#系数矩阵输出到result.txt
with open('coefficient.txt','w') as f_result:
    for row in coe:
        for colume in range(1,(len(var)+1)):
            if colume in row:
                f_result.write(row[colume])
                f_result.write(' ')
            else:
                f_result.write('0')
                f_result.write(' ')
        f_result.write(';')
#参数变量矩阵输出到variable.txt
with open('variable.txt','w') as f_variable:
    for x in range(1,(len(var)+1)):
        f_variable.write(var[x])
        f_variable.write(';')
    

# -*- coding: utf-8 -*-
#!/usr/bin/env python
# fomular.py
num_err = 0             
string_err = ''
item_err = {}
flag_err = {}
data_err = []       #每一项
sign_err = []       #项的符号
coeff_err = []      #项的系数
variable_err = []   #项的变量
var_err = {}        #提取的变量（有顺序）
coe_err = []        #合并的参数（有顺序，与提取的变量对应）
#提取项和项的符号
with open('error.txt','r') as file:
    str = ''
    while str != '\'':
        str = file.read(1)
        if str in ['[']:
            str = file.read(1)
            if str in ['+', '-']:
                flag_err[(num_err+1)] = str
                str = file.read(1)
            else:
                flag_err[(num_err+1)] = '+'
        if str in [' ', ',']:
            continue
        if str in ['+', '-', ']']:
            num_err = num_err + 1
            item_err[num_err] =string_err
            string_err = ''
        else:
            string_err = string_err + str
        if str == ']':
            data_err.append(item_err)
            sign_err.append(flag_err)
            item_err = {}
            flag_err = {}
            num_err = 0
        if str in ['+', '-']:
            flag_err[(num_err+1)] = str

#提取项的系数和变量
for x in data_err:
    item_err = {}
    flag_err = {}
    num_err = 0
    for y in x:
        ss = ''
        string_err = ''
        flag_temp = 0
        for z in x[y]:
            if flag_temp == 1:
                if z in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    string_err = string_err + z
                else:
                    if z == '*':
                        string_err = string_err + '*'
                    elif z == ')':
                        if(ss[-1] == '*'):
                            l = len(ss)
                            ss = ss[0: (l - 1)] + ')'
                        else:
                            ss = ss + ')'
                    flag_temp = 0
            else:
                if z in ['u', 'm', 'p']:
                    flag_temp = 1
                    string_err = string_err + z
                else:
                    ss = ss + z
        if(ss[-1] == '*'):
            l = len(ss)
            ss = ss[0: (l - 1)]
        if(string_err[-1] == '*'):
            l = len(string_err)
            string_err = string_err[0: (l - 1)]
        item_err[y] = string_err
        flag_err[y] = ss
    coeff_err.append(flag_err)
    variable_err.append(item_err)

#同变量合并系数
num_err = 0
var_err = var_temp
for row in range(len(variable_err)):
    item_err = {}
    for num_err in variable_err[row]:
        if var_err[( variable_err[row][num_err] )] not in item_err:
            item_err[( var_err[( variable_err[row][num_err] )] )] = sign_err[row][num_err] + coeff_err[row][num_err]
        else:
            item_err[( var_err[( variable_err[row][num_err] )] )] += sign_err[row][num_err] + coeff_err[row][num_err]
    coe_err.append(item_err)
    
var_temp = var_err
var_err = {}
for x in var_temp:
    var_err[var_temp[x]] = x

#系数矩阵输出到result.txt
with open('coefficient_err.txt','w') as f_result:
    for row in coe_err:
        for colume in range(1,(len(var_err)+1)):
            if colume in row:
                f_result.write(row[colume])
                f_result.write(' ')
            else:
                f_result.write('0')
                f_result.write(' ')
        f_result.write(';')
#参数变量矩阵输出到variable.txt
with open('variable_err.txt','w') as f_variable:
    for x in range(1,(len(var_err)+1)):
        f_variable.write(var_err[x])
        f_variable.write(';')


    
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# fomular.py
num_b = 0             
string_b = ''
item_b = {}
flag_b = {}
data_b = []       #每一项
sign_b = []       #项的符号
coeff_b = []      #项的系数
variable_b = []   #项的变量
var_b = {}        #提取的变量（有顺序）
coe_b = []        #合并的参数（有顺序，与提取的变量对应）
#提取项和项的符号
with open('b.txt','r') as file:
    str = ''
    while str != '\'':
        str = file.read(1)
        if str in ['[']:
            str = file.read(1)
            if str in ['+', '-']:
                flag_b[(num_b+1)] = str
                str = file.read(1)
            else:
                flag_b[(num_b+1)] = '+'
        if str in [' ', ',']:
            continue
        if str in ['+', '-', ']']:
            num_b = num_b + 1
            item_b[num_b] =string_b
            string_b = ''
        else:
            string_b = string_b + str
        if str == ']':
            data_b.append(item_b)
            sign_b.append(flag_b)
            item_b = {}
            flag_b = {}
            num_b = 0
        if str in ['+', '-']:
            flag_b[(num_b+1)] = str

#提取项的系数和变量
for x in data_b:
    item_b = {}
    flag_b = {}
    num_b = 0
    for y in x:
        ss = ''
        string_b = ''
        flag_temp = 0
        for z in x[y]:
            if flag_temp == 1:
                if z in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    string_b = string_b + z
                else:
                    if z == '*':
                        string_b = string_b + '*'
                    elif z == ')':
                        if(ss[-1] == '*'):
                            l = len(ss)
                            ss = ss[0: (l - 1)] + ')'
                        else:
                            ss = ss + ')'
                    flag_temp = 0
            else:
                if z in ['u', 'm', 'p']:
                    flag_temp = 1
                    string_b = string_b + z
                else:
                    ss = ss + z
        if(ss[-1] == '*'):
            l = len(ss)
            ss = ss[0: (l - 1)]
        if(string_b[-1] == '*'):
            l = len(string_b)
            string_b = string_b[0: (l - 1)]
        item_b[y] = string_b
        flag_b[y] = ss
    coeff_b.append(flag_b)
    variable_b.append(item_b)

#同变量合并系数
num_b = 0
var_b = var_temp
for row in range(len(variable_b)):
    item_b = {}
    for num_b in variable_b[row]:
        if var_b[( variable_b[row][num_b] )] not in item_b:
            item_b[( var_b[( variable_b[row][num_b] )] )] = sign_b[row][num_b] + coeff_b[row][num_b]
        else:
            item_b[( var_b[( variable_b[row][num_b] )] )] += sign_b[row][num_b] + coeff_b[row][num_b]
    coe_b.append(item_b)
    
var_temp = var_b
var_b = {}
for x in var_temp:
    var_b[var_temp[x]] = x

#系数矩阵输出到result.txt
with open('coefficient_b.txt','w') as f_result:
    for row in coe_b:
        for colume in range(1,(len(var_b)+1)):
            if colume in row:
                f_result.write(row[colume])
                f_result.write(' ')
            else:
                f_result.write('0')
                f_result.write(' ')
        f_result.write(';')
#参数变量矩阵输出到variable.txt
with open('variable_b.txt','w') as f_variable:
    for x in range(1,(len(var_b)+1)):
        f_variable.write(var_b[x])
        f_variable.write(';')
    



    
    
    



    
    
