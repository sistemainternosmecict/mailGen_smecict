#!/usr/bin/env python3
"""
Script para remover versões de pacotes de um arquivo requirements.txt
Mantém apenas os nomes dos pacotes, removendo operadores de versão e números.
"""

import re
import sys
from pathlib import Path


def remover_versoes(linha):
    """
    Remove versões e operadores de uma linha do requirements.txt
    
    Args:
        linha: String contendo a linha do requirements
    
    Returns:
        String com apenas o nome do pacote
    """
    # Remove espaços em branco no início e fim
    linha = linha.strip()
    
    # Ignora linhas vazias e comentários
    if not linha or linha.startswith('#'):
        return linha
    
    # Remove tudo após operadores de versão (==, >=, <=, >, <, ~=, !=)
    # ou após caracteres especiais como @ (para URLs de git)
    linha_limpa = re.split(r'[=<>!~@\[]', linha)[0].strip()
    
    return linha_limpa


def processar_arquivo(arquivo_entrada, arquivo_saida=None):
    """
    Processa o arquivo requirements.txt e remove as versões
    
    Args:
        arquivo_entrada: Caminho do arquivo requirements.txt original
        arquivo_saida: Caminho do arquivo de saída (opcional)
    """
    arquivo_entrada = Path(arquivo_entrada)
    
    if not arquivo_entrada.exists():
        print(f"Erro: Arquivo '{arquivo_entrada}' não encontrado!")
        sys.exit(1)
    
    # Define o arquivo de saída
    if arquivo_saida is None:
        arquivo_saida = arquivo_entrada.parent / f"{arquivo_entrada.stem}_sem_versoes{arquivo_entrada.suffix}"
    else:
        arquivo_saida = Path(arquivo_saida)
    
    # Lê o arquivo original
    with open(arquivo_entrada, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    
    # Processa cada linha
    linhas_processadas = []
    for linha in linhas:
        linha_limpa = remover_versoes(linha)
        if linha_limpa:  # Adiciona apenas se não for vazia
            linhas_processadas.append(linha_limpa + '\n')
    
    # Salva o arquivo processado
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        f.writelines(linhas_processadas)
    
    print(f"✓ Processamento concluído!")
    print(f"  Arquivo original: {arquivo_entrada}")
    print(f"  Arquivo gerado: {arquivo_saida}")
    print(f"  Total de pacotes: {len([l for l in linhas_processadas if not l.startswith('#')])}")


def main():
    """Função principal"""
    if len(sys.argv) < 2:
        print("Uso: python remover_versoes.py <arquivo_requirements.txt> [arquivo_saida]")
        print("\nExemplos:")
        print("  python remover_versoes.py requirements.txt")
        print("  python remover_versoes.py requirements.txt requirements_clean.txt")
        sys.exit(1)
    
    arquivo_entrada = sys.argv[1]
    arquivo_saida = sys.argv[2] if len(sys.argv) > 2 else None
    
    processar_arquivo(arquivo_entrada, arquivo_saida)


if __name__ == "__main__":
    main()
