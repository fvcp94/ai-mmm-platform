# AI-Powered Marketing Mix Modeling Platform

An end-to-end **AI-driven marketing analytics platform** that automates Marketing Mix Modeling (MMM), causal inference, and executive decision-making using **multi-agent LLM orchestration**, **Bayesian modeling**, and **retrieval-augmented generation (RAG)** — all powered by **100% free OpenRouter models**.

---

## 🚀 Overview

This project demonstrates how modern AI systems can replace weeks of manual marketing analysis with a **fully automated, statistically rigorous, and business-focused workflow**.

From raw marketing data to executive-ready recommendations — **in minutes, at zero inference cost**.

---

## 🤖 Multi-Agent AI Architecture

The platform uses **LangGraph** to orchestrate multiple specialized AI agents that collaborate like a real analytics consulting team.

### Agents
- **Data Analyst Agent**
  - Data quality checks and validation
  - Feature engineering recommendations
  - Seasonality and trend detection

- **MMM Specialist Agent**
  - Bayesian Marketing Mix Modeling
  - Channel contribution and ROI estimation
  - Saturation and diminishing returns analysis

- **Causal Inference Agent**
  - Experiment design (Geo-tests, A/B tests, DiD)
  - Incrementality validation
  - Power analysis and statistical significance testing

- **Business Strategist Agent**
  - Budget reallocation strategies
  - ROI optimization recommendations
  - Risk assessment and assumptions review

- **Presentation Builder Agent**
  - Executive summaries
  - Insight narratives
  - Visualization-ready outputs

---

## 📊 Core Capabilities

### Marketing Mix Modeling (MMM)
- Bayesian MMM with uncertainty quantification
- Channel contribution decomposition
- ROI and marginal ROI estimation
- Saturation curves and spend optimization

### Causal Inference & Experimentation
- Geo-experiments
- Difference-in-Differences (DiD)
- Synthetic control methods
- Sample size, power, and MDE calculations

### RAG-Powered Knowledge Hub
- Grounded answers using marketing science literature
- Industry benchmarks and best practices
- Transparent citations for every response

### Scenario Planning
- Interactive budget allocation
- Revenue and ROI forecasting
- Monte Carlo simulations for uncertainty
- Executive-ready scenario comparisons

---

## 🏗️ System Architecture

```
Streamlit Web Application
        │
LangGraph Multi-Agent Orchestration
        │
├── Bayesian MMM Engine (PyMC / statsmodels)
├── Causal Inference Engine (DoWhy / CausalML)
├── RAG Knowledge System (ChromaDB)
└── Scenario Optimization & Visualization
```

---

## 🛠️ Tech Stack

### AI & Orchestration
- OpenRouter (LLaMA 3.1, Qwen, Mistral – free models)
- LangGraph
- LangChain

### Analytics & Modeling
- PyMC / Bayesian Modeling
- DoWhy, CausalML
- Scikit-learn

### Data & Visualization
- Pandas, NumPy, DuckDB
- Plotly

### App & Deployment
- Streamlit (Streamlit Cloud)
- GitHub Actions (CI/CD)

---

## ▶️ Running Locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app/app.py
```

---

## 🌐 Deployment

Designed for **Streamlit Cloud** with zero infrastructure cost.

Required secret:
```toml
OPENROUTER_API_KEY="your_openrouter_api_key"
```

---

## 👤 Author

**Febin Varghese**  
Senior Data Scientist | Applied Machine Learning | Bayesian Modeling | Causal Inference | Marketing Analytics
