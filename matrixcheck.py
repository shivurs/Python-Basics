import matrix_utils

A = [[3, 4, 5, 10], [6, 7, 8, 11], [9, 1, 2, 12], [0, 1, -1, 30]]
print(A)
print('The diagonal of A is', matrix_utils.diagonal(A))
print('The transpose of A is', matrix_utils.transpose(A))