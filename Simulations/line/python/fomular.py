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
    

    



    
    
