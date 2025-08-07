import streamlit as st
# Configuração da página
st.set_page_config(
    page_title="💰 Dashboard Finanças Pessoais",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from streamlit_extras.badges import badge
from streamlit_extras.metric_cards import style_metric_cards
import warnings
warnings.filterwarnings('ignore')


# CSS customizado para melhorar a aparência
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-container {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .badge-container {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        justify-content: center;
        margin: 1rem 0;
    }
    .progress-container {
        margin: 1rem 0;
        padding: 1rem;
        border-radius: 10px;
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<h1 class="main-header">💰 Dashboard de Finanças Pessoais</h1>', unsafe_allow_html=True)
st.markdown("### 🎓 Semana de Educação Financeira - Ferramenta Interativa de Aprendizado")

# Sidebar para configurações
with st.sidebar:
    st.header("⚙️ Configurações")
    
    # Upload do arquivo
    st.subheader("📁 Upload do Extrato")
    uploaded_file = st.file_uploader(
        "Arraste e solte seu arquivo CSV aqui:",
        type=['csv'],
        help="Formato esperado: data, descricao, categoria, valor, tipo, tags"
    )
    
    # Dados de exemplo
    if st.button("📊 Usar Dados de Exemplo"):
        # Criar dados de exemplo
        dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
        np.random.seed(42)
        
        sample_data = []
        categorias = ['Alimentação', 'Transporte', 'Saúde', 'Entretenimento', 'Educação', 'Moradia']
        
        for date in dates:
            # Adicionar algumas transações por dia
            for _ in range(np.random.randint(1, 4)):
                categoria = np.random.choice(categorias)
                tipo = np.random.choice(['debito', 'credito'], p=[0.7, 0.3])
                
                if tipo == 'debito':
                    valor = -np.random.uniform(20, 500)
                    descricao = f"Gasto em {categoria.lower()}"
                else:
                    valor = np.random.uniform(1000, 3000)
                    descricao = "Salário" if valor > 2000 else "Freelance"
                    categoria = "Renda"
                
                sample_data.append({
                    'data': date.strftime('%Y-%m-%d'),
                    'descricao': descricao,
                    'categoria': categoria,
                    'valor': round(valor, 2),
                    'tipo': tipo,
                    'tags': 'Exemplo'
                })
        
        st.session_state['sample_df'] = pd.DataFrame(sample_data)

# Função para processar os dados
def process_data(df):
    df['data'] = pd.to_datetime(df['data'])
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
    df = df.dropna(subset=['valor'])
    df['mes'] = df['data'].dt.to_period('M')
    return df

# Carregar dados
df = None
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        df = process_data(df)
        st.success("✅ Arquivo carregado com sucesso!")
    except Exception as e:
        st.error(f"❌ Erro ao carregar arquivo: {str(e)}")
elif 'sample_df' in st.session_state:
    df = st.session_state['sample_df'].copy()
    df = process_data(df)

if df is not None:
    # Filtros na sidebar
    with st.sidebar:
        st.subheader("🔍 Filtros")
        
        # Filtro de período
        min_date = df['data'].min().date()
        max_date = df['data'].max().date()
        
        date_range = st.date_input(
            "Período:",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        if len(date_range) == 2:
            start_date, end_date = date_range
            df_filtered = df[(df['data'].dt.date >= start_date) & (df['data'].dt.date <= end_date)]
        else:
            df_filtered = df
        
        # Filtro de categoria
        categorias_disponiveis = df_filtered['categoria'].unique()
        categorias_selecionadas = st.multiselect(
            "Categorias:",
            categorias_disponiveis,
            default=categorias_disponiveis
        )
        
        df_filtered = df_filtered[df_filtered['categoria'].isin(categorias_selecionadas)]

    # KPIs principais
    col1, col2, col3 = st.columns(3)
    
    total_creditos = df_filtered[df_filtered['tipo'] == 'credito']['valor'].sum()
    total_debitos = abs(df_filtered[df_filtered['tipo'] == 'debito']['valor'].sum())
    saldo = total_creditos - total_debitos
    
    with col1:
        st.metric(
            label="💵 Renda Total",
            value=f"R$ {total_creditos:,.2f}",
            delta=f"+{total_creditos:,.2f}"
        )
    
    with col2:
        st.metric(
            label="💸 Despesa Total",
            value=f"R$ {total_debitos:,.2f}",
            delta=f"-{total_debitos:,.2f}"
        )
    
    with col3:
        delta_color = "inverse" if saldo >= 0 else "normal"
        st.metric(
            label="💰 Saldo",
            value=f"R$ {saldo:,.2f}",
            delta=f"{saldo:,.2f}",
            delta_color=delta_color
        )
    
    # Aplicar estilo aos cards de métrica
    style_metric_cards()
    
    # Seção de Metas e Gamificação
    st.header("🎯 Metas e Conquistas")
    
    # Obter categorias de despesas (excluindo 'Renda')
    categorias_despesas = df_filtered[
        (df_filtered['tipo'] == 'debito') & 
        (df_filtered['categoria'] != 'Renda')
    ]['categoria'].unique()
    
    if len(categorias_despesas) > 0:
        # Input de metas por categoria
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📊 Definir Metas Mensais por Categoria")
            
            if 'metas' not in st.session_state:
                st.session_state['metas'] = {}
            
            metas_cols = st.columns(2)
            for i, categoria in enumerate(categorias_despesas):
                with metas_cols[i % 2]:
                    meta_atual = st.session_state['metas'].get(categoria, 1000.0)
                    st.session_state['metas'][categoria] = st.number_input(
                        f"Meta {categoria}",
                        min_value=0.0,
                        value=float(meta_atual),
                        step=50.0,
                        format="%.2f",
                        key=f"meta_{categoria}"
                    )
        
        with col2:
            st.subheader("🏆 Badges Conquistadas")
            
            # Sistema de badges
            badges_conquistadas = []
            
            for categoria in categorias_despesas:
                gasto_categoria = abs(df_filtered[
                    (df_filtered['categoria'] == categoria) & 
                    (df_filtered['tipo'] == 'debito')
                ]['valor'].sum())
                
                meta_categoria = st.session_state['metas'].get(categoria, 1000.0)
                
                if gasto_categoria <= meta_categoria:
                    if gasto_categoria <= meta_categoria * 0.7:
                        badge_type = "🥇 Ouro"
                        badge_color = "gold"
                    elif (gasto_categoria > meta_categoria * 0.70) and (gasto_categoria <= meta_categoria * 0.85):
                        badge_type = "🥈 Prata"
                        badge_color = "silver"
                    elif (gasto_categoria > meta_categoria * 0.85) and (gasto_categoria <= meta_categoria):
                        badge_type = "🥉 Bronze"
                        badge_color = "bronze"
                    
                    badges_conquistadas.append((categoria, badge_type, badge_color))
                    
                else:
                    if (gasto_categoria > meta_categoria) and (gasto_categoria <= meta_categoria * 1.2):
                        badge_type = "📊 Acima da Meta"
                        badge_color = "yellow"
                    elif (gasto_categoria > meta_categoria * 1.2) and (gasto_categoria <= meta_categoria * 1.5):
                        badge_type = "⚠️ Alerta Alto"
                        badge_color = "orange"
                    elif (gasto_categoria > meta_categoria * 1.5):
                        badge_type = "🚨 Alerta Crítico"
                        badge_color = "red"
                    
                    badges_conquistadas.append((categoria, badge_type, badge_color))
            
            # Exibir badges
            if badges_conquistadas:
                for categoria, badge_type, color in badges_conquistadas:
                    st.success(f"{badge_type} - {categoria}")
            else:
                st.info("Continue economizando para ganhar badges! 💪")
        
        # Progress bars por categoria
        st.subheader("📈 Progresso das Metas")
        
        progress_data = []
        for categoria in categorias_despesas:
            gasto_categoria = abs(df_filtered[
                (df_filtered['categoria'] == categoria) & 
                (df_filtered['tipo'] == 'debito')
            ]['valor'].sum())
            
            meta_categoria = st.session_state['metas'].get(categoria, 1000.0)
            percentual_real = (gasto_categoria / meta_categoria) * 100 if meta_categoria > 0 else 0
            percentual_barra = min(percentual_real, 100)  # Barra limitada a 100%
            
            progress_data.append({
                'categoria': categoria,
                'gasto': gasto_categoria,
                'meta': meta_categoria,
                'percentual': percentual_real
            })
            
            # Progress bar visual
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**{categoria}**")
                if percentual_real <= 70:
                    st.progress(percentual_barra/100, text=f"{percentual_real:.1f}% da meta")
                elif percentual_real <= 85:
                    st.progress(percentual_barra/100, text=f"⚠️ {percentual_real:.1f}% da meta")
                elif percentual_real <= 100:
                    st.progress(percentual_barra/100, text=f"🚨 {percentual_real:.1f}% da meta")
                else:
                    # Quando ultrapassar 100%, usar CSS para deixar a barra vermelha
                    st.markdown(f"""
                    <div style="margin-bottom: 10px;">
                        <div style="background-color: #ff4444; height: 20px; border-radius: 10px; width: 100%; position: relative;">
                            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: white; font-weight: bold; font-size: 12px;">
                                🚨 {percentual_real:.1f}% da meta
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                st.metric("Gasto", f"R$ {gasto_categoria:,.2f}")
            
            with col3:
                st.metric("Meta", f"R$ {meta_categoria:,.2f}")
    
    # Gráficos
    st.header("📊 Análises Visuais")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de pizza - Despesas por categoria
        despesas_por_categoria = df_filtered[df_filtered['tipo'] == 'debito'].groupby('categoria')['valor'].sum().abs()
        
        if not despesas_por_categoria.empty:
            fig_pie = px.pie(
                values=despesas_por_categoria.values,
                names=despesas_por_categoria.index,
                title="🍕 Distribuição de Despesas por Categoria",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Gráfico de barras - Top categorias de despesa
        if not despesas_por_categoria.empty:
            fig_bar = px.bar(
                x=despesas_por_categoria.values,
                y=despesas_por_categoria.index,
                orientation='h',
                title="📊 Ranking de Despesas por Categoria",
                labels={'x': 'Valor (R$)', 'y': 'Categoria'},
                color=despesas_por_categoria.values,
                color_continuous_scale='Reds'
            )
            fig_bar.update_layout(showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)
    
    # Gráfico de linha temporal - Saldo acumulado
    st.subheader("📈 Evolução do Saldo ao Longo do Tempo")
    
    df_timeline = df_filtered.sort_values('data').copy()
    df_timeline['saldo_acumulado'] = df_timeline['valor'].cumsum()
    
    fig_timeline = go.Figure()
    
    fig_timeline.add_trace(go.Scatter(
        x=df_timeline['data'],
        y=df_timeline['saldo_acumulado'],
        mode='lines+markers',
        name='Saldo Acumulado',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=6),
        hovertemplate='Data: %{x}<br>Saldo: R$ %{y:,.2f}<extra></extra>'
    ))
    
    # Adicionar linha zero
    fig_timeline.add_hline(y=0, line_dash="dash", line_color="red", 
                          annotation_text="Linha Zero", annotation_position="bottom right")
    
    fig_timeline.update_layout(
        title="Evolução do Saldo Acumulado",
        xaxis_title="Data",
        yaxis_title="Saldo (R$)",
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Análise mensal
    st.subheader("📅 Análise Mensal")
    
    df_mensal = df_filtered.groupby(['mes', 'tipo'])['valor'].sum().unstack(fill_value=0)
    if 'debito' in df_mensal.columns:
        df_mensal['debito'] = df_mensal['debito'].abs()
    
    fig_mensal = go.Figure()
    
    if 'credito' in df_mensal.columns:
        fig_mensal.add_trace(go.Bar(
            name='Receitas',
            x=[str(mes) for mes in df_mensal.index],
            y=df_mensal['credito'],
            marker_color='green',
            opacity=0.8
        ))
    
    if 'debito' in df_mensal.columns:
        fig_mensal.add_trace(go.Bar(
            name='Despesas',
            x=[str(mes) for mes in df_mensal.index],
            y=df_mensal['debito'],
            marker_color='red',
            opacity=0.8
        ))
    
    fig_mensal.update_layout(
        title='Receitas vs Despesas por Mês',
        xaxis_title='Mês',
        yaxis_title='Valor (R$)',
        barmode='group',
        height=400
    )
    
    st.plotly_chart(fig_mensal, use_container_width=True)
    
    # Tabela filtrável
    st.header("📋 Extrato Detalhado")
    
    # Filtros adicionais para a tabela
    col1, col2, col3 = st.columns(3)
    
    with col1:
        tipo_filtro = st.selectbox(
            "Tipo de Transação:",
            ['Todos'] + list(df_filtered['tipo'].unique())
        )
    
    with col2:
        valor_min = st.number_input(
            "Valor Mínimo:",
            value=0.0,
            step=10.0
        )
    
    with col3:
        busca_descricao = st.text_input(
            "Buscar na Descrição:",
            placeholder="Digite para buscar..."
        )
    
    # Aplicar filtros na tabela
    df_tabela = df_filtered.copy()
    
    if tipo_filtro != 'Todos':
        df_tabela = df_tabela[df_tabela['tipo'] == tipo_filtro]
    
    df_tabela = df_tabela[abs(df_tabela['valor']) >= valor_min]
    
    if busca_descricao:
        df_tabela = df_tabela[df_tabela['descricao'].str.contains(busca_descricao, case=False, na=False)]
    
    # Formatar valores para exibição
    df_display = df_tabela.copy()
    df_display['valor'] = df_display['valor'].apply(lambda x: f"R$ {x:,.2f}")
    df_display['data'] = df_display['data'].dt.strftime('%d/%m/%Y')
    
    # Ordenar por data (mais recente primeiro)
    df_display = df_display.sort_values('data', ascending=False)
    
    st.dataframe(
        df_display[['data', 'descricao', 'categoria', 'valor', 'tipo', 'tags']],
        use_container_width=True,
        hide_index=True
    )
    
    # Estatísticas resumidas
    st.header("📊 Estatísticas Resumidas")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_transacoes = len(df_filtered)
        st.metric("Total de Transações", total_transacoes)
    
    with col2:
        ticket_medio = df_filtered[df_filtered['tipo'] == 'debito']['valor'].mean()
        st.metric("Ticket Médio (Despesas)", f"R$ {abs(ticket_medio):,.2f}")
    
    with col3:
        maior_despesa = df_filtered[df_filtered['tipo'] == 'debito']['valor'].min()
        st.metric("Maior Despesa", f"R$ {abs(maior_despesa):,.2f}")
    
    with col4:
        dias_analisados = (df_filtered['data'].max() - df_filtered['data'].min()).days + 1
        st.metric("Período Analisado", f"{dias_analisados} dias")

else:
    # Instruções quando não há dados
    st.info("👆 Faça upload do seu arquivo CSV ou use os dados de exemplo para começar!")
    
    with st.expander("📋 Formato esperado do arquivo CSV"):
        st.write("""
        **Colunas obrigatórias:**
        - `data`: Data da transação (formato YYYY-MM-DD ou DD/MM/YYYY)
        - `descricao`: Descrição da transação
        - `categoria`: Categoria da transação (ex: Alimentação, Transporte, etc.)
        - `valor`: Valor da transação (positivo para creditos, negativo para debitos)
        - `tipo`: Tipo da transação ('credito' ou 'debito')
        - `tags`: Observações adicionais (opcional)
        
        **Exemplo:**
        ```
        data,descricao,categoria,valor,tipo,tags
        2024-01-15,Supermercado ABC,Alimentação,-150.50,debito,
        2024-01-20,Salário,Renda,3000.00,credito,
        ```
        """)
    
    st.markdown("---")
    st.markdown("""
    ### 🎓 Sobre este Dashboard
    
    Este dashboard foi desenvolvido como ferramenta educacional para a **Semana de Educação Financeira**. 
    
    **Recursos disponíveis:**
    - 📊 Visualizações interativas de receitas e despesas
    - 🎯 Sistema de metas por categoria
    - 🏆 Gamificação com badges de conquista
    - 📈 Análise temporal do saldo
    - 🔍 Filtros avançados para análise detalhada
    
    **Objetivo pedagógico:** Demonstrar como a tecnologia pode tornar o controle financeiro mais envolvente e educativo!
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>💡 <strong>Dashboard de Finanças Pessoais</strong> | Desenvolvido para Educação Financeira</p>
    <p>🎓 Ferramenta interativa para aprendizado de conceitos financeiros</p>
    <p> Prof. josé Américo</p>
</div>
""", unsafe_allow_html=True)