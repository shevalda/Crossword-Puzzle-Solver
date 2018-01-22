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

def checkingPlaceholder(matrix,n):
    li = []
    hor_l = []
    ver_l = []

    for i in range(n):
        for j in range(n):
            # horizontal
            if matrix[i][j] == '-':
                hor_l.append((i,j))
            elif len(hor_l) == 1:
                hor_l = []
            elif hor_l != []:
                li.append(hor_l)
                hor_l = []
            
            # vertical
            if matrix[j][i] == '-':
                ver_l.append((j,i))
            elif len(ver_l) == 1:
                ver_l = []
            elif ver_l != []:
                    li.append(ver_l)
                    ver_l = []
        if hor_l != []:
            li.append(hor_l)
            hor_l =[]
        if ver_l != []:
            li.append(ver_l)
            ver_l = []

    return li

def checkIntersections(matrix, placeholder):
    li = []

    for i in range(len(placeholder)):
        for blank in placeholder[(i+1):]:
            li.extend([inter for inter in placeholder[i] if inter in blank])

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

def displayBoard(matrix):
    " Menampilkan papan Crossword "
    for baris in matrix:
        print(' '.join(map(str, baris)))

# PROGRAM UTAMA
if __name__ == "__main__":
    fn = input("Nama file eksternal : ")        # file name
    
    N, board, listOfWords = fileToProgram(fn)   # berapa N kotak, matriks papan, daftar kata

    print("Before solved")
    displayBoard(board)
    print()

    blankPlaceholder = checkingPlaceholder(board, N)

    intersections = checkIntersections(board, blankPlaceholder)

    uniqueLengthWords = uniqueLength(blankPlaceholder, listOfWords)

    if uniqueLengthWords != [[]]:
        for word in uniqueLengthWords:
            ph = matchingUniquePlaceholder(blankPlaceholder, word)
            board = insertWordOnBoard(board, ph, word)
        
        print("After words with unique length inserted")
        displayBoard(board)
        print()