import pandas as pd
import re

def formatar_nome_escola(nome):
    """
    Formata o nome da escola de MAIÚSCULAS para Título Adequado.
    Mantém preposições e artigos em minúsculas quando apropriado.
    """
    if pd.isna(nome):
        return nome
    
    # Palavras que devem ficar em minúsculas (exceto no início)
    palavras_minusculas = {'da', 'de', 'do', 'das', 'dos', 'e', 'em', 'o', 'a', 'os', 'as'}
    
    # Converte para minúsculas e divide em palavras
    palavras = str(nome).lower().split()
    
    # Formata cada palavra
    palavras_formatadas = []
    for i, palavra in enumerate(palavras):
        # Primeira palavra sempre com inicial maiúscula
        if i == 0:
            palavras_formatadas.append(palavra.capitalize())
        # Palavras que devem ficar em minúsculas
        elif palavra in palavras_minusculas:
            palavras_formatadas.append(palavra)
        # Demais palavras com inicial maiúscula
        else:
            palavras_formatadas.append(palavra.capitalize())
    
    return ' '.join(palavras_formatadas)

def gerar_senha(nome_escola):
    """
    Gera senha no formato #primeirapalavrarelevante123
    """
    if pd.isna(nome_escola):
        return ""
    
    # Converte para minúsculas
    nome = str(nome_escola).lower()
    
    # Prefixos a serem removidos
    prefixos = [
        'escola municipal ',
        'escola municipalizada ',
        'creche municipal ',
        'casa creche ',
        'colegio ',
        'colégio ',
        'centro municipal de educacao ',
        'centro municipal de educação '
    ]
    
    # Remove o prefixo
    for prefixo in prefixos:
        if nome.startswith(prefixo):
            nome = nome[len(prefixo):]
            break
    
    # Palavras a serem ignoradas
    palavras_ignorar = {'vereador', 'vereadora', 'professor', 'professora', 'doutor', 'doutora', 'dr', 'dra'}
    
    # Divide em palavras e pega a primeira palavra relevante
    palavras = nome.split()
    primeira_palavra = ""
    
    for palavra in palavras:
        if palavra not in palavras_ignorar:
            primeira_palavra = palavra
            break
    
    if not primeira_palavra:
        primeira_palavra = palavras[0] if palavras else ""
    
    # Remove acentos e caracteres especiais
    primeira_palavra = primeira_palavra.replace('ã', 'a').replace('á', 'a').replace('â', 'a')
    primeira_palavra = primeira_palavra.replace('é', 'e').replace('ê', 'e')
    primeira_palavra = primeira_palavra.replace('í', 'i')
    primeira_palavra = primeira_palavra.replace('ó', 'o').replace('ô', 'o').replace('õ', 'o')
    primeira_palavra = primeira_palavra.replace('ú', 'u')
    primeira_palavra = primeira_palavra.replace('ç', 'c')
    
    # Remove caracteres não alfanuméricos
    primeira_palavra = re.sub(r'[^a-z0-9]', '', primeira_palavra)
    
    return f"#{primeira_palavra}123"

# Ler o arquivo XLSX
arquivo_entrada = 'alunos.xlsx'  # Altere para o nome do seu arquivo
arquivo_saida = 'arquivo_formatado.xlsx'

# Ler o arquivo
df = pd.read_excel(arquivo_entrada)

# Formatar a terceira coluna (índice 2 - coluna "Unidade")
if len(df.columns) >= 3:
    nome_coluna = df.columns[2]
    df[nome_coluna] = df[nome_coluna].apply(formatar_nome_escola)
    
    # Gerar senhas baseadas na coluna de unidade
    senhas = df[nome_coluna].apply(gerar_senha)
    
    # Inserir a coluna de senha na posição 7 (índice 6)
    if len(df.columns) >= 6:
        # Se já existem 6 ou mais colunas, insere na posição 6 (7ª coluna)
        df.insert(6, 'Senha', senhas)
    else:
        # Se não, adiciona no final
        df['Senha'] = senhas
    
    # Salvar o arquivo formatado
    with pd.ExcelWriter(arquivo_saida, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
        
        # Ajustar a formatação da coluna de matrícula para evitar notação científica
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        
        # Formatar a primeira coluna como número inteiro
        for row in range(2, len(df) + 2):  # Começa em 2 porque a linha 1 é o cabeçalho
            cell = worksheet.cell(row=row, column=1)
            cell.number_format = '0'  # Formato de número inteiro sem decimais
    
    print(f"Arquivo formatado salvo como: {arquivo_saida}")
    print("\nPrimeiras linhas:")
    print(df.head(10))
else:
    print("Erro: O arquivo não possui 3 colunas.")