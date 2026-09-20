# 🚍 Plataforma Integrada de Telemetria Preditiva & Suprimentos - Transtusa Joinville

Uma solução completa de **Inteligência Artificial Preditiva, Telemetria CAN Bus, Gestão do Setor de Compras B2B e Análise Financeira** desenvolvida para a operação da **Transporte e Turismo Santo Antônio Ltda. (Transtusa)** em Joinville/SC.

A plataforma monitora a frota de **mais de 300 ônibus**, reduz a ocupação diária da oficina de **110 para 44 veículos/dia (-60%)**, antecipa falhas mecânicas com até 20 dias de antecedência e direciona as ordens de compra para o **Atacado Nacional pelo menor valor do Brasil**.

---

## 🛠️ Funcionalidades do Software

A aplicação principal (`app_streamlit_transtusa.py`) é organizada em **8 abas interativas**:

### 1. 📊 Dashboard Executivo & Preditivo
* **Métricas Principais**: Visão geral da frota (301 ônibus), redução na oficina (-60%), economia líquida anual (R\$ 15,95 Mi) e tempo de Payback (23 dias).
* **Gráficos Comparativos**: Análise visual de custos operacionais (R\$ 30,11M vs. R\$ 14,51M) e fluxo de veículos parados.
* **Lead Time Preditivo por Sensor**: Gráfico exibindo a antecedência em dias gerada por cada sensor antes de falhas graves (2 a 20 dias).

### 2. 🛒 Setor de Compras & Menor Custo (Procurement Decision System)
* **Inteligência de Menor Valor**: Sistema que utiliza a janela de tempo da manutenção preditiva (3 a 10 dias) para indicar a **compra pelo menor valor do Brasil** no Atacado Nacional (SP/RS) ou Hubs Regionais (PR) com descontos de **30% a 40,5%**.
* **Simulador de Antecedência**: Permite ajustar a janela de dias para comparar os valores entre o varejo emergencial local (Joinville) e o atacado em lote.
* **Cálculo de Economia em Reais**: Exibe a economia bruta gerada por lote e botões diretos para envio de pedido via **WhatsApp Direct** ou **E-mail**.

### 3. 🧰 Sensores & Alocação 3D no Veículo
* **Esquema Técnico de Distribuição**:
  * **Painel/Cabine**: Gateway IoT 4G/GPS (Conectado à porta OBD-II / J1939).
  * **Eixos / Freios**: Sensores de espessura de lona de freio (< 3.0 mm) e pressão de cuíca pneumática (PSI).
  * **Motor / Câmbio**: Transdutor de temperatura do fluido de transmissão (Distrito Perini > 100 °C) e viscosidade óptica do óleo do cárter.
  * **Suspensão / Pneus**: Acelerômetro Triaxial MPU (feixes de mola para serras/rua) e TPMS sem fio nas 6 rodas.
* **CAPEX e Cronograma**: Detalhamento do kit de R\$ 3.000,00 por ônibus e plano de instalação em 38 dias úteis (~1,5 mês).

### 4. 🏬 Marketplace B2B de Fornecedores Homologados
* **Locais (Joinville/SC)**: Zezinho Distribuidora, Forparts / Rede Âncora, FASA Peças e Truck Parts (Atendimento Express 2h-4h).
* **Regionais (SC/PR)**: Pardiesel e Rodoparaná / Dutra Autopeças (12h-24h | 18% a 25% OFF).
* **Atacado Nacional (SP/RS)**: Marcopolo Parts Central e Anchieta / Cometa Distribuidora (24h-72h | 25% a 40.5% OFF).

### 5. 🏦 Simulador Interativo de Financiamento BNDES
* **Simulador de Crédito**: Sliders para simular investimentos entre R\$ 500 mil e R\$ 5,0 milhões.
* **Linhas Elegíveis**: BNDES FINAME (TLP + 2,5% a.a.), FINEP Inovação (6% a.a.), Leasing HaaS Hardware e Crédito ESG.
* **Análise de Fluxo de Caixa**: Prova que a economia gerada (R\$ 1,32M/mês) cobre a parcela do financiamento sobrante com saldo positivo desde o 1º mês.

### 6. 📱 Painel Embarcado do Motorista (App Cliente)
* Simulação da tela do computador de bordo do ônibus com medidores digitais em tempo real (RPM, velocidade, temperatura, lona de freio e pressão pneumática de ar) e alertas de condução defensiva.

### 7. 🌐 API & Telemetria RESTful JSON
* Exibição dos payloads JSON recebidos via rede CAN bus J1939 e simulação do teste de estresse e ingestão no servidor FastAPI.

### 8. 🗺️ Monitoramento Geográfico das Linhas de Joinville
* Mapeamento interativo dos terminais centrais e de bairro (Terminal Central, Estação Iririú, Estação Itaum, Pirabeiraba, Distrito Perini e Terminal Sul).
