# Powered by Luiz Yokoyama Felix de Souza

# ATENÇÃO! É PRECISO INSTALAR A API PANDAS COM O COMANDO NO PROMPT: pip install pandas

import lexico
import sintatico  # importa o meu analizador sintático

arq = open('FONTE.ALG')  # Carrega o arquivo fonte

if __name__ == '__main__':
    sintatico.sintatico(arq)

arq.close()  # Fecha do arquivo fonte #BOAPRATICA