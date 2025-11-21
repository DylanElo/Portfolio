# 3️⃣ Strategy Document

**(C’est le pont entre “on a un problème” et “voilà comment on va l’adresser avec la data”)**

**Projet** : Stratégie d’analyse de la performance des animés récents  
**BI Lead** : Dylan Elo

## 1. Vision

Mettre en place une première base analytique permettant au studio de comprendre ce qui fait le succès ou l’échec de ses animés récents, et de réutiliser ce cadre pour les futurs projets.

## 2. Approche générale

### Comprendre le besoin métier
*   Collecter les questions des stakeholders (production, marketing, direction).
*   Les reformuler en questions analytiques et en KPIs.

### Concevoir le modèle de données
Structurer les données autour :
*   d’une table **Dim_Anime** (infos générales),
*   de tables de faits (**Fact_Rating**, **Fact_Audience**, **Fact_Sentiment**, **Fact_Production**).

### Construire le pipeline
*   Récupération des données publiques (scraping/API).
*   Nettoyage, jointure et calcul des métriques (Python/SQL).
*   Export dans un modèle propre (CSV / base SQL).

### Développer le dashboard
*   1 page exécutive + 1 page détail par anime.
*   Filtres simples (ancien vs récent, genre, type de série).

### Synthèse & recommandations
*   Interprétation des résultats.
*   Propositions concrètes pour la roadmap de production & marketing.

## 3. Données & sources

**Sources publiques :**
*   Notes, votes, genres, années de diffusion.
*   Commentaires / reviews pour sentiment.

**Données simulées :**
*   Budget catégorie (low / medium / high).
*   Problèmes de prod (retard, staff change, rush).
*   Intensité marketing (faible / moyenne / forte).

*Note : Ces données sont utilisées comme proxy réaliste pour un exercice BI.*

## 4. Outils & stack

*   **Collecte / transformation** : Python + Pandas / SQL.
*   **Stockage** : SQLite.
*   **Visualisation** : Chart.js (Custom Web Dashboard).
*   **Documentation** : README GitHub + Google Docs/Slides pour la partie business.

## 5. Roadmap (simple)

**Semaine 1 :**
*   Finaliser Stakeholder + Executive + Strategy docs.
*   Choisir 4–6 animés cibles.
*   Collecter les données brutes.

**Semaine 2 :**
*   Nettoyage + construction du modèle de données.
*   Création des KPIs.

**Semaine 3 :**
*   Construction du dashboard.
*   Rédaction des insights + recommandations.

**Semaine 4 (optionnel – polish portfolio) :**
*   Screenshots, README propre, petite présentation type “case study”.
