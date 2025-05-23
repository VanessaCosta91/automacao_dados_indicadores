# Automação de Indicadores de E-commerce com BigQuery + Python

Este projeto desenvolve e automatiza KPIs operacionais e estratégicos de uma base pública de e-commerce.

---

## Principais KPIs

- Vendas por mês
- Ticket médio por categoria
- Tempo médio de entrega
- Percentual de devoluções e cancelamentos
- Volume de pedidos por mês

---

## Pipeline automatizada

O projeto executa as etapas de ETL com:

- **Extração:** dados coletados diretamente do Google BigQuery (`thelook_ecommerce`)
- **Transformação:** cálculos de KPIs, médias móveis, percentuais e crescimento mês a mês
- **Carga:** exportação dos dados para `.csv` para visualização no Power BI

---

## Agregações e cálculos em Python

- Conversão de consultas SQL para DataFrame (`google.cloud.bigquery`)
- Cálculos Complementares:
  - Crescimento percentual mês a mês (`pct_change`)
  - Média móvel de 3 meses (`rolling`)
- Exportação dos Resultados para `.csv`

---

## Tecnologias Utilizadas

- Python 
- Google BigQuery
- Pandas
- Power BI
- Agendador de Tarefas (Windows)

---


## Como executar o projeto

1. Clone o repositório:

```bash
git clone https://github.com/VanessaCosta91/automacao_dados_indicadores.git
cd automacao_dados_indicadores
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Adicione a chave `chave_bigquery.json` na raiz do projeto

5. Execute o pipeline:

```bash
python run_pipeline.py
```

6. Os arquivos CSV serão salvos na pasta do projeto para uso no Power BI

---

## Dashboard

O dashboard criado no Power BI consome os arquivos `.csv` exportados e apresenta os KPIs com filtros mensais.  
A visualização está disponível na pasta [dashboard](./dashboard) (print, .pbix e PDF).

---

## Agendamento

A execução pode ser automatizada via:

- **Script `.bat`** (executar_pipeline.bat)
- **Agendador de Tarefas do Windows**

---

## 📄 Documentação

Para mais detalhes técnicos, consulte [documentacao_projeto.md](./documentacao_projeto.md).

---


Desenvolvido por Vanessa Costa — Portfólio em Análise de Dados.
