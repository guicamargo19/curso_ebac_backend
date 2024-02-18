def ler_arquivo(nome_arquivo):
    for linha in open(nome_arquivo, 'r', encoding='utf8'):
        yield linha


vendas = ler_arquivo("Assessment/movies.csv")

for venda in vendas:
    print(venda)
