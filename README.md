# Scripts uteis para gerenciamento do WORKSPACE

Como rodar

```python3

Iniciar o UV
$ uv init

Iniciar o venv do projeto
$ uv run

Sincronizar dependencias do projeto
$ uv sync

```

- createRooms: realiza a criação de salas na unidade indicada
    - Edite o PARENT_ORG_PATH para o nome da unidade no workspace
    - Edite o SALAS para uma lista de strings contendo o numero da sala ou da turma
    - Rode o script: uv run createRooms.py
