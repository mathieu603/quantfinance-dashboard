
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ==========================================
# 1. CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="QuantFinance | Market Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. DESIGN CSS
# ==========================================

st.markdown("""
<style>
    .stApp {
        background-color: #0b1120;
        color: #e2e8f0;
    }

    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #273449;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    h1, h2, h3 {
        color: #f1f5f9 !important;
    }

    p, label {
        color: #cbd5e1;
    }

    .hero {
        background: linear-gradient(120deg, #16243b, #102c35);
        border: 1px solid #2b4659;
        border-radius: 18px;
        padding: 28px 30px;
        margin-bottom: 25px;
    }

    .hero-label {
        color: #38bdf8;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .hero-title {
        color: #f8fafc;
        font-size: 32px;
        font-weight: 750;
        margin-top: 8px;
    }

    .hero-description {
        color: #a8b8cc;
        font-size: 15px;
        margin-top: 8px;
    }

    div[data-testid="stMetric"] {
        background: #111c2e;
        border: 1px solid #29384d;
        padding: 18px;
        border-radius: 14px;
    }

    div[data-testid="stMetricLabel"] {
        color: #a8b8cc;
    }

    div[data-testid="stMetricValue"] {
        color: #f8fafc;
    }

    .section-note {
        color: #94a3b8;
        font-size: 13px;
        margin-top: -8px;
        margin-bottom: 15px;
    }

    .footer {
        color: #718096;
        font-size: 12px;
        text-align: center;
        border-top: 1px solid #273449;
        margin-top: 40px;
        padding-top: 20px;
    }

    div.stButton > button {
        background-color: #0ea5e9;
        color: white;
        border: none;
        border-radius: 9px;
        font-weight: 600;
        min-height: 45px;
        width: 100%;
    }

    div.stButton > button:hover {
        background-color: #0284c7;
        color: white;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. FONCTIONS
# ==========================================

@st.cache_data(ttl=900)
def charger_donnees(ticker, periode):
    data = yf.download(
        ticker,
        period=periode,
        auto_adjust=True,
        progress=False
    )

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    return data


def creer_graphique(x, y, titre, nom_y, couleur="#38bdf8"):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode="lines",
        name=nom_y,
        line=dict(color=couleur, width=2.5),
        fill="tozeroy" if "Drawdown" in titre else None,
        fillcolor="rgba(56, 189, 248, 0.10)"
        if "Drawdown" in titre else None,
        hovertemplate="%{x|%d/%m/%Y}<br>"
                      + nom_y + " : %{y:.2f}<extra></extra>"
    ))

    fig.update_layout(
        title=dict(
            text=titre,
            font=dict(size=17, color="#e2e8f0")
        ),
        paper_bgcolor="#111c2e",
        plot_bgcolor="#111c2e",
        font=dict(color="#94a3b8"),
        margin=dict(l=15, r=15, t=55, b=15),
        height=340,
        hovermode="x unified",
        xaxis=dict(
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            title=nom_y,
            gridcolor="#263449",
            zeroline=False
        ),
        showlegend=False
    )

    return fig


# ==========================================
# 4. BARRE LATERALE
# ==========================================

with st.sidebar:
    st.markdown("## 📈 QuantFinance")
    st.caption("MARKET ANALYTICS")
    st.divider()

    st.markdown("### Paramètres")

    ticker = st.selectbox(
        "Actif financier",
        ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"],
        format_func=lambda x: {
            "AAPL": "Apple · AAPL",
            "MSFT": "Microsoft · MSFT",
            "GOOGL": "Alphabet · GOOGL",
            "AMZN": "Amazon · AMZN",
            "NVDA": "NVIDIA · NVDA"
        }[x]
    )

    periode_label = st.selectbox(
        "Période d'analyse",
        ["6 mois", "1 an", "2 ans", "5 ans"],
        index=1
    )

    periodes = {
        "6 mois": "6mo",
        "1 an": "1y",
        "2 ans": "2y",
        "5 ans": "5y"
    }

    analyser = st.button(
        "Lancer l'analyse",
        type="primary"
    )

    st.divider()
    st.caption("OUTILS")
    st.markdown("📊 Analyse de performance")
    st.markdown("📉 Mesure du risque")
    st.markdown("📈 Visualisation financière")

    st.divider()
    st.caption("Données via Yahoo Finance")
    st.caption("Projet personnel · Python")


# ==========================================
# 5. EN-TETE
# ==========================================

st.markdown("""
<div class="hero">
    <div class="hero-label">QUANTITATIVE FINANCE · DATA ANALYTICS</div>
    <div class="hero-title">Market Intelligence Dashboard</div>
    <div class="hero-description">
        Analyse des performances boursières et mesure du risque
        à partir de données financières historiques.
    </div>
</div>
""", unsafe_allow_html=True)

# Conserver l'analyse affichée lors des changements d'interface
if "analyse" not in st.session_state:
    st.session_state["analyse"] = {
        "ticker": "AAPL",
        "periode": "1 an"
    }

if analyser:
    st.session_state["analyse"] = {
        "ticker": ticker,
        "periode": periode_label
    }

ticker_actif = st.session_state["analyse"]["ticker"]
periode_active = st.session_state["analyse"]["periode"]

st.markdown(
    f"### Vue d'ensemble — {ticker_actif}"
)

st.markdown(
    '<div class="section-note">'
    'Indicateurs calculés sur la période sélectionnée.'
    '</div>',
    unsafe_allow_html=True
)

# ==========================================
# 6. TELECHARGEMENT ET CALCULS
# ==========================================

with st.spinner("Chargement des données financières..."):
    try:
        data = charger_donnees(
            ticker_actif,
            {
                "6 mois": "6mo",
                "1 an": "1y",
                "2 ans": "2y",
                "5 ans": "5y"
            }[periode_active]
        )

        if data.empty or "Close" not in data.columns:
            st.error(
                "Aucune donnée reçue. Vérifie ta connexion Internet."
            )
            st.stop()

        prix = data["Close"].dropna()

        if len(prix) < 2:
            st.error("Historique insuffisant pour calculer les indicateurs.")
            st.stop()

        rendements = prix.pct_change().dropna()

        rendement_total = prix.iloc[-1] / prix.iloc[0] - 1
        volatilite = rendements.std() * np.sqrt(252)

        drawdown = prix / prix.cummax() - 1
        drawdown_max = drawdown.min()

        ecart_type = rendements.std()

        # Ratio de Sharpe simplifié, avec taux sans risque nul
        sharpe = (
            rendements.mean() / ecart_type * np.sqrt(252)
            if ecart_type > 0 else np.nan
        )

        dernier_cours = prix.iloc[-1]
        variation_jour = (
            prix.iloc[-1] / prix.iloc[-2] - 1
        )

        # ==========================================
        # 7. CARTES D'INDICATEURS
        # ==========================================

        st.markdown("#### Indicateurs clés")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Dernier cours ajusté",
            f"${dernier_cours:,.2f}",
            f"{variation_jour:+.2%} sur la dernière séance"
        )

        c2.metric(
            "Rendement total",
            f"{rendement_total:+.2%}"
        )

        c3.metric(
            "Volatilité annualisée",
            f"{volatilite:.2%}"
        )

        c4.metric(
            "Ratio de Sharpe",
            f"{sharpe:.2f}" if pd.notna(sharpe) else "N/A"
        )

        # ==========================================
        # 8. GRAPHIQUES
        # ==========================================

        st.markdown("---")
        gauche, droite = st.columns([1.7, 1])

        with gauche:
            st.markdown("#### Évolution du cours")
            st.caption(
                "Prix ajusté en dollars américains · "
                "Historique de la période choisie"
            )

            fig_prix = creer_graphique(
                prix.index,
                prix.values,
                f"{ticker_actif} — Historique du cours",
                "Cours ($)"
            )

            st.plotly_chart(
                fig_prix,
                use_container_width=True
            )

        with droite:
            st.markdown("#### Analyse du risque")
            st.caption("Baisse depuis le précédent sommet")

            fig_dd = creer_graphique(
                drawdown.index,
                drawdown.values * 100,
                "Drawdown au cours du temps",
                "Drawdown (%)",
                couleur="#fb7185"
            )

            st.plotly_chart(
                fig_dd,
                use_container_width=True
            )

        # ==========================================
        # 9. INTERPRETATION
        # ==========================================

        st.markdown("---")
        st.markdown("#### Synthèse de l'analyse")

        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("**Performance**")

            if rendement_total > 0:
                st.success(
                    f"L'action progresse de {rendement_total:.2%} "
                    "sur la période observée."
                )
            elif rendement_total < 0:
                st.warning(
                    f"L'action recule de {abs(rendement_total):.2%} "
                    "sur la période observée."
                )
            else:
                st.info("Le rendement est nul sur la période.")

        with col_b:
            st.markdown("**Risque historique**")

            st.write(
                f"La volatilité annualisée atteint **{volatilite:.2%}**."
            )

            st.write(
                f"Le drawdown maximal atteint **{drawdown_max:.2%}**."
            )

        with st.expander("Comprendre les indicateurs"):
            st.markdown("""
            - **Rendement total :** évolution du cours entre le début
              et la fin de la période.
            - **Volatilité annualisée :** mesure la dispersion des
              rendements quotidiens, annualisée avec 252 séances.
            - **Drawdown maximal :** plus forte baisse depuis un
              sommet antérieur.
            - **Ratio de Sharpe :** rendement moyen excédentaire
              divisé par la volatilité. Ici, le taux sans risque est
              supposé nul ; ce ratio est une approximation historique.
            """)

        # ==========================================
        # 10. TABLEAU DES DONNEES
        # ==========================================

        with st.expander("Consulter les dernières observations"):
            tableau = data.tail(10).sort_index(ascending=False)
            st.dataframe(
                tableau,
                use_container_width=True
            )

        st.caption(
            f"Données du {prix.index[0].date()} au "
            f"{prix.index[-1].date()} · Source : Yahoo Finance"
        )

    except Exception as e:
        st.error(
            "Impossible de terminer l'analyse. "
            "Vérifie la connexion Internet et réessaie."
        )
        st.code(str(e))




# ==========================================
# 10B. COMPARAISON DE PLUSIEURS ACTIONS
# ==========================================

st.markdown("---")
st.header("📊 Comparaison multi-actifs")
st.write(
    "Compare les performances et les risques de plusieurs actions "
    "sur la même période."
)

actions_disponibles = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Alphabet": "GOOGL",
    "Amazon": "AMZN",
    "NVIDIA": "NVDA",
    "Meta": "META"
}

actions_choisies = st.multiselect(
    "Choisir les actions à comparer",
    options=list(actions_disponibles.keys()),
    default=["Apple", "Microsoft", "NVIDIA"]
)

if len(actions_choisies) < 2:
    st.info("Choisis au moins deux actions pour les comparer.")
else:
    tickers_comparaison = [
        actions_disponibles[nom] for nom in actions_choisies
    ]

    @st.cache_data(ttl=900)
    def charger_comparaison(tickers, periode):
        resultats = {}

        for symbole in tickers:
            df = yf.download(
                symbole,
                period=periode,
                auto_adjust=True,
                progress=False
            )

            if not df.empty:
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)

                if "Close" in df.columns:
                    resultats[symbole] = df["Close"].rename(symbole)

        if not resultats:
            return pd.DataFrame()

        return pd.concat(resultats.values(), axis=1).dropna()

    try:
        with st.spinner("Chargement des actions..."):
            cours = charger_comparaison(
                tuple(tickers_comparaison),
                {
                    "6 mois": "6mo",
                    "1 an": "1y",
                    "2 ans": "2y",
                    "5 ans": "5y"
                }[periode_active]
            )

        if cours.empty or len(cours) < 2:
            st.warning(
                "Les données sont insuffisantes pour comparer "
                "ces actions sur cette période."
            )
        else:
            # Graphique des performances, base 100
            performance_base100 = cours.div(cours.iloc[0]).mul(100)

            st.subheader("Performance comparée")
            st.caption(
                "Chaque série commence à 100 pour faciliter "
                "la comparaison des évolutions."
            )

            fig_comparaison = go.Figure()

            for symbole in performance_base100.columns:
                fig_comparaison.add_trace(
                    go.Scatter(
                        x=performance_base100.index,
                        y=performance_base100[symbole],
                        mode="lines",
                        name=symbole,
                        line=dict(width=2.5),
                        hovertemplate=(
                            "%{x|%d/%m/%Y}<br>"
                            + symbole
                            + " : %{y:.2f}<extra></extra>"
                        )
                    )
                )

            fig_comparaison.update_layout(
                paper_bgcolor="#111c2e",
                plot_bgcolor="#111c2e",
                font=dict(color="#cbd5e1"),
                height=420,
                hovermode="x unified",
                xaxis=dict(showgrid=False),
                yaxis=dict(
                    title="Indice de performance (base 100)",
                    gridcolor="#263449"
                ),
                legend=dict(orientation="h", y=-0.2),
                margin=dict(l=15, r=15, t=30, b=55)
            )

            st.plotly_chart(
                fig_comparaison,
                use_container_width=True
            )

            # Calcul des indicateurs par action
            rendements_multi = cours.pct_change().dropna()
            lignes = []

            for symbole in cours.columns:
                serie = cours[symbole].dropna()
                r = serie.pct_change().dropna()

                rendement_total = serie.iloc[-1] / serie.iloc[0] - 1
                volatilite = r.std() * np.sqrt(252)
                dd = (serie / serie.cummax() - 1).min()

                sharpe = (
                    r.mean() / r.std() * np.sqrt(252)
                    if r.std() > 0 else np.nan
                )

                lignes.append({
                    "Action": symbole,
                    "Rendement total": rendement_total,
                    "Volatilité annualisée": volatilite,
                    "Drawdown maximal": dd,
                    "Ratio de Sharpe": sharpe
                })

            tableau_comparaison = pd.DataFrame(lignes).set_index("Action")

            st.subheader("Tableau comparatif")
            st.dataframe(
                tableau_comparaison.style.format({
                    "Rendement total": "{:.2%}",
                    "Volatilité annualisée": "{:.2%}",
                    "Drawdown maximal": "{:.2%}",
                    "Ratio de Sharpe": "{:.2f}"
                }),
                use_container_width=True
            )

            # Matrice de corrélation des rendements quotidiens
            st.subheader("Matrice de corrélation")
            correlation = rendements_multi.corr()

            fig_corr = go.Figure(
                data=go.Heatmap(
                    z=correlation.values,
                    x=correlation.columns,
                    y=correlation.index,
                    zmin=-1,
                    zmax=1,
                    colorscale="RdBu",
                    reversescale=True,
                    text=np.round(correlation.values, 2),
                    texttemplate="%{text}",
                    colorbar=dict(title="Corrélation")
                )
            )

            fig_corr.update_layout(
                paper_bgcolor="#111c2e",
                plot_bgcolor="#111c2e",
                font=dict(color="#e2e8f0"),
                height=350,
                margin=dict(l=15, r=15, t=30, b=15)
            )

            st.plotly_chart(
                fig_corr,
                use_container_width=True
            )

            st.caption(
                "Les corrélations sont calculées sur les rendements "
                "quotidiens communs aux actions sélectionnées. "
                "Les résultats dépendent de la période observée."
            )

    except Exception as e:
        st.error("La comparaison n'a pas pu être calculée.")
        st.code(str(e))


# ==========================================
# 11. PIED DE PAGE
# ==========================================

st.markdown("""
<div class="footer">
    QUANTFINANCE · Projet personnel de finance quantitative<br>
    Python · Streamlit · Pandas · Plotly · yfinance<br><br>
    Outil pédagogique. Les données peuvent être retardées.
    Les performances passées ne préjugent pas des performances futures.
    Ce site ne constitue pas un conseil en investissement.
</div>
""", unsafe_allow_html=True)



