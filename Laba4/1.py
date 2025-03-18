from xmlrpc.client import MAXINT
import math

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

def gettext():
    file = open("text.txt", "r")
    text = file.read()
    file.close()

    text = text.lower()

    return text

def sortbysecond(arr : list):
    dlist = arr.copy()
    for i in range(len(dlist)-1):
        for j in range(len(dlist)-1-i):
            if(dlist[j][1] < dlist[j+1][1]):
                dlist[j],dlist[j+1] = dlist[j+1],dlist[j]
    return dlist

def frequency(text : str, a : str):
    return text.count(a)

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

def calculate_shannon_entropy(frequencies,text_len):

    entropy = 0
    for freq in frequencies:
        entropy -= (freq[1]/text_len) * math.log2(freq[1]/text_len)
    return entropy

def main():
    text = gettext()

    #1 Статистический анализ
    allsymbols = set(text)
    symbolchance = list()
    for i in allsymbols:
        symbolchance.append([i,frequency(text,i)])

    alltwos = set()
    for i in range(len(text)-1):
        alltwos.add(text[i]+text[i+1])

    twoschance = list()
    for i in alltwos:
        twoschance.append([i,frequency(text,i)])

    symbolchance = sortbysecond(symbolchance)
    twoschance = sortbysecond(twoschance)

    print("Исходный текст:",text)

    print("Частотность символов:",symbolchance)
    print("Частотность пар:",twoschance)

    #2.1 Построение кодов Хаффмана
    codes = haffmancode(symbolchance)
    print("Коды Хаффмана:",codes)

    #2.2 Кодированние текста
    Haffmantext = encodetext(text,codes)
    print("Закодированный с помощью кодов Хаффмана текст:",Haffmantext)

    print("Длина текста, закодированного с помощью кодов Хаффмана:",len(Haffmantext))
    print("Длина исходного текста, закодированного 5 битными кодами:",len(text)*5)

    #2.3 Раскодирование текста
    decryptedtext = decodetext(Haffmantext,codes)
    print("Раскодированный текст:",decryptedtext)
    print("Его длина:",len(decryptedtext))

    if text == decryptedtext: print("Исходный текст совпадает с раскодированным")
    else: print("Исходный текст не совпадает с раскодированным")
    #2.4 Вычисление количества информации по формуле Шенона
    print("Энтропия Шенона:",calculate_shannon_entropy(symbolchance,len(text)))
    print("Количество бит на символ в случае с кодами Хаффмана:",len(Haffmantext)/len(text))
    print("Количество бит на символ в случае с 5 битовыми кодами: 5")
def test():
    ...

if __name__ == "__main__":
    main()
    #test()