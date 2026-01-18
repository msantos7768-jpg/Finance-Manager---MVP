#importando o tkinter
from tkinter import *
from tkinter import Tk, ttk
from tkinter import messagebox

#importanto Pillow
from PIL import Image, ImageTk

#Importando progress bar
from tkinter.ttk import Progressbar

#Import Matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

#Importando o Tk calendário
from tkcalendar import Calendar, DateEntry
from datetime import date

#importando funções do banco de dados
from view import porcentagem_valor, pizza_valores, bar_valor, bar_valores, inserir_categoria, inserir_gastos, inserir_receita, verCategorias, verReceitas, tabela, exclusaoGastos, exclusaoReceitas
 
#CORES
co0 = "#2e2d2b" 
co1 = "#feffff" 
co2 = "#4fa882"
co3 = "#38576b"
co4 = "#403d3d"
co5 = "#e06636"
co6 = "#038cfc"
co7 = "#3fbfb9"
co8 = "#263238"
co9 = "#e9edf5"
co10 = "#0B4008"

colors = ['#C9A24D', '#2F7D32', '#274360',
'#3A3A3A','#C9A24D', '#bb5555']

# Criando a janela de visualização
janela = Tk()
janela.title("Finance Manager")
janela.geometry('900x650')
janela.configure(background=co9)
janela.resizable(False, False)

style= ttk.Style(janela)
style.theme_use("clam")

#Criando frames de divisão da janela
frameTop = Frame(janela, width=1050,  height=50,bg=co10, relief="flat")
frameTop.grid(row=0,column=0)

frameMiddle = Frame(janela, width=1050,  height=361,bg=co1, pady=20, relief="raised")
frameMiddle.grid(row=1,column=0, pady=1, padx=0, sticky=NSEW)

frameDown = Frame(janela, width=1043,  height=300,bg=co1, relief="flat")
frameDown.grid(row=2,column=0, pady=0, padx=10, sticky=NSEW)

#Frame dentro da Frame Down
frameTabela = Frame(frameDown, width=300, height=250, bg=co1)
frameTabela.grid(row=0, column=0)

#Frame inserção de dados dentro da Frame Down
frameOperacoes = Frame(frameDown, width=220, height=250, bg=co1)
frameOperacoes.grid(row=0, column=1, padx=5)

#frame de Configurações dentro do Frame Down
frameConfiguracao = Frame(frameDown, width=220, height=250, bg=co1)
frameConfiguracao.grid(row=0, column=2, padx=5)

#Design Frame Top
#Acessando a imagem
app_img = Image.open("Logo sem fundo - FM.png")
app_img = app_img.resize((50, 50))  # resize correto
app_img = ImageTk.PhotoImage(app_img)

app_logo = Label(
    frameTop,
    image=app_img,
    text="  Finance Manager - MVP",
    compound=LEFT,
    padx=10,
    anchor=NW,
    font=('Alata', 20),
    bg=co10,
    fg=co1
)

app_logo.place(x=0, y=0)

#Função tree como global-----------------------------
global tree

def inserirCat():
    nome = e_valor_categoria.get()

    lista_inserir = [nome]
    
    for i in lista_inserir:
        if i=='':
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return

        
    #inserindo a lista para a função da view 
    inserir_categoria(lista_inserir)
    messagebox.showinfo('Sucesso!', "Dados inseridos com sucesso!")

    e_valor_categoria.delete(0, 'end')

    # Pegando os valores de categoria
    categorias_funcao = verCategorias()
    categoria = []

    for i in categorias_funcao:
        categoria.append(i[1])
    
    #atualizando a lista de categorias
    combo_categoria_despesas['values'] = (categoria)

#Função para inserir receitas------------------------

def inserirReceitas():
    nome = 'Receita'
    data = e_cal_receitas.get_date()
    valor = e_valor_receita.get()

    lista_inserir = [nome, data, valor]

    for i in lista_inserir:
        if i=='':
            messagebox.showerror('Erro', 'Preencha todos os campos' )
            return
    
    #Chamando a função de inserir receitas presente no db

    inserir_receita(lista_inserir)
    messagebox.showinfo ('Sucesso', 'Os dados foram inseridos com sucesso!')

    e_cal_receitas.delete(0, 'end')
    e_valor_receita.delete(0,'end')

    #Atualizando dados nos gráficos
    verReceitas()
    porcentagem()
    graficoBar()
    resumoTotal()
    graficoPizza()
    atualizarTabela()

#Função para inserir despesas------------------------
def inserirDespesas():
    nome = combo_categoria_despesas.get()
    data = e_cal_despesas.get_date()
    valor = e_valor_despesas.get()

    lista_inserir = [nome, data, valor]

    for i in lista_inserir:
        if i=='':
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return
    #Chamando a função de despesas da view
    inserir_gastos(lista_inserir)
    messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')

    combo_categoria_despesas.delete(0,'end')
    e_cal_despesas.delete(0,'end')
    e_valor_despesas.delete(0,'end')

    #Atualizando dados
    verReceitas()
    porcentagem()
    graficoBar()
    resumoTotal()
    graficoPizza()
    atualizarTabela()

#Função para deletar---------------- -----------------
def deletar_dados():
    try:
        treev_dados = tree.focus()
        treev_dicionario = tree.item(treev_dados)
        treev_lista = treev_dicionario['values']
        valor = treev_lista[0]
        nome = treev_lista[1]
        nome.lower()

        if nome =='Receita':
            exclusaoReceitas([valor])
            messagebox.showinfo('Sucesso', 'Os dados foram excluídos com sucesso')

             #Atualizando dados
            verReceitas()
            porcentagem()
            graficoBar()
            resumoTotal()
            graficoPizza()
        else:
            exclusaoGastos([valor])
            messagebox.showinfo('Sucesso', 'Os dados foram excluídos com sucesso')

             #Atualizando dados
            verReceitas()
            porcentagem()
            graficoBar()
            resumoTotal()
            graficoPizza()
            atualizarTabela()

    except IndexError:
        messagebox.showerror('Erro', 'Selecione um dos dados da tabela')

#Porcentagem-----------------------------------------
def porcentagem():
    l_nome = Label(frameMiddle, text="Percentual de Receita Restante", height=1, anchor=NW, font=('Verdana 12'), bg=co1, fg=co4)
    l_nome.place(x=7, y=5)

    style = ttk.Style()
    style.theme_use('default')
    style.configure("black.horizontal.TProgressbar", background=co10)
    style.configure("TProgressbar", thickness=25)
    bar = Progressbar(frameMiddle, length=180, style='black.Horizontal.TProgressbar')

    bar = Progressbar(frameMiddle, length=180)
    bar.place(x=10, y=35)
    #bar ['value'] = 100

    #valor = 100
    bar["value"] = porcentagem_valor()[0]

    valor = porcentagem_valor()[0]

    l_porcentagem = Label(frameMiddle, text="{:,.2f}%".format(valor), anchor=NW, font=('Verdana 12'), bg=co1, fg=co4)
    l_porcentagem.place(x=200, y=35)

#Função do gráfico em barras-------------------      
def graficoBar():
    lista_categorias = ['Renda', 'Despesas', 'Saldo']
    lista_valores = bar_valor()

    #Faça as figuras e atribua objetos de eixo
    figura = plt.Figure(figsize=(4, 3.45), dpi=60)
    ax = figura.add_subplot(111)
    #ax.autoscale(enable=True, axis='both, tight=None)

    ax.bar(lista_categorias, lista_valores, color= colors, width=0.9)
    #create a list to collect the plt.patches data

    c = 0
    #set individual bar lables using above list
    for i in ax.patches:
        # get_x pulls left or right; get_height pushes up or down
        ax.text(i.get_x()-.001, i.get_height()+.5,
                str("{:,.0f}".format(lista_valores[c])), fontsize=17, fontstyle='italic', verticalalignment='bottom',)
        c += 1

    ax.set_xticklabels(lista_categorias, fontsize=16)

    ax.patch.set_facecolor('#ffffff')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.spines['bottom'].set_linewidth(1)
    ax.spines['right'].set_linewidth(0)
    ax.spines['top'].set_linewidth(0)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['left'].set_linewidth(1)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(bottom=False, left=False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(False, color='#EEEEEE')
    ax.xaxis.grid(False)

    canva = FigureCanvasTkAgg(figura, frameMiddle)
    canva.get_tk_widget().place(x=10, y=70)

#Função de Resumo de renda e despesas---------------
def resumoTotal():
    valor = bar_valor()

    l_linha = Label(frameMiddle, text="", width=215, height=1, anchor=NW, font=('Arial 1'), bg='#545454')
    l_linha.place(x=309, y=52)
    l_sumario = Label(frameMiddle, text="Renda Total Mensal      ".upper(), anchor=NW, font=('Verdana 12'), bg=co1, fg=co10)
    l_sumario.place(x=309, y=35)
    l_sumario = Label(frameMiddle, text="R$ {:,.2f}".format(valor[0]), anchor=NW, font=('Arial 17'), bg=co1, fg='#000000')
    l_sumario.place(x=309, y=70)

    l_linha2 = Label(frameMiddle, text="", width=215, height=1, anchor=NW, font=('Arial 1'), bg='#545454')
    l_linha2.place(x=309, y=132)
    l_sumario2 = Label(frameMiddle, text="Despesa Total Mensal      ".upper(), anchor=NW, font=('Verdana 12'), bg=co1, fg=co10)
    l_sumario2.place(x=309, y=115)
    l_sumario2 = Label(frameMiddle, text="R$ {:,.2f}".format(valor[1]), anchor=NW, font=('Arial 17'), bg=co1, fg='#000000')
    l_sumario2 .place(x=309, y=150)

    l_linha3 = Label(frameMiddle, text="", width=215, height=1, anchor=NW, font=('Arial 1'), bg='#545454')
    l_linha3.place(x=309, y=207)
    l_sumario3 = Label(frameMiddle, text="Saldo Total em Caixa      ".upper(), anchor=NW, font=('Verdana 12'), bg=co1, fg=co10)
    l_sumario3.place(x=309, y=190)
    l_sumario3 = Label(frameMiddle, text="R$ {:,.2f}".format(valor[2]), anchor=NW, font=('Arial 17'), bg=co1, fg='#000000')
    l_sumario3.place(x=309, y=220)

#Função de visualização de gráfico pizza-------------
def graficoPizza():
    #Fazendo as figuras e atribuindo objetos ao exio
    figura = plt.Figure(figsize=(5,3), dpi=90)
    ax = figura.add_subplot(111)

    lista_valores = pizza_valores()[1]
    lista_categorias = pizza_valores()[0]

    #only "explode" the 2nd slice (i.e. 'Hogs')

    explode = []
    for i in lista_categorias:
        explode.append(0.05)
    
    ax.pie(lista_valores, explode=explode, wedgeprops=dict(width=0.2), autopct='%1.1f%%', colors=colors, shadow=True, startangle=90)

    ax.legend(lista_categorias, loc="center right", bbox_to_anchor=(1.55, 0.50))

    canva_categoria = FigureCanvasTkAgg(figura, frameMiddle)
    canva_categoria.get_tk_widget().place(x=443, y=5)

#Tabela de receitas e despesas-----------------------
l_tabela = Label(frameMiddle, text=" Receitas e Despesas",anchor=NW, font=('Verdana 12 '), bg=co10, fg=co1)
l_tabela.place(x=5,y=309)

# Função para mostrar a renda
def visualizacaoRenda():
     tabela_head = ['Id', 'Categoria', 'Data', 'Valor']
     lista_itens = tabela()

     global tree 

     tree = ttk.Treeview(frameTabela, selectmode='extended', columns= tabela_head, show='headings')

    #Rolamento Vertical
     vsb = ttk.Scrollbar(frameTabela, orient="vertical", command=tree.yview)

     #Rolamento Horizontal
     hsb = ttk.Scrollbar(frameTabela, orient="horizontal", command= tree.xview)

     tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

     tree.grid(column=0, row=0, sticky='nsew')
     vsb.grid(column=1, row=0, sticky='ns')
     hsb.grid(column=0, row=1, sticky='ew')

     hd=["center","center","center", "center"]
     h=[30,100,100,100]
     n=0

     for col in tabela_head:
        tree.heading(col, text=col.title(), anchor=CENTER)
    
        tree.column(col, width=h[n],anchor=hd[n])
        
        n+=1

     for item in lista_itens:
        tree.insert('', 'end', values=item)

     atualizarTabela()
   
def atualizarTabela():
    # Limpa a tabela
    for item in tree.get_children():
        tree.delete(item)

    # Busca dados atualizados
    lista_itens = tabela()

    # Insere novamente
    for item in lista_itens:
        tree.insert('', 'end', values=item)


#Configuração da inserção de despesas
l_info = Label(frameOperacoes, text="Insira novas despesas", height=1,anchor=NW, font=('Verdana 10 bold'), bg=co1, fg=co4)
l_info.place(x=10, y=10)

#Categoria-------------------------------------------
l_categoria = Label(frameOperacoes, text="Categoria", height=1,anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_categoria.place(x=10, y=40)

#Selecionando as Categorias--------------------------

categoria_funcao = verCategorias()
categoria = []

for i in categoria_funcao:
    categoria.append(i[1])

combo_categoria_despesas = ttk.Combobox(frameOperacoes, width=10, font=('Ivy 10'))
combo_categoria_despesas['values'] = (categoria)
combo_categoria_despesas.place(x=110, y=41)

#Despesas-------------------------------------------
l_cal_despesas = Label(frameOperacoes, text="Data", height=1,anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_cal_despesas.place(x=10, y=70)
e_cal_despesas = DateEntry(frameOperacoes, width=12, background=co10, foreground='white', borderwidth=2, year=2026)
e_cal_despesas.place(x=110, y=71)

#Valor-------------------------------------------
l_valor_despesas = Label(frameOperacoes, text="Valor Total", height=1,anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_valor_despesas.place(x=10, y=100)
e_valor_despesas = Entry(frameOperacoes, width=14, justify='left', relief='solid')
e_valor_despesas.place(x=110, y=101)

#Imput de inserir

img_add_despesas = Image.open('Botão de adição.png')
img_add_despesas = img_add_despesas.resize((17,17))
img_add_despesas = ImageTk.PhotoImage(img_add_despesas)

bt_add_despesas= Button(frameOperacoes, command=inserirDespesas ,  image=img_add_despesas, text="Adicionar".upper(), width=80, height=25,compound=LEFT, anchor=NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=RIDGE)

bt_add_despesas.place(x=110,y=131)

#Input de delete-------------------------------------
l_del_dados = Label(frameOperacoes, text="Excluir dados" ,height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_del_dados.place(x=10, y=190)

img_del_despesas = Image.open('lixeira.png')
img_del_despesas = img_del_despesas.resize((17,17))
img_del_despesas = ImageTk.PhotoImage(img_del_despesas)

bt_del_despesas= Button(frameOperacoes, command=deletar_dados ,  image=img_del_despesas, text="Deletar".upper(), width=80,compound=LEFT, anchor=NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=RIDGE)

bt_del_despesas.place(x=110,y=190)

#Configurando Receitas-------------------------------
l_config = Label(frameConfiguracao, text='Insira novas receitas', height=1, anchor=NW, font=('Verdana 10 bold'), bg=co1, fg=co4)
l_config.place(x=10, y=10)

l_cal_receitas = Label(frameConfiguracao, text="Data", height=1,anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_cal_receitas.place(x=15, y=38)
e_cal_receitas = DateEntry(frameConfiguracao, width=12, background=co10, foreground='white', borderwidth=2, year=2026)
e_cal_receitas.place(x=110, y=40)

l_valor_receita = Label(frameConfiguracao, text="Valor Total", height=1,anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_valor_receita.place(x=15, y=68)
e_valor_receita = Entry(frameConfiguracao, width=14, justify='left', relief='solid')
e_valor_receita.place(x=110, y=70)

img_add_receitas = Image.open('Botão de adição.png')
img_add_receitas = img_add_receitas.resize((17,17))
img_add_receitas = ImageTk.PhotoImage(img_add_receitas)

bt_add_receitas= Button(frameConfiguracao, command=inserirReceitas ,  image=img_add_receitas, text="Adicionar".upper(), width=80,compound=LEFT, anchor=NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=RIDGE)

bt_add_receitas.place(x=110,y=100)


l_addCat = Label(frameConfiguracao, text='Insira novas categorias', height=1, anchor=NW, font=('Verdana 10 bold'), bg=co1, fg=co4)
l_addCat.place(x=15, y=130)

l_add_categorias = Label(frameConfiguracao, text="Categoria", height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_add_categorias.place(x=15, y=160)
e_valor_categoria = Entry(frameConfiguracao, width=14, justify='left', relief='solid')
e_valor_categoria.place(x=110, y=160)

img_add_categoria = Image.open('Botão de adição.png')
img_add_categoria = img_add_categoria.resize((17,17))
img_add_categoria = ImageTk.PhotoImage(img_add_categoria)

bt_add_categoria= Button(frameConfiguracao ,command=inserirCat,  image=img_add_categoria, text="Adicionar".upper(), width=80,compound=LEFT, anchor=NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=RIDGE)

bt_add_categoria.place(x=110,y=190)

graficoPizza()
resumoTotal()
porcentagem()
graficoBar()
visualizacaoRenda() 
janela.mainloop()
