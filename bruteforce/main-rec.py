from copy import deepcopy
from timeit import default_timer

def fileToProgram(file_name):
    " Membaca dari file eksternal "
    file = open(file_name, "r")
    n = int(file.readline())        # membaca banyak kolom dan baris pada papan crossword
    matrix = []
    word_list = []
    for line in file:               # membaca papan crossword
        if (line[0] == "-") or (line[0] == "#"):
            temp = [char for char in line]
            temp = temp[:len(temp)-1]
            matrix.append(temp)
        elif line != '\n':          # membaca kata-kata yang ada di dalam crossword
            word_list.extend(line.split(";"))
    file.close()
    
    word_list = [[char for char in word] for word in word_list[:]]
    return n, matrix, word_list

def checkingPlaceholder(matrix, n):
    " Mencari kotak yang kosong di papan Crossword "
    temp_l = []
    
    # horizontal
    hor_l = []
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == '-':
                temp_l.append((i,j))
            elif len(temp_l) == 1:
                temp_l = []
            elif len(temp_l) > 1:
                hor_l.append(temp_l)
                temp_l = []
        if len(temp_l) > 1:
            hor_l.append(temp_l)
        temp_l =[]
    
    # vertical
    ver_l = []
    for i in range(n):
        for j in range(n):
            if matrix[j][i] == '-':
                temp_l.append((j,i))
            elif len(temp_l) == 1:
                temp_l = []
            elif len(temp_l) > 1:
                ver_l.append(temp_l)
                temp_l = []
        if len(temp_l) > 1:
            ver_l.append(temp_l)
        temp_l = []
    return hor_l + ver_l

def solvingThePuzzle(matrix, placeholder, original_list, rec_list, word_container):
    " Fungsi rekursif yang digunakan untuk memberikan solusi yang benar "
    if rec_list == []:      # basis rekursif
        crntMatrix = completeBoard(matrix, placeholder, word_container)
        if isTheSolution(crntMatrix, placeholder, original_list):
            return crntMatrix
        else:
            return []
    else:
        for word in rec_list[:]:
            new_word_container = deepcopy(word_container)
            new_word_container.append(word)
            new_rec_list = deepcopy(rec_list)
            del new_rec_list[new_rec_list.index(word)]
            crntMatrix = solvingThePuzzle(matrix, placeholder, original_list, new_rec_list, new_word_container)
            if crntMatrix != []:
                return crntMatrix
        return []

def completeBoard(matrix, placeholder, word_container):
    " Mengisi papan Crossword dari kosong sampai penuh "
    temp_container = deepcopy(word_container)
    for p in placeholder:
        word_candidates = [w for w in temp_container if len(w) == len(p)]
        matrix = insertWordOnBoard(matrix, p, word_candidates[0])
        del temp_container[temp_container.index(word_candidates[0])]
    return matrix

def insertWordOnBoard(matrix, placeholder, word):
    " Menulis kata pada kumpulan kotak yang telah ditentukan "
    for p, w in zip(placeholder, word):
        matrix[p[0]][p[1]] = w
    return matrix

def isTheSolution(matrix, placeholder, word_list):
    " Mengecek apakah papan yang telah terisi semua adalah solusi yang benar "
    for p in placeholder:
        word = []
        for coor in p:
            word.extend([matrix[coor[0]][coor[1]]])
        if word not in word_list:
            return False
    return True

def displayBoard(matrix):
    " Menampilkan papan Crossword "
    for baris in matrix:
        print(' '.join(map(str, baris)))

if __name__ == "__main__":
    fn = input("Nama file eksternal : ")            # nama file

    N, board, listOfWords = fileToProgram(fn)       # berapa N kotak; matriks papan; daftar kata

    start_time = default_timer()

    blankPlaceholder = checkingPlaceholder(board, N)

    list_duplicate = deepcopy(listOfWords)

    solution = solvingThePuzzle(board, blankPlaceholder, listOfWords, list_duplicate, [])

    end_time = default_timer()

    print("Solusi")
    displayBoard(board)

    print()
    print("Waktu eksekusi:", (end_time - start_time)*1000, "ms")