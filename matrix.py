def read_matrix(filename):
    with open(filename, "r") as f:
        return [list(map(int, line.split())) for line in f]

def print_matrix(M, name):
    print(f"\n{name}:")
    for row in M:
        print(" ".join(f"{x:4}" for x in row))

def transpose(M):
    return [list(row) for row in zip(*M)]

def mul(A, B):
    n = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

def scalar_mult(K, M):
    n = len(M)
    return [[K * M[i][j] for j in range(n)] for i in range(n)]

def sub(A, B):
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]

def get_regions(n):
    r1, r2, r3, r4 = [], [], [], []
    for i in range(n):
        for j in range(n):
            if i < j and i + j < n - 1:
                r1.append((i, j))
            elif i < j and i + j > n - 1:
                r2.append((i, j))
            elif i > j and i + j > n - 1:
                r3.append((i, j))
            elif i > j and i + j < n - 1:
                r4.append((i, j))
    return r1, r2, r3, r4

def count_greater_than_K_even_cols(A, region, K):
    return sum(1 for i, j in region if j % 2 == 0 and A[i][j] > K)

def product_even_in_odd_rows(A, region):
    product = 1
    for i, j in region:
        if i % 2 == 1 and A[i][j] % 2 == 0:
            product *= A[i][j]
    return product

def build_F(A, K):
    n = len(A)
    F = [row[:] for row in A]
    r1, r2, r3, r4 = get_regions(n)

    count_2 = count_greater_than_K_even_cols(A, r2, K)
    prod_3 = product_even_in_odd_rows(A, r3)

    print(f"Количество чисел > K в четных столбцах области 2: {count_2}")
    print(f"Произведение четных чисел в нечетных строках области 3: {prod_3}")

    if count_2 < prod_3:
        # Симметричная замена областей 2 и 3
        for (i2, j2), (i3, j3) in zip(r2, r3):
            F[i2][j2], F[i3][j3] = F[i3][j3], F[i2][j2]
    else:
        # Несимметричная замена области 1 и 3 (область 1 заменяется областью 3)
        for (i1, j1), (i3, j3) in zip(r1, r3):
            F[i1][j1] = A[i3][j3]

    return F

def main():
    K = int(input("Введите K: "))
    A = read_matrix("matrix.txt")
    print_matrix(A, "Матрица A")

    r1, r2, r3, r4 = get_regions(len(A))
    print("Область 1:", r1)
    print("Область 2:", r2)
    print("Область 3:", r3)
    print("Область 4:", r4)

    F = build_F(A, K)
    print_matrix(F, "Матрица F")

    AF = mul(A, F)
    KAF = scalar_mult(K, AF)
    KAT = scalar_mult(K, transpose(A))
    result = sub(KAF, KAT)
    print_matrix(result, "Результат K*A*F - K*A^T")

if __name__ == "__main__":
    main()
