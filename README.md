# 📧 Sistema de Gestão de Usuários Google Workspace

Secretaria Municipal de Educação, Cultura, Inclusão, Ciência e Tecnologia

## 📌 Descrição Geral

Este software foi desenvolvido para automatizar e agilizar a criação, atualização, listagem e remoção de contas de e-mail institucionais no Google Workspace da Secretaria Municipal de Educação, Cultura, Inclusão, Ciência e Tecnologia.

Ele é voltado principalmente para:

- Criação de e-mails institucionais de alunos
- Atualização em massa de senhas
- Organização de usuários por Unidades Organizacionais (OU)
- Integração com arquivos Excel para operações em lote

O sistema utiliza a Google Admin SDK (Directory API) e depende de credenciais geradas no Google Cloud Platform.

## 🏛️ Instituição

Secretaria Municipal de Educação, Cultura, Inclusão, Ciência e Tecnologia
Subsecretaria de Tecnologia – Setor de TI

## 👨‍💻 Autor

- Autor: Thyéz de Oliveira Monteiro
- Cargo: Assessor de Informática
- Local de Trabalho: Sala 25
- Setor: TI – Subsecretaria de Tecnologia
- Ano de Desenvolvimento: 2024

Projeto desenvolvido com o objetivo de **otimizar processos administrativos**, reduzir trabalho manual e evitar erros na criação de contas institucionais.

## ⚙️ Tecnologias Utilizadas

- Python 3.10+
- Google Admin SDK (Directory API)
- Google Cloud Platform
- Pandas / OpenPyXL (para Excel)
- JSON
- APIs do Google

## 🔐 Pré-requisitos

- Python instalado

```python
python --version
``` 

- Credenciais do Google Cloud
- Criar um projeto no Google Cloud
- Ativar a Admin SDK API
Criar uma Service Account
Delegar autoridade no Google Workspace
Gerar o arquivo de credenciais (.json)

## Permissões necessárias

- Gerenciar usuários
- Criar, editar e remover contas
- Alterar senhas
- Listar usuários por OU

## ⚠️ Sem essas credenciais, o sistema não funcionará.

```
📁 Estrutura Básica do Projeto
📦 projeto
 ┣ 📜 main.py
 ┣ 📜 gad.py
 ┣ 📜 conversor_json.py
 ┣ 📜 credenciais.json
 ┣ 📜 README.md
```

## 🚀 Inicialização

```python
from gad import GoogleAdminDirectory

admin_directory = GoogleAdminDirectory("VARIOS_ALUNOS.xlsx")
```

O arquivo Excel pode ser usado para operações em lote, como criação ou redefinição de senhas.

## 📘 Tutorial de Uso das Funções

🔹 1. Listar usuários (com limite)
admin_directory.list_users(20)


### 📌 Lista até 20 usuários do domínio.

🔹 2. Buscar e-mail pelo nome completo
admin_directory.get_email_by_fullname("Alice Victória Rangel")


### 📌 Retorna o e-mail institucional associado ao nome completo informado.

🔹 3. Criar um novo usuário
admin_directory.insert_user(
    "123456@smec.saquarema.rj.gov.br",
    "João",
    "Silva",
    "senhaInicial123",
    "/ESCOLAS/Escola Municipal Vilatur"
)


### 📌 Cria um novo usuário com:

E-mail

Nome

Sobrenome

Senha inicial

Unidade Organizacional

🔹 4. Atualizar usuário existente
admin_directory.update_user(
    "123456@smec.saquarema.rj.gov.br",
    password="novaSenha123",
    org_unit_path="/ESCOLAS/Escola Municipal Vilatur",
    change_password_at_next_login=False
)


### 📌 Permite:

Alterar senha

Mudar unidade organizacional

Definir se o usuário deve trocar a senha no próximo login

🔹 5. Remover usuário
admin_directory.delete_user("usuario@smec.saquarema.rj.gov.br")


### 📌 Remove permanentemente a conta do Google Workspace.

⚠️ Ação irreversível.

🔹 6. Operações em lote com lista de alunos
alunos = [
    {"nome": "Aluno de exemplo", "matricula": "00000000000000"},
]

for aluno in alunos:
    admin_directory.update_user(
        f"{aluno['matricula']}@smec.saquarema.rj.gov.br",
        password="vilatur123",
        org_unit_path="/ESCOLAS/Escola Municipal Vilatur",
        change_password_at_next_login=False
    )


### 📌 Ideal para:

Atualizar vários usuários

Resetar senhas em massa

Padronizar OU

🔹 7. Listar usuários por Unidade Organizacional
admin_directory.list_users_by_org_unit(
    "/ESCOLAS/Casa Creche Dona Zildinha",
    10
)


### 📌 Lista usuários pertencentes a uma OU específica.

🔹 8. Ler alunos de um arquivo Excel
alunos = admin_directory.read_novos_alunos()


### 📌 Lê automaticamente os dados de alunos a partir de um .xlsx.

🔹 9. Criar usuários a partir de Excel
toadd = admin_directory.prepare_users_from_xlsx()
admin_directory.insert_users_from_prepared_list(toadd)


### 📌 Fluxo completo:

Lê o Excel

Prepara os dados

Cria os usuários automaticamente

🔹 10. Remover usuários com base em Excel
admin_directory.delete_users_from_xlsx()


### 📌 Remove contas listadas no arquivo Excel.

🔹 11. Resetar senhas usando Excel
admin_directory.reset_passwords_from_xlsx()


### 📌 Ideal para início de ano letivo ou redefinições em massa.

🔹 12. Converter Markdown para Excel
admin_directory.convert_md_to_xlsx("test.md", "output.xlsx")


### 📌 Útil para transformar relatórios em planilhas.

## 🔒 Segurança

As credenciais **NUNCA** devem ser compartilhadas
O acesso deve ser restrito ao setor de TI
Recomenda-se armazenar o arquivo .json fora do repositório público

## 📄 Licença e Uso

Software de uso institucional interno, exclusivo da
Secretaria Municipal de Educação, Cultura, Inclusão, Ciência e Tecnologia.