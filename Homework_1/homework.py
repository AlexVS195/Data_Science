import numpy as np

# 1. Створення одновимірного масиву (вектора) з першими 10-ма натуральними числами
vector = np.arange(1, 11)
print("Vector:", vector)

# 2. Створення двовимірного масиву (матриці) розміром 3x3, заповніть його нулями
matrix_3x3 = np.zeros((3, 3))
print("Matrix 3x3:", matrix_3x3)

# 3. Створення масиву розміром 5x5, заповніть його випадковими цілими числами в діапазоні від 1 до 10
matrix_5x5 = np.random.randint(1, 11, size=(5, 5))
print("Matrix 5x5:", matrix_5x5)

# 4. Створення масиву розміром 4x4, заповніть його випадковими дійсними числами в діапазоні від 0 до 1
matrix_4x4 = np.random.rand(4, 4)
print("Matrix 4x4:", matrix_4x4)

# 5. Створення двох одновимірних масивів розміром 5, виконання поелементних операцій
array1 = np.random.randint(1, 11, size=5)
array2 = np.random.randint(1, 11, size=5)
print("Array1:", array1)
print("Array2:", array2)
print("Addition:", array1 + array2)
print("Subtraction:", array1 - array2)
print("Multiplication:", array1 * array2)

# 6. Створення двох векторів розміром 7, знаходження скалярного добутку
vector1 = np.random.randint(1, 11, size=7)
vector2 = np.random.randint(1, 11, size=7)
print("Vector1:", vector1)
print("Vector2:", vector2)
print("Dot product:", np.dot(vector1, vector2))

# 7. Створення двох матриць розміром 2x2 та 2x3 та їх перемноження
matrix1 = np.random.randint(1, 11, size=(2, 2))
matrix2 = np.random.randint(1, 11, size=(2, 3))
print("Matrix 1:\n", matrix1)
print("Matrix 2:\n", matrix2)
try:
    result_matrix = np.dot(matrix1, matrix2)
    print("Result of multiplication:\n", result_matrix)
except ValueError as e:
    print("Error:", e)

# 8. Створення матриці розміром 3x3 та знаходження її оберненої матриці
matrix3 = np.random.randint(1, 11, size=(3, 3))
print("Matrix 3:\n", matrix3)
try:
    inverse_matrix = np.linalg.inv(matrix3)
    print("Inverse of Matrix 3:\n", inverse_matrix)
except np.linalg.LinAlgError as e:
    print("Error:", e)

# 9. Створення матриці розміром 4x4 та транспонування її
matrix4 = np.random.rand(4, 4)
print("Matrix 4:\n", matrix4)
transposed_matrix = matrix4.T
print("Transposed Matrix 4:\n", transposed_matrix)

# 10. Створення матриці розміром 3x4 та вектора розміром 4 та їх перемноження
matrix5 = np.random.randint(1, 11, size=(3, 4))
vector1 = np.random.randint(1, 11, size=4)
print("Matrix 5:\n", matrix5)
print("Vector 1:\n", vector1)
result_vector = np.dot(matrix5, vector1)
print("Result of matrix-vector multiplication:\n", result_vector)

# 11. Створення матриці розміром 2x3 та вектора розміром 3 та їх перемноження
matrix1 = np.random.rand(2, 3)
vector1 = np.random.rand(3)
print("Matrix 1:\n", matrix1)
print("Vector 1:\n", vector1)
result_vector = np.dot(matrix1, vector1)
print("Result of matrix-vector multiplication:\n", result_vector)

# 12. Створення двох матриць розміром 2x2 та виконання їхнього поелементного множення
matrix2 = np.random.randint(1, 11, size=(2, 2))
matrix3 = np.random.randint(1, 11, size=(2, 2))
print("Matrix 2:\n", matrix2)
print("Matrix 3:\n", matrix3)
elementwise_product = np.multiply(matrix2, matrix3)
print("Elementwise product:\n", elementwise_product)

# 13. Створення двох матриць розміром 2x2 та знаходження їх добутку
matrix4 = np.random.randint(1, 11, size=(2, 2))
matrix5 = np.random.randint(1, 11, size=(2, 2))
print("Matrix 4:\n", matrix4)
print("Matrix 5:\n", matrix5)
product_matrix = np.dot(matrix4, matrix5)
print("Product of matrices:\n", product_matrix)

# 14. Створення матриці розміром 5x5 та знаходження суми її елементів
matrix6 = np.random.randint(1, 101, size=(5, 5))
print("Matrix 6:\n", matrix6)
sum_elements = np.sum(matrix6)
print("Sum of elements:\n", sum_elements)

# 15. Створення двох матриць розміром 4x4 та знаходження їх різниці
matrix1 = np.random.randint(1, 11, size=(4, 4))
matrix2 = np.random.randint(1, 11, size=(4, 4))
print("Matrix 1:\n", matrix1)
print("Matrix 2:\n", matrix2)
difference_matrix = np.subtract(matrix1, matrix2)
print("Difference of matrices:\n", difference_matrix)

# 16. Створення матриці розміром 3x3 та знаходження вектора сум рядків
matrix3 = np.random.rand(3, 3)
print("Matrix 3:\n", matrix3)
row_sums = matrix3.sum(axis=1)
row_sums_vector = row_sums[:, np.newaxis]
print("Vector of row sums:\n", row_sums_vector)

# 17. Створення матриці розміром 3x4 та матриці з квадратами її елементів
matrix4 = np.random.randint(1, 11, size=(3, 4))
print("Matrix 4:\n", matrix4)
squared_matrix = np.square(matrix4)
print("Squared matrix:\n", squared_matrix)

# 18. Створення вектора розміром 4 та знаходження вектора з квадратними коренями його елементів
vector1 = np.random.randint(1, 51, size=4)
print("Vector 1:\n", vector1)
sqrt_vector = np.sqrt(vector1)
print("Vector with square roots:\n", sqrt_vector)