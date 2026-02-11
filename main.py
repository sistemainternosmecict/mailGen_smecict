from gad import GoogleAdminDirectory
from conversor_json import converter_json_para_lista
import json

admin_directory = GoogleAdminDirectory("arquivo_formatado.xlsx")

# LISTAR TODOS OS USUARIOS, COM LIMITE DE REGISTROS-------------------------
# admin_directory.list_users(20)

# OBTER EMAIL PELO NOME COMPLETO---------------------------------------------
# admin_directory.get_email_by_fullname("Alice Victória Rangel")

#
#
# LOOPING RODAR EM UMA LISTA DE ALUNOS NO MODELO ABAIXO-----------------------

# LER ARQUIVO EXCEL (novos_alunos.xlsx)
alunos = admin_directory.read_novos_alunos()
# print(alunos)

# alunos = [
#     {"nome": "Aluno de exemplo", "matricula": "00000000000000"},
# ]

for aluno in alunos[9630:]:
    print(f"Processando aluno: {aluno['Nome']} - Matrícula: {aluno['Matricula']} Senha: {aluno['Senha']} - Unidade: {aluno['Unidade']}")
    # TRATAR O NOME COMPLETO ---------------------------------------
    nome_list = aluno["Nome"].split(" ")
    # pre_mail = (f"{nome_list[0]}{nome_list[1][0]}{nome_list[-1]}").lower()
    # nome_temp = admin_directory.resumir_nome(aluno['Nome'])
    
    # INSERIR NOVO USUARIO---------------------------------------------------
    if admin_directory.insert_user(f'{aluno["Matricula"]}@smec.saquarema.rj.gov.br', nome_list[0], " ".join(nome_list[1:]), aluno["Senha"], f'/ESCOLAS/{aluno["Unidade"]}'):
        print(f"Usuário {aluno['Matricula']} inserido com sucesso.")
    else:        print(f"Falha ao inserir usuário {aluno['Matricula']}.")

    # OBTER EMAIL PELO NOME COMPLETO-----------------------------------------
    # admin_directory.get_email_by_fullname(aluno['Nome'])
    
    # ATUALIZAR USUARIO------------------------------------------------------
    admin_directory.update_user(f"{aluno['Matricula']}@smec.saquarema.rj.gov.br", password=aluno["Senha"], org_unit_path=f"/ESCOLAS/{aluno['Unidade']}", change_password_at_next_login=False)
    
    # REMOVER USUARIO-------------------------------------------------------
    # admin_directory.delete_user(f"{nome_temp}@smec.saquarema.rj.gov.br")

# FIM DO LOOPING-------------------------------------------------------------
#
#

# INSERÇAO DE UM NOVO USUARIO--------------------------------------------------
# admin_directory.insert_user("THYEZ@smec.saquarema.rj.gov.br", "THYEZ", "OLIVEIRA", "provisorio2025", "/SMECICT")

# REMOÇÃO DE UM USUARIO--------------------------------------------------------
# admin_directory.delete_user("anonimo@smec.saquarema.rj.gov.br")

# ATUALIZAÇÃO DE USUARIO----------------------------------------------------
# admin_directory.update_user("00000000000@smec.saquarema.rj.gov.br", password="#ESCOLA123")

# LISTAR USUARIOS POR UNIDADE ORGANIZACIONAL--------------------------------
# admin_directory.list_users_by_org_unit("/ESCOLAS/Casa Creche Dona Zildinha", 10)


# print(alunos)
# for aluno in alunos:
#     print(aluno["Matricula"], aluno["Nome"], aluno["Unidade"])
#     data = admin_directory.get_email_by_fullname(aluno['Nome'])
    # print(f"Email do aluno: {data['primaryEmail']}")

# ADICIONAR USUARIOS DO ARQUIVO EXCEL (novos_alunos.xlsx)
# toadd = admin_directory.prepare_users_from_xlsx()
# print(toadd)
# admin_directory.insert_users_from_prepared_list(toadd)

# REMOVER USUARIOS DO ARQUIVO EXCEL (novos_alunos.xlsx)
# admin_directory.delete_users_from_xlsx()

# CONVERTER MD para XLSX
# admin_directory.convert_md_to_xlsx("test.md", "output.xlsx")

# ATUALIZAR SENHA PELO ARQUIVO EXCEL
# admin_directory.reset_passwords_from_xlsx()