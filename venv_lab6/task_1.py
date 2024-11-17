"""
Lab 6, variant 17
"""

matrix_A = [[66,21,-3,-1,90],[1,74,-2,80,-1],[10,30,20,-50,91],[2,4,5,81,0],[33,69,-5,51,24]]

def sort_matrix(matrix, mode):
    """
    Can sort matrixes with 2 modes, column and row; mode = 1 - row mode, mode = 0 - column mode
    """
    is_sorted_outer = False
    is_sorted_inner = False
    iter_x = 0
    iter_y = 0
    if mode:
        while is_sorted_outer is False:
            if iter_y < len(matrix):
                while is_sorted_inner is False:
                    iter_x += 1
                    if iter_x < (len(matrix[iter_y])):
                        if matrix[iter_y][iter_x] > matrix[iter_y][iter_x - 1]:
                            _temp_a,_temp_b = matrix[iter_y][iter_x],matrix[iter_y][iter_x - 1]
                            matrix[iter_y][iter_x],matrix[iter_y][iter_x - 1] = _temp_b,_temp_a
                            iter_x = 0
                    else:
                        is_sorted_inner = True
                        iter_x = 0
            else:
                is_sorted_outer = True
            iter_y +=1
            is_sorted_inner = False
    else:
        while is_sorted_outer is False:
            if iter_x < len(matrix[iter_y]):
                while is_sorted_inner is False:
                    iter_y += 1
                    if iter_y < (len(matrix)):
                        if matrix[iter_y][iter_x] > matrix[iter_y - 1][iter_x]:
                            _temp_a,_temp_b = matrix[iter_y][iter_x],matrix[iter_y - 1][iter_x]
                            matrix[iter_y][iter_x],matrix[iter_y - 1][iter_x] = _temp_b,_temp_a
                            iter_y = 0
                    else:
                        is_sorted_inner = True
                        iter_y = 0
            else:
                is_sorted_outer = True
            iter_x += 1
            is_sorted_inner = False

def get_geometrical_average(matrix):
    """
    Takes a matrix, gets a geometrical average of each row
    and creates a list out of all geometrical averages
    """
    list_of_averages = []
    product = 1.0
    for lst in matrix:
        for elem in lst:
            product *= elem
        list_of_averages.append((product ** (1 / 5)))
        product = 1.0
    return list_of_averages

def big_f_function(lst):
    """
    Takes a list of geometrical averages, returns arithmetic average of it's elements
    """
    _sum = 0
    for el in lst:
        _sum += el
    return _sum / len(lst)

sort_matrix(matrix_A, 0)
for row in matrix_A:
    print(row)
print(get_geometrical_average(matrix_A))
print(big_f_function(get_geometrical_average(matrix_A)))
