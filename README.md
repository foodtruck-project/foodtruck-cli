# Food Truck CLI

Uma interface de linha de comando para gerenciamento de food trucks construída com Python e UV.

## 🚀 Configuração Rápida

### Pré-requisitos
- Python 3.13 ou superior
- UV package manager

### Script de Instalação

O projeto oferece um script de instalação cross-platform:

- **`install.py`** - Script Python cross-platform (Windows, Linux, macOS)

### Instalação
```bash
# Clone o repositório
git clone <seu-repo-url>
cd foodtruck-cli

# Configuração completa com um comando
uv run task init
```

### Instalação Manual
```bash
# Instalar dependências e CLI
uv sync

# Usando o script Python (cross-platform)
python3 install.py
```

## 📖 Como Usar

### Executar o CLI:
```bash
# Forma mais simples
uv run foodtruck

# Após instalação global
foodtruck
```

### Comandos Disponíveis:
```bash
# Verificar dependências
foodtruck check

# Configurar ambiente de desenvolvimento
foodtruck setup

# Gerar scripts de completion
foodtruck completion
```



### Shell Completion:
```bash
# Gerar scripts de completion para todos os shells
foodtruck completion

# Instalar completion para um shell específico
foodtruck completion bash --install
foodtruck completion zsh --install
foodtruck completion fish --install
foodtruck completion powershell --install

# Gerar e salvar em arquivo específico
foodtruck completion bash --output ~/.local/share/bash-completion/completions/foodtruck
```

### Qualidade de Código:
```bash
# Verificar código
uv run task lint

# Verificar tipos
uv run task typecheck

# Executar testes
uv run task test
```

## 🏗️ Estrutura do Projeto

```
foodtruck-cli/
├── foodtruck_cli/           # Pacote principal
│   ├── __init__.py         # Inicialização do pacote
│   ├── main.py            # Ponto de entrada CLI
│   ├── console.py         # Utilitários de console
│   └── commands/          # Comandos do CLI
│       ├── __init__.py    # Inicialização dos comandos
│       ├── check.py       # Comando de verificação
│       ├── completion.py  # Comando de completion
│       ├── setup.py       # Comando de configuração
│       └── foodtruck.yaml # Especificação do carapace para completion
├── pyproject.toml        # Configuração do projeto
├── install.py            # Script de instalação Python (cross-platform)
└── README.md            # Este arquivo
```

## 🔧 Script de Instalação

### Características do `install.py`

| Característica | Valor |
|----------------|-------|
| **Plataforma** | Cross-platform (Windows, Linux, macOS) |
| **Dependências** | Python 3.6+ |
| **Shell Support** | zsh, bash, PowerShell |
| **Wrapper Script** | `.bat` (Windows), `.sh` (Unix) |
| **Encoding** | UTF-8 com fallback |

### Vantagens

- ✅ Funciona em Windows, Linux e macOS
- ✅ Suporte nativo ao PowerShell no Windows
- ✅ Melhor tratamento de encoding
- ✅ Criação automática de diretórios
- ✅ Mensagens de erro mais detalhadas
- ✅ Código mais modular e testável

- ✅ Suporte a Bash, Zsh e PowerShell
- ✅ Auto-completion com carapace-bin

## 🔧 Configuração de Qualidade

### Ruff (Linter)
O projeto usa o Ruff para verificação de código com as seguintes configurações:

```toml
[tool.ruff]
target-version = "py313"    # Python 3.13+
line-length = 88           # Comprimento de linha

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "A", "C4", "SIM", "TCH", "Q", "ARG", "PIE", "T20", "PYI", "PT", "RSE", "RET", "SLF", "SLOT", "PTH", "ERA", "PD", "PGH", "PL", "TRY", "NPY", "AIR", "PERF", "FURB", "LOG", "RUF"]
ignore = ["E501", "B008", "C901", "T201", "PLW1510", "PLC0415"]
```

#### Regras Principais:
- **E, F, W**: Erros e warnings básicos (pycodestyle, pyflakes)
- **I**: Organização de imports (isort)
- **N**: Nomenclatura (pep8-naming)
- **UP**: Upgrades de sintaxe (pyupgrade)
- **B**: Detecção de bugs (flake8-bugbear)
- **A**: Builtins (flake8-builtins)
- **C4**: Comprehensions (flake8-comprehensions)
- **SIM**: Simplificações (flake8-simplify)
- **TCH**: Type checking (flake8-type-checking)
- **Q**: Quotes (flake8-quotes)
- **ARG**: Argumentos não utilizados
- **PIE**: Python idioms (flake8-pie)
- **T20**: Print statements
- **PYI**: Type stubs
- **PT**: Pytest style
- **RSE**: Raise statements
- **RET**: Return statements
- **SLF**: Self
- **SLOT**: Slots
- **PTH**: Pathlib
- **ERA**: Comentários
- **PD**: Pandas
- **PGH**: PyGrep hooks
- **PL**: Pylint
- **TRY**: Try/except
- **NPY**: NumPy
- **AIR**: Airflow
- **PERF**: Performance
- **FURB**: Refurb
- **LOG**: Logging
- **RUF**: Regras específicas do Ruff

#### Regras Ignoradas:
- **E501**: Linha muito longa (controlado por line-length)
- **B008**: Chamadas de função em argumentos padrão
- **C901**: Função muito complexa
- **T201**: Print statements (permitido para CLIs)
- **PLW1510**: subprocess.run sem check explícito
- **PLC0415**: Import dentro de função (útil para testes)

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.
