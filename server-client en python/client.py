import socket
import tkinter as tk

PORT = 8080
# adresse IP : 192.168.157.119
SERVER_IP = "127.0.0.1"
FILENAME = "liste_presence.txt"

# Créer une fenêtre Tkinter pour la pop-up
root = tk.Tk()

# Définir les widgets pour entrer le nom et le prénom
tk.Label(root, text="Nom :").grid(row=0)
tk.Label(root, text="Prénom :").grid(row=1)
nom_entry = tk.Entry(root)
prenom_entry = tk.Entry(root)
nom_entry.grid(row=0, column=1)
prenom_entry.grid(row=1, column=1)


def envoyer_presence():
    nom = nom_entry.get() + " " + prenom_entry.get()
    presence = "oui"

    # Créer un socket client
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Établir la connexion avec le serveur
    sock.connect((SERVER_IP, PORT))

    # Envoyer les données de présence au serveur
    buffer = f"{nom} {presence}".encode('utf-8')
    sock.sendall(buffer)
    print(f"Données de présence envoyées : {buffer.decode('utf-8')}")

    # Fermer la connexion
    sock.close()

    # Fermer la fenêtre Tkinter
    root.destroy()


# Définir le bouton pour envoyer les données de présence
tk.Button(root, text="Envoyer", command=envoyer_presence).grid(row=2, column=0, columnspan=2)

# Lancer la boucle principale Tkinter
root.mainloop()

