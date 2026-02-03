# 📚 BetterClassroom

Plateforme d’apprentissage moderne, interactive et performante.

Objectif : dépasser les plateformes e-learning classiques grâce à :
- contenu HTML ultra rapide
- édition simple
- interactivité forte
- apprentissage adaptatif
- labs pratiques
- gamification

---

# 🧠 Stack technique officielle

## Backend
- Langage : Python 3.12+
- Framework : Django 5+
- ORM : Django ORM
- API : Django REST Framework
- Base de données : PostgreSQL
- Cache : Redis
- Tâches asynchrones : Celery
- Auth : Django Auth + JWT
- Stockage fichiers : S3 / MinIO

## Frontend
- Langage : TypeScript
- Framework : React (ou Vue)
- Build : Vite
- Styling : TailwindCSS
- Éditeur riche : TipTap / EditorJS
- Drag & drop : DnD Kit

## Infra
- Docker
- Nginx
- CI/CD (GitHub Actions)
- CDN pour assets statics

---

# 🏗️ Architecture générale

Frontend SPA → API Django → DB PostgreSQL → Stockage HTML statique

Les pages de cours sont servies en HTML statique pour performance maximale.

---

# 📖 Système de création de cours

## Langages utilisés
- HTML
- CSS
- JS léger
- Sauvegarde via backend Python

## Fonctionnalités
- Génération automatique dossier
- Sauvegarde HTML statique
- Templates préfaits
- Éditeur visuel WYSIWYG (React)
- Éditeur code HTML/CSS
- Prévisualisation live
- Drag & drop blocs

## Structure fichiers
/courses/{course_title}/
page_1.html
page_2.html
page_3.html
resume.html
notes.html
assets/

---

# 🧱 Blocs de contenu

Implémentés en React + JSON schema

- Texte riche
- Images
- Vidéo
- Code avec coloration syntaxique (Prism.js)
- Quiz interactifs
- Exercices pratiques
- Fichiers téléchargeables
- Iframe
- Diagrammes (Mermaid.js)

---

# 📈 Expérience pédagogique

## Progression (Python + DB)
- Suivi page par page
- Pourcentage de complétion
- Reprise automatique
- Streak d’apprentissage

## Évaluation
- Quiz auto-corrigés
- QCM
- Code runner (Docker sandbox)
- Notation automatique
- Feedback instantané

## Gamification
- Badges
- XP
- Niveaux
- Classements
- Succès

---

# 🌟 Fonctionnalités différenciantes

## Apprentissage adaptatif (Python + analytics)
- Recommandation de chapitres
- Détection des lacunes
- Parcours personnalisé

## Mode Lab
- Terminal sandbox
- Containers Docker isolés
- Exécution code Python/JS

## Social learning
- Commentaires
- Notes privées/publiques
- Groupes d’étude
- Chat temps réel (WebSocket / Django Channels)

## IA pédagogique
- Résumés automatiques
- Quiz générés
- Explications alternatives

## Offline
- PWA
- Cache local

## Versionning
- Historique modifications
- Rollback
- Diff HTML

## Marketplace
- Publication de cours
- Paiements Stripe

---

# ⚡ Performance

- HTML statique
- Lazy loading
- CDN
- Lighthouse > 90
- Temps < 1s

---

# 🔒 Sécurité (géré par Django)

Automatique :
- Protection XSS
- Protection CSRF
- Protection SQL injection
- Hash mots de passe sécurisé
- Permissions/Rôles
- Sessions sécurisées

---

# 📊 Analytics

- Temps par page
- Taux complétion
- Abandon
- Heatmaps
- Export CSV

---

# 🧪 Déploiement

- Docker
- Tests unitaires (pytest)
- Tests E2E (Playwright)
- Staging + Production
- Monitoring (Sentry)

---

# 🎯 Résumé technique

Tu codes principalement :
- Python (backend logique métier)
- TypeScript/React (UI)
- HTML/CSS (contenu cours)

Tu ne codes PAS :
- auth
- sécurité
- admin
- ORM
(car Django les fournit déjà)

---

# 📜 Licence
À définir
