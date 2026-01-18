#importando SQLite
import sqlite3 as lite
import pandas as pd

 #Criando a conexão com o BD
con = lite.connect('dados.db')

#Funções de Inserção---------------------------------

#Inserindo categorias
def inserir_categoria(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Categoria (nome) VALUES (?)"
        cur.execute(query,i)

#Inserindo receitas
def inserir_receita(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Receitas (categoria, adicionado_em, valor) VALUES (?, ?, ?)"
        cur.execute(query,i)

#Inserir gastos
def inserir_gastos(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO Gastos (categoria, retirado_em, valor) VALUES (?,?,?)"
        cur.execute(query,i)


#Funções de exclusão---------------------------------

# Deletar receitas
def exclusaoReceitas(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Receitas WHERE id=?"
        cur.execute(query, i)

#Deletar gastos

def exclusaoGastos(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Gastos WHERE id=?"
        cur.execute(query, i)

#Funções de visualição-------------------------------

#Função visualização de categorias
def verCategorias():
    lista_itens = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Categoria")
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)

    return lista_itens
print(verCategorias())

#Função visualização de receitas
def verReceitas():
    lista_itens = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Receitas")
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)

    return lista_itens
print(verReceitas())

#Função visualização de gastos
def verGastos():
    lista_itens = []

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Gastos")
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)

    return lista_itens

def tabela():
    gastos = verGastos()
    receitas = verReceitas()

    tabela_lista = []

    for i in gastos:
        tabela_lista.append(i)
    
    for i in receitas:
        tabela_lista.append(i)
    
    return tabela_lista

#Função para dados do gráfico em barras
def bar_valores():
    #Receita total
    receitas = verReceitas()
    receita_lista = []

    for i in receitas:
        receita_lista.append(i[3])

#Função para atualização de valores do gráfico de barras
def bar_valor():
    #Receita total-----------------------------------
    receitas = verReceitas()
    receitas_lista = []

    for i in receitas:
        receitas_lista.append(i[3])

    receita_total = sum(receitas_lista)

    #Despesas total----------------------------------
    despesas = verGastos()
    despesa_lista = []

    for i in despesas:
        despesa_lista.append(i[3])

    despesas_total = sum(despesa_lista)
    
    #Saldo total-------------------------------------
    saldo_total = receita_total - despesas_total

    return[receita_total, despesas_total, saldo_total]

#Função para o gráfico pizza
def pizza_valores():
    gastos = verGastos()
    tabela_lista = []

    for i in gastos:
        tabela_lista.append(i)
    
    dataframe = pd.DataFrame(tabela_lista, columns = ['id', 'categoria', 'Data', 'valor'])

    dataframe = dataframe.groupby('categoria')['valor'].sum()

    lista_quantias = dataframe.values.tolist()
    lista_categorias = []

    for i in dataframe.index:
        lista_categorias.append(i)

    return([lista_categorias, lista_quantias])
    
def porcentagem_valor():
        #Receita total-----------------------------------
    receitas = verReceitas()
    receitas_lista = []

    for i in receitas:
        receitas_lista.append(i[3])

    receita_total = sum(receitas_lista)

    #Despesas total----------------------------------
    despesas = verGastos()
    despesa_lista = []

    for i in despesas:
        despesa_lista.append(i[3])

    despesas_total = sum(despesa_lista)
    
    #porcentagem total-------------------------------
    total = ((receita_total - despesas_total) / receita_total) * 100

    return[total]