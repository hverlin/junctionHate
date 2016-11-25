# Installation Simonetti

## Introduction 

Ce document présente le déroulement de l'installation de l'application de pointage.

L'application est composée de deux parties.

- simonetti-backend (serveur Django)
- simonetti-frontend (frontend Angular2)

## Avant de commencer

Ce tutoriel a été fait pour ubuntu 16.04, avec la configuration par défaut.
(testé dans un conteneur LXD). Merci d'adapter les étapes ci-dessous en fonction des caractéristiques du serveur.

Les choses suivantes sont supposées dans le reste du document:
 - username : **simonetti**
 - url frontend : **pointage.simonetti.fr**
 - url backend : **api.pointage.simonetti.fr**
 
## Installation du Back-end

### Installation des dépendances

Libre office est nécessaire pour la génération des des pdfs.

```
sudo add-apt-repository ppa:libreoffice/ppa
sudo apt-get update
sudo apt-get -y install libreoffice 
```

L'application a été testée avec **postgresql 9.5**.
(Il est fort probable qu'elle fonctionne avec mysql ou sqllite)
```
sudo apt-get install -y postgresql-9.5 postgresql-contrib-9.5
sudo apt-get install -y postgresql-doc-9.5 postgresql-server-dev-9.5 nginx
```

**Python** est nécessaire pour faire tourner le serveur
```
sudo apt-get install -y python3 python3-pip python-dev python3-dev python-pip virtualenvwrapper
```

**Git** est également nécessaire pour télécharger le code source.

**Attention** : Bien redémarré le shell pour que l'installation de virtualenvwrapper soit prise en compte.
(initialisation des variables d'environement)

### Mise en place de la base de données
```
sudo -u postgres createuser simonetti
sudo -u postgres createdb simonetti -O simonetti
```

Il faut ensuite changer le mot de passe de l'utilisateur **simonetti** via ``psql``:

```
psql
\password simonetti
```

### Mise en place de l'environement python

Installation du pack locale fr_utf8 avec cette commande. Sélectionnner **fr_FR.utf8**. 
```
sudo dpkg-reconfigure locales
```

Téléchargement du code

```
cd ~
git clone https://gitlab.com/hverlin/simonetti-backend simonetti-backend
cd simonetti-backend
```

Créer un nouvel environnement nommé **simonetti**.
```
mkvirtualenv -p /usr/bin/python3.5 simonetti
```

La suite de la documentation suppose que vous travailler dans l'environnement **simonetti**.
Taper la ligne suivante si ce n'est pas le cas :
```
workon simonetti
```

Installer les dépendances pythons
```
pip install -r requirements.txt
```

Ensuite, il faut copier le fichier ``settings_local.template.py`` et créer un fichier nommé ``settings_local.py``.
```
cp junction_hate/settings_local.template.py settings_local.py
```

Vous devez ensuite compléter le fichier ``settings_local.py`` avec vos paramètres :
```
DEBUG=False

SECRET_KEY = 'CHANGER LA CLEF SECRETE'

# PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'simonetti',
        'HOST': 'localhost',
        'PASSWORD': 'simonetti',
        'PORT': '5432',
        'USER': 'simonetti',
    }
}

ALLOWED_HOSTS = ["api.pointage.simonetti.fr", "pointage.simonetti.fr"]

# Configuration du serveur email
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'email@gmail.com'
EMAIL_HOST_PASSWORD = 'password'
```

Initialiser la base de données
```
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
```

Il faut ensuite créer un administrateur. Cela se fait avec la commande suivante. 
L'username permet de se connecter au site ensuite.
**Mettre une adresse mail valide en tant que nom d'utilisateur.**
```
python manage.py createsuperuser
```

Vous devez ensuite vous assurer que tout fonctionne
```
workon simonetti
python manage.py runserver 0.0.0.0:8000
```
Il doit alors etre possible de voir la page d'accueil de l'api à ``ipduserveur:8000``. 
(le pare-feu étant configuré correctement au préalable)
Le serveur est alors configuré en mode développement et sera configuré pour la production ensuite.

## Installation du front-end

### Téléchargement du code
```
cd ~
git clone https://gitlab.com/hverlin/simonetti-frontend.git simonetti-frontend
cd simonetti-frontend
```

### Paramètres

Il est nécessaire de changer l'url de l'api avec celle utilisée par votre serveur.
```
vi src/app/shared/config.ts 
```

### Build de production
Il est nécessaire d'avoir nodejs > v.6 installé.
Pour cela la méthode la plus simple est d'utiliser **nvm** qui sert à gérer les versions de node.

```
wget -qO- https://raw.githubusercontent.com/creationix/nvm/v0.31.4/install.sh | bash
```

Les commandes suivantes installent node et les dépendances nécessaires au build.
```
nvm install
nvm use

# dependances globales
npm install typings webpack-dev-server rimraf webpack -g
npm install

# build du code de production
npm run build:prod
```


## Mise en production

La mise production consiste à installer et configurer **nginx** et **gunicorn**.

### Création d'un service pour Gunicorn

La première chose consiste à créer un fichier qui permettra de gérer le service gunicorn.

```
sudo vi /etc/systemd/system/gunicorn.service
```

Voici le contenu du fichier à adapter :
```
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=simonetti
Group=www-data
WorkingDirectory=/home/simonetti/simonetti-backend
ExecStart=/home/simonetti/.virtualenvs/simonetti/bin/gunicorn --workers 3 --bind unix:/home/simonetti/simonetti-backend/junction_hate.sock junction_hate.wsgi:application

[Install]
WantedBy=multi-user.target
```

Ensuite, il faut s'assurer que le dossier contenant le socket est éxécutable.
```
chmod +x /home/simonetti/ /home/simonetti/simonetti-backend/
chmod g+s /home/simonetti/simonetti-backend/
```


Enfin, il suffit d'éxécuter les commandes suivantes pour lancer et activer le service gunicorn au démarrage.
```
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

### Configuration de nginx en proxy pour gunicorn



Configuration de nginx en proxy pour gunicorn
```
sudo vi /etc/nginx/sites-available/simonetti-backend
```

```
server {
	listen 80 ;
	listen [::]:80 ;

	server_name .api.pointage.simonetti.fr;

    location = /favicon.ico { access_log off; log_not_found off; }
	
	location /static/ {
	    root /home/simonetti/simonetti-backend;
	}

        location / {
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
	        proxy_pass http://unix:/home/simonetti/simonetti-backend/junction_hate.sock; 
       }
}
```

Configuration de nginx pour servir le front-end :
```
sudo vi /etc/nginx/sites-available/simonetti-frontend
```

```
server {
	listen 80;
	listen [::]:80;

	server_name pointage.simonetti.fr;

	location / {
	    root /home/simonetti/simonetti-frontend/dist;
	}
}
```

```
sudo ln -s /etc/nginx/sites-available/simonetti-backend /etc/nginx/sites-enabled
sudo ln -s /etc/nginx/sites-available/simonetti-frontend /etc/nginx/sites-enabled
```


Tester la configuration avec :
```
sudo nginx -t
```

S'il n'y a pas d'erreur, il est alors possible de redémarrer nginx :
```
sudo systemctl restart nginx
```

Si votre serveur DNS est configuré correctement, vous devriez avoir une application fonctionnelle. 
Pour plus de sécurité, et évitez l'envoi des mots en clair, il est recommandé d'utiliser **https** plutot que **http** pour communiquer avec le backend.

### Ajout de l'https

Il est également possible de configurer nginx pour servir le contenu en https.
Ceci peut se faire gratuitement avec **let's encrypt**.
Ce tutoriel est très complet si besoin :
 [secure nginx with let's encrypt](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-16-04)


# Interface Super Admin
Il est possible d'accéder à l'interface d'administration sur l'ensemble des objets de la base de données via l'url suivante :
```
http://api.pointage.simonetti.fr/admin
```

Cela permet de pouvoir supprimer définitevement certaines ressources de la base.


# Ajout de la liste des tâches
Il est possible d'ajouter un ensemble de tâches à l'aide d'un fichier csv.
Il suffit de se rendre à l'url suivante :
```
http://api.pointage.simonetti.fr/csv/upload/
```

Un fichier d'exemple est disponible à la racine du projet. Attention de bien respecté la structure suivante :
```
categorie,sous_categorie,code,designation,unite,pu
Menuiserie Intérieure,Divers,TP00,tarif de pose chantier,U,12
```