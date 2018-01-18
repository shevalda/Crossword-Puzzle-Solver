import copy

def fileToProgram(file_name, matrix, word_list):
    file = open(file_name, "r")
    for line in file:
        if (line[0] == "-") or (line[0] == "#"):    # matriks crossword
            temp = list(line.split())
            matrix.append(temp)
        elif line != '\n':                          # daftar kata dalam crossword
            word_list.extend(line.split(";"))
            print("word_list ", word_list)
    file.close()

""" PROGRAM UTAMA """
if __name__ == "__main__":