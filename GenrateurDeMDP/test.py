import tkinter as tk


def show_toast(message, duration=3000):
    """ Affiche un toast message dans une fenêtre Tkinter """
    toast = tk.Toplevel()
    toast.overrideredirect(True)  # Supprime la barre de titre
    toast.attributes('-topmost', True)  # Toujours au premier plan

    # Obtenir la position de l'écran
    screen_width = toast.winfo_screenwidth()
    screen_height = toast.winfo_screenheight()

    # Définir la taille et la position du toast (en bas au centre)
    toast_width = 250
    toast_height = 50
    x_position = (screen_width - toast_width) // 2
    y_position = screen_height - toast_height - 50  # 50px du bas

    toast.geometry(f"{toast_width}x{toast_height}+{x_position}+{y_position}")

    # Ajouter un label avec le message
    label = tk.Label(toast, text=message, bg="white", fg="black", padx=10, pady=5)
    label.pack(expand=True, fill='both')
    # Fermer automatiquement après `duration` millisecondes
    toast.after(duration, toast.destroy)

    return toast


# Exemple d'utilisation
root = tk.Tk()
root.withdraw()  # Masquer la fenêtre principale

show_toast("Action effectuée avec succès !")

root.mainloop()
