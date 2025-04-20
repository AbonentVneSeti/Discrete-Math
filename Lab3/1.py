import math

def to_ansi(data : str):
    ascii_table = {
        'a' : 97,'b' : 98,'c' : 99,'d' : 100,'e' : 101,'f' : 102,'g' : 103,'h' : 104,'i' : 105,'j' : 106,'k' : 107,'l' : 108,'m' : 109,'n' : 110,'o' : 111,'p' : 112,'q' : 113,'r' : 114,'s' : 115,'t' : 116,'u' : 117,'v' : 118,'w' : 119,'x' : 120,'y' : 121,'z' : 122
    }

    ansi_data = ""
    for i in data:
        ansi_data += bin(ascii_table[i]).replace('b','')
    return ansi_data

def codeHemming(bindata : str):
    hemmingdata = ""

    i = 0
    j = 0
    while (i < 2**( int(math.log(len(bindata),2))+1 ) ) and (j < len(bindata)):
        if math.log(i+1,2).is_integer():
            hemmingdata += "0"
        else:
            hemmingdata += bindata[j]
            j+=1
        i+=1

    tmp = list()
    for i in range(int(math.log(len(bindata),2))+1):
        tmp.append(2**i)

    for i in tmp:
        sum = 0
        for j in range(i-1,len(hemmingdata),i+i):
            for k in range(i):
                if(j+k < len(hemmingdata)):
                    sum += int(hemmingdata[j+k])

        if(sum % 2 == 0):
            hemmingdata = hemmingdata[:i-1] + "0" + hemmingdata[i:]
        else:
            hemmingdata = hemmingdata[:i - 1] + "1" + hemmingdata[i:]


    return hemmingdata

def damage(data : str, index : int):
    if(data[index] == '0'):
        data = data[:index] + '1' + data[index+1:]
    else:
        data = data[:index] + '0' + data[index + 1:]
    return data

def repairHemming(data : list):
    tmp = list()
    for i in range(int(math.log(len(data), 2)+1)):
        tmp.append(2 ** i)

    repindex = 0
    for i in tmp:
        sum = 0
        for j in range(i - 1, len(data), i + i):
            for k in range(i):
                if j + k < len(data) and j+k != i-1:
                    sum += int(data[j + k])

        if (sum % 2 == 0 and data[i-1] == '1') or (sum % 2 == 1 and data[i-1] == '0'):
            repindex += i

    if data[repindex - 1] == "0":
        data = data[:repindex - 1] + "1" + data[repindex:]
    else:
        data = data[:repindex - 1] + "0" + data[repindex:]

    return data

def decodeHemming(data : list):
    decodedata = ""

    for i in range(len(data)):
        if not(math.log(i+1,2).is_integer()):
            decodedata += data[i]

    return decodedata

def from_ansi(data : str):
    rev_ascii_table = { '01100001' : 'a','01100010' : 'b','01100011' : 'c','01100100' : 'd','01100101' : 'e','01100110' : 'f','01100111' : 'g','01101000' : 'h','01101001' : 'i','01101010' : 'j','01101011' : 'k','01101100' : 'l','01101101' : 'm','01101110' : 'n','01101111' : 'o','01110000' : 'p','01110001' : 'q','01110010' : 'r','01110011' : 's','01110100' : 't','01110101' : 'u','01110110' : 'v','01110111' : 'w','01111000' : 'x','01111001' : 'y','01111010' : 'z' }

    strdata = data
    for i in range(0,len(data)-7, 8):
        strdata = strdata.replace(data[i:i+8],rev_ascii_table[data[i:i+8]],1)

    return strdata

def main():
    data = "incident"
    print("Исходная строка:", data)

    data = to_ansi(data)
    print("Иходная строка в ANSI коде:",data)

    data = [ data[:(len(data)//2)], data[(len(data)//2):]]
    data = [codeHemming(data[0]),codeHemming(data[1])]
    print("Код Хемминга:",data)

    data = [damage(data[0],3-1),damage(data[1],25-1)]
    print("Строка с ошибками:",data)

    data = [repairHemming(data[0]),repairHemming(data[1])]
    print("Восстановленная строка:",data)

    data = decodeHemming(data[0])+decodeHemming(data[1])
    print("Восстановленная строка в ANSI коде:", data)

    data = from_ansi(data)
    print("Восстановленная строка:", data)

def test():
    # data = codeHemming("10110101")
    # print(data)
    # data = damage(data,10)
    # print(data)
    #
    # data = repairHemming(data)
    # print(data)
    j = 97
    for i in "abcdefghijklmnopqrstuvwxyz":
        print('\''+bin(j).replace('b','')+'\'','\''+i+'\'',sep = ' : ',end =',')
        j+=1


if __name__ == "__main__":
    main()
    #test()