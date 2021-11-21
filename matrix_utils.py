def diagonal(matrix):   # accept a square matrix
    dia_matrix = []
    for i in range(len(matrix)):
        dia_matrix.append(matrix[i][i])
    return dia_matrix   # return the diagonal of the matrix as a list

def transpose(matrix):  # accept whatever size matrix
    trans_matrix = []
    trans_row = []
    j = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[1])):
            trans_row = [matrix[i][j], matrix[i][j]]
            trans_matrix.append(trans_row)
    return trans_matrix
