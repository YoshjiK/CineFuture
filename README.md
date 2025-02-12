![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0.1-green.svg)
![TMDB](https://img.shields.io/badge/TMDB-API-yellow.svg)

## 📖 À Propos

CinéCreuse est un moteur de recherche et de recommandation de films spécialement conçu pour les habitants de la Creuse (France). Le projet utilise l'intelligence artificielle pour suggérer des films en se basant sur une analyse approfondie des préférences cinématographiques locales.

## 🎯 Caractéristiques

- 🔍 **Recherche Intelligente** : Trouvez rapidement des films par titre
- 🎲 **Recommandations Personnalisées** : Suggestions basées sur les goûts des Creusois
- 🎭 **Détails Complets** : Informations détaillées sur chaque film via l'API TMDB
- 🇫🇷 **Interface en Français** : Application entièrement localisée

## 🛠️ Technologies Utilisées

- **Backend** : Python, Flask
- **Data Science** : Pandas, Scikit-learn
- **Base de Données** : Parquet
- **API** : TMDB (The Movie Database)

## ⚙️ Installation

1. Clonez le repository :
```bash
git clone [URL_DU_REPO]
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Lancez l'application :
```bash
python app.py
```

## 📚 Structure du Projet

```
PROJET 2/
├── app.py              # Application principale Flask
├── recommander.py      # Logique de recommandation
├── requirements.txt    # Dépendances Python
├── static/            # Fichiers statiques (CSS, JS)
├── templates/         # Templates HTML
└── final_V8.parquet   # Base de données des films
```

## 🔧 Configuration

1. Créez un compte sur [TMDB](https://www.themoviedb.org/)
2. Obtenez une clé API
3. Configurez la clé dans `app.py`

## 📊 Base de Données

La base de données a été spécialement filtrée et optimisée pour correspondre aux préférences cinématographiques des habitants de la Creuse, basée sur une étude des habitudes locales.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- 🐛 Signaler des bugs
- 💡 Proposer des nouvelles fonctionnalités
- 📝 Améliorer la documentation

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.

## 👥 Contact

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue sur GitHub.
