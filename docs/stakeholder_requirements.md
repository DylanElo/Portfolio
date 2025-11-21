# 1️⃣ Stakeholder Requirements Document

**Projet** : Diagnostic performance des animés récents de Studio Pierrot  
**Rôle** : BI Analyst  
**Date** : 2024-11-22

## 1. Contexte

Studio Pierrot constate une baisse de performance sur plusieurs animés récents (audience, notes, perception fans), en comparaison avec ses franchises historiques (ex. Naruto Shippuden, Bleach).
La direction souhaite comprendre ce qui ne fonctionne plus et identifier des leviers concrets pour améliorer la performance des futurs projets.

## 2. Objectifs business (haut niveau)

*   Identifier les facteurs clés associés à la sous-performance des animés récents (contenu, format, production, marketing, diffusion, etc.).
*   Comparer la performance des nouveaux titres avec celle des franchises historiques du studio.
*   Prioriser 3–5 recommandations actionnables pour les futurs projets (format, nombre d’épisodes, gestion des fillers, qualité visuelle, etc.).
*   Mettre à disposition un dashboard simple permettant aux équipes métier de suivre ces indicateurs dans le temps.

## 3. Stakeholders principaux

| Stakeholder | Rôle / Fonction | Intérêt principal |
| :--- | :--- | :--- |
| **Directeur de production** | Supervise l’ensemble des animés | Comprendre l’impact du planning & des fillers |
| **Producteur exécutif** | Responsable des grandes licences | Protéger la valeur des IP, arbitrer les investissements |
| **Responsable marketing** | Gère promo & campagnes | Optimiser les campagnes selon le potentiel des séries |
| **Responsable diffusion** | Gère horaires / chaînes / plateformes | Maximiser l’audience par créneau & plateforme |
| **Finance / Direction** | Vision globale de rentabilité | Décider où investir, arrêter ou pivoter certains projets |
| **BI / Data team lead** | Porte le projet data | S’assurer que les KPIs sont fiables et réutilisables |

## 4. Besoins par stakeholder

### Directeur de production

**Questions :**
*   Quels animés récents ont les plus fortes chutes d’audience par épisode ?
*   Y a-t-il corrélation entre % d’épisodes fillers et baisse des notes/sentiment fans ?
*   Les changements de staff ou de planning (rush) impactent-ils la perception des fans ?

**Besoins :**
*   Vue comparant la performance des animés récents vs anciens.
*   KPIs : drop-off par épisode, % fillers, “production stability index”.
*   Drilldown par série / épisode.

### Responsable marketing

**Questions :**
*   Quels animés génèrent le plus de buzz positif vs bad buzz ?
*   Quelles campagnes (teasers, collabs, OP/ED) sont associées à de bonnes performances ?
*   Quels segments d’audience (jeunes, fans historiques, plateformes) réagissent le mieux ?

**Besoins :**
*   KPIs : sentiment score, volume de commentaires, évolution avant / pendant / après diffusion.
*   Segmentation par série, période, type de campagne.

### Responsable diffusion

**Questions :**
*   Quels créneaux / saisons de diffusion produisent la meilleure rétention d’audience ?
*   Les animés récents souffrent-ils d’une concurrence plus forte sur certains slots ?

**Besoins :**
*   Vue par série + créneau horaire + plateforme.
*   KPIs : audience moyenne, taux de complétion, drop-off.

### Finance / Direction

**Questions :**
*   Quelles séries sont “sous-performantes” par rapport à leur budget / importance stratégique ?
*   Quels types de projets faudrait-il prioriser à l’avenir ?

**Besoins :**
*   Vue synthétique : top / flop des animés récents.
*   3–5 recommandations claires avec impact estimé (ex : réduire les fillers, passer à des saisons plus courtes).

## 5. Questions analytiques prioritaires (cross-stakeholders)

*   Comment la performance des animés récents (audience, notes, sentiment) se compare-t-elle à celle des anciens succès de Pierrot ?
*   Quel est le pattern de drop-off entre les épisodes (à quel moment les spectateurs décrochent) ?
*   Quel est l’impact :
    *   du nombre d’épisodes,
    *   des fillers,
    *   des problèmes de production (simulés),
    *   sur la satisfaction fans (notes, sentiment) ?
*   Comment les décisions de diffusion et marketing influencent-elles la performance globale ?

## 6. Contraintes & hypothèses

*   Certaines données sont publiques (notes, votes, dates, etc.), d’autres sont simulées (budget, problèmes de prod, campagnes marketing).
*   Le périmètre initial se concentre sur 4–6 animés clés pour un POC (Naruto Shippuden, Bleach, Boruto, Tokyo Ghoul:re, etc.).
*   Le projet est réalisé à des fins d’illustration BI (portfolio) et ne reflète pas les données internes réelles de Studio Pierrot.
