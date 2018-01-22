from copy import deepcopy

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
                # ## BEGIN - TO BE DELETED
                # print("sum bcs", w)
                # ## END - TO BE DELETED
        li.extend([word_sum])
        word_sum = 0

    return li

def matchingWithCharOnBoard(matrix, placeholder, intersects, word_list):

    for i in intersects:
        if matrix[i[0][0]][i[0][1]] != '-':
            for word in word_list[:]:
                # ## BEGIN - TO BE DELETED
                # print("index", i[1].index(i[0]))
                # ## END - TO BE DELETED
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

    intersections = checkIntersections(holL, verL)

    # Mengisi kotak yang panjangnya unik
    uniqueLengthWords = uniqueLength(listOfWords)

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
    while not(isRemainingWordLengthUnique(notYetUsedWords)):
        # ## BEGIN - TO BE DELETED
        # if len(notYetUsedPlaceholder) == 2 or len(notYetUsedWords) == 2:
        #     print("notYetUsedPlaceholder", notYetUsedPlaceholder)
        #     print("notYetUsedWords", notYetUsedWords)
        # ## END - TO BE DELETED

        crntPlaceholder = notYetUsedPlaceholder.pop(0)

        # ## BEGIN - TO BE DELETED
        # if len(notYetUsedPlaceholder) == 2 or len(notYetUsedWords) == 2:
        #     print("crntPlaceholder", crntPlaceholder)
        # ## END - TO BE DELETED

        word_candidates = [w for w in notYetUsedWords if len(w) == len(crntPlaceholder)]
        intersects = [[p, ph] for p in crntPlaceholder for ph in blankPlaceholder if (ph != crntPlaceholder) and (p in ph)]
        
        # ## BEGIN - TO BE DELETED
        # if ['G', 'U', 'T', 'S'] in word_candidates:
        #     print("intersects", intersects)
        #     print("word_candidates BEFORE", word_candidates)
        # ## END - TO BE DELETED

        # Jika ada interseksi yang sudah diisi, eliminasi kata yang tidak mungkin muat
        word_candidates = matchingWithCharOnBoard(board, crntPlaceholder, intersects, word_candidates)

        # ## BEGIN - TO BE DELETED
        # if ['G', 'U', 'T', 'S'] in word_candidates:      
        #     print("word_candidates AFTER ELIMINATION", word_candidates)
        # ## END - TO BE DELETED
        if len(word_candidates) != 1:
            for word in word_candidates[:]:          
                # ## BEGIN - TO BE DELETED
                # if ['G', 'U', 'T', 'S'] in word_candidates:
                #     print("word", word)
                # ## END - TO BE DELETED
                
                ins_candidates_len = candidatesLengthThatIntersects(word, intersects, listOfWords, crntPlaceholder)

                # ## BEGIN - TO BE DELETED
                # if ['G', 'U', 'T', 'S'] in word_candidates:
                #     print("ins_candidates_len", ins_candidates_len)
                # ## END - TO BE DELETED

                if (0 in ins_candidates_len):
                    word_candidates.pop(word_candidates.index(word))
                
                # ## BEGIN - TO BE DELETED
                # if ['G', 'U', 'T', 'S'] in word_candidates:
                #     print("word_candidates AFTER", word_candidates)
                # ## END - TO BE DELETED
        
        if len(word_candidates) == 1:
            inserted = True
            board = insertWordOnBoard(board, crntPlaceholder, word_candidates[0])
            usedWords.append(word_candidates[0])
            notYetUsedWords.pop(notYetUsedWords.index(word_candidates[0]))
            
            ## BEGIN - TO BE DELETED
            displayBoard(board)
            print()
            ## END - TO BE DELETED
            
            # ## BEGIN - TO BE DELETED
            # if ['G', 'U', 'T', 'S'] in word_candidates:
            #     break
            # ## END - TO BE DELETED
        else:
            notYetUsedPlaceholder.append(crntPlaceholder)
        

    if notYetUsedWords != []:
        for word in notYetUsedWords[:]:
            usedWords.append(word)
            notYetUsedWords.pop(notYetUsedWords.index(word))

            ph = matchingUniquePlaceholder(notYetUsedPlaceholder, word)
            usedPlaceholder.append(ph)
            notYetUsedPlaceholder.pop(notYetUsedPlaceholder.index(ph))

            board = insertWordOnBoard(board, ph, word)  

    print("After all words inserted")
    displayBoard(board)