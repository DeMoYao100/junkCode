import random

fp_in = open("main.cpp","r+")
fp_out = open("main.cpp","r+")
asm_block = "__asm volatile(\n"
sym_1 = {'*' : 'mul' , '!' : 'not' , '<<' : 'shl', '>>' : 'shr'}
sym_2 = {'-' : 'sub' , '+' : 'add' , '^' : 'xor'}
flower = 0

def gen_random_fun_name(randomlength=8):
    random_str = ""
    base_str ='ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz'
    length = len(base_str) -1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str

def gen_random_fun(num):
    fun = ""
    op_list = []
    temp_num_list = []
    result = num
    result_tmp = 0
    times = random.randint(1,20)
    for i in range(times):
        fun += "\""
        a = random.randint(1,2)
        if (a == 1):
            b = random.randint(2,3)
            op_list.append(b)
            if (b == 1):
                fun += "mul"
                result *= result
                fun += " %rax;\"\n"
            elif (b == 2):
                fun += "shl"
                result = result << 1
                fun += " $1, %rax;\"\n"
            elif (b == 3):
                fun += "sar"
                result = result >> 1
                fun += " $1, %rax;\"\n"
        elif (a == 2):
            b = random.randint(1,3)
            op_list.append(b+10)
            temp_num = random.randint(1,5)
            temp_num_list.append(temp_num)
            if (b == 1):
                fun += "sub $"
                result -= temp_num
            elif (b == 2):
                fun += "add $"
                result += temp_num
            elif (b == 3):
                fun += "xor $"
                result ^= temp_num
            fun += str(temp_num)
            fun += ", %rax;\"\n"
    result_tmp = result
    i = 0
    for op in op_list:
        if (op < 10):
            if (op == 1):
                result *= result
            elif (op == 2):
                result = result << 1
            elif (op == 3):
                result = result >> 1

        elif (op > 10):
            if (op == 11):
                result -= temp_num_list[i]
            elif (op == 12):
                result += temp_num_list[i]
            elif (op == 13):
                result ^= temp_num_list[i]
            i += 1
    fun += "\"cmp $"
    fun += str(result)
    fun += ", %rax;\"\n"

    re = True
    if (result_tmp == result):  #防止生成一个中间量和结尾量相同的导致逻辑错误破坏源码
        re = False
    return re, fun



if __name__ == "__main__":
    while (True):
        a = fp_in.readline()
        fp_out.writelines(a)
        if (a == ""):
            break
        if (a.find('(') != -1 and a.find(')') != -1 and a.find('{') != -1 and a.find('for') == -1 and a.find('while') == -1):
            choose = random.randint(1,3)
            times = random.randint(0, 8)
            if (choose > 2):
                for i in range(times):
                    if (a.find('}') != -1):
                        break
                    a = fp_in.readline()
                    if (a.find('}') == -1):
                        fp_out.writelines(a)

            asm_block = "__asm volatile(\n"
            asm_block += "\"push %rax;  \"\n"
            asm_block += "\"xor %rax, %rax;\"\n"
            asm_block += "\"xor $"
            numb = random.randint(1,2)
            numstr = str(numb)
            asm_block += numstr
            asm_block += ", %rax;\"\n"
            asm_block += "\"call "
            func = gen_random_fun_name()
            asm_block += func
            asm_block += ";\"\n\""
            asm_block += func
            asm_block += ":;\"\n"

            #生成随机操作
            re = False
            tmp = ""
            while (re == False):
                re,tmp = gen_random_fun(numb)
            asm_block += tmp
            asm_block += "\"jz  "
            func = gen_random_fun_name()
            asm_block += func
            asm_block += ";\"\n"
            asm_block += "\"ret;\"\n"
            asm_block += "\""
            asm_block += func
            asm_block += ":;\"\n"
            asm_block += "\"pop %rax;  \"\n"
            asm_block += ");\n"

            fp_out.writelines(asm_block)
            flower += 1
            if (a.find('}') != -1):
                fp_out.writelines(a)

    print("flowers' number: " + str(flower))
    fp_in.close()
    fp_out.close()
