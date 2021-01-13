# Projet SYSG5 : Time Setup

Application permettant de régler l’heure de diﬀérentes machines se trouvant dans un même réseau en utilisant le protocole «NTP». 

## Installation de l'environnement virtuel Python3.6.3

Installer les diﬀérentes dépendances

`./installationPython`

## Activation de l'environnement installé

Activer l'environnement

`source ~/pythonsProjet-SysG5_TimeSetup/python3.6.3/bin/activate`


## Modification des différentes adresses IP

Insérer les adresses IP des machines du serveur dans le fichier "ipAdresses" sans préciser celle de la machine qui va lancer le script 

## Lancement de l'application

Lancer l'application

`python ressources/scriptPython/TimeSetup.py`

## Usage

### Envoie par broadcast

Lorsque vous entrez la commande suivante:
`timesetup -b`
ou
`timesetup --broadcast`
Vous réglerez l’heure de toutes les machines du serveur, dont l'adresse IP se trouve dans le fichier *__ressources/src/ipAdresses__* à partir de votre machine.

### Configuration sur chaque client

Lorsque vous entrez la commande suivante:
`timesetup -c`
ou
`timesetup --configure`
Vous ajoutez un script qui règle l'heure sur chaque machines du serveur, dont l'adresse IP se trouve dans le fichier *__ressources/src/ipAdresses__* afin qu'un **Cron** se lance chaque jour à 8:45.
### Vider l'affichage
Pour vider l'invite de commande:
`clear`

### Quitter l'application 

Pour quitter l'application, il vous suffit de taper la commande suivante:
`timesetup -e`
ou
`timesetup --exit`
