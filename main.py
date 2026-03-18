from gad import GoogleAdminDirectory
from conversor_json import converter_json_para_lista
from createRooms import criar_sala
import json

admin_directory = GoogleAdminDirectory("alunos_gustavo_formatado.xlsx")

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
#     {"nome": "Aluno de exemplo", "matriculicula": "00000000000000"},
# ]

for idx, aluno in enumerate(alunos, start=1):
    if not aluno["matricula"] == None:
        mat = aluno["matricula"]
#        turma = int(aluno["Turma"])
#        turma_str = str(turma)
#        unidade = aluno["Unidade"]
#        senha = aluno["senha"]
        senha = "#gustavo123"
#        unidade_para_sala = f"/ESCOLAS/{unidade}"
#        if unidade_para_sala and turma_str:
#            admin_directory.criar_sala(unidade_para_sala, turma_str)
        print(f" ------------------")
        print(f"Processando ID: {idx} MATRICULA: {mat} ")
    # TRATAR O NOME COMPLETO ---------------------------------------
        nome_list = aluno["nome"].split(" ")
   # pre_mail = (f"{nome_list[0]}{nome_list[1][0]}{nome_list[-1]}").lower()
    # nome_temp = admin_directory.resumir_nome(aluno['Nome'])

    # INSERIR NOVO USUARIO---------------------------------------------------
    if admin_directory.insert_user(f'{mat}@smec.saquarema.rj.gov.br', nome_list[0], " ".join(nome_list[1:]), senha, f"/ESCOLAS/Colégio Municipal Gustavo Campos Da Silveira"):
        print(f"Usuário {mat} inserido com sucesso.")
    else:        
        print(f"Falha ao inserir usuário {mat}.")

    # OBTER EMAIL PELO NOME COMPLETO-----------------------------------------
    # admin_directory.get_email_by_fullname(aluno['Nome'])

    # ATUALIZAR USUARIO------------------------------------------------------
    admin_directory.update_user(f'{mat}@smec.saquarema.rj.gov.br', password=senha, org_unit_path=f"/ESCOLAS/Colégio Municipal Gustavo Campos Da Silveira", change_password_at_next_login=False)

    # REMOVER USUARIO-------------------------------------------------------
#    admin_directory.delete_user(f"{aluno['Matricula']}@smec.saquarema.rj.gov.br")
    print("===================")

#FIM FIM DO LOOPING-------------------------------------------------------------
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
#toadd = admin_directory.prepare_users_from_xlsx()
#print(toadd)
#admin_directory.insert_users_from_prepared_list(toadd)

# REMOVER USUARIOS DO ARQUIVO EXCEL (novos_alunos.xlsx)
# admin_directory.delete_users_from_xlsx()

# CONVERTER MD para XLSX
# admin_directory.convert_md_to_xlsx("test.md", "output.xlsx")

# ATUALIZAR SENHA PELO ARQUIVO EXCEL
#admin_directory.reset_passwords_from_xlsx("luciana123", False)
