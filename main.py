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

def displayBoard(matrix):
    " Menampilkan papan Crossword "
    for baris in matrix:
        for kolom in baris:
            print(kolom, end=" ")
        print()

# PROGRAM UTAMA
if __name__ == "__main__":
    fn = input("Nama file eksternal : ")        # file name
    
    N, board, listOfWords = fileToProgram(fn)   # berapa N kotak, matriks papan, daftar kata

    blankPlaceholder = checkingPlaceholder(board, N)