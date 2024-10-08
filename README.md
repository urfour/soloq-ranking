# SoloQ Ranking

Ce projet est une application web Flask qui affiche le classement des invocateurs de League of Legends en utilisant les données de l'API OPGG. L'application met à jour les informations des invocateurs à intervalles réguliers et les affiche sur une page web.

## Fonctionnalités

- Affiche le classement des invocateurs avec leurs informations de rang, division, LP, victoires, défaites et taux de victoire.
- Affiche les trois dernières parties jouées pour chaque invocateur avec des bandeaux colorés (bleu pour les victoires, rouge pour les défaites).
- Met à jour automatiquement les informations des invocateurs toutes les minutes.

## Prérequis

- Python 3.x
- pip (Python package installer)

## Installation

1. Cloner le dépôt :

   ```sh
   git clone https://github.com/votre-utilisateur/soloq-ranking.git
   cd soloq-ranking
   ```

2. Installer les dépendances :

    ```sh
    pip install -r requirements.txt
    ```

## Utilisation

1. Lancer l'application Flask :

    ```sh
    python soloq.py
    ```

2. Ouvrir le navigateur et accéder à (`http://127.0.0.1:5000`) pour voir le classement des invocateurs.
