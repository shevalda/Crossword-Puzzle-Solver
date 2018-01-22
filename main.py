from copy import copy, deepcopy

def fileToProgram(file_name):
    " Mengolah isi file eksternal "
    file = open(file_name, "r")
    n = int(file.readline())
    matrix = []
    word_list = []
    for line in file:
        if (line[0] == "-") or (line[0] == "#"):    # matriks crossword
            temp = [char for char in line]
            temp = temp[:len(temp)-1]
            matrix.append(temp)
        elif line != '\n':                          # daftar kata dalam crossword
            word_list.extend(line.split(";"))
    file.close()
    
    word_list = [[char for char in word] for word in word_list[:]]
    
    return n, matrix, word_list

def checkingPlaceholder(matrix, n):
    temp_l = []
    
    # horizontal
    li = []
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

def checkIntersections(matrix, hor_l, ver_l):
    li = []

    for ph in hor_l:
        for pv in ver_l:
            lt = [p1 for p1 in ph for p2 in pv if p1 == p2]
            if lt != []:
                li.extend(lt)

    return li

def uniqueLength(placeholder, word_list):
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

def candidatesThatIntersects(word, intersects, word_list):
    li = []
    for intersect in intersects:
        li.append([w for w in word_list if len(w) == len(word) and w[intersect[1].index(intersect[0])] == word[intersect[1].index(intersect[0])] and w != word])
    return li

def displayBoard(matrix):
    " Menampilkan papan Crossword "
    for baris in matrix:
        print(' '.join(map(str, baris)))

# PROGRAM UTAMA
if __name__ == "__main__":
    fn = input("Nama file eksternal : ")        # file name
    
    N, board, listOfWords = fileToProgram(fn)   # berapa N kotak, matriks papan, daftar kata

    usedWords = []
    notYetUsedWords = deepcopy(listOfWords)

    print("Before solved")
    displayBoard(board)
    print()

    holL, verL = checkingPlaceholder(board, N)
    blankPlaceholder = holL + verL

    usedPlaceholder = []
    notYetUsedPlaceholder = deepcopy(blankPlaceholder)

    intersections = checkIntersections(board, holL, verL)

    # Mengisi kotak yang panjangnya unik
    uniqueLengthWords = uniqueLength(notYetUsedPlaceholder, listOfWords)

    if uniqueLengthWords != [[]]:
        for word in uniqueLengthWords:
            usedWords.append(word)
            notYetUsedWords.pop(notYetUsedWords.index(word))

            ph = matchingUniquePlaceholder(blankPlaceholder, word)
            usedPlaceholder.append(ph)
            notYetUsedPlaceholder.pop(notYetUsedPlaceholder.index(ph))

            board = insertWordOnBoard(board, ph, word)  
        
        print("After words with unique length inserted")
        displayBoard(board)
        print()
    
    # while len(notYetUsedPlaceholder) > 0:
    #     crntPlaceholder = notYetUsedPlaceholder.pop(0)

    #     ## BEGIN - TO BE DELETED
    #     print("crntPlaceholder", crntPlaceholder)
    #     ## END - TO BE DELETED

    #     inserted = False
    #     word_candidates = [w for w in notYetUsedWords if len(w) == len(crntPlaceholder)]
    #     intersects = [[p, ph] for p in crntPlaceholder for ph in blankPlaceholder if (ph != crntPlaceholder) and (p in ph)]
    #     ## BEGIN - TO BE DELETED
    #     print("intersects", intersects)
    #     ## END - TO BE DELETED
    #     for word in word_candidates:
    #         ins_candidates = candidatesThatIntersects(word, intersects, notYetUsedWords)

    #         ## BEGIN - TO BE DELETED
    #         print("word", word)
    #         print("ins_candidates", ins_candidates)
    #         ## END - TO BE DELETED

    #         # if # cek apakah aman utk memasukkan kata #:
    #         #     inserted = True
    #         #     board = insertWordOnBoard(board, crntPlaceholder, word)
    #         #     usedWords.append(word)
    #         #     notYetUsedWords.pop(notYetUsedWords.index(word))
    #     # kalau masih tidak pasti
    #     if not(inserted):
    #         notYetUsedPlaceholder.append(crntPlaceholder)

    #     displayBoard(board)
    
    # print("After all words inserted")
    # displayBoard(board)