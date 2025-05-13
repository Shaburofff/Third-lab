def read_matrix(f): return [list(map(int, line.split())) for line in open(f)]
def print_matrix(m, name): print(f"\n{name}:"); [print(" ".join(f"{x:4}" for x in row)) for row in m]
def transpose(m): return [list(row) for row in zip(*m)]
def mul(A, B): return [[sum(A[i][k] * B[k][j] for k in range(len(A))) for j in range(len(A))] for i in range(len(A))]
def scalar_mult(K, M): return [[K * M[i][j] for j in range(len(M))] for i in range(len(M))]
def add(A, B): return [[A[i][j] + B[i][j] for j in range(len(A))] for i in range(len(A))]
def sub(A, B): return [[A[i][j] - B[i][j] for j in range(len(A))] for i in range(len(A))]

def get_regions(n):
    r1, r2, r3, r4 = [], [], [], []
    for i in range(n):
        for j in range(n):
            if i < j and i + j < n - 1: r1.append((i, j))
            elif i < j and i + j > n - 1: r2.append((i, j))
            elif i > j and i + j > n - 1: r3.append((i, j))
            elif i > j and i + j < n - 1: r4.append((i, j))
    return r1, r2, r3, r4

def count_greater_than_K_even_cols(A, region, K):
    return sum(1 for i, j in region if j % 2 == 0 and A[i][j] > K)

def product_of_even_in_odd_rows(A, region):
    p = 1
    for i, j in region:
        if i % 2 == 1 and A[i][j] % 2 == 0:
            p *= A[i][j]
    return p

def build_F(A, K):
    n = len(A)
    F = [row[:] for row in A]
    r1, r2, r3, r4 = get_regions(n)
    count_2 = count_greater_than_K_even_cols(A, r2, K)
    prod_3 = product_of_even_in_odd_rows(A, r3)
    print(f"\nЭлементов > K в чётных столбцах области 2: {count_2}")
    print(f"Произведение чётных в нечётных строках области 3: {prod_3}")
    if count_2 < prod_3:
        for (i2, j2), (i3, j3) in zip(r2, r3):
            F[i2][j2], F[i3][j3] = F[i3][j3], F[i2][j2]
    else:
        for (i1, j1), (i3, j3) in zip(r1, r3):
            F[i1][j1], F[i3][j3] = A[i3][j3], A[i1][j1]  # несимметрично
    return F

def main():
    K = int(input("Введите K: "))
    A = read_matrix("matrix.txt")
    print_matrix(A, "Матрица A")
    F = build_F(A, K)
    print_matrix(F, "Матрица F")
    AF = mul(A, F)
    KAF = scalar_mult(K, AF)
    KAT = scalar_mult(K, transpose(A))
    result = sub(KAF, KAT)
    print_matrix(result, "Результат: K*A*F - K*A^T")

main()
