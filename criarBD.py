#importando SQLite
import sqlite3 as lite

 #Criando a conexão com o BD
con = lite.connect('dados.db')

#Criando tabela de categorias do BD

with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE Categoria(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT)")

#Criando tabela de receitas
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE Receitas (id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, adicionado_em DATE, valor DECIMAL )")

#Criando tabela de gastos
with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE Gastos (id INTEGER PRIMARY KEY AUTOINCREMENT, categoria TEXT, retirado_em DATE, valor DECIMAL)")
