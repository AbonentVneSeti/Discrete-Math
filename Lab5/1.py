import random

def mult_poly_on_matrix(poly:str,matrix : list[list[int]]) -> 'str':
    res = ''
    for j in matrix:
        tmp = 0
        for k in range(len(j)):
            tmp += int(poly[k]) * j[k]
        res += '1' if tmp % 2 == 1 else '0'
    return res

def trans_matrix(matrix):
    result_matrix = list()
    for i in range(len(matrix[0])):
        result_matrix.append(list(0 for i in range(len(matrix))))

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            result_matrix[j][i] = matrix[i][j]

    return result_matrix

def get_gen_matrix(n : int,m : int, gen_poly : str):
    result =[list( int(gen_poly[i]) if i < len(gen_poly) else 0  for i in range(n))]
    for j in range(1,m):
        result.append(list( int(gen_poly[i-j]) if  0 <= i-j < len(gen_poly) else 0  for i in range(n)))
    return result

def get_all_codes(gen_matrix):
    codes_len = len(gen_matrix)

    all_vectors = list(bin(i)[2:] for i in range(2**codes_len))
    for i in range(len(all_vectors)):
        if len(all_vectors[i]) < codes_len:
            all_vectors[i] = '0'*(codes_len - len(all_vectors[i])) + all_vectors[i]

    codes = set()
    for vect in all_vectors:
        codes.add(mult_poly_on_matrix(vect,trans_matrix(gen_matrix)))

    return codes

def hamming_distance(str1 : str, str2: str)-> int:
    res = 0
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            res +=1
    return res

def get_min_dist(codes : list[str]) -> int:
    min_dist = 52
    for i in range(len(codes)-1):
        for j in range(i+1,len(codes)):
            dist = hamming_distance(codes[i],codes[j])
            if dist < min_dist:
                min_dist = dist
    return min_dist

def ex_find_error(codes):
    print("Пример обнаружения ошибок")
    code = codes[random.randint(0,len(codes)-1)]

    num_of_errors = random.randint(0,2)
    for i in range(num_of_errors):
        ind = random.randint(0,len(code)-1)
        if code[ind] == '0':
            code = code[:ind] + '1' + code[ind+1:]
        else:
            code = code[:ind] + '0' + code[ind + 1:]

    print("Количество ошибок:", num_of_errors)
    print("Пусть получено: c =", code, len(code))

    if code in codes:
        print("Ошибок нет, т.к. c является кодовым словом")
    else:
        print("Есть ошибки, т.к. c не является кодовым словом")

def ex_fix_error(codes : list[str]):
    print("Пример исправления ошибок")
    orig_code = codes[random.randint(0,len(codes)-1)]
    print(f"Пусть отправлено:\n{orig_code}")

    ind = random.randint(0,len(orig_code)-1)
    er_code = orig_code[:ind]+'1'+orig_code[ind+1:] if orig_code[ind] == '0' else orig_code[:ind]+'0'+orig_code[ind+1:]
    print(f"Полученная строка с ошибкой в {ind+1} бите\n{er_code}")

    ind_with_min_distance = -1
    min_dist = 1000
    for i in range(len(codes)):
        curr_dist = hamming_distance(er_code,codes[i])
        if curr_dist < min_dist:
            ind_with_min_distance = i
            min_dist = curr_dist
        #elif curr_dist == min_dist:
        #    ind_with_min_distance.append(i)

    print(f"Минимальное расстояние от полученного кода до всех оставшихся: {min_dist}")
    print(f"Исправленный код: {codes[ind_with_min_distance]}")
    print("Исправленный код совпадает с отправленным:", codes[ind_with_min_distance] == orig_code)

def ex_found_not_fixed(codes : list[str]):
    print("Вектор в котором нельзя исправить ошибки")
    orig_code = codes[1337]

    print("Исходный код:", orig_code)
    er_code = orig_code
    ind = [5,19]
    for i in ind:
        er_code = er_code[:i] + '1' + er_code[i+1:] if er_code[i] == '0' else er_code[:i] + '0' + er_code[i+1:]
    print(f"Полученный вектор с ошибками в {ind} битах: {er_code}")

    print("Полученный вектор пришёл есть в кодах:",er_code in codes)

    ind_with_min_distance = list()
    min_dist = 1000
    for i in range(len(codes)):
        curr_dist = hamming_distance(er_code, codes[i])
        if curr_dist < min_dist:
            ind_with_min_distance = [i]
            min_dist = curr_dist
        elif curr_dist == min_dist:
           ind_with_min_distance.append(i)

    print(f"Векторы с минимальным расстоянием {min_dist} до ошибочного:", [codes[i] for i in ind_with_min_distance])
    print("Полученный код не совпадает с исходным.")

def part_table_of_hemming_distances(codes : list[str], n : int) -> list[list[int]]:
    result = list()
    for i in range(n):
        tmp = list()
        for j in range(n):
            tmp.append(hamming_distance(codes[i],codes[j]))
        result.append(tmp)

    return result
def main():
    n = 21
    m = 15
    gen_poly = '1110101'

    print("Пункт 1:")
    gen_matrix = get_gen_matrix(n,m,gen_poly)
    print(f"Порождающая матрица кода, размера {len(gen_matrix)}x{len(gen_matrix[0])}:")
    for i in gen_matrix:
        print(*i)
    codes = list(get_all_codes(gen_matrix))
    codes.sort()
    print("Количество всех кодовых слов:",len(codes))

    #min_distance = get_min_dist(codes)# ждать слишком долго
    min_distance = 3
    print("Минимальное кодовое расстояние:",min_distance)

    print("\nПункт 2:\nХарактеристики кода")
    print("Код может гарантированно обнаруживать ошибки кратности", min_distance - 1)
    print("Код может гарантированно исправлять ошибки кратности", int((min_distance - 1)/2))

    print("\nПункт 3:")
    ex_find_error(codes)
    print()
    ex_fix_error(codes)

    print("\nПункт 4:")
    ex_found_not_fixed(codes)

    print("\nПункт 5:")
    print("Фрагмент таблицы с расстояниями:")
    table = part_table_of_hemming_distances(codes,10)
    for i in table:
        print(*i)

    print("Фрагмент множества кодовых слов:")
    for i in range(3500,3510):
        print(codes[i])


if __name__ == "__main__":
    main()
