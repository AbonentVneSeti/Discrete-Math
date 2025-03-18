import math
from multiprocessing.reduction import send_handle


#Степень сжатия
def compression_ratio(uncompressed_data : str, compressed_data : str) -> float:
    return len(compressed_data)/len(uncompressed_data)
#Коэффициент сжатия
def compression_factor(uncompressed_data : str, compressed_data : str) -> float:
    return len(uncompressed_data)/len(compressed_data)

def frac_to_binfrac(num : float, nums  = -1)->str:
    res = "0."
    while(num > 0):
        num*=2
        if(num == 1): break
        if(num > 1):
            res+='1'
            num-=1
        else:
            res+="0"
        if(nums != 0):
            nums -= 1
        if(nums == 0): break

    return res

def binfrac_to_dec(num: str) -> float:
    res = float(0)
    cnt = 0
    for i in num[2:]:
        cnt-=1
        if i == '1':
            res += 2**cnt
    return res

def schennon_entropy(symbolchance : list, lenght : int)-> int:
    sum = 0
    for i in symbolchance:
        sum -= i[1]*math.log(i[1],2)
    return int(lenght*sum)

def arithmetic_code(data : str, symbolchance : list) -> str:
    symbolspos = [i[0] for i in symbolchance]
    start = 0
    end = 1
    for i in data:
        segments = list()
        for j in symbolchance:
            segments.append( start + (end-start)*j[1] + (segments[-1]-start if len(segments) != 0 else 0) )
        if symbolspos.index(i) == 0:
            start = start
            end = segments[0]
        else:
            start = segments[symbolspos.index(i)-1]
            end = segments[symbolspos.index(i)]

    cnt = 0
    number = (end-start)/2
    while(int(number) == 0):
        number *= 10
        cnt+=1

    result = int(end*10**cnt-number+1)/(10**cnt)
    print(schennon_entropy(symbolchance,len(data)))
    return frac_to_binfrac(result,schennon_entropy(symbolchance,len(data)))[2:]

def arithmetic_decode(data : str, symbolchance : list) -> str:
    data = "0." + data
    data = binfrac_to_dec(data)

    flag = True

    start = 0
    end = 1

    res = ""
    while(flag):
        segments = list()
        for j in symbolchance:
            segments.append(start + (end - start) * j[1] + (segments[-1] - start if len(segments) != 0 else 0))
        #print(segments)

        minind = -1
        maxind = 0
        for i in range(len(segments)):
            if data > segments[i]:
                minind = i-1
            if data < segments[i]:
                maxind = i
                break

        if start == segments[minind] and end == segments[maxind]:
            break
        res += symbolchance[minind+1][0]
        if minind != -1 :
            start = segments[minind]
        end = segments[maxind]

        #print(data,start,end)

    return res

def main():
    data = "acefdb"
    symbolchance = [['a',0.1],['b',0.15],['c',0.05],['d',0.5],['e',0.1],['f',0.1]]

    #не роботоет
    data += '!'
    for i in symbolchance:
        i[1] = i[1]*(1-1/len(data))
    symbolchance.append(['!',1/len(data)])


    #symbolchance = { 'a' : 0.1, 'b' : 0.15 , 'c' : 0.05, 'd' : 0.5, 'e' : 0.1, 'f' : 0.1}
    arithmetic = arithmetic_code(data,symbolchance)
    print("Исходная строка:",data)
    print("Закодированная строка",arithmetic)
    print("Декодированная строка",arithmetic_decode(arithmetic,symbolchance))
    print("Коэффициент сжатия:", compression_ratio(data*int(math.log2(len(symbolchance))+1), arithmetic))
    print("степень сжатия:", compression_factor(data*int(math.log2(len(symbolchance))+1), arithmetic))
    print(symbolchance)
if __name__ == "__main__":
    main()


#
#!decode
#!
#
#
#