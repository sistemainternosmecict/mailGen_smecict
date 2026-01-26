import json

def converter_json_para_lista(json_data):
    data = json.loads(json_data) if isinstance(json_data, str) else json_data

    alunos = []
    for user in data.get("users", []):
        nome = f"{user.get('First Name [Required]', '').strip()} {user.get('Last Name [Required]', '').strip()}"
        email = user.get("Email Address [Required]", "")
        matricula = email.split("@")[0] if "@" in email else ""
        alunos.append({
            "matricula": matricula,
            "nome": nome.title().strip()
        })

    return alunos

if __name__ == "__main__":
    with open("todos_alunos_vilatur.json", "r", encoding="utf-8") as f:
        dados = json.load(f)

    alunos = converter_json_para_lista(dados)
    print(alunos)