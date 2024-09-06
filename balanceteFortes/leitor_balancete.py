import pdfplumber
import pandas as pd
import re

def leitor_balancete(file):
    """Recebe um pdf com um balancete emitido pelo Fortes AC e o transforma em um
    Pandas Dataframe"""
  # Abrir o arquivo PDF
    with pdfplumber.open('mod_balancete_fortes.pdf') as pdf:
        pages = pdf.pages
        text = ''
        for page in pages:
            text += page.extract_text()

    # Dividir o texto em linhas
    lines = text.split('\n')

    # Inicializar listas para as colunas
    conta = []
    descricao = []
    saldo_anterior = []
    debitos = []
    creditos = []
    saldo_atual = []
    tipo_saldo = []

    # Flag para iniciar a extração após a linha "Conta"
    start_extracting = False

    # Regex ajustado para capturar os dados corretamente
    pattern = re.compile(r'^(\d[\d.]*)\s+(.+[\w]*)\s+(\d{1,3}(?:\.\d{3})*,\d{2})\s+(\d{1,3}(?:\.\d{3})*,\d{2})\s+(\d{1,3}(?:\.\d{3})*,\d{2})\s+(\d{1,3}(?:\.\d{3})*,\d{2})\s+([DC])')

    pattern_sem_DC = re.compile(r'^(\d[\d.]*)\s+(.+[\w]*)\s+(\d{1,3}(?:\.\d{3})*,\d{2})\s+(\d{1,3}(?:\.\d{3})*,\d{2})\s+(\d{1,3}(?:\.\d{3})*,\d{2})\s+(\d{1,3}(?:\.\d{3})*,\d{2})')

    for line in lines:
        if line.startswith("Conta"):
            start_extracting = True
            continue
        if start_extracting:
            if line.startswith("quinta-feira"):
                break

            # Aplicar regex para capturar os dados
            match = pattern.search(line)
            #print(line)
            if match:
                conta.append(match.group(1))
                descricao.append(match.group(2).strip())
                saldo_anterior.append(match.group(3).replace('.', '').replace(',', '.'))
                debitos.append(match.group(4).replace('.', '').replace(',', '.'))
                creditos.append(match.group(5).replace('.', '').replace(',', '.'))
                saldo_atual.append(match.group(6).replace('.', '').replace(',', '.'))
                tipo_saldo.append(match.group(7))
            else:
                match = pattern_sem_DC.search(line)
                if match:  
                    conta.append(match.group(1))
                    descricao.append(match.group(2).strip())
                    saldo_anterior.append(match.group(3).replace('.', '').replace(',', '.'))
                    debitos.append(match.group(4).replace('.', '').replace(',', '.'))
                    creditos.append(match.group(5).replace('.', '').replace(',', '.'))
                    saldo_atual.append(match.group(6).replace('.', '').replace(',', '.'))
                    tipo_saldo.append('0')
    # Criar o DataFrame
    df = pd.DataFrame({
        'Conta': conta,
        'Descrição': descricao,
        'Saldo Anterior': saldo_anterior,
        'Débitos': debitos,
        'Créditos': creditos,
        'Saldo Atual': saldo_atual,
        'TipoSaldo': tipo_saldo
    })

        # Converter colunas numéricas para float
    df[['Saldo Anterior', 'Débitos', 'Créditos', 'Saldo Atual']] = df[['Saldo Anterior', 'Débitos', 'Créditos', 'Saldo Atual']].astype(float)

    # Exibir o DataFrame
    return(df)

print(leitor_balancete('mod_balancete_fortes.pdf'))

print(leitor_balancete.__doc__)