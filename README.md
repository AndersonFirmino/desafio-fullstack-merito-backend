# Dashboard de Investimentos - Mérito Invest Backend

## 📘 Descrição do Projeto
Sistema de API RESTful para gerenciamento de fundos de investimento e transações, permitindo visualizar o resumo da carteira de investimentos do cliente. Desenvolvido como parte do desafio técnico da Mérito Investimentos.

### Tecnologias Utilizadas
- Django 4.2
- Django REST Framework 3.14
- SQLite (Banco de dados local)
- Docker e Docker Compose
- Pytest (Testes automatizados)
- GitHub Actions (CI/CD)

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos
- Python 3.11+
- Pip (Gerenciador de pacotes do Python)

### Passo a passo

1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd merito_invest_backend
```

2. Crie e ative um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências
```bash
pip install -r requirements.txt
```

4. Execute as migrações
```bash
python manage.py migrate
```

5. Carregue os dados iniciais (seed)
```bash
python manage.py seed
```

6. Inicie o servidor de desenvolvimento
```bash
python manage.py runserver
```

O servidor estará disponível em http://localhost:8000

## 🐳 Como Executar com Docker

1. Certifique-se de ter o Docker e o Docker Compose instalados

2. Execute o comando para construir e iniciar os containers
```bash
docker compose up --build
```

O servidor estará disponível em http://localhost:8000

## 🧪 Testes

Execute os testes automatizados com o comando:
```bash
pytest
```

## 📬 Endpoints Principais

- `/api/investment-funds/` – CRUD de fundos de investimento
- `/api/transactions/` – CRUD de movimentações (aportes e resgates)
- `/wallet/summary/` – Resumo da carteira do cliente com valores atualizados

## 📡 Como Testar a API

A API pode ser testada de várias maneiras:

- **Navegador**: Django REST Framework fornece uma interface interativa para testar os endpoints
- **Ferramentas**: Postman ou Insomnia são ótimas opções para testar APIs
- **Terminal**: Usando comandos curl diretamente no terminal

### Exemplos práticos com curl:

#### Listar fundos
```bash
curl http://localhost:8000/api/investment-funds/
```

#### Criar fundo
```bash
curl -X POST http://localhost:8000/api/investment-funds/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Fundo XPTO", "ticker": "XPTO11", "fund_type": "FII", "unit_price": "100.00"}'
```

#### Listar transações
```bash
curl http://localhost:8000/api/transactions/
```

#### Criar transação
```bash
curl -X POST http://localhost:8000/api/transactions/ \
  -H "Content-Type: application/json" \
  -d '{"fund": 1, "transaction_type": "aporte", "value": "500.00", "quantity": "5", "date": "2025-05-11"}'
```

#### Ver resumo da carteira
```bash
curl http://localhost:8000/wallet/summary/
```

> Substitua `fund: 1` pelo ID real do fundo cadastrado, se necessário.

## ⚙️ CI/CD com GitHub Actions

O projeto utiliza GitHub Actions para automação de testes e build de imagem Docker sempre que houver mudanças na branch main. A configuração do workflow pode ser encontrada em:

`.github/workflows/deploy.yml`

O pipeline realiza:
1. Verificação de formatação de código com Black
2. Execução de testes automatizados
3. Build da imagem Docker
4. Preparação para deploy (configurável conforme necessidade)

---

⚠️ Este projeto foi desenvolvido exclusivamente para fins de avaliação técnica.
