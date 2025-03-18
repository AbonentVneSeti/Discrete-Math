import random
from xmlrpc.client import MAXINT

class Node:
    def __init__(self, key : int, value : str):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

    def __eq__(self, other):
        return (self.key == other.key and self.value == other.value and self.left == other.left and self.right == other.right)

def get_codes_pre_order(node, codes : list, code = ""):
    if node.left:
        get_codes_pre_order(node.left,codes, code + "0")
    if node.right:
        get_codes_pre_order(node.right,codes, code + "1")
    if not node.left and not node.right:
        codes.append([node.value,code])

def haffmancode(symbolchance):
    nodesarr = list()
    for i in symbolchance:
        nodesarr.append(Node(i[1],i[0]))

    while(len(nodesarr) > 1):
        min1 = Node(MAXINT,"NotASymbol")
        min2 = Node(MAXINT,"NotASymbol")
        for i in nodesarr:
            if i.key < min1.key:
                min1, min2 = i, min1
            elif i.key < min2.key and i.value != min1.value:
                min2 = i

        tmp = Node(min1.key + min2.key,min1.value + min2.value)
        tmp.left = min1
        tmp.right = min2

        nodesarr.remove(min1)
        nodesarr.remove(min2)

        nodesarr.append(tmp)

    #print(nodesarr[0].value)
    codes = list()
    get_codes_pre_order(nodesarr[0],codes)
    return codes

def sortbysecond(arr : list):
    dlist = arr.copy()
    for i in range(len(dlist)-1):
        for j in range(len(dlist)-1-i):
            if(dlist[j][1] < dlist[j+1][1]):
                dlist[j],dlist[j+1] = dlist[j+1],dlist[j]
    return dlist

def encodetext(text : str, codes : list):
    for i in codes:
        text = text.replace(i[0], i[1])
    return text

def decodetext(encoded_text : str, codes : list):
    decryptedtext = ""
    current_code = ""

    for bit in encoded_text:
        current_code += bit
        for code in codes:
            if current_code == code[1]:
                decryptedtext += code[0]
                current_code = ""
                break

    return decryptedtext

#Степень сжатия
def compression_ratio(uncompressed_data : str, compressed_data : str) -> float:
    return len(compressed_data)/len(uncompressed_data)
#Коэффициент сжатия
def compression_factor(uncompressed_data : str, compressed_data : str) -> float:
    return len(uncompressed_data)/len(compressed_data)

def main():
    symbolchance = [['A',1],['B',1],['C',9],['D', 15],['E',19],['F',23],['G',32]][::-1]
    codes = haffmancode(symbolchance)
    print("Искомые коды Хаффмана:",codes)

    #Примеры

    print("#" * 500)
    print("Идеальный пример:")
    text = 'A' + 'B' + 'C' * 9 + 'D' * 15 + 'E' * 19 + 'F' * 23 + 'G' * 32
    print("Исходный текст:\n", text)
    encoded_text = encodetext(text, codes)
    print("Закодированный текст:\n", encoded_text)
    print("раскодированный текст:\n", decodetext(encoded_text, codes))

    print("Степень сжатия:", compression_ratio(text * 3, encoded_text))
    print("Коэффициент сжатия:", compression_factor(text * 3, encoded_text))


    symbols = "ABCDEFG"
    for i in range(2):
        print("#"*500)
        print("Случайный пример №",i+1, sep = '')
        text = ""
        for j in range(random.randint(50,150)):
            text += symbols[random.randint(0,len(symbols)-1)]
        print("Исходный текст:\n",text)
        encoded_text = encodetext(text,codes)
        print("Закодированный текст:\n",encoded_text)
        print("раскодированный текст:\n", decodetext(encoded_text, codes))

        print("Степень сжатия:", compression_ratio(text*3,encoded_text))
        print("Коэффициент сжатия:", compression_factor(text*3, encoded_text))

if __name__ == "__main__":
    main()