import os.path
import pandas as pd
import unicodedata

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/admin.directory.user"]

class GoogleAdminDirectory:
    def __init__(self, excel_filename):
        self.creds = self.authenticate()
        self.service = build("admin", "directory_v1", credentials=self.creds)
        self.file_path = excel_filename
        self.defaultPassword = "#osiris123"

    def authenticate(self):
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        return creds

    def list_users(self, max_results=10):
        print("Getting the first", max_results, "users in the domain")
        results = (
            self.service.users()
            .list(customer="my_customer", maxResults=max_results, orderBy="email")
            .execute()
        )
        users = results.get("users", [])
        if not users:
            print("No users in the domain.")
        else:
            print("Users:")
            for user in users:
                print(f"{user['primaryEmail']} ({user['name']['fullName']})")

    def get_user_by_fullname(self, full_name):
        results = (
            self.service.users()
            .list(customer="my_customer", maxResults=10)
            .execute()
        )
        users = results.get("users", [])
        for user in users:
            print(f"{user['primaryEmail']} ({user['name']['fullName']})")

    def get_email_by_fullname(self, full_name):
        results = (
            self.service.users()
            .list(customer="my_customer", maxResults=100)
            .execute()
        )
        users = results.get("users", [])
        
        # Normaliza o nome de busca (remove acentos e converte para minúsculas)
        normalized_search_name = unicodedata.normalize('NFD', full_name.lower()).encode('ASCII', 'ignore').decode('ASCII')
        
        for user in users:
            if 'name' in user and 'fullName' in user['name']:
                if user['name']['fullName'] == full_name:
                    print(user)
                # user_full_name = user['name']['fullName']
            #     # Normaliza o nome do usuário para comparação
                # normalized_user_name = unicodedata.normalize('NFD', user_full_name.lower()).encode('ASCII', 'ignore').decode('ASCII')
                
            #     # Verifica se o nome corresponde (busca exata ou parcial)
                # if user_full_name == full_name:
                #     print(user)
                #     return {
                #         "primaryEmail": user.get("primaryEmail", "")
                #     }
            #             "fullName": user_full_name,
            #             "givenName": user['name'].get("givenName", ""),
            #             "familyName": user['name'].get("familyName", ""),
            #             "orgUnitPath": user.get("orgUnitPath", ""),
            #             "isAdmin": user.get("isAdmin", False),
            #             "isEnforcedIn2Sv": user.get("isEnforcedIn2Sv", False),
            #             "isEnrolledIn2Sv": user.get("isEnrolledIn2Sv", False),
            #             "creationTime": user.get("creationTime", ""),
            #             "lastLoginTime": user.get("lastLoginTime", ""),
            #             "suspended": user.get("suspended", False)
            #         }
        
        # Se não encontrou o usuário, retorna None
        print(f"Usuário com nome '{full_name}' não encontrado.")
        return None
    
    def list_users_by_org_unit(self, org_unit_path, max_results=10):
        print(f"Getting users from organizational unit: {org_unit_path}")
        results = (
            self.service.users()
            .list(customer="my_customer", query=f"orgUnitPath='{org_unit_path}'", maxResults=max_results, orderBy="email")
            .execute()
        )
        users = results.get("users", [])
        if not users:
            print(f"No users found in {org_unit_path}.")
        else:
            print("Users:")
            for user in users:
                print(f"{user['primaryEmail']} ({user['name']['fullName']})")

    def insert_user(self, primary_email, given_name, family_name, password, org_unit_path="/", changePasswordAtNextLogin=False):
        user_info = {
            "primaryEmail": primary_email,
            "name": {
                "givenName": given_name,
                "familyName": family_name
            },
            "password": password,
            "orgUnitPath": org_unit_path,
            "changePasswordAtNextLogin": changePasswordAtNextLogin
        }
        try:
            user = self.service.users().insert(body=user_info).execute()
            print(f"[REGISTRADO] Usuário {user['primaryEmail']} criado!")
            return True
        except Exception as e:
            if e.reason == "Entity already exists.":
                print(f"[CANCELADO] Usuário já registrado! {user_info['primaryEmail']}")
            return False
    
    def delete_user(self, primary_email):
        try:
            self.service.users().delete(userKey=primary_email).execute()
            print(f"[REMOVIDO] Usuário {primary_email} removido.")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def update_user(self, primary_email, given_name=None, family_name=None, new_primary_email=None, password=None, org_unit_path=None, change_password_at_next_login=False):
        user_info = {}
        
        if given_name or family_name:
            user_info["name"] = {}
            if given_name:
                user_info["name"]["givenName"] = given_name
            if family_name:
                user_info["name"]["familyName"] = family_name
        
        if new_primary_email:
            user_info["primaryEmail"] = new_primary_email
        
        if password:
            user_info["password"] = password
        
        if org_unit_path:
            user_info["orgUnitPath"] = org_unit_path
        
        # Adiciona a configuração para forçar mudança de senha no próximo login
        user_info["changePasswordAtNextLogin"] = change_password_at_next_login
        
        if not user_info:
            print("No update parameters provided.")
            return
        
        try:
            updated_user = self.service.users().update(userKey=primary_email, body=user_info).execute()
            print(f"User {primary_email} updated successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def read_novos_alunos(self):
        if not os.path.exists(self.file_path):
            print("File not found: novos_alunos.xlsx")
            return []
        
        df = pd.read_excel(self.file_path)
        return df.to_dict(orient="records")
    
    def prepare_users_from_xlsx(self):
        alunos = self.read_novos_alunos()
        if not alunos:
            print("No student data found.")
            return []
        
        prepared_users = []
        for aluno in alunos:
            mat = aluno.get("mat")
            nome_completo = aluno.get("nome", " ").split()
            given_name = nome_completo[0]
            family_name = " ".join(nome_completo[1:]) if len(nome_completo) > 1 else ""
            primary_email = f"{mat}@smec.saquarema.rj.gov.br"
            password = self.defaultPassword
            org_unit_path = "/"
            
            prepared_users.append({
                "primaryEmail": primary_email,
                "givenName": given_name,
                "familyName": family_name,
                "password": password,
                "orgUnitPath": org_unit_path
            })
        
        return prepared_users
    
    def insert_users_from_prepared_list(self, prepared_users):
        for idx ,user in enumerate(prepared_users):
            status = "CANCELADO"
            res = self.insert_user(
                user["primaryEmail"], 
                user["givenName"], 
                user["familyName"], 
                user["password"], 
                user["orgUnitPath"]
            )

            if res:
                status = "INSERIDO"

            self.update_status_in_xlsx(idx, status)

    def convert_md_to_xlsx(self, markdown_file, output_xlsx):
        with open(markdown_file, "r", encoding="utf-8") as f:
            md_content = f.readlines()
        
        data = []
        for line in md_content:
            if "|" in line: #and not line.startswith("|"):
                columns = [col.strip() for col in line.split("|") if col.strip()]
                print(columns)
                if len(columns) == 3:
                    data.append({"mat": columns[2], "nome": columns[1]})
        
        if data:
            df = pd.DataFrame(data)
            df.to_excel(output_xlsx, index=False)
            print(f"Converted {markdown_file} to {output_xlsx}")
        else:
            print("No valid data found in the Markdown file.")

    def delete_users_from_xlsx(self):
        alunos = self.read_novos_alunos()
        if not alunos:
            print("No student data found.")
            return
        
        for aluno in alunos:
            mat = aluno.get("mat")
            primary_email = f"{mat}@smec.saquarema.rj.gov.br"
            self.delete_user(primary_email)
    
    def update_status_in_xlsx(self, row_index, status):
        if not os.path.exists(self.file_path):
            print("Arquivo não encontrado:", self.file_path)
            return
        
        df = pd.read_excel(self.file_path)
        if "status" not in df.columns:
            df["status"] = ""
        
        df.at[row_index, "status"] = status
        df.to_excel(self.file_path, index=False)
        print(f"Status atualizado na linha {row_index}: {status}")

    def reset_passwords_from_xlsx(self, new_password="provisorio2025", force_change_at_login=True):
        if not os.path.exists(self.file_path):
            print("Arquivo não encontrado:", self.file_path)
            return
        
        df = pd.read_excel(self.file_path)
        if df.empty or "email" not in df.columns:
            print("Arquivo não possui uma coluna 'email'.")
            return
        
        print(f"Iniciando redefinição de senhas para: {new_password}")
        if force_change_at_login:
            print("Usuários serão forçados a alterar a senha no próximo login.")
        
        for idx, row in df.iterrows():
            email = row["email"]
            if pd.notna(email):
                try:
                    self.update_user(
                        primary_email=email,
                        password=new_password,
                        change_password_at_next_login=force_change_at_login
                    )
                    status_msg = "SENHA ATUALIZADA"
                    if force_change_at_login:
                        status_msg += " (MUDANÇA OBRIGATÓRIA)"
                    print(f"[ATUALIZADO] Senha redefinida para {email}")
                    df.at[idx, "status"] = status_msg
                except Exception as e:
                    print(f"Erro ao atualizar senha para {email}: {e}")
                    df.at[idx, "status"] = f"ERRO: {e}"
            else:
                print(f"Linha {idx}: email vazio ou inválido")
                df.at[idx, "status"] = "EMAIL INVÁLIDO"
        
        df.to_excel(self.file_path, index=False)
        print("Processo de redefinição de senhas concluído.")
    
    def resumir_nome(self, nome: str) -> str:
        # palavras que devem ser removidas
        ignorar = {"de", "da", "do", "dos"}
        
        # transforma em minúsculo e divide por espaços
        partes = nome.lower().split()
        
        if len(partes) == 0:
            return ""
        
        # primeiro nome completo
        primeiro = partes[0]
        
        # último sobrenome completo
        ultimo = partes[-1]
        
        # sobrenomes do meio (descartando os "de", "da", etc.)
        meio = [p[0] for p in partes[1:-1] if p not in ignorar]
        
        # junta tudo
        resultado = primeiro + "".join(meio) + ultimo
        return resultado
