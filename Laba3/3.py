#Степень сжатия
def compression_ratio(uncompressed_data : str, compressed_data : str) -> float:
    return len(compressed_data)/len(uncompressed_data)

#Коэффициент сжатия
def compression_factor(uncompressed_data : str, compressed_data : str) -> float:
    return len(uncompressed_data)/len(compressed_data)

def to_RLE(data : str) -> str:
    res = ""
    cnt = 0
    lastsym = ''
    for i in data:
        if lastsym == i:
            cnt+=1
        elif lastsym != "":
            res += str(cnt+1) + lastsym
            cnt = 0
        lastsym = i
    res += str(cnt+1) + lastsym
    return res

def from_RLE(data : str) -> str:
    res = ""

    cnt = ''
    for i in data:
        if i.isdigit():
            cnt += i
        else:
            res += i*int(cnt)
            cnt = ""
    return res

def main():
    data = "addddghtyyyyyyyyyiklopppppppppppp"
    print("Исходная строка:",data)
    RLEdata = to_RLE(data)
    print("Сжатая RLE строка:",RLEdata)
    print("Восстановленная строка:",from_RLE(RLEdata))

    print("Степень сжатия:", compression_ratio(data,RLEdata))
    print("Коэффициент сжатия:", compression_factor(data, RLEdata))

if __name__ == "__main__":
    main()