import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import time
from datetime import datetime

# ==============================================================================
# CONFIGURAÇÃO DA PÁGINA STREAMLIT
# ==============================================================================
st.set_page_config(
    page_title="Plataforma Integrada Transtusa - Telemetria & IA Preditiva",
    page_icon="🚍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# ESTILIZAÇÃO VISUAL CUSTOMIZADA (CSS TRANSTUSA BLUE)
# ==============================================================================
st.markdown("""
<style>
    /* Estilo do cabeçalho e elementos principais */
    .main-header {
        background: linear-gradient(135deg, #002B49 0%, #005691 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    }
    .main-header h1 {
        color: #FFFFFF !important;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        margin: 0;
    }
    .main-header p {
        color: #E0F2FE;
        font-size: 1.1rem;
        margin-top: 5px;
    }
    
    /* Cards de Métricas */
    .metric-card {
        background-color: #FFFFFF;
        border-left: 5px solid #005691;
        padding: 18px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        text-align: center;
    }
    .metric-title {
        font-size: 0.9rem;
        color: #64748B;
        font-weight: 600;
        text-transform: uppercase;
    }
    .metric-value {
        font-size: 1.8rem;
        color: #0F172A;
        font-weight: 700;
        margin: 8px 0;
    }
    .metric-sub {
        font-size: 0.85rem;
        color: #16A34A;
        font-weight: 600;
    }
    
    /* Estilo de Sensores e Posição no Ônibus */
    .sensor-box {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .sensor-header {
        font-weight: bold;
        color: #002B49;
        font-size: 1.1rem;
    }

    /* Cards de Fornecedores e Compras */
    .procurement-card {
        background-color: #F0FDF4;
        border: 2px solid #16A34A;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(22, 163, 74, 0.12);
    }
    .vendor-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    .vendor-card:hover {
        transform: translateY(-2px);
        border-color: #005691;
    }
    .badge-local { background-color: #FEE2E2; color: #991B1B; padding: 4px 8px; border-radius: 6px; font-weight: bold; font-size: 0.8rem; }
    .badge-pr { background-color: #DBEAFE; color: #1D4ED8; padding: 4px 8px; border-radius: 6px; font-weight: bold; font-size: 0.8rem; }
    .badge-br { background-color: #DCFCE7; color: #15803D; padding: 4px 8px; border-radius: 6px; font-weight: bold; font-size: 0.8rem; }

    /* Botões WhatsApp e Email */
    .btn-wsp {
        background-color: #25D366;
        color: white !important;
        padding: 8px 16px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin-right: 8px;
    }
    .btn-email {
        background-color: #005691;
        color: white !important;
        padding: 8px 16px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# CABEÇALHO DA PLATAFORMA (DESIGN CORPORATIVO TRANSTUSA)
# ==============================================================================
st.markdown("""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1>🚍 TRANSTUSA - PLATAFORMA INTEGRADA DE MANUTENÇÃO PREDITIVA</h1>
            <p>Telemetria CAN Bus, Otimização de Compras (Menor Custo x Prazo Preditivo), Gestão de Frota (301 Ônibus) e Financiamento BNDES</p>
        </div>
        <div style="text-align: right; background: rgba(255,255,255,0.1); padding: 10px 18px; border-radius: 8px;">
            <strong style="color: #67E8F9;">SISTEMA OPERACIONAL: ATIVO</strong><br>
            <span style="font-size: 0.85rem; color: #E0F2FE;">Joinville & Rio Negrinho / SC</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# NAVEGAÇÃO POR ABAS (TABS)
# ==============================================================================
tab_dash, tab_procurement, tab_sensores, tab_vendors, tab_finan, tab_driver, tab_api, tab_mapa = st.tabs([
    "📊 Dashboard & Preditivo",
    "🛒 Setor de Compras & Menor Custo",
    "🧰 Sensores & Alocação 3D",
    "🏬 Marketplace Fornecedores",
    "🏦 Simulador Financiamento BNDES",
    "📱 Painel do Motorista",
    "🌐 API & Telemetria JSON",
    "🗺️ Mapa das Linhas Joinville"
])

# ==============================================================================
# ABA 1: DASHBOARD EXECUTIVO & PREDITIVO
# ==============================================================================
with tab_dash:
    st.subheader("📈 Visão Geral de Impacto Operacional e Redução de Custos")
    
    # Linha de Métricas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Frota Total Monitorada</div>
            <div class="metric-value">301 Ônibus</div>
            <div class="metric-sub">Urbano, Fretamento e Intermunicipal</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card" style="border-left-color: #22C55E;">
            <div class="metric-title">Fila diária na Oficina</div>
            <div class="metric-value">110 ➔ 44/dia</div>
            <div class="metric-sub">📉 -60% de Ocupação Diária</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card" style="border-left-color: #EAB308;">
            <div class="metric-title">Economia Líquida Anual</div>
            <div class="metric-value">R$ 15,95 M</div>
            <div class="metric-sub">Peças, Oficina e Inatividade</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="metric-card" style="border-left-color: #06B6D4;">
            <div class="metric-title">Tempo de Payback CAPEX</div>
            <div class="metric-value">23 Dias</div>
            <div class="metric-sub">Retorno do Investimento de R$ 1,02M</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.markdown("#### 🚌 Ocupação Diária da Oficina (Ônibus Parados)")
        fig, ax = plt.subplots(figsize=(6, 3.8))
        categorias = ['Tradicional (Sem IA)', 'Preditiva (Com IA)']
        valores = [110, 44]
        cores = ['#EF4444', '#10B981']
        bars = ax.bar(categorias, valores, color=cores, width=0.45)
        ax.set_ylabel("Ônibus na Oficina/Dia")
        ax.set_ylim(0, 130)
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2.0, yval + 3, f"{yval:.0f} ônibus/dia", ha='center', fontweight='bold')
        st.pyplot(fig)
        
    with col_g2:
        st.markdown("#### 💰 Custo Operacional Anual de Manutenção (R$ Milhões)")
        fig2, ax2 = plt.subplots(figsize=(6, 3.8))
        v_custos = [30.11, 14.51]
        bars2 = ax2.bar(categorias, v_custos, color=['#B91C1C', '#047857'], width=0.45)
        ax2.set_ylabel("R$ Milhões / Ano")
        ax2.set_ylim(0, 35)
        for bar in bars2:
            yval = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 1, f"R$ {yval:.2f}M", ha='center', fontweight='bold')
        st.pyplot(fig2)

    st.info("ℹ️ **Indicadores Operacionais de Joinville**: A Transtusa percorre 40 mil km/dia, transporta 70 mil passageiros/dia e higieniza 150 veículos diariamente com 120 mil litros de água reciclada.")

# ==============================================================================
# ABA 2: SETOR DE COMPRAS & INTELIGÊNCIA DE MENOR CUSTO X PRAZO PREDITIVO
# ==============================================================================
with tab_procurement:
    st.subheader("🛒 Módulo do Setor de Compras - Otimização de Custos x Prazo Preditivo")
    st.write("Diferente dos sistemas tradicionais que compram no varejo local mais caro por desespero de emergência, a **IA Preditiva antecipa a manutenção em 3 a 10 dias**. Isso permite ao setor de compras adquirir componentes no **Atacado Nacional e Hubs Regionais pelo menor valor de aquisição do Brasil**.")

    col_p1, col_p2 = st.columns([1, 1.2])

    with col_p1:
        st.markdown("#### ⚙️ Parâmetros do Alerta Telemétrico & Janela de Manutenção")
        
        peca_selecionada = st.selectbox("Componente com Alerta Preditivo", [
            "Jogo Lonas de Freio (MBB O-500) - 301 Ônibus",
            "Tambor de Freio Traseiro Urbano",
            "Kit de Embreagem Completo (Sachs)",
            "Filtro Diesel S10 (Caixa c/ 10 un.)",
            "Lanterna LED Traseira Completa"
        ])
        
        qtd_pecas = st.number_input("Quantidade para Aquisição (Kits/Peças)", min_value=1, max_value=500, value=20, step=5)
        
        prazo_antecedencia = st.slider(
            "⏳ Antecedência Detectada pelos Sensores (Dias até a Manutenção)",
            min_value=1, max_value=10, value=5,
            help="Sensores telemétricos identificam o desgaste com dias de antecedência. Quanto maior o prazo, menor o custo de aquisição!"
        )

        st.markdown("---")
        st.markdown("#### 💡 Regra do Algoritmo de Compras Inteligente")
        if prazo_antecedencia >= 3:
            st.success(f"✅ **JANELA PREDITIVA IDEAL ({prazo_antecedencia} DIAS)**: O sistema alocou a compra no **Atacado Nacional / Hub Regional (Menor Valor de Aquisição)**. O frete chega a tempo para a manutenção agendada e a Transtusa economiza até 40,5%!")
        else:
            st.warning(f"⚠️ **JANELA CURTA ({prazo_antecedencia} DIAS)**: Prazo apertado. O sistema recomenda o Hub Regional ou Varejo Local Express para evitar que o ônibus fique inativo.")

    with col_p2:
        st.markdown("#### 🎯 Matriz Comparativa de Opções para o Setor de Compras")

        # Dados de Preços por Peça
        tabela_precos_base = {
            "Jogo Lonas de Freio (MBB O-500) - 301 Ônibus": {"local": 680.0, "hub_pr": 520.0, "atacado_br": 420.0, "desc": 38.2, "forn_br": "Anchieta / Cometa Distribuidora (SP)", "forn_pr": "Rodoparaná Autopeças (Curitiba/PR)", "forn_sc": "Zezinho / Forparts (Joinville)"},
            "Tambor de Freio Traseiro Urbano": {"local": 1305.0, "hub_pr": 1050.0, "atacado_br": 820.0, "desc": 37.2, "forn_br": "Marcopolo Parts Central (RS)", "forn_pr": "Pardiesel Peças (SC/PR)", "forn_sc": "FASA / Truck Parts (Joinville)"},
            "Kit de Embreagem Completo (Sachs)": {"local": 4200.0, "hub_pr": 3400.0, "atacado_br": 2850.0, "desc": 32.1, "forn_br": "Anchieta / Cometa Distribuidora (SP)", "forn_pr": "Ingá Peças e Transmissões (PR)", "forn_sc": "Zezinho Autopeças (Joinville)"},
            "Filtro Diesel S10 (Caixa c/ 10 un.)": {"local": 1850.0, "hub_pr": 1400.0, "atacado_br": 1100.0, "desc": 40.5, "forn_br": "Anchieta Distribuidora (SP)", "forn_pr": "Rodoparaná Autopeças (PR)", "forn_sc": "Forparts / Rede Âncora (Joinville)"},
            "Lanterna LED Traseira Completa": {"local": 450.0, "hub_pr": 350.0, "atacado_br": 270.0, "desc": 40.0, "forn_br": "Marcopolo Parts Central (RS)", "forn_pr": "Pardiesel Peças (SC)", "forn_sc": "Truck Parts (Joinville)"}
        }

        info_p = tabela_precos_base[peca_selecionada]
        p_local = info_p["local"] * qtd_pecas
        p_pr = info_p["hub_pr"] * qtd_pecas
        p_br = info_p["atacado_br"] * qtd_pecas
        economia_br = p_local - p_br

        # Recomendação Baseada no Custo e Prazo
        if prazo_antecedencia >= 3:
            recomendacao_txt = f"""
            <div class="procurement-card">
                <h3 style="color: #15803D; margin-top: 0;">🏆 RECOMENDAÇÃO OFICIAL: MENOR VALOR DE AQUISIÇÃO</h3>
                <p style="font-size: 1.1rem; color: #002B49;"><b>Fornecedor Indicado:</b> {info_p['forn_br']}</p>
                <p><b>Preço Total do Lote ({qtd_pecas} un.):</b> <span style="font-size: 1.4rem; color: #16A34A; font-weight: bold;">R$ {p_br:,.2f}</span> (vs R$ {p_local:,.2f} no varejo local)</p>
                <p><b>Prazo de Entrega:</b> 48 a 72 Horas (Chega {prazo_antecedencia - 2} dias antes da manutenção agendada)</p>
                <p><b>Economia Direta neste Lote:</b> <span style="color: #15803D; font-weight: bold; font-size: 1.2rem;">R$ {economia_br:,.2f} ({info_p['desc']}% OFF)</span></p>
                <hr>
                <a href="mailto:vendas@anchietapecas.com.br?subject=Ordem%20de%20Compra%20Preditiva%20Transtusa&body=Solicitamos%20a%20compra%20de%20{qtd_pecas}%20unidades%20de%20{peca_selecionada}%20pelo%20valor%20unitario%20de%20R$%20{info_p['atacado_br']:.2f}" class="btn-email">✉️ Emitir Ordem de Compra de Menor Custo</a>
            </div>
            """
        else:
            recomendacao_txt = f"""
            <div class="procurement-card" style="border-color: #EAB308; background-color: #FEFCE8;">
                <h3 style="color: #854D0E; margin-top: 0;">⚡ RECOMENDAÇÃO EMERGENCIAL (ENTREGA EXPRESSA)</h3>
                <p style="font-size: 1.1rem; color: #002B49;"><b>Fornecedor Indicado:</b> {info_p['forn_sc']}</p>
                <p><b>Preço Total do Lote ({qtd_pecas} un.):</b> R$ {p_local:,.2f}</p>
                <p><b>Prazo de Entrega:</b> 2 a 4 Horas (Atendimento imediato na garagem)</p>
                <p style="color: #A16207;">⚠️ <i>Nota: Para economizar R$ {economia_br:,.2f}, aumente a janela de antecedência preditiva nas rotinas de vistoria dos sensores.</i></p>
                <hr>
                <a href="https://wa.me/554734661000?text=Solicitacao%20emergencial%20Transtusa%20para%20{qtd_pecas}%20unidades%20de%20{peca_selecionada}" class="btn-wsp">📱 Enviar Pedido Urgente via WhatsApp</a>
            </div>
            """

        st.markdown(recomendacao_txt, unsafe_allow_html=True)

        st.markdown("#### 📋 Comparativo Completo de Canais de Suprimento")
        df_canais = pd.DataFrame({
            "Canal de Fornecimento": ["Atacado Nacional (SP/RS) - MENOR VALOR", "Hub Regional (Paraná) - CUSTO MÉDIO", "Varejo Local (Joinville) - EMERGÊNCIA"],
            "Preço Unitário": [f"R$ {info_p['atacado_br']:,.2f}", f"R$ {info_p['hub_pr']:,.2f}", f"R$ {info_p['local']:,.2f}"],
            "Total Lote": [f"R$ {p_br:,.2f}", f"R$ {p_pr:,.2f}", f"R$ {p_local:,.2f}"],
            "Prazo Entrega": ["48 - 72 Horas", "12 - 24 Horas", "2 - 4 Horas"],
            "Desconto em Relação ao Varejo": [f"{info_p['desc']}% OFF (Melhor Opção)", f"~20% OFF", "0% (Preço Cheio)"]
        })
        st.dataframe(df_canais, use_container_width=True)

# ==============================================================================
# ABA 3: SENSORES & ALOCAÇÃO NO ÔNIBUS
# ==============================================================================
with tab_sensores:
    st.subheader("🧰 Onde e Como Alocar Cada Sensor no Ônibus")
    st.write("Esquema técnico de distribuição do Kit de Telemetria V5 por veículo da frota de 301 ônibus:")
    
    col_s1, col_s2 = st.columns([1.2, 1])
    
    with col_s1:
        st.markdown("""
        <div class="sensor-box">
            <div class="sensor-header">1. 🖥️ Módulo Central IoT Gateway 4G/GPS (Painel / Cabine)</div>
            <p><b>Local de Alocação:</b> Atrás do painel principal de instrumentos, conectado à porta de diagnóstico OBD-II / J1939.</p>
            <p><b>Métricas Lidas:</b> Rotação do motor (RPM), velocidade telemétrica, códigos de erro da ECU e localização GPS via 4G.</p>
            <span class="badge-pr">Custo Unitário: R$ 1.200,00 | Instalação: 60 min</span>
        </div>
        
        <div class="sensor-box">
            <div class="sensor-header">2. 🛑 Sensores Eletrônicos de Freio & Ar (Eixos Dianteiro e Traseiro)</div>
            <p><b>Local de Alocação:</b> Acoplado na sapata das lonas de freio das rodas traseiras e transdutor pneumático no reservatório das cuícas de ar.</p>
            <p><b>Métricas Lidas:</b> Espessura residual da lona em milímetros (alerta < 3.0 mm) e pressão de estanqueidade do ar (PSI).</p>
            <span class="badge-pr">Custo Unitário: R$ 500,00 | Instalação: 30 min</span>
        </div>

        <div class="sensor-box">
            <div class="sensor-header">3. ⚙️ Transdutores Térmicos e Ópticos (Motor & Câmbio)</div>
            <p><b>Local de Alocação:</b> Rosqueado na carcaça da caixa de transmissão e no bujão do cárter de óleo lubrificante.</p>
            <p><b>Métricas Lidas:</b> Temperatura do fluido de câmbio (alerta para tráfego pesado no Distrito Perini > 100°C) e índice óptico de contaminação do óleo por água.</p>
            <span class="badge-pr">Custo Unitário: R$ 450,00 | Instalação: 35 min</span>
        </div>

        <div class="sensor-box">
            <div class="sensor-header">4. 🛞 Acelerômetro Triaxial & Kit TPMS (Suspensão e Pneus)</div>
            <p><b>Local de Alocação:</b> Acelerômetro fixado no feixe de molas da suspensão e vistorias TPMS sem fio nas válvulas das 6 rodas.</p>
            <p><b>Métricas Lidas:</b> Nível de vibração estrutural G-Force (linhas rurais de Pirabeiraba/Quiriri) e calibragem/temperatura em tempo real dos pneus.</p>
            <span class="badge-pr">Custo Unitário: R$ 850,00 | Instalação: 25 min</span>
        </div>
        """, unsafe_allow_html=True)

    with col_s2:
        st.markdown("#### 📋 Resumo financeiro do CAPEX do Kit")
        df_kit = pd.DataFrame({
            "Equipamento": ["Gateway IoT 4G/GPS", "Transdutores de Pressão/Temp.", "Sensores de Lona de Freio & Ar", "Acelerômetro MPU + TPMS"],
            "Custo Unitário": [1200.0, 450.0, 500.0, 850.0],
            "Tempo (min)": [60, 35, 30, 25]
        })
        st.dataframe(df_kit, use_container_width=True)
        
        st.success("""
        **Total do Kit por Ônibus**: R$ 3.000,00  
        **Tempo de Instalação por Veículo**: 2,5 Horas (150 minutos)  
        **CAPEX Hardware 301 Ônibus**: R$ 903.000,00  
        **Mão de Obra e Setup**: R$ 120.400,00  
        **CAPEX TOTAL**: **R$ 1.023.400,00**
        """)
        
        st.info("⏱️ **Cronograma de Instalação**: Com 2 duplas de técnicos equipando 8 ônibus/dia durante a rotina de lavação diária, a frota inteira fica equipada em **38 dias úteis (~1,5 mês)**.")

# ==============================================================================
# ABA 4: MARKETPLACE DE FORNECEDORES
# ==============================================================================
with tab_vendors:
    st.subheader("🏬 Marketplace B2B de Fornecedores de Peças em SC, PR e Brasil")
    st.write("A inteligência preditiva consulta o estoque desses parceiros homologados e emite ordens de compra automáticas com o menor preço de atacado:")
    
    # Fornecedores Mapeados
    vendors = [
        {
            "nome": "Anchieta / Cometa Distribuidora",
            "cidade": "São Paulo & ABC / SP",
            "badge": "badge-br",
            "badge_txt": "Nacional Hub SP (MENOR VALOR)",
            "esp": "Maior Atacado Nacional para Chassis Mercedes-Benz O-500",
            "prazo": "48 a 72 Horas",
            "desc": "25% a 40% (Mega Atacado)",
            "wsp": "551120415889",
            "email": "vendas@anchietapecas.com.br"
        },
        {
            "nome": "Marcopolo Parts Central",
            "cidade": "Caxias do Sul / RS",
            "badge": "badge-br",
            "badge_txt": "Nacional Hub RS (MENOR VALOR)",
            "esp": "Carrocerias, Iluminação LED, Multiplex e Peças de Fábrica",
            "prazo": "24 a 48 Horas",
            "desc": "22% a 38% (Fábrica)",
            "wsp": "555421014000",
            "email": "pecas@marcopolo.com.br"
        },
        {
            "nome": "Rodoparaná / Dutra Autopeças",
            "cidade": "Curitiba & São José dos Pinhais / PR",
            "badge": "badge-pr",
            "badge_txt": "Hub Regional PR",
            "esp": "Sistemas de Freio e Eixos Pesados (Fras-le, Sachs, Eaton)",
            "prazo": "12 a 24 Horas",
            "desc": "18% a 25% (Atacado PR)",
            "wsp": "554133818000",
            "email": "atendimento@rodoparana.com.br"
        },
        {
            "nome": "Pardiesel Peças para Ônibus",
            "cidade": "Criciúma & Joinville / SC",
            "badge": "badge-pr",
            "badge_txt": "Estadual SC",
            "esp": "Componentes Exclusivos de Ônibus Scania, Mercedes-Benz, Volvo",
            "prazo": "24 Horas (Next Day)",
            "desc": "12% a 18% (Atacado SC)",
            "wsp": "554834310000",
            "email": "vendas@pardiesel.com.br"
        },
        {
            "nome": "Zezinho Distribuidora de Autopeças",
            "cidade": "Joinville / SC (Jarivatuba)",
            "badge": "badge-local",
            "badge_txt": "Local Joinville (Express)",
            "esp": "Motores, Câmbio, Freios e Embreagens Pesadas",
            "prazo": "2 a 4 Horas (Express)",
            "desc": "5% (Varejo Local)",
            "wsp": "554734661000",
            "email": "vendas@zezinhoautopecas.com.br"
        },
        {
            "nome": "Forparts Autopeças (Rede Âncora)",
            "cidade": "Joinville / SC (Bom Retiro)",
            "badge": "badge-local",
            "badge_txt": "Local Joinville (Express)",
            "esp": "Sistemas de Freio, Suspensão, Bosch, Cobreq, Cofap",
            "prazo": "2 a 4 Horas",
            "desc": "8% (Local)",
            "wsp": "554734357999",
            "email": "contato@forparts.com.br"
        }
    ]
    
    col_v1, col_v2 = st.columns(2)
    for i, v in enumerate(vendors):
        col_target = col_v1 if i % 2 == 0 else col_v2
        with col_target:
            st.markdown(f"""
            <div class="vendor-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong style="font-size: 1.1rem; color: #002B49;">{v['nome']}</strong>
                    <span class="{v['badge']}">{v['badge_txt']}</span>
                </div>
                <p style="color: #64748B; margin: 4px 0;">📍 {v['cidade']}</p>
                <p style="font-size: 0.9rem;"><b>Especialidade:</b> {v['esp']}</p>
                <p style="font-size: 0.85rem; color: #005691;">⏱️ <b>Prazo:</b> {v['prazo']} | 🏷️ <b>Desconto Escala:</b> Até {v['desc']}</p>
                <div style="margin-top: 10px;">
                    <a href="https://wa.me/{v['wsp']}?text=Ol%C3%A1%2C%20sou%20da%20Transtusa%20e%20gostaria%20de%20cotar%20pe%C3%A7as" target="_blank" class="btn-wsp">📱 WhatsApp</a>
                    <a href="mailto:{v['email']}?subject=Cotacao%20Transtusa%20Manutencao" class="btn-email">✉️ Enviar E-mail</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# ABA 5: SIMULADOR INTERATIVO DE FINANCIAMENTO BNDES
# ==============================================================================
with tab_finan:
    st.subheader("🏦 Simulador Visual de Financiamento do CAPEX e Linhas de Crédito")
    st.write("Simule diferentes valores de investimento, carência e prazos para apresentar opções de financiamento à Diretoria da Transtusa:")
    
    col_f1, col_f2 = st.columns([1, 1.2])
    
    with col_f1:
        st.markdown("#### ⚙️ Parâmetros da Simulação")
        
        val_invest = st.slider("Valor do Investimento / Empréstimo (R$)", min_value=500000, max_value=5000000, value=1023400, step=100000)
        
        linha_credito = st.selectbox("Linha de Financiamento", [
            "BNDES FINAME (TLP + 2.5% a.a.)",
            "FINEP Inovação Tecnológica (Subvenção 6% a.a.)",
            "Leasing HaaS Hardware (100% OPEX Faturado)",
            "Crédito ESG / Sustainability-Linked (Banco do Brasil)"
        ])
        
        carencia_meses = st.slider("Prazo de Carência (Meses)", min_value=0, max_value=24, value=12)
        prazo_meses = st.slider("Prazo de Amortização (Meses)", min_value=12, max_value=60, value=36)
        
        # Cálculo Simulado
        taxa_anual = 0.085 if "BNDES" in linha_credito else (0.06 if "FINEP" in linha_credito else 0.11)
        taxa_mensal = taxa_anual / 12.0
        
        parcela_estimada = (val_invest * (1 + taxa_mensal)**prazo_meses * taxa_mensal) / ((1 + taxa_mensal)**prazo_meses - 1)
        economia_mensal_gerada = 1329000.0  # Economia mensal média gerada pela redução de oficina
        
    with col_f2:
        st.markdown("#### 📊 Resultado Financeiro do Projeto Financiado")
        
        st.markdown(f"""
        <div style="background-color: #F0FDF4; border: 2px solid #22C55E; padding: 20px; border-radius: 10px;">
            <h3 style="color: #15803D; margin-0;">💡 Economia Mensal Criada pela IA: R$ {economia_mensal_gerada:,.2f} / mês</h3>
            <hr>
            <p><b>Parcela do Financiamento Calculada:</b> R$ {parcela_estimada:,.2f} / mês</p>
            <p><b>Linha Escolhida:</b> {linha_credito}</p>
            <p><b>Prazo de Carência:</b> {carencia_meses} meses (Economia acumulada na carência: <b>R$ {carencia_meses * economia_mensal_gerada:,.2f}</b>)</p>
            <h4 style="color: #005691;">Fluxo de Caixa Líquido Mensal no Período: + R$ {(economia_mensal_gerada - parcela_estimada):,.2f} / mês</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.success("✅ **Conclusão para a Diretoria**: Como a economia operacional mensal gerada (R$ 1,32M) é **mais de 30 vezes maior** que a parcela do financiamento, o projeto auto-financia seu CAPEX desde o 1º mês!")

# ==============================================================================
# ABA 6: PAINEL EMBARCADO DO MOTORISTA
# ==============================================================================
with tab_driver:
    st.subheader("📱 Computador de Bordo Embarcado (Visão do Motorista)")
    st.write("Interface que roda no tablet embarcado no painel do ônibus:")
    
    col_d1, col_d2 = st.columns([1, 1])
    
    with col_d1:
        st.markdown("#### 🚌 Parâmetros do Veículo em Rota")
        veiculo_sel = st.selectbox("Selecione o Ônibus", ["BUS-2309 (Linha 0426 - Perini)", "BUS-1721 (Linha 0300 - Itaum)", "BUS-4019 (Linha 4019 - Pirabeiraba)"])
        
        vel = st.slider("Velocidade (km/h)", 0, 90, 45)
        rpm = st.slider("RPM do Motor", 800, 2500, 1650)
        temp_mot = st.slider("Temperatura do Motor (°C)", 70.0, 115.0, 88.0)
        freio_mm = st.slider("Espessura Lona de Freio (mm)", 1.0, 12.0, 2.5)
        
    with col_d2:
        st.markdown("#### 📟 Display do Painel em Tempo Real")
        
        # Lógica de Alerta
        if freio_mm < 3.0:
            alerta_box = """
            <div style="background-color: #FEF2F2; border-left: 6px solid #EF4444; padding: 15px; border-radius: 8px;">
                <h4 style="color: #991B1B; margin:0;">🛑 ALERTA CRÍTICO: FREIO COM DESGASTE ELEVADO</h4>
                <p style="color: #7F1D1D;">Lona de freio em <b>{freio_mm:.1f} mm</b> (Limite de segurança: 3.0 mm).<br>
                <b>Ação Automática:</b> Peça comprada no Atacado de Menor Valor e reservada na garagem para o término do turno.</p>
            </div>
            """.format(freio_mm=freio_mm)
        elif temp_mot > 100.0:
            alerta_box = """
            <div style="background-color: #FFFBEB; border-left: 6px solid #F59E0B; padding: 15px; border-radius: 8px;">
                <h4 style="color: #92400E; margin:0;">⚠️ ATENÇÃO: ELEVAÇÃO DE TEMPERATURA</h4>
                <p style="color: #78350F;">Temperatura do motor em <b>{temp_mot:.1f} °C</b>.<br> Reduza a marcha e evite acelerações bruscas no trecho atual.</p>
            </div>
            """.format(temp_mot=temp_mot)
        else:
            alerta_box = """
            <div style="background-color: #F0FDF4; border-left: 6px solid #22C55E; padding: 15px; border-radius: 8px;">
                <h4 style="color: #166534; margin:0;">🟢 SISTEMAS OPERANDO COM SEGURANÇA</h4>
                <p style="color: #14532D;">Todos os parâmetros telemétricos estão dentro dos limites ideais de operação.</p>
            </div>
            """
            
        st.markdown(alerta_box, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background-color: #0F172A; color: #38BDF8; padding: 20px; border-radius: 10px; font-family: monospace; margin-top: 15px;">
            <p>VEÍCULO: {veiculo_sel}</p>
            <p>VELOCIDADE: {vel} km/h | RPM: {rpm} RPM</p>
            <p>TEMP. MOTOR: {temp_mot:.1f} °C | LONA FREIO: {freio_mm:.1f} mm</p>
            <p>PRESSÃO PNEUMÁTICA AR: 110 PSI | SINAL 4G: 📶 100%</p>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# ABA 7: API & TELEMETRIA JSON
# ==============================================================================
with tab_api:
    st.subheader("🌐 API RESTful & Ingestão de Telemetria JSON")
    st.write("Serviço em FastAPI que processa as requisições enviadas pelos Gateways IoT 4G dos ônibus:")
    
    col_a1, col_a2 = st.columns(2)
    
    with col_a1:
        st.markdown("#### 📄 Exemplo de Payload Telemétrico Recebido (JSON)")
        sample_json = {
            "veiculo_id": "BUS-2309",
            "linha_codigo": "0426",
            "timestamp": datetime.now().isoformat(),
            "telemetria": {
                "rpm_motor": 1850,
                "velocidade_kmh": 48.5,
                "temperatura_motor_c": 89.2,
                "temperatura_cambio_c": 98.4,
                "espessura_lona_freio_mm": 2.8,
                "vibracao_suspensao_g": 0.42
            }
        }
        st.code(json.dumps(sample_json, indent=2), language="json")
        
    with col_a2:
        st.markdown("#### 🛠️ Endpoints Disponíveis na Plataforma")
        st.markdown("""
        * **`POST /api/v1/telemetria`**: Ingestão de telemetria dos ônibus em tempo real.
        * **`GET /api/v1/alertas`**: Retorna os alertas ativos de manutenção preditiva.
        * **`GET /api/v1/marketplace/pedidos`**: Lista ordens de compras automáticas de peças pelo menor valor.
        * **`GET /api/v1/dashboard/executivo`**: Métricas consolidadas para a diretoria.
        """)
        
        if st.button("🚀 Simular Ingestão Telemétrica no Servidor"):
            st.success("✅ Pacote telemétrico processado! Ordem de compra otimizada enviada ao Atacado Nacional pelo menor preço de mercado.")

# ==============================================================================
# ABA 8: MAPA DAS LINHAS DE JOINVILLE
# ==============================================================================
with tab_mapa:
    st.subheader("🗺️ Monitoramento Geográfico das Linhas e Ônibus de Joinville")
    st.write("Visualização telemétrica dos ônibus trafegando nos principais corredores e terminais da Transtusa:")
    
    # Coordenadas reais de Joinville
    df_map = pd.DataFrame({
        'lat': [-26.3015, -26.2750, -26.3280, -26.2410, -26.2950, -26.3120],
        'lon': [-48.8442, -48.8350, -48.8390, -48.8820, -48.8890, -48.8520],
        'nome': ['Terminal Central (Rua 9 de Março)', 'Estação Iririú', 'Estação Itaum', 'Estação Pirabeiraba', 'Distrito Perini (Linha 0426)', 'Terminal Sul']
    })
    
    st.map(df_map, zoom=12, use_container_width=True)
    st.caption("📍 PONTOS DE MONITORAMENTO: Terminal Central, Estação Iririú, Estação Itaum, Estação Pirabeiraba, Distrito Industrial Perini e Terminal Sul.")

# ==============================================================================
# RODAPÉ
# ==============================================================================
st.markdown("---")
st.markdown("🏢 **Transporte e Turismo Santo Antônio Ltda. (Transtusa)** | Desenvolvido para a Diretoria Executiva & Equipe de Manutenção")
