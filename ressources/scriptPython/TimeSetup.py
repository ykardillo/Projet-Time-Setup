import paramiko
import ntplib
import progressbar
import os

from scp import SCPClient
from time import sleep
from time import ctime
from termcolor import colored

#Variables globales
username = "user0"
password = "user0"
root_password = "Labo503"
adressIpFilepath = "ressources/src/ipAdresses"
scriptNtp = "ressources/src/scriptNtp"




#Cette fonction récupére l'heure local via NTP
def setupTime():
    try:
        c = ntplib.NTPClient()
        response = c.request('pool.ntp.org', version=3)
        ts = ctime(response.tx_time)
        liste = ts.split(' ')
        return "\""+liste[3]+' '+liste[1]+' '+liste[5]+' '+liste[4]+"\""
    except:
        print(colored("\nErreur :",'red')+" Impossible de récupérer l'heure avec le protocole NTP")
        exit()
    

    
#Récupération de l'heure local via NTP
heure = setupTime()


#Cette fonction crée un crone et le répend dans les différentes machines 
def configuration():
    
    #Modification du script ntp en y ajoutant le bon root password
    f = open(scriptNtp,"w+")
    f.write("#!/bin/bash\n\necho \""+root_password+"\" | sudo -S service ntpd stop\necho \""+root_password+"\" | sudo -S ntpdate be.pool.ntp.org\necho \""+root_password+"\" | sudo -S service ntpd start")
    f.close()
    
    
    with open(adressIpFilepath) as fd:
        lines = fd.read().splitlines()
        for line in lines:
            try:
                #Connexion au clients
                print("\nConnexion à : "+line+"...")
                bar = progressbar.ProgressBar(maxval=10, \
                    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
                bar.start()
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname = line, username = username, password = password)
                
                #Affichage de la bar de chargement
                for i in range(10):
                    bar.update(i+1)
                    sleep(0.1)
                bar.finish()
                
                #Envoi du fichier scriptNtp
                scp = SCPClient(ssh_client.get_transport())
                scp.put('ressources/src/scriptNtp')
                scp.close()
                
                #Ajout de la tache de syncronisation de l'heure au crontab des différentes machines
                transport = ssh_client.get_transport()
                session = transport.open_session()
                session.set_combine_stderr(True)
                session.get_pty()
                
                #session.exec_command("echo \"40 8 * * * ./scriptNtp\" | crontab -")
                session.exec_command("echo \"* * * * * ./scriptNtp\" | crontab -")
                
                print(colored("SYNCRONISATION DE L'HEURE EFFECTUEE",'green'))
            except:
                print(colored("\nErreur :",'red')+" Connexion échoué avec la machine "+line)


#Cette fonction se connecte en ssh au différentes machines et règle l'heure de ceux-ci.
def broadcast():
    with open(adressIpFilepath) as fd:
        lines = fd.read().splitlines()
        for line in lines:
            try:
                #Connexion au clients
                print("\nConnexion à : "+line+"...")
                bar = progressbar.ProgressBar(maxval=10, \
                    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
                bar.start()
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname = line, username = username, password = password)
                for i in range(10):
                    bar.update(i+1)
                    sleep(0.1)
                bar.finish()
                
                print(colored("Connexion établie\n",'green'))
                
                transport = ssh_client.get_transport()
                session = transport.open_session()
                session.set_combine_stderr(True)
                session.get_pty()
                
                #Lancement des commandes
                heure = setupTime()
                session.exec_command("sudo date -s "+heure)
                stdin = session.makefile('wb', -1)
                stdout = session.makefile('rb', -1)
                
                #Ecrit le password root
                stdin.write(root_password +'\n')
                stdin.flush()
                print(colored("SYNCRONISATION DE L'HEURE EFFECTUEE",'green'))
                #Affichage de la console client
                #for lines in stdout.read().splitlines(): 
                    #print('%s' % lines)
            except:
                print(colored("\nErreur :",'red')+" Connexion échoué avec la machine "+line)
                



#Cette fonction  affiche l'aide de l'application.
def displayHelp():
    print('\033[1m' + "\nNAME" + '\033[0m' + "\n\t timesetup - the stupid hour manager\n\n\t clear - clear the terminal screen ")
    print('\033[1m' + "\nSYNOPSIS" + '\033[0m' + "\n\t "+'\033[4m'+"timesetup"+'\033[0m'+" [-b] [--broadcast] [-c] [--configure] [-h] [--help] [-e] [--exit]\n\n\t "+'\033[4m'+"clear"+'\033[0m')
    print('\033[1m'+"\nOPTIONS"+'\033[0m')
    print("\t-b, --broadcast\n\t   Règle l’heure de toutes les machines du serveur, dont l'adresse IP se trouve dans le fichier \"ipAdresses\" à partir de votre machine.\n")
    print("\t-c, --configure\n\t   Ajoute un script qui règle l'heure sur chaque machines du serveur, dont l'adresse IP se trouve dans le fichier \"ipAdresses\" à partir de votre machine afin qu'un "+'\033[1m'+"Cron"+'\033[0m'+" se lance chaque jour à 8:45.\n")
    print("\t-h, --help\n\t   Afficher l'aide.\n")
    print("\t-e, --exit\n\t   Quitter.")
    print('\033[1m' + "\nAUTHORS" + '\033[0m' + "\n\t42933 Achetouan Mohammed.\n\t45682 Kardillo Younes.")








#Cette fonction affiche le nom du projet avec style.
def displayTitle():
    print("\n")
    print(colored("  ______                _____      __ ",'yellow'))
    print(colored(" /_  __(_)___ ___  ___ / ___/___  / /___  ______ ",'yellow'))
    print(colored("  / / / / __ `__ \\/ _ \\__ \\ / _ \\/ __/ / / / __ \\ ",'yellow'))
    print(colored(" / / / / / / / / /  __/__/ /  __/ /_/ /_/ / /_/ /  ",'yellow'))
    print(colored("/_/ /_/_/ /_/ /_/\\___/____/\\___/\\__/\\__,_/ .___/ ",'yellow'))
    print(colored("                                        /_/  ",'yellow'))

#Cette fonction permet de vider le terminal.
def clear():
    os.system('clear')
    

#Cette fonction lance l'application et demande à l'utlisateur quelle méthode il souhaite utiliser.
def main():
    displayTitle()
    while True:
        heure = setupTime()
        value = input(colored("\nHeure BE: ",'yellow')+ heure + " > ")
        if (value == "timesetup -b" or value == "timesetup --broadcast" ):
            print(colored("\nEnvoi en broadcast...\n",'cyan')) 
            broadcast()
            
        elif(value == "timesetup -c" or value == "timesetup --configure" ):
            print(colored("\nConfiguration sur chaque clients\n",'cyan'))
            configuration()
            
        elif(value == "timesetup -h" or value == "timesetup --help" ):
            clear()
            displayHelp()
            
        elif(value == "clear"):
            clear()
            
        elif (value == "timesetup -e" or value == "timesetup --exit" ):
            print(colored("\nDéconnexion...",'red'))
            break
        else:
            print(colored("\nErreur :",'red')+" '"+value+"': n'est pas une commande timesetup. Voir 'timesetup --help'")

    print("\n")



#Lancement du main
main()
exit()


