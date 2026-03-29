# Guide CI/CD - AEBM Demo Cloud

## 1. Objectif
Ce projet dispose maintenant d'un pipeline GitHub Actions pour:
- valider le projet en CI sur Linux et Windows
- lancer les quality gates D1 + D3
- deplacer automatiquement le dernier commit `main` valide vers une branche de demo `streamlit-demo`

Cette branche `streamlit-demo` est pensee pour etre connectee a Streamlit Community Cloud.

## 2. Workflows
### CI
Fichier:
- `.github/workflows/ci.yml`

Comportement:
- declenchement sur `push`, `pull_request`, `workflow_dispatch`
- smoke test sur `ubuntu-latest` et `windows-latest`
- installation via `requirements.lock`
- `scripts/preflight.py --quick`
- tests D1 avec couverture minimale a 20%
- gate D3 avec `--min-micro-f1 0.65`
- upload de `coverage.xml` et des artefacts D3

### CD demo
Fichier:
- `.github/workflows/cd-demo.yml`

Comportement:
- demarre quand le workflow `ci` se termine avec succes
- ne se lance que pour un `push` sur `main`
- pousse le commit valide vers la branche `streamlit-demo`

## 3. Comment connecter Streamlit Community Cloud
Dans Streamlit Community Cloud:
1. creer une nouvelle app depuis le repo GitHub
2. choisir la branche `streamlit-demo`
3. choisir le fichier d'entree `app.py`
4. ajouter les secrets applicatifs dans l'interface Streamlit

Secrets attendus:
- `AEBM_NEO4J_MODE=cloud`
- `NEO4J_URI`
- `NEO4J_USER`
- `NEO4J_PASSWORD`
- `GROQ_API_KEY`
- `LLM_MODEL=llama-3.3-70b-versatile`

## 4. Flux recommande
1. ouvrir une PR
2. laisser la CI verifier preflight + tests + gates
3. merger sur `main`
4. laisser le workflow CD mettre a jour `streamlit-demo`
5. Streamlit Community Cloud redeploie automatiquement la demo

## 5. Notes pratiques
- le lockfile est maintenant compatible Linux/Windows pour `pywin32`
- les tests CI utilisent des repertoires temporaires isoles pour eviter les conflits sur `.coverage` et `pytest` temp/cache
- `scripts/test_d1.ps1` reutilise la meme logique de repertoires temporaires pour les executions locales
