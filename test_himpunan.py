import itertools, random
from klasifikasi_himpunan import *

def test_ops():
    A, B, U = {1,2,3}, {3,4}, {1,2,3,4,5}
    assert union(A,B) == {1,2,3,4}
    assert intersection(A,B) == {3}
    assert difference(A,B) == {1,2}
    assert complement(A,U) == {4,5}

def test_pie_random():
    random.seed(1)
    for _ in range(200):
        n = random.randint(2,5)
        sets = {f"S{i}": {x for x in range(30) if random.random()<.4} for i in range(n)}
        total,_ = pie_count(sets)
        assert total == len(union(*sets.values()))

def test_datasets():
    for f,expected in [("data/dataset1_keahlian_mahasiswa.csv",18),
                       ("data/dataset2_platform_responden.csv",19)]:
        U,G = load_dataset(f)
        total,_ = pie_count(G)
        assert total == expected == len(union(*G.values()))

if __name__ == "__main__":
    test_ops(); test_pie_random(); test_datasets(); print("Semua tes lulus")
