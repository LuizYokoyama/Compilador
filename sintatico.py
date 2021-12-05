# Powered by Luiz Yokoyama Felix de Souza

# ATENÇÃO! É PRECISO INSTALAR A API PANDAS COM O COMANDO NO PROMPT: pip install pandas
import pandas as pd
import lexico  # importa o meu analizador léxico

nSimb = {   1:	["P'", 'P', 1],
            2:	['P', 'inicio V A', 3],
            3:	['V', 'varinicio LV', 2],
            4:	['LV',	'D LV',	2],
            5:	['LV',	'varfim;',	2],
            6:	['D',	'id TIPO;',	3],
            7:	['TIPO',	'int',	1],
            8:	['TIPO',	'real',	1],
            9:	['TIPO',	'lit',	1],
            10:	['A',	'ES A',	2],
            11:	['ES',	'leia id;',	3],
            12:	['ES',	'escreva ARG;',	3],
            13:	['ARG',	'literal',	1],
            14:	['ARG',	'num',	1],
            15:	['ARG',	'id',	1],
            16:	['A',	'CMD A',	2],
            17:	['CMD',	'id rcb LD;',	4],
            18:	['LD',	'OPRD opm OPRD',	3],
            19:	['LD',	'OPRD',	1],
            20:	['OPRD',	'id',	1],
            21:	['OPRD',	'num',	1],
            22:	['A',	'COND A',	2],
            23:	['COND',	'CABEÇALHO CORPO',	2],
            24:	['CABEÇALHO',	'se ( EXP_R ) então',	5],
            25:	['EXP_R',	'OPRD opr OPRD',	3],
            26:	['CORPO',	'ES CORPO',	2],
            27:	['CORPO',	'CMD CORPO',	2],
            28:	['CORPO',	'COND CORPO',	2],
            29:	['CORPO',	'fimse',	1],
            30:	['A',	'fim',	1]
            }

goto = pd.read_csv('goto.csv', na_filter=False, delimiter=';')
acoes = pd.read_csv('actions.csv', na_filter=False, delimiter=';')
pilha = [0]
ps = []
validar = []
t = 0
s = 0 # seja s o estado topo da pilha
a = [] # seja a símbolo de w$
ACTION_sa = ''
tBeta = 0
A = ''
B = ''
x = 0
linha = 0
coluna = 0
linhaAnt = 0
tAnt = []
tAntAnt = []
token = []
colunaAnt = 0
qtdErros = 0
lex = ''

def action():
    global t
    global tBeta
    global A
    global B
    global s
    global a
    global ACTION_sa
    s = pilha.pop()
    pilha.append(s)
    ACTION_sa = ''
    ACTION_sa = acoes[a][s]
    if ACTION_sa == '':
        return
    if ACTION_sa == 'accept':
        A = nSimb[1][0]
        B = nSimb[1][1]
        imprima_produ_A_B()
        if qtdErros == 0:
            print(ACTION_sa)
        return
    t = acoes[a][s][1:]  # numero do estado
    t = int(t)
    if ACTION_sa[0] == 'R':
        tBeta = nSimb[t][2]  # tamanho de Beta
        A = nSimb[t][0]
        B = nSimb[t][1]

def seja_a(arq):
    global a, qtdErros, lex, tAnt, tAntAnt, token
    global linha, linhaAnt
    global coluna, colunaAnt

    while True:
        tAntAnt = tAnt
        tAnt = token
        token = lexico.lexico(arq)  # solicita o token ao analisador léxico
        print(token)
        if token[0] == 'ERRO':  # se for erro léxico
            qtdErros += 1
            print('\033[31m'+'Erro Léxico: ' + token[1]+', ' + token[2]+'\033[0;0m')  # imprime o erro
        elif token[0][0] == 'ERRO_C':  # se for erro léxico: char inválido
            qtdErros += 1
            print('\033[31m'+'Erro Léxico: ' + token[1][1]+', ' + token[1][2]+'\033[0;0m')  # imprime o erro
        else:
            a = token[0][1]  # símbolo
            lex = token[0][0]  # lexema
            linhaAnt = linha
            colunaAnt = coluna
            linha = token[1][0]
            coluna = token[1][1]
            break

def desempilhaTamanhoBeta():
    global validar
    for i in range(tBeta):
        pilha.pop()
        validar.append(ps.pop())

def faca_t_ser_topo_pilha():
    global t
    t = pilha.pop()
    pilha.append(t)

def achaTokenSinc(arq):
    while True:
        seja_a(arq)
        if a in ['PT_V','fim','$']:
            break

def empilhe_goto_tA():
    if goto[A][t] != '':
        pilha.append(int(goto[A][t]))
    else:
        pilha.append(1)

def imprima_produ_A_B():
    print('\033[36m'+"Produção: "+'\033[0;0m' + A + " -> " + B)






def sintatico(arq):

    seja_a(arq)
    while True:
        action()
        if ACTION_sa != '':
            if ACTION_sa[0] == 'S':
                pilha.append(t)
                ps.append(token)
                seja_a(arq)
            elif ACTION_sa[0] == 'R':
                desempilhaTamanhoBeta()
                faca_t_ser_topo_pilha()
                empilhe_goto_tA()
                imprima_produ_A_B()
            elif ACTION_sa == 'accept':
                if qtdErros == 0:
                    print('\033[34m'+'Código reconhecido com sucesso!'+'\033[0;0m')
                else:
                    print('\033[31m'+'O código não foi reconhecido pois apresenta: '+str(qtdErros)+' Erro(s)'+'\033[0;0m')
                break
            else:
                chameRotinaRecuperacaoDeErro(arq)
        else:
            chameRotinaRecuperacaoDeErro(arq)











def chameRotinaRecuperacaoDeErro(arq):

    global qtdErros, a, x
    if not x:
        qtdErros += 1
        print('\033[31m'+'ERRO SINTÁTICO:'+'\033[0;0m')
    if ACTION_sa == 'e0':
        print('\033[31m'+'Palavra chave "inicio" é esperada - linha: '+str(linha)+' coluna: '+str(coluna)+'\033[0;0m')
        if a != 'varinicio':
            seja_a(arq)
        pilha.append(2)
        return
    elif ACTION_sa == 'e1':
        print('\033[31m'+'Palavra chave "varinicio" é esperada - linha: '+str(linha)+' coluna: '+str(coluna)+'\033[0;0m')
        seja_a(arq)
        pilha.append(4)
        return
    elif ACTION_sa == 'e2':
        print('\033[31m'+'É esperado o ";" - linha: '+str(linhaAnt)+' coluna: '+str(colunaAnt)+'\033[0;0m')
    elif ACTION_sa == 'e3':
        print('\033[31m'+'Palavra chave "varfim" é esperada - linha: '+str(linha)+' coluna: '+str(coluna)+'\033[0;0m')
        seja_a(arq)
        pilha.append(17)
        return
    elif ACTION_sa == 'e4':
        if lex == '(':
            print('\033[31m'+'Palavra chave "se" é esperada - linha: ' + str(linha) + ' coluna: ' + str(coluna)+'\033[0;0m')
            seja_a(arq)
            pilha.append(54)
            return
        if lex != 'escreva':
            print('\033[31m'+'Palavra chave "escreva" é esperada - linha: '+str(linhaAnt)+' coluna: '+str(colunaAnt)+'\033[0;0m')
            seja_a(arq)
            pilha.append(30)
        else:
            print('\033[31m'+'Não esperado: "id" - linha: ' + str(linhaAnt) + ' coluna: ' + str(colunaAnt)+'\033[0;0m')
            pilha.pop()
        return
    elif ACTION_sa == 'e5':
        print('\033[31m' + 'Palavra chave "então" é esperada - linha: ' + str(linha) + ' coluna: ' + str(coluna) + '\033[0;0m')
        if a != 'escreva' and a != 'se':
            seja_a(arq)
        pilha.append(9)
        return
    elif ACTION_sa == 'e6':
        print('\033[31m'+'É esperado o tipo: "inteiro, real ou lit" - linha: '+str(linhaAnt)+' coluna: '+str(colunaAnt)+'\033[0;0m')
        seja_a(arq)
        pilha.append(23)
        return
    elif ACTION_sa == 'e7':
        if lex == '(':
            print('\033[31m'+'É esperado "se" - linha: ' + str(linhaAnt) + ' coluna: ' + str(colunaAnt)+'\033[0;0m')
            pilha.append(3)
            pilha.append(53)
            return
        print('\033[31m'+'Não esperado: "'+lex+'" - linha: '+str(linha)+' coluna: '+str(coluna)+'\033[0;0m')
        if a == 'inteiro' or a == 'real':
            seja_a(arq)
        elif a == 'lit':
            achaTokenSinc(arq)
            achaTokenSinc(arq)
            achaTokenSinc(arq)
            achaTokenSinc(arq)
            achaTokenSinc(arq)
            pilha.append(16)
            return
        pilha.pop()
        return
    elif ACTION_sa == 'e8':
        if tAntAnt[0][1] == 'fimse':
            print('\033[31m' + 'Falta "fimse" - linha: ' + str(linhaAnt) + ' coluna: ' + str(colunaAnt) + '\033[0;0m')
            pilha.pop(); pilha.pop(); x = 1
            achaTokenSinc(arq)
            return
        elif tAnt[0][0] == 'ERRO_C':
            achaTokenSinc(arq)
            return
        if not x: print('\033[31m'+'Não esperado: "'+lex+'" - linha: '+str(linha)+' coluna: '+str(coluna-1)+'\033[0;0m')
        x = 1
        pilha.pop()
        achaTokenSinc(arq)
        pilha.append(32)
        return
    elif ACTION_sa == 'e9':
        if lex == '(':
            print('\033[31m'+'Palavra chave "se" é esperada - linha: ' + str(linha) + ' coluna: ' + str(coluna)+'\033[0;0m')
            pilha.pop()
            pilha.append(11)
            pilha.append(53)
            pilha.append(54)
            seja_a(arq)
            return
        if not x: print('\033[31m'+'Não esperado o "'+lex+'" - linha: '+str(linhaAnt)+' coluna: '+str(colunaAnt)+'\033[0;0m')
        seja_a(arq)
        return
    elif ACTION_sa == 'e10':
        print('\033[31m'+'É esperado fechar parênteses. Encontrado: "'+lex+'" - linha: '+str(linhaAnt)+' coluna: '+str(colunaAnt)+'\033[0;0m')
        seja_a(arq)
        return
    elif ACTION_sa == 'e11':
        print('\033[31m'+'Não esperado: "'+lex+'" - linha: '+str(linhaAnt)+' coluna: '+str(colunaAnt)+'\033[0;0m')
        if a == 'entao':
            pilha.pop()
            pilha.append(9)
        achaTokenSinc(arq)
        return
    elif ACTION_sa == 'e12':
        print('\033[31m'+'Não esperado o "'+lex+'" - linha: '+str(linha)+' coluna: '+str(coluna)+'\033[0;0m')
        achaTokenSinc(arq)
        return
    elif ACTION_sa == 'e13':
        print('\033[31m'+'Esperado operador matemático ou ";". Encontrado: "'+lex+'" - linha: '+str(linhaAnt)+' coluna: '+str(colunaAnt)+'\033[0;0m')
        seja_a(arq)
        pilha.append(38)
        return
    elif ACTION_sa == 'e14':
        print('\033[31m'+'É esperada Expressão Relacional - linha: '+str(linha)+' coluna: '+str(coluna)+'\033[0;0m')
        seja_a(arq)
        if a == 'OPR':
            pilha.append(55)
            return
    elif ACTION_sa == 'e15':
        print('\033[31m'+'É esperado Operador Relacional - linha: '+str(linha)+' coluna: '+str(coluna)+'\033[0;0m')
        pilha.append(56)
        return
    elif ACTION_sa == 'e16':
        print('\033[31m'+'É esperada Expressão Relacional - linha: '+str(linha)+' coluna: '+str(coluna-1)+'\033[0;0m')
        if a == 'OPM':
            pilha.append(56)
            pilha.append(57)
            seja_a(arq)
            seja_a(arq)
            return
        else:
            a = 'FC_P'
        pilha.append(56)
        pilha.append(57)
        return
    elif ACTION_sa == 'e17':
        if tAntAnt[0][1] == 'fimse':
            print('\033[31m' + 'Falta "fimse" - linha: ' + str(linhaAnt) + ' coluna: ' + str(colunaAnt) + '\033[0;0m')
            pilha.pop(); pilha.pop(); x = 1
            achaTokenSinc(arq)
            return
        x = 1
        print('\033[31m'+'É esperado Operador de Atribuição - linha: '+str(linha)+' coluna: '+str(coluna)+'\033[0;0m')
        pilha.pop()
        achaTokenSinc(arq)
        return
    elif ACTION_sa == 'e18':
        if not x: print('\033[31m'+'Não esperado o "'+lex+'" - linha: '+str(linha)+' coluna: '+str(coluna)+'\033[0;0m')
        pilha.pop()
    achaTokenSinc(arq)

