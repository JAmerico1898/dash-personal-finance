# 💰 Dashboard de Finanças Pessoais

Uma ferramenta interativa e gamificada para controle financeiro desenvolvida em Streamlit, criada especialmente para a **Semana de Educação Financeira**.

## 🎯 Objetivo

Este dashboard foi desenvolvido como recurso pedagógico para tornar o aprendizado de educação financeira mais envolvente e interativo, demonstrando como a tecnologia pode ser utilizada para facilitar o controle de finanças pessoais.

## ✨ Funcionalidades

### 📊 **Dashboard Completo**
- **KPI Cards**: Visualização de Renda Total, Despesas e Saldo
- **Gráfico de Pizza**: Distribuição de despesas por categoria
- **Ranking de Despesas**: Gráfico de barras das principais categorias
- **Linha Temporal**: Evolução do saldo acumulado ao longo do tempo
- **Análise Mensal**: Comparativo de receitas vs despesas por mês

### 🎮 **Sistema Gamificado**
- **Definição de Metas**: Configure metas mensais por categoria de gasto
- **Sistema de Badges**: Conquiste medalhas baseadas no seu desempenho
  - 🥇 **Ouro**: Gasto ≤ 70% da meta
  - 🥈 **Prata**: Gasto ≤ 85% da meta
  - 🥉 **Bronze**: Gasto ≤ 100% da meta
- **Badges Negativas**: Alertas quando metas são ultrapassadas
  - 📊 **Acima da Meta**: Excesso até 20%
  - ⚠️ **Alerta Alto**: Excesso de 20% a 50%
  - 🚨 **Alerta Crítico**: Excesso acima de 50%
- **Progress Bars**: Acompanhamento visual do progresso das metas

### 🔍 **Análise Avançada**
- **Filtros Interativos**: Por período, categoria e tipo de transação
- **Tabela Filtrável**: Extrato detalhado com busca por descrição
- **Estatísticas Resumidas**: Métricas importantes como ticket médio e maior despesa

## 🚀 Instalação e Execução

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone o repositório**
```bash
git clone [url-do-repositorio]
cd dashboard-financas-pessoais
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Execute a aplicação**
```bash
streamlit run dash.py
```

4. **Acesse no navegador**
A aplicação estará disponível em: `http://localhost:8501`

## 📁 Formato do Arquivo CSV

O dashboard aceita arquivos CSV com as seguintes colunas obrigatórias:

| Coluna | Tipo | Descrição | Exemplo |
|--------|------|-----------|---------|
| `data` | Data | Data da transação (YYYY-MM-DD ou DD/MM/YYYY) | 2024-01-15 |
| `descricao` | Texto | Descrição da transação | Supermercado ABC |
| `categoria` | Texto | Categoria da despesa | Alimentação |
| `valor` | Número | Valor da transação (positivo para créditos, negativo para débitos) | -150.50 |
| `tipo` | Texto | Tipo da transação ('credito' ou 'debito') | debito |
| `tags` | Texto | Observações adicionais (opcional) | Compra mensal |

### Exemplo de CSV:
```csv
data,descricao,categoria,valor,tipo,tags
2024-01-15,Supermercado ABC,Alimentação,-150.50,debito,
2024-01-20,Salário,Renda,3000.00,credito,
2024-01-22,Uber,Transporte,-25.00,debito,
```

## 🎓 Uso Educacional

### Para Professores
- Use o botão "📊 Usar Dados de Exemplo" para demonstrações rápidas
- Explore diferentes cenários ajustando as metas
- Mostre como a gamificação motiva o controle financeiro
- Demonstre a importância de categorizar despesas

### Para Alunos
- Faça upload do seu próprio extrato bancário
- Defina metas realistas para cada categoria
- Acompanhe seu progresso através das badges
- Use os filtros para análises detalhadas

## 🛠️ Tecnologias Utilizadas

- **Streamlit**: Framework para criação de aplicações web
- **Pandas**: Manipulação e análise de dados
- **Plotly**: Gráficos interativos
- **NumPy**: Computação numérica
- **Streamlit-Extras**: Componentes adicionais (badges e metric cards)

## 📊 Capturas de Tela

### Dashboard Principal
- KPI cards com métricas principais
- Gráficos interativos de despesas

### Sistema de Gamificação
- Badges conquistadas por categoria
- Progress bars das metas
- Alertas visuais para gastos excessivos

### Análise Temporal
- Evolução do saldo ao longo do tempo
- Comparativo mensal de receitas e despesas

## 🤝 Contribuição

Este projeto foi desenvolvido para fins educacionais. Contribuições são bem-vindas:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📝 Licença

Este projeto foi desenvolvido para fins educacionais e está disponível sob licença MIT.

## 👨‍🏫 Sobre

Desenvolvido como ferramenta pedagógica para a **Semana de Educação Financeira**, demonstrando como a tecnologia pode tornar o aprendizado de finanças mais interativo e envolvente.

---

💡 **Dashboard de Finanças Pessoais** | 🎓 Ferramenta interativa para aprendizado de conceitos financeiros
