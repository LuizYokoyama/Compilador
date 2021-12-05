# Powered by Luiz Yokoyama Felix de Souza

import string

# VARIÁVEIS GLOBAIS
linha = 1
coluna = 1

# TABELA DE TRANSIÇÃO DE ESTADOS E TAMBÉM DE ESTADOS FINAIS: "prox"
prox = {
    0: {'*': 17, '+': 17, '-': 17, '/': 17, '<': 13, '>': 16, '=': 15, '(': 18, ')': 19, '{': 10, ';': 20, '\n': 0,
        '"': 7, '0': 1, '1': 1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1, '9': 1, ' ': 0, '\t': 0}, # ainda serão inseridas as letras
    1: {'E': 4, 'e': 4, '.': 2, '0': 1, '1': 1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 1, '8': 1, '9': 1},
    2: {'0': 3, '1': 3, '2': 3, '3': 3, '4': 3, '5': 3, '6': 3, '7': 3, '8': 3, '9': 3},
    3: {'E': 4, 'e': 4, '0': 3, '1': 3, '2': 3, '3': 3, '4': 3, '5': 3, '6': 3, '7': 3, '8': 3, '9': 3},
    4: {'+': 5, '-': 5, '0': 6, '1': 6, '2': 6, '3': 6, '4': 6, '5': 6, '6': 6, '7': 6, '8': 6, '9': 6},
    5: {'0': 6, '1': 6, '2': 6, '3': 6, '4': 6, '5': 6, '6': 6, '7': 6, '8': 6, '9': 6},
    6: {'0': 6, '1': 6, '2': 6, '3': 6, '4': 6, '5': 6, '6': 6, '7': 6, '8': 6, '9': 6},
    7: {'á': 7, 'é': 7, 'í': 7, 'ó': 7, 'ú': 7, 'à': 7, 'ã': 7, 'â': 7, 'ê': 7, 'ô': 7, 'ç': 7,
        'Á': 7, 'É': 7, 'Í': 7, 'Ó': 7, 'Ú': 7, 'À': 7, 'Ã': 7, 'Â': 7, 'Ê': 7, 'Ô': 7, 'Ç': 7, 'º': 7, 'ª': 7},
    9: {'_': 9, '0': 9, '1': 9, '2': 9, '3': 9, '4': 9, '5': 9, '6': 9, '7': 9, '8': 9, '9': 9},  # ainda serão inseridas as letras
    10: {'á': 10, 'é': 10, 'í': 10, 'ó': 10, 'ú': 10, 'à': 10, 'ã': 10, 'â': 10, 'ê': 10, 'ô': 10, 'ç': 10, 'Á': 10,
         'É': 10, 'Í': 10, 'Ó': 10, 'Ú': 10, 'À': 10, 'Ã': 10, 'Â': 10, 'Ê': 10, 'Ô': 10, 'Ç': 10, 'º': 10, 'ª': 10},
    13: {'-': 14, '>': 15, '=': 15},
    16: {'=': 15},
    'final': {1: 'Num', 3: 'Num', 6: 'Num', 8: 'Literal', 9: 'id', 11: 'Comentário', 12: 'EOF',
              13: 'OPR', 14: 'RCB', 15: 'OPR', 16: 'OPR', 17: 'OPM', 18: 'AB_P', 19: 'FC_P', 20: 'PT_V'}
    }
# COMPLEMENTAÇÃO DA TABELA DE TRANSIÇÃO DE ESTADOS "prox"
L = {L: 9 for L in string.ascii_letters}
prox[0].update(L)     # insere o reconhecimento de letras para o Estado 0
prox[9].update(L)     # insere o reconhecimento de letras para o Estado 9
T = {T: 7 for T in string.printable}
prox[7].update(T)     # insere o reconhecimento de todos os caracteres, exceto os acentuados, ç, º e ª
prox[7].update({'"': 8})    # " tem que ir para o estado 8
prox[7].pop('\n')  # retira o \n, então, \n vai indicar o fim da sequência
T = {T: 10 for T in string.printable}
prox[10].update(T)    # insere o reconhecimento de todos os caracteres, exceto os acentuados, ç, º e ª
prox[10].update({'}': 11})    # } tem que ir para o estado 11
prox[10].pop('\n')  # retira o \n, então, \n vai indicar o fim da sequência

# CRIAÇÃO DA TABELA DE SÍMBOLOS --- estrutura: [LEXEMA, TOKEN, TIPO]
simbolos = ['inicio', 'varinicio', 'se', 'varfim', 'escreva','leia', 'entao', 'fimse', 'fim', 'inteiro', 'lit', 'real']  # lista de simbolos, auxiliar da criação da tabela de símbolos
tSimb = {simbolos[i] : [simbolos[i] , simbolos[i], simbolos[i]] for i in range(len(simbolos))}  # Cria a tabela de Símbolos "tSimb"

def lexico(arq):
    pAnt = arq.tell()  # registra a posição de inicio da leitura do lexema no arquivo fonte
    pos = pAnt  # como ainda não leu nenhum caractere, a posição atual é a mesma da anterior
    estado = 0  # inicia o autômato no estado 0
    c = ''  # declara a variável que receberá o caractere lido do arquivo fonte
    token = ''  # declara a variável que receberá o nome do token reconhecido
    lexema = ''  # declara a variável que receberá a sequência reconhecida
    erro = ''
    global linha  # contador de linhas
    global coluna  # contador de colunas
    while token == '':  # enquanto não for fim de arquivo
        c = arq.read(1)  # Lê um caracter no arquivo fonte
        pAnt = pos  # posiçao anterior de leitura
        pos += 1    # posição atual de leitura no arquivo
        if estado == 0:
            lexema = ''  # no estado 0, o espaço, \n e \t são reconhecidos mas não devem ser retornados
        if estado in prox:         # testa se possui prox, para evitar erro de chave se não possuir
            if c in prox[estado]:  # testa se o caracter lido leva a um próximo estado, para evitar erro de chave se não levar
                estado = prox[estado][c]  # agora sim, caracter lido leva a um próximo estado
                if c != '\n':  # \n é reconhecido, mas não será retornado
                    lexema += c  # o caractere reconhecido é adicionado ao lexema
                    coluna += 4 if c == '\t' else 1 # aumenta o número da coluna se for tabulação, neste caso, a tabulação vale 4 colunas
                else:
                    linha += 1  # se for quebra de linha, incrementa o contador de linhas
                    coluna = 1  # se for quebra de linha, o contador de colunas recomeça em 1
            elif estado in prox['final']:  # verifica o estado final
                token = prox['final'][estado]  # localiza o nome do token do estado final
            else:
                if c == '':  # se fim de arquivo
                    return [['$', '$', ''], [linha, coluna]]   # retorna o tokem de fim de arquivo fonte
                if c == '\n':  # indica quebra de linha sem ter fechado aspas ou chave
                    arq.seek(pAnt)  # posiciona a leitura após o erro, voltando o \n
                    if estado == 7:  # deveria ter fechado aspas
                        return ['ERRO', 'linha: ' + str(linha) + ', coluna: ' + str(coluna -1), 'Aspas não fechadas: ' + lexema]
                    elif estado == 10:  # deveria ter fechado chaves
                        return ['ERRO', 'linha: ' + str(linha) + ', coluna: ' + str(coluna - 1), 'Chaves  não fechadas: ' + lexema]
                erro = ['ERRO', 'linha: ' + str(linha)+  ', coluna: '+str(coluna), 'caractere inválido: ' + str(c)]  # caractere inválido neste estado
        else:
            token = prox['final'][estado]

    if c != '':  # se não chegou ao final do arquivo
        if arq.tell() == pos + 1 or linha < 3 :  # evitar o Bug do Python: tell() só retorna um número preciso se o arquivo for lido como binário
            arq.seek(pos)  # volta a leitura, pois o último caracter lido não entrou na cadeia reconhecida, então, deverá ser relido
        else:
            arq.seek(pAnt)  # se der Bug do Python, tem que voltar mais uma posição
    if erro != '':
        return [['ERRO_C', token, ''], erro]   # retorna o token de erro: caracter inválido

    if token == 'id':  # se for id, será preciso registrar na tabela de símbolos
        if lexema in tSimb:  # verifica se já tem na tabela de símbolos
            return [tSimb[lexema], [linha, coluna]]  # Retorna o token encontrado na tabela de símbolos
        else:  # se não tiver na tabela de símbolos, será inserido:
            tSimb.update({lexema: [lexema, token, lexema]})  # insere o novo identificador na tabela de símbolos
            return [tSimb[lexema], [linha, coluna]]  # Retorna o token que acabou se ser inserido, e já é encontrado na tabela de símbolos
    else:
        if token == 'Comentário':
            return lexico(arq)   # Não retorna comentários, retorna o próximo token
        return [[lexema, token, lexema], [linha, coluna]]  if token != 'RCB' else [[lexema, token, '='], [linha, coluna]]  # retorna o token








