import csv
import socket
import os
import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

PORT = 8080
FILENAME = "fiche_presence.csv"
dir_path = "/home/erwan"
file_path = os.path.join(dir_path, FILENAME)
email_addr = "erwan.bouvart@gmail.com"
email_password = "Auvers950"

os.makedirs(dir_path, exist_ok=True)

# Créer un socket serveur
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("", PORT))


# Fonction pour envoyer le fichier par mail
def send_email():
    # Créer le message email
    msg = MIMEMultipart()
    msg['From'] = email_addr
    msg['To'] = email_addr
    msg['Subject'] = "Fiche de présence"

    # Ajouter le fichier en pièce jointe
    with open(file_path, "rb") as f:
        attach = MIMEApplication(f.read(), _subtype="csv")
        attach.add_header('Content-Disposition', 'attachment', filename=str(FILENAME))
        msg.attach(attach)

    # Connexion au serveur SMTP et envoi du mail
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('erwan.bouvart@gmail.com', 'Auvers950')
    text = msg.as_string()
    server.sendmail('erwan.bouvart@gmail.com', 'erwan.bouvart@gmail.com', text)
    server.quit()
    #with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
     #   smtp.login(email_addr, email_password)
      #  smtp.send_message(msg)


# Fonction pour démarrer le serveur
def start_server():
    # Ouvrir le socket serveur
    server_socket.listen(1)
    print("Le serveur est en écoute...")
    file_exists = False
    try:
        with open(FILENAME, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row == ["Adresse IP", "Nom", "Prénom", "Présence", "Filière", "Classe"]:
                    file_exists = True
                    break
    except FileNotFoundError:
        pass

    # Ouvrir le fichier CSV en mode append
    with open(FILENAME, "a", newline='') as f:
        writer = csv.writer(f)
        # Écrire les en-têtes de colonne
        if file_exists == False :
            writer.writerow(["Adresse IP", "Nom", "Prénom", "Présence", "Filière", "Classe"])

        while True:
            # Attendre les connexions entrantes
            client_socket, client_address = server_socket.accept()
            print(f"Adresse IP du client : {client_address[0]}")

            # Lire les données envoyées par le client
            data = client_socket.recv(1024).decode()
            print(f"Données de présence reçues : {data}")

            # Diviser les données en champs
            fields = data.split()
            for i in fields :
                print(i)

            # Écrire les données dans le fichier CSV
            writer.writerow([client_address[0], fields[0], fields[1], fields[2], "INEM", "ING 3"])
            print(f"Données de présence écrites dans le fichier {FILENAME}")

            # Envoyer une réponse de confirmation au client
            ack = b"OK"
            client_socket.send(ack)
            print(f"Réponse envoyée au client : {ack.decode()}")

            # Fermer la connexion avec le client
            #send_email()
            client_socket.close()


# Fonction pour fermer le serveur
def stop_server():
    # Fermer le socket serveur
    server_socket.close()

    # Supprimer le fichier de fiche de présence
    os.remove(file_path)


start_server()

# Planifier l'exécution du serveur de 9h à 12h et de 14h à 18h
#schedule.every().day.at("22:47").do(start_server)
#schedule.every().day.at("22:50").do(stop_server)
#schedule.every().day.at("12:00").do(stop_server)
#schedule.every().day.at("14:58").do(start_server)
#schedule.every().day.at("15:00").do(send_email)
#schedule.every().day.at("15:00").do(stop_server)
