import collections
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import sqlite3 as sql



#Variaveis globais
salasecafe = ['---']
salas = {}
cafes = {}
lista_membros = []
lotacao = 0
count_membros = 0
evento = ''
i = 0

#### Funções ####


# Função botão 'gravar Evento'
def gravarEvento():
    global evento
    if len(entryNomeEvent.get()) == 0:                                  #Condição - campo preenchido
        messagebox.showinfo("Erro", "Favor preencher o campo!")
    else:
        evento = entryNomeEvent.get()                                   #Adiciona o nome do evento para a var 'evento'
        entryNomeEvent.config(state = 'disabled')                       #Desativa campo de entrada próprio
        gravarCadSalas['state']= tk.NORMAL                              #Ativa o botão 'cadastrar salas'
        gravarCadEvento['state'] = tk.DISABLED                          #Desativa o botão 'Cadastrar Evento'



# Função botão 'Cadastrar Salas'

def gravarSalas():
    global salas
    global lotacao
    global salasecafe
    if len(entryNomeSala1.get()) == 0 or len(entryNomeSala2.get()) == 0 or len(entryLotSala1.get()) == 0 or len(entryLotSala2.get()) == 0:   # Condição Campos não vazios
        messagebox.showinfo('Erro', " Favor preencher todos os campos!")
    elif int(entryLotSala1.get()) - int(entryLotSala2.get()) > 1 or int(entryLotSala1.get()) - int(entryLotSala2.get()) < -1:                # Condição Diferença das salas <= 1
        messagebox.showinfo("Erro", "Diferença entre as lotações das salas maior que 1")
    elif entryNomeSala1.get() == entryNomeSala2.get():                                                                          #Condição nomes diferente para salas
        messagebox.showinfo("Erro", "Utilizar nomes diferentes para as salas!")
    else:   
        salasecafe.append(entryNomeSala1.get())                                                                                 #Adiciona as entradas para a lista 'salasecafe'
        salasecafe.append(entryNomeSala2.get())
        salas[entryNomeSala1.get()]=entryLotSala1.get()                                                                         # Adicionar nome da sala e lotação à variavel global
        salas[entryNomeSala2.get()]=entryLotSala2.get()
        lotacao = int(entryLotSala1.get()) + int(entryLotSala2.get())                                                           # Calcular a lotação total
        messagebox.showinfo("Concluido", "Cadastro das salas concluido")                                                        # Mensagem 
        gravarCadSalas['state']=tk.DISABLED                                                                                     # Desativar botão de cadastro
        gravarCadCafes['state']=tk.NORMAL                                                                                       # Ativar botão cadastro de espaços de café
        entryNomeSala1.config(state='disabled')                                                                                 # Desabilitar os campos de entrada
        entryLotSala1.config(state='disabled')                                                                                  
        entryNomeSala2.config(state='disabled')
        entryLotSala2.config(state='disabled')



# Função botão 'gravar cafés'

def gravarCafes():
    global salasecafe
    global cafes
    global lotacao
    global variavel
    if len(entryNomeCafe1.get()) == 0 or len(entryLotCafe1.get()) == 0 or len(entryNomeCafe2.get()) == 0 or len(entryLotCafe2.get()) == 0:  # Condição Campos não vazios
        messagebox.showinfo("Erro", "Favor preencher todos os campos!")
    elif (int(entryLotCafe1.get()) + int(entryLotCafe2.get())) != lotacao:                                                                  # Condição Lotacao dos cafés = lotação das salas
        messagebox.showinfo("Erro", "Lotacao total dos espaços de Coffe-Break deve ser igual a lotação total das salas!")
    elif entryNomeCafe1.get() == entryNomeCafe2.get():                                                                                      # Condição Nomes diferentes para os cafés
         messagebox.showinfo("Erro", "Utilizar nomes diferentes para os espaços!") 
    elif int(entryLotCafe1.get()) - int(entryLotCafe2.get()) > 1 or int(entryLotCafe1.get()) - int(entryLotCafe2.get()) < -1:                # Condição Diferença Lotacção café <= 1
        messagebox.showinfo("Erro", "Diferença entre as lotações das salas maior que 1")    
    else:
        cafes[entryNomeCafe1.get()]=entryLotCafe1.get()                             # Adicionar os inputs para a variavel 'cafes'
        cafes[entryNomeCafe2.get()]=entryLotCafe2.get()     
        salasecafe.append(entryNomeCafe1.get())                                     # Adiciona inputs para a lista 'salaseecafe'
        salasecafe.append(entryNomeCafe2.get())                        
        messagebox.showinfo("Concluido", "Cadastro das salas concluido")   
        gravarCadCafes['state']= tk.DISABLED                                        # Desabilitar o botão 'Cadastrar cafés'
        entryNomeCafe1.config(state='disabled')                                     # Limpar campos de entrada
        entryLotCafe1.config(state='disabled')
        entryNomeCafe2.config(state='disabled')
        entryLotCafe2.config(state='disabled')
        gravarCadMembros.config(state='normal')                                     # Habilitar botão 'Cadastrar novo participante'




#Função Botão 'gravar participante'
def gravarMembros():
    global evento
    global lista_membros
    global count_membros
    global salas
    global cafes
    global i                                                                                                        #Contador do processo iterativo abaixo
    cafes = {k: v for k, v in sorted(cafes.items(), key=lambda item: item[1], reverse = False)}                     # Organiza a variavel cafes em ordem crescente de lotação
    salas = {k: v for k, v in sorted(salas.items(), key=lambda item: item[1], reverse = False)}                     # Organiza a variavel salas em ordem crescente de lotação
    if len(entryCadMembros.get()) == 0:                                                                      # Condição Campo não vazio
        messagebox.showinfo("Erro", "Favor preencher o campo!")
    elif count_membros >= lotacao:                                                                           # Condição Lotação máxima atingida
        messagebox.showinfo("Erro", "Lotação máxima atingida!")
        gravarCadMembros.config(state = 'disabled')
    elif entryCadMembros.get() in lista_membros:                                                             # Condição nomes diferentes
        messagebox.showinfo("Erro", "Nome já está cadastrado")
                #### O Processo funciona em 4 casos, alternando para cada entrada de forma a fazer a alteração de sala diretamente ####
                # A variavel evento é adicionada de forma a futuramente poder selecionar eventos diferentes no banco
    else:                                   # Caso 1 - Participante 1Turno sala maior, 2Turno sala maior, Cafe maior (Maior lotação)
        if i == 0:
            lista_membros.append(entryCadMembros.get())                                                      # Adiciona membro na lista para verificação de nomes diferente
            c.execute("""INSERT INTO evento VALUES (:id,:nome,:sala1Turno,:sala2Turno,:cafe,:eventoNome)""", # Adiciona no banco as variaveis no primeiro caso
        {
            'id': count_membros,
            'nome': entryCadMembros.get(),
            'sala1Turno': list(salas.keys())[1],
            'sala2Turno': list(salas.keys())[1],
            'cafe': list(cafes.keys())[1],
            'eventoNome': evento
        })
            count_membros += 1
            conn.commit()
            i +=1                                                                                              # \/ Mensagem de sucesso no cadastro
            labelCadSuc = Label(windowPrincipal, text = str(entryCadMembros.get()) + 'Cadastrado com sucesso!', fg = 'Green', font = ('Arial', 12 , 'bold'))
            labelCadSuc.grid(column= 1, row = 13)
            entryCadMembros.delete(0,END)                                                                      #Esvazia o campo de entrada
            
        elif i ==1:                         # Caso 2 - Participante 1Turno sala menor, 2Turno sala menor, Cafe menor
            lista_membros.append(entryCadMembros.get())                                                      # Adiciona membro na lista para verificação de nomes diferente
            c.execute("""INSERT INTO evento VALUES (:id,:nome,:sala1Turno,:sala2Turno,:cafe,:eventoNome)""", # Adiciona no banco as variaveis no segundo caso
        {
            'id': count_membros,
            'nome': entryCadMembros.get(),
            'sala1Turno': list(salas.keys())[0],
            'sala2Turno': list(salas.keys())[0],
            'cafe': list(cafes.keys())[0],
            'eventoNome': evento
        })
            count_membros += 1
            conn.commit()
            i+=1                                                                                              # \/ Mensagem de sucesso no cadastro
            labelCadSuc = Label(windowPrincipal, text = str(entryCadMembros.get()) + 'Cadastrado com sucesso!', fg = 'Green', font = ('Arial', 12 , 'bold'))
            labelCadSuc.grid(column= 1, row = 13)
            entryCadMembros.delete(0,END)                                                                      #Esvazia o campo de entrada

        elif i == 2:                         # Caso 3 - Participante 1Turno sala menor, 2Turno sala maior, Cafe maior
            lista_membros.append(entryCadMembros.get())                                                      # Adiciona membro na lista para verificação de nomes diferente
            c.execute("""INSERT INTO evento VALUES (:id,:nome,:sala1Turno,:sala2Turno,:cafe,:eventoNome)""", # Adiciona no banco as variaveis no terceiro caso
        {
            'id': count_membros,
            'nome': entryCadMembros.get(),
            'sala1Turno': list(salas.keys())[1],
            'sala2Turno': list(salas.keys())[0],
            'cafe': list(cafes.keys())[1],
            'eventoNome': evento
        })
            count_membros += 1
            conn.commit()
            i +=1                                                                                              # \/ Mensagem de sucesso no cadastro
            labelCadSuc = Label(windowPrincipal, text = str(entryCadMembros.get()) + 'Cadastrado com sucesso!', fg = 'Green', font = ('Arial', 12 , 'bold'))
            labelCadSuc.grid(column= 1, row = 13)
            entryCadMembros.delete(0,END)                                                                      #Esvazia o campo de entrada

        elif i ==3:                         # Caso 4 - Participante 1Turno sala maior, 2Turno sala menor, Cafe menor
            lista_membros.append(entryCadMembros.get())
            c.execute("""INSERT INTO evento VALUES (:id,:nome,:sala1Turno,:sala2Turno,:cafe,:eventoNome)""", # Adiciona no banco as variaveis no quarto caso
        {
            'id': count_membros,
            'nome': entryCadMembros.get(),
            'sala1Turno': list(salas.keys())[0],
            'sala2Turno': list(salas.keys())[1],
            'cafe': list(cafes.keys())[0],
            'eventoNome': evento
        })
            count_membros += 1
            conn.commit()
            i = 0                                                                                              # \/ Mensagem de sucesso no cadastro
            labelCadSuc = Label(windowPrincipal, text = str(entryCadMembros.get()) + ' - Cadastrado com sucesso!', fg = 'Green', font = ('Arial', 12 , 'bold'))
            labelCadSuc.grid(column= 1, row = 13)
            entryCadMembros.delete(0,END)                                                                      #Esvazia o campo de entrada

    
    consulSala.config(state = 'normal')                                                                        # Libera os botoes de consultas após primeiro cadastro
    consulCafe.config(state = 'normal')
    consulPart.config(state = 'normal')





# Função Consultar Sala

def consultaSala():
    global evento
    if entryConsulSala.get() in salas:                                                                     # Condição - sala digitada em lista salas
        windowConsultaSala = tk.Tk()                                                                       # Cria janela
        windowConsultaSala.title("Consulta da sala" + str(entryConsulSala.get()))
        entrada = str(entryConsulSala.get())                                                               # Entrada
        c.execute("SELECT nome FROM Evento WHERE sala1Turno = ? AND eventoNome = ?",(entrada,evento))                               # Seleciona os nomes com sala em primeiro turno
        query = str(c.fetchall())                                                                          # !!!! Melhorar a forma de limpar dos dados !!!! 
        q1 = query.replace("[('", "")                                                                      # Limpando os dados pro print no label
        q2 =q1.replace("',), ('", "\n")
        q3=q2.replace("',)]","")
        labelQuerySalaTit = Label(windowConsultaSala, text = ' Participantes na sala "' + str(entryConsulSala.get()) + '" no primeiro turno: ') # Print dos dados no Primeiro Label
        labelQuerySalaTit.grid(column= 1 , row = 1)
        labelQuerySala = Label(windowConsultaSala, text = q3)
        labelQuerySala.grid(column=1,row=2)
        LabelQuerySalaTit1 = Label(windowConsultaSala, text = ' Participantes na sala "' + str(entryConsulSala.get()) + '" no segundo turno: ')  # Segundo Label
        LabelQuerySalaTit1.grid(column=1, row = 3)
        c.execute("SELECT nome FROM Evento WHERE sala2Turno = ? AND eventoNome = ?", (entrada,evento))                              # Selecionas os nomes com sala em segundo turno
        query2 = str(c.fetchall())
        q2_1 = query2.replace("[('", "")
        q2_2 =q2_1.replace("',), ('", "\n")
        q2_3=q2_2.replace("',)]","")
        LabelQuerySala2 = Label(windowConsultaSala, text = q2_3)                                           # Print dos nomes Que tem a sala em 2 turno
        LabelQuerySala2.grid(column=1,row =4 )
    else:                                                                                                  # Msg erro caso entrada não seja válida
        messagebox.showinfo("Erro", "Digitar uma sala válida")


    
# Função Consultar Espaço de Coffe-Break
def consultaEspaco():
    if entryConsulCafe.get() in cafes:                                                                      # Condição entrada na lista cafes
        windowConsultaCafe = tk.Tk()                                                                        # Cria Janela
        windowConsultaCafe.title("Consulta do espaço" + str(entryConsulCafe.get()))
        entrada = str(entryConsulCafe.get())
        c.execute("SELECT nome FROM Evento WHERE cafe = ? AND eventoNome = ?",(entrada,evento,))                                      # Sleciona os nomes no espaco de cafe da entrada
        query = str(c.fetchall())
        q1 = query.replace("[('", "")
        q2 =q1.replace("',), ('", "\n")
        q3=q2.replace("',)]","")
        labelQueryCafeTit = Label(windowConsultaCafe, text = ' Participantes no espaço "'  + str(entryConsulCafe.get()) + '" :')     # Label de abertura
        labelQueryCafeTit.grid(column= 1 , row = 1)
        labelQueryCafe = Label(windowConsultaCafe, text = q3)                                                                       # Label com os nomes
        labelQueryCafe.grid(column=1,row=2)

    else:                                                                                                   # Msg erro caso entrada não valida
        messagebox.showinfo("Erro", "Digitar um espaço válido")


#Função Consultar Participante
def consultaParticipante():
    if entryConsulPart.get() in lista_membros:                                                               # Condição entry na lista_membros
        windowConsulMembro= tk.Tk()                                                                          # Cria janela
        windowConsulMembro.title("Consulta de Participantes")
        entrada = str(entryConsulPart.get())
        c.execute("SELECT sala1Turno FROM Evento WHERE nome = ? AND eventoNome = ?",(entrada,evento,))            # Seleciona a sala 1 Turno do participante
        query = str(c.fetchall())
        q1 = query.replace("[('", "")
        q2 =q1.replace("',), ('", "\n")
        q3=q2.replace("',)]","")
        LabelQueryPartTit = Label(windowConsulMembro, text = ' O Participante "' + entrada + '" está registrado na sala "' + q3 + '" para o primeiro turno') # Print sala 1 turno do participante
        LabelQueryPartTit.grid(column = 0, row= 0)
        c.execute("SELECT sala2Turno FROM Evento WHERE nome = ? AND eventoNome = ?",(entrada,evento))               # Seleciona a sala 2 turno do participante
        query2 = str(c.fetchall())
        q2_1 = query2.replace("[('", "")
        q2_2 =q2_1.replace("',), ('", "\n")
        q2_3=q2_2.replace("',)]","")
        LabelQueryPart1 = Label(windowConsulMembro, text = ', Registrado na sala "' + q2_3 + '" para o segundo turno')    # Print sala 2 turno do participante
        LabelQueryPart1.grid(column = 0, row= 1)
        c.execute("SELECT cafe FROM Evento Where nome = ? AND eventoNome =?",(entrada,evento,))                         # Seleciona espaco cafe do participante
        query3 = str(c.fetchall())
        q3_1 = query3.replace("[('", "")
        q3_2 =q3_1.replace("',), ('", "\n")
        q3_3=q3_2.replace("',)]","")
        LabelQueryPart1 = Label(windowConsulMembro, text = 'e no espaço de Coffe-break ' + q3_3)                        # Print espaco cafe do aprticipante
        LabelQueryPart1.grid(column = 0, row= 2)






# Criar o banco Evento.db                                                   #Tabela    ----     id  ,   nome    ,   sala1Turno  ,   sala2Turno  ,   cafe    ,   eventoNome  -------
conn = sql.connect('Evento.db')                                             #entrada   ----     int     str          str              str           str             str
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS evento (
    id integer,
    nome text,
    sala1Turno text,
    sala2Turno text,
    cafe text,
    eventoNome text
    )""")

conn.commit()


# Inicia a janela principal
windowPrincipal = tk.Tk()
windowPrincipal.title("Cadastro e Consulta de eventos")
windowPrincipal.minsize(1024,768)

#### 1. Espaço Nome do Evento ####

# Campo para nomear evento
labelCadEvent = Label(windowPrincipal, text= "1. Criar evento:", font =('Arial', 16, 'bold'))
labelCadEvent2 = Label(windowPrincipal, text= "Digite o nome do evento: ")
entryNomeEvent = Entry(windowPrincipal,state = NORMAL)
labelCadEvent.grid(column=1, row =0, sticky =W)
labelCadEvent2.grid(column=1, row = 1, sticky =E)
entryNomeEvent.grid(column=2, row =1, sticky =W)
# Botão para nomear evento
gravarCadEvento= tk.Button(windowPrincipal, text='Nomear Evento', padx=10, pady=5, fg = "white", bg="#263D42", command = gravarEvento )
gravarCadEvento.grid(column = 3, row = 1)

#### 2. Espaço para Cadastro das Salas ####

# Campo para preenchimento do Cadastro de salas
labelCadSalas = Label(windowPrincipal, text= "2. Cadastro das salas:", font =('Arial', 16, 'bold'))
labelNomeSala1 = Label(windowPrincipal, text= "Digite o nome da primeira sala: ")
entryNomeSala1 = Entry(windowPrincipal,state = NORMAL)
labelLotSala1 = Label(windowPrincipal, text= "Digite a lotação da primeira sala: ")
entryLotSala1 = Entry(windowPrincipal)
labelNomeSala2 = Label(windowPrincipal, text= "Digite o nome da segunda sala: ")
entryNomeSala2 = Entry(windowPrincipal)
labelLotSala2 = Label(windowPrincipal, text= "Digite a lotação da segunda sala: ")
entryLotSala2 = Entry(windowPrincipal)
# Organização dos campos para Cadastro de Salas
labelCadSalas.grid(column=1, row =3, sticky = W)
labelNomeSala1.grid(column = 1, row =4, sticky = E)
entryNomeSala1.grid(column= 2, row =4)
labelLotSala1.grid(column= 1,row =5, sticky = E)
entryLotSala1.grid(column = 2,row =5)
labelNomeSala2.grid(column=1, row = 6, sticky = E)
entryNomeSala2.grid(column=2,row=6)
labelLotSala2.grid(column=1,row=7, sticky = E)
entryLotSala2.grid(column=2,row=7)
#Criar o Botão para Gravar o Cadastro de Salas
gravarCadSalas = tk.Button(windowPrincipal, text= "Cadastrar Sala", padx=10, pady=5, fg = "white", bg="#263D42", command = gravarSalas, state = 'disabled')
gravarCadSalas.grid(column=2,row=8)
#Espaçamento entre titulo e as outras linhas
windowPrincipal.grid_rowconfigure(1, minsize=40)
#Espaçamento entre os campos de cadastro de café e salas
windowPrincipal.grid_columnconfigure(3, minsize=80)

#### 3. Espaço para cadastro dos Cafés ####

# Campo para preenchimento do Cadastro dos cafés
labelCadCafes = Label(windowPrincipal, text= "3. Cadastro dos espaços de Coffe-Break:", font =('Arial', 16, 'bold'))
labelNomeCafe1 = Label(windowPrincipal, text= "Digite o nome do primeiro espaço: ")
entryNomeCafe1 = Entry(windowPrincipal)
labelLotCafe1 = Label(windowPrincipal, text= "Digite a lotação do primeiro espaço: ")
entryLotCafe1 = Entry(windowPrincipal)
labelNomeCafe2 = Label(windowPrincipal, text= "Digite o nome do segundo espaço: ")
entryNomeCafe2 = Entry(windowPrincipal)
labelLotCafe2 = Label(windowPrincipal, text= "Digite a lotação do segundo espaço: ")
entryLotCafe2 = Entry(windowPrincipal)
# Organização dos campos para Cadastro dos cafés
labelCadCafes.grid(column=4, row =3, sticky = W, columnspan= 2)
labelNomeCafe1.grid(column = 4, row =4, sticky = W)
entryNomeCafe1.grid(column= 5, row =4)
labelLotCafe1.grid(column= 4,row =5, sticky = W)
entryLotCafe1.grid(column = 5,row =5)
labelNomeCafe2.grid(column=4, row = 6, sticky = W)
entryNomeCafe2.grid(column=5,row=6)
labelLotCafe2.grid(column=4,row=7, sticky = W)
entryLotCafe2.grid(column=5,row=7)
# Botão para Gravar o Cadastro dos cafés
gravarCadCafes = tk.Button(windowPrincipal, text= "Cadastrar Espaço para Coffe-Break", padx=10, pady=5, fg = "white", bg="#263D42", command = gravarCafes, state = 'disabled')
gravarCadCafes.grid(column=5,row=8)

#### 4. Espaço cadastro de novos participantes #####

#Espaçamento entre Cadastro Membros e Cadastro Salas
windowPrincipal.grid_rowconfigure(9, minsize=40)
#Espaçamento entre titulo e as outras linhas
windowPrincipal.grid_rowconfigure(10, minsize=40)
# Campos preenchimento
labelCadMembros = Label(windowPrincipal, text= "4. Cadastrar Participantes", font =('Arial', 16, 'bold'))
labelCadMembros1 = Label(windowPrincipal, text = "Nome completo do Participante: ")
entryCadMembros = Entry(windowPrincipal)
labelCadMembros.grid(column= 1, row = 11)
labelCadMembros1.grid(column= 1, row = 12)
entryCadMembros.grid(column = 2, row = 12)
# #Espaço na linha para mensagem em baixo do campos
# windowPrincipal.grid_rowconfigure(13, minsize=20)
#Botão para Cadastro
gravarCadMembros = tk.Button(windowPrincipal, text= ' Cadastrar novo Participante', padx=10, pady=5, fg = "white", bg="#263D42",command = gravarMembros, state = 'disabled' )
gravarCadMembros.grid(column= 2, row = 13)


#### 5. Espaço  Consultar Salas

labelConsSala = Label(windowPrincipal, text= "5. Consultar Sala", font =('Arial', 16, 'bold'))
labelConsSala.grid(column= 4, row = 11, sticky = W, columnspan=2)
labelConsSala1 = Label ( windowPrincipal, text = ' Digite a sala que deseja consultar:')
labelConsSala1.grid(column = 4, row = 12)
entryConsulSala= Entry(windowPrincipal)
entryConsulSala.grid(column= 5, row = 12 )
# Definir botão Consultar Sala
consulSala = tk.Button(windowPrincipal, text= 'Consultar sala', padx=10, pady=5, fg = "white", bg="#263D42",command = consultaSala, state = 'disabled' )
consulSala.grid(column= 4, row = 13, sticky= E)




#### 6. Espaço Consulta espaços de Coffe-Break####

labelConsCafe = Label(windowPrincipal, text= "6. Consultar Espaço de Coffe-Break", font =('Arial', 16, 'bold'))
labelConsCafe.grid(column= 1, row = 15, sticky = W, columnspan=2)
labelConsCafe1 = Label ( windowPrincipal, text = ' Digite o espaço que deseja consultar:')
labelConsCafe1.grid(column = 1, row = 16)
entryConsulCafe= Entry(windowPrincipal)
entryConsulCafe.grid(column= 2, row = 16 )
# Definir botão Consultar espaço
consulCafe = tk.Button(windowPrincipal, text= 'Consultar espaço', padx=10, pady=5, fg = "white", bg="#263D42",command = consultaEspaco, state = 'disabled' )
consulCafe.grid(column= 1, row = 17, sticky= E)
windowPrincipal.grid_rowconfigure(14, minsize=40)


#### 6. Espaço Consulta de Participante####

labelConsPart = Label(windowPrincipal, text= "7. Consultar Participante", font =('Arial', 16, 'bold'))
labelConsPart.grid(column= 4, row = 15, sticky = W, columnspan=2)
labelConsPart1 = Label ( windowPrincipal, text = ' Digite o nome completo do participante que deseja consultar:')
labelConsPart1.grid(column = 4, row = 16)
entryConsulPart= Entry(windowPrincipal)
entryConsulPart.grid(column= 5, row = 16 )
# Definir botão Consultar espaço
consulPart = tk.Button(windowPrincipal, text= 'Consultar Participante', padx=10, pady=5, fg = "white", bg="#263D42",command = consultaParticipante, state = 'disabled' )
consulPart.grid(column= 4, row = 17, sticky= E)
windowPrincipal.grid_rowconfigure(14, minsize=40)





windowPrincipal.mainloop()