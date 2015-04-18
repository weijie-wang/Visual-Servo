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
for x in variable_err:
    for y in x:
        if x[y] not in var_err:
            num_err = num_err  + 1
            var_err[(x[y])] = num_err
print len(var_err)
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
    

    



    
    
