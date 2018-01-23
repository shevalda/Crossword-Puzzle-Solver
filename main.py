from copy import deepcopy
from timeit import default_timer

def fileToProgram(file_name):
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
    return hor_l, ver_l

def checkIntersections(hor_l, ver_l):
    li = []

    for ph in hor_l:
        for pv in ver_l:
            lt = [p1 for p1 in ph for p2 in pv if p1 == p2]
            if lt != []:
                li.extend(lt)
    return li

def uniqueLength(word_list):
    li = []

    for word in word_list:
        if len([w for w in word_list if len(w) == len(word)]) == 1:
            li.append(word)
    return li

def insertWordOnBoard(matrix, placeholder, word):
    for p, w in zip(placeholder, word):
        matrix[p[0]][p[1]] = w
    return matrix

def matchingUniquePlaceholder(placeholder, word):
    for ph in placeholder:
        if len(ph) == len(word):
            return ph

def candidatesLengthThatIntersects(word, intersects, word_list, placeholder):
    li = []
    word_sum = 0

    for i in intersects:
        for w in [wt for wt in word_list if len(wt) == len(i[1])]:
            if w[i[1].index(i[0])] == word[placeholder.index(i[0])]:
                word_sum += 1
        li.extend([word_sum])
        word_sum = 0
    return li

def matchingWithCharOnBoard(matrix, placeholder, intersects, word_list):
    for i in intersects:
        if matrix[i[0][0]][i[0][1]] != '-':
            for word in word_list[:]:
                if matrix[i[0][0]][i[0][1]] != word[placeholder.index(i[0])]:
                    word_list.pop(word_list.index(word))
    return word_list

def isRemainingWordLengthUnique(word_list):
    if len(word_list) <= 1:
        return True
    else:
        for word in word_list:
            if len([w for w in word_list if w != word and len(w) == len(word)]) != 0:
                return False
        return True

def deleteDuplicates(word_list):
    for word in word_list:
        if word_list.count(word) > 1:
            word_list.pop(word_list.index(word))
    return word_list

def displayBoard(matrix):
    " Menampilkan papan Crossword "
    for baris in matrix:
        print(' '.join(map(str, baris)))

# PROGRAM UTAMA
if __name__ == "__main__":
    fn = input("Nama file eksternal : ")            # nama file

    N, board, listOfWords = fileToProgram(fn)       # berapa N kotak; matriks papan; daftar kata
    
    start_time = default_timer()

    notYetUsedWords = deepcopy(listOfWords)         # mencatat kata yang belum dimasukkan di papan

    ## Mencatat kumpulan kotak yang kosong di papan
    holL, verL = checkingPlaceholder(board, N)
    blankPlaceholder = holL + verL

    notYetUsedPlaceholder = deepcopy(blankPlaceholder)  # mencatat kotak yang belum diisi

    intersections = checkIntersections(holL, verL)  # mencatat kotak yang menjadi persimpangan

    ## Mengisi kotak yang panjangnya unik
    uniqueLengthWords = uniqueLength(listOfWords)
    if uniqueLengthWords != [[]]:
        for word in uniqueLengthWords:
            notYetUsedWords.pop(notYetUsedWords.index(word))

            ph = matchingUniquePlaceholder(blankPlaceholder, word)
            notYetUsedPlaceholder.pop(notYetUsedPlaceholder.index(ph))

            board = insertWordOnBoard(board, ph, word)  

    ## Mengisi kotak sampai kata-kata yang tersisa masing-masing punya panjang kata yang unik
    while not(isRemainingWordLengthUnique(notYetUsedWords)):
        crntPlaceholder = notYetUsedPlaceholder.pop(0)

        word_candidates = [w for w in notYetUsedWords if len(w) == len(crntPlaceholder)]
        intersects = [[p, ph] for p in crntPlaceholder for ph in blankPlaceholder if (ph != crntPlaceholder) and (p in ph)]

        ## Eliminasi 1: Menghapus kata yang tidak cocok dengan kata yang sudah dimasukkan di papan
        word_candidates = matchingWithCharOnBoard(board, crntPlaceholder, intersects, word_candidates)
        
        ## Eliminasi 2: Memastikan semua kata yang di dalam list word_candidates unik
        word_candidates = deleteDuplicates(word_candidates)
        
        ## Eliminasi 3: Menghapus semua kata yang tidak mempunyai kata kandidat
        if len(word_candidates) != 1:
            for word in word_candidates[:]:          
                ins_candidates_len = candidatesLengthThatIntersects(word, intersects, listOfWords, crntPlaceholder)

                if (0 in ins_candidates_len):
                    word_candidates.pop(word_candidates.index(word))
        
        if len(word_candidates) == 1:   ## Jika kandidat kata hanya ada satu, masukkan ke papan
            board = insertWordOnBoard(board, crntPlaceholder, word_candidates[0])
            notYetUsedWords.pop(notYetUsedWords.index(word_candidates[0]))            
        else:                           ## Jika kandidat kata ada lebih dari satu, maka kotak belum diisi dulu
            notYetUsedPlaceholder.append(crntPlaceholder)
    
    ## Jika terdapat kata-kata yang belum terpakai dan masing-masing kata unik panjangnya
    if notYetUsedWords != []:
        for word in notYetUsedWords[:]:
            notYetUsedWords.pop(notYetUsedWords.index(word))

            ph = matchingUniquePlaceholder(notYetUsedPlaceholder, word)
            notYetUsedPlaceholder.pop(notYetUsedPlaceholder.index(ph))

            board = insertWordOnBoard(board, ph, word)

    end_time = default_timer()

    print()
    print("Solution")
    displayBoard(board)

    print()
    print("Waktu eksekusi:", (end_time - start_time) * 1000, "ms")