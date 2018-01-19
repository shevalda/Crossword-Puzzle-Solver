import copy

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
    return n, matrix, word_list

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

    horizontal, vertical = searchForBlanks(board,N)