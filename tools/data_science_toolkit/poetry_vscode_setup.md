# Configurer un projet Python avec Poetry dans VS Code

*Par Arthur Cartel Foahom Gouabou*
[cartelgouabou.github.io](https://cartelgouabou.github.io/)  •  [LinkedIn](https://www.linkedin.com/in/arthur-cartel-foahom-gouabou-phd-41041195/)

Ce tutoriel vous guide pas à pas dans la création et la configuration d’un projet Python moderne à l’aide de **Poetry** et **VS Code**.

Vous apprendrez à :

- Initialiser un projet structuré avec `poetry new`
- Gérer les dépendances proprement
- Créer et activer un environnement virtuel isolé
- Intégrer des outils de qualité de code (black, ruff, pytest) dans VS Code

### Pourquoi utiliser Poetry ?

Poetry est une alternative puissante à `pip`, `virtualenv`, ou `pipenv`, car il unifie la gestion de projet Python avec :

- Une configuration claire dans un seul fichier (`pyproject.toml`)
- Des environnements virtuels automatiques
- Une gestion explicite des dépendances et de leurs versions
- Des commandes simples pour ajouter, verrouiller, tester ou packager un projet

C’est aujourd’hui un outil largement adopté dans les projets professionnels et open source.Ce guide explique pas à pas comment configurer un environnement de développement Python avec **Poetry** dans **Visual Studio Code (VS Code)**, en s'appuyant sur la structure générée par défaut depuis la version 2.1 de Poetry.

---

## Prérequis

Assurez-vous d'avoir les éléments suivants installés :

- [Python](https://www.python.org/downloads/) (v3.7 ou plus)
- [VS Code](https://code.visualstudio.com/)
- L'extension **Python** pour VS Code
- (Optionnel) [Git](https://git-scm.com/)

---

## 1. Installer Poetry

### Sur Linux / macOS

Ouvrez un terminal et exécutez :

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Sur Windows

Ouvrez **PowerShell** et exécutez :

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

> Assurez-vous que `python` est accessible via PowerShell (`python --version`).

Redémarrez votre terminal si besoin, puis vérifiez l'installation :

```bash
poetry --version
```

## Ajouter Poetry au PATH (si `poetry` n’est pas reconnu)

Il se peut que `poetry` ne fonctionne pas immédiatement car \*\*le répertoire contenant l'exécutable n'est pas dans votre \*\*\`\`.

### 🚩 Symptôme :

```powershell
poetry : commande introuvable
```

### Solution sous Windows (avec PowerShell)

#### 1. Vérifier manuellement le chemin d'installation
Après l'installation, `poetry.exe` est souvent situé ici :

```makefile
C:\Users\<votre_nom>\AppData\Roaming\Python\Scripts\poetry.exe
```

Testez l'exécutable directement avec :

Cela retournera un chemin similaire à :

```powershell
& "C:\Users\<votre_nom>\AppData\Roaming\Python\Scripts\poetry.exe" --version
```
Si cela fonctionne, passez à l'étape suivante.

#### 2. Ajouter ce chemin au `PATH` (PowerShell)

Vous avez deux options pour rendre poetry disponible en tant que commande globale :

✅ Option A – Automatiquement via PowerShell

```powershell
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Users\<votre_nom>\AppData\Roaming\Python\Scripts", "User")
```

Remplacez <votre_nom> par votre nom d’utilisateur Windows si.

🖱️ Option B – Manuellement via l’interface Windows
1. Ouvrir le menu Démarrer → Rechercher "variables d’environnement"

2. Cliquer sur "Variables d’environnement..."

3. Dans la section "Variables utilisateur", sélectionner Path puis cliquer sur "Modifier"

4. Cliquer sur "Nouveau" puis ajouter :

```makefile
C:\Users\<votre_nom>\AppData\Roaming\Python\Scripts
```

5. Valider tous les écrans

Redémarrez ensuite PowerShell ou VS Code et testez :

```powershell
poetry --version
```
### Solution sous Linux / macOS

#### 1.  Recherchez où Poetry est installé :

```bash
find $HOME -type f -name "poetry" 2>/dev/null
```

Cela peut retourner par exemple :

```
/home/<votre_nom>/.local/share/pypoetry/venv/bin/poetry
```

#### 2. Ajoutez le dossier contenant `poetry` à votre `PATH` :

```bash
export PATH="$HOME/.local/bin:$PATH"
```
Remplacer '$PATH' ci-dessus par le schemin obtenu precedemment

#### 3. Rendez ce changement permanent :

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
# Fermez puis rouvrez votre terminal pour que les modifications prennent effet
```
Remplacer '$PATH' ci-dessus par le schemin obtenu precedemment

#### 4. Vérifiez que Poetry fonctionne :

````bash
poetry --version
````

---

## 2. Créer un projet Python avec Poetry

Dans un terminal, placez-vous dans le dossier où vous souhaitez créer le projet, puis exécutez :

```bash
poetry new mon_projet
cd mon_projet
```

Depuis Poetry 2.1, cette commande génère la structure suivante :

```
mon_projet/
├── src/
│   └── mon_projet/
│       └── __init__.py
├── tests/
│   └── __init__.py
├── pyproject.toml
└── README.md
```

Cette structure respecte les bonnes pratiques modernes, notamment en data science, en séparant clairement le code source (`src/`) des autres composants du projet.

Pour permettre les imports depuis `src/`, ajoutez la variable d’environnement `PYTHONPATH` :

### Linux / macOS

```bash
export PYTHONPATH="$(pwd)/src"
```

### Windows (PowerShell)

```powershell
$env:PYTHONPATH="$(Get-Location)\src"
```

---

## 3. Ouvrir le projet dans VS Code

```bash
code .
```

---

## 4. Créer et utiliser l'environnement virtuel

Configurez Poetry pour stocker l’environnement virtuel dans le dossier du projet :

```bash
poetry config virtualenvs.in-project true
```

Ensuite, installez les dépendances (et créez l’environnement si nécessaire) :

```bash
poetry install
```

### Activer manuellement l’environnement virtuel

1. Obtenez le chemin de l’environnement :

```bash
poetry env info --path
```

2. Activez-le selon votre système :

#### Sous Linux / macOS

```bash
source <chemin>/bin/activate
```

#### Sous Windows (PowerShell)

Placez-vous dans le dossier `Scripts` retourné par la commande précédente, puis :

```powershell
.\activate
```

> Remplacez `<chemin>` par le chemin réel de l’environnement retourné par Poetry.

### Différence entre `poetry install` et activation

- `poetry install` : installe les dépendances depuis `pyproject.toml`.
- Activer l’environnement : permet d’exécuter les commandes dans ce contexte (`python`, `pytest`, etc.).

---

## 5. Sélectionner l'interpréteur dans VS Code

1. Ouvrez la palette de commande (`Ctrl+Shift+P`)
2. Tapez : `Python: Select Interpreter`
3. Choisissez le chemin vers `.venv/bin/python` (Linux/macOS) ou `Scripts/python.exe` (Windows)

Vous pouvez aussi obtenir le chemin avec :

```bash
poetry env info --path
```

---

## 6. Installer des dépendances

### Comment Poetry distingue les dépendances ?

Poetry gère deux types de dépendances distinctes :

- **Dépendances de production** : ajoutées avec `poetry add`. Ce sont les bibliothèques nécessaires pour exécuter votre application (ex : `pandas`, `numpy`, `requests`).
- **Dépendances de développement** : ajoutées avec `poetry add --dev`. Ce sont des outils utilisés uniquement pour le développement (ex : `black`, `pytest`, `ruff`).

Cette distinction est visible dans le fichier `pyproject.toml` :

- Les dépendances classiques sont listées dans `[tool.poetry.dependencies]`
- Les dépendances de développement dans `[tool.poetry.group.dev.dependencies]`

### Quand cette distinction est-elle utile ?

Quand quelqu’un exécute :

```bash
poetry install
```

Poetry installe **toutes** les dépendances (prod + dev).

Mais si vous voulez installer uniquement les dépendances de production (par exemple pour un déploiement) :

```bash
poetry install --no-dev
```

Cela installe uniquement ce qui est strictement nécessaire pour faire fonctionner l’application.

---

### Ajouter une bibliothèque standard

```bash
poetry add pandas
```

### Ajouter des dépendances de développement

```bash
poetry add --dev black pytest ruff
```

Les dépendances de développement sont utiles pour le formatage, le linting, et les tests.

Elles ne sont utilisées **que pendant le développement**, et non lors de l'exécution normale du programme. Cela permet de garder l'environnement de production léger, rapide à installer, et sécurisé.

### Exemples d'usages :

- **black** : formate automatiquement votre code Python pour le rendre plus lisible et homogène (style PEP8).
- **pytest** : exécute les tests unitaires pour s'assurer que le code fonctionne correctement.
- **ruff** : vérifie le respect des conventions, détecte les erreurs de code, les imports inutiles, etc.

### Pourquoi les isoler ?

1. Pour **ne pas polluer l'environnement de production** avec des outils inutiles au bon fonctionnement de l'application.
2. Pour **faciliter les mises à jour et la gestion des versions** de ces outils, indépendamment des bibliothèques de production.
3. Pour **standardiser l'environnement de développement** et garantir que tous les développeurs utilisent les mêmes outils.

### Cas d'usage typiques en data science :

- Utiliser `black` pour formater automatiquement vos scripts de prétraitement (`src/preprocessing.py`).
- Lancer `pytest` sur des fonctions d’ingénierie de variables pour valider qu’elles traitent correctement les cas limites.
- Utiliser `ruff` pour s'assurer que les notebooks exportés en `.py` n'ont pas d'importations inutiles ou de styles incohérents.

---

## 7. Configurer les outils de code dans VS Code

Configurer des outils comme **Black** et **Ruff** dans VS Code permet d’automatiser certaines tâches importantes :

- **Améliorer la lisibilité** du code avec un formatage cohérent.
- **Prévenir les erreurs** courantes avant même l'exécution.
- **Standardiser le style** de code dans une équipe.
- **Gagner du temps** en évitant les corrections manuelles et les oublis.

Ces outils s’intègrent directement dans VS Code pour offrir des retours en temps réel sur la qualité du code, et appliquer des corrections automatiquement à l’enregistrement d’un fichier.

### Formatage automatique avec Black

Créez un dossier `.vscode` à la **racine du projet** (là où se trouve `pyproject.toml`), puis ajoutez un fichier `settings.json` à l’intérieur. VS Code le détectera automatiquement si vous ouvrez le dossier principal du projet avec `code .`.

Vous pouvez créer ce fichier rapidement avec la commande :

```bash
code .vscode/settings.json
```

Voici un exemple de contenu pour activer le formatage automatique avec Black :

```json
{
  "python.formatting.provider": "black",
  "editor.formatOnSave": true
}
```

### Linter avec Ruff

Ajoutez dans `pyproject.toml` :

```toml
[tool.ruff]
line-length = 88
select = ["E", "F", "I"]
```

#### Explication de cette configuration :

- `line-length = 88` : définit la longueur maximale des lignes à 88 caractères, une valeur recommandée par Black et largement utilisée dans la communauté Python.
- `select = ["E", "F", "I"]` : indique à Ruff quels types de règles appliquer :
  - `E` : erreurs de style selon [pycodestyle](https://pycodestyle.pycqa.org/), comme les espaces mal placés ou les mauvaises indentations.
  - `F` : erreurs détectées par [pyflakes](https://github.com/PyCQA/pyflakes), comme les variables non utilisées ou les noms non définis.
  - `I` : vérifications liées à l’ordre des imports (équivalent à isort).

Cette configuration permet de couvrir les erreurs les plus fréquentes tout en gardant un style propre et standardisé dans vos fichiers Python.

---

## 8. Lancer les tests

```bash
poetry run pytest
```

Cette commande exécute les tests dans le dossier `tests/` à l'intérieur de l'environnement virtuel.

---

## 9. Partager son environnement avec d'autres utilisateurs

Lorsque vous souhaitez permettre à d’autres personnes de reproduire votre environnement Poetry (par exemple un collègue ou un collaborateur open source), voici ce qu’il faut faire :

1. **Assurez-vous que vos dépendances sont bien à jour**

```bash
poetry lock
```

Cela crée ou met à jour le fichier `poetry.lock` qui contient les versions exactes de toutes les dépendances.

2. **Partagez les fichiers suivants dans votre dépôt Git** :

   - `pyproject.toml` (configuration déclarative)
   - `poetry.lock` (verrouillage des versions)

3. **Indiquez à la personne de faire simplement :**

```bash
poetry install
```

Cela :

- Crée l’environnement virtuel localement (si nécessaire)
- Installe exactement les mêmes versions de bibliothèques définies dans `poetry.lock`

4. (Optionnel) Pour reproduire uniquement l’environnement de production :

```bash
poetry install --no-dev
```

---

## Commandes utiles

| Action                    | Commande                                                                          |
| ------------------------- | --------------------------------------------------------------------------------- |
| Activer l’environnement   | `source .venv/bin/activate` (Linux/macOS) ou `.\.venv\Scripts\activate` (Windows) |
| Installer les dépendances | `poetry install`                                                                  |
| Ajouter une bibliothèque  | `poetry add nom_du_package`                                                       |
| Lancer un script          | `poetry run python script.py`                                                     |
| Lister les dépendances    | `poetry show`                                                                     |

---

## Références

- [Documentation officielle de Poetry](https://python-poetry.org/docs/)
- [Extension Python pour VS Code](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

---

## 🎉 Bravo !

Vous êtes allé jusqu’au bout ! Vous avez maintenant un projet Python propre, isolé, bien structuré, avec un environnement virtuel géré par Poetry, un linter, un formateur, des tests unitaires, et une intégration complète dans VS Code.

Ce socle est idéal pour des projets professionnels, open source ou data science.

Continuez à développer, tester et améliorer votre projet avec confiance. Bon code ! 


<sub>Document rédigé par Arthur Cartel Foahom Gouabou – Formateur & Data Scientist  •  [https://cartelgouabou.github.io/](https://cartelgouabou.github.io/)  •  [LinkedIn](https://www.linkedin.com/in/arthur-cartel-foahom-gouabou-phd-41041195/)</sub>
