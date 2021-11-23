def diagonal(matrix):   # accept a square matrix
    dia_matrix = []
    for i in range(len(matrix)):
        dia_matrix.append(matrix[i][i])
    return dia_matrix   # return the diagonal of the matrix as a list

def transpose(matrix):  # accept whatever size matrix
    trans_matrix = []   # create empty output matrix
    for i in range(len(matrix[0])):         # iterate over row elements
        trans_row = []                      # create empty rows for output matrix and remove any residual row updates
        for j in range(len(matrix)):        # iterate over columns
            trans_row.append(matrix[j][i])  # set new row elements (swapped indices)
        trans_matrix.append(trans_row)      # add new row to output matrix
    return trans_matrix                     # return output matrix
