from tkinter import *
from tkinter.filedialog import askopenfilename,asksaveasfilename
from math import sqrt

def raccourci_fermeture(event) : fermeture()
def fermeture() : fenetre.destroy()

def raccourci_open_file(event) : open_file()
def open_file() :
    global grille
    global taille
    rep = askopenfilename(title="Ouvrir un fichier",filetypes=[('text files','.txt')])
    if rep != "" :
        f = open(rep,"r")
        grille = f.read().split(",")
        f.close()
        grille = [int(i) for i in grille]
        taille = int(sqrt(len(grille)))
    affich()

def raccourci_save_as(event) : save_as()
def save_as() :
    rep = asksaveasfilename(title="Enregistrer un fichier",filetypes=[('text files','.txt')],defaultextension=".txt")
    if rep != "" :
        f = open(rep,"w")
        l = [str(i) for i in grille]
        f.write(",".join(l))
        f.close()

def mouse_button_down(event) :
    global grille
    global iterations
    if 0 < event.x < 500 and 0 < event.y < 500 : grille[int((event.y//(500/taille))*taille+event.x//(500/taille))],iterations = int(outil.get()),0
    affich()

def key_down_return(event) :
    global taille
    try :
        taille = int(entree.get())
        crea_grille()
    except : a = 0

def key_down_return2(event) :
    global limite
    try : limite = int(entree2.get())
    except : a = 0

def key_down_return3(event) :
    global delai
    try : delai = int(entree3.get())
    except : a = 0

def change_compteur() :
    global compteur
    compteur = 1 if compteur == 0 else 0

def clear_compteur() :
    global iterations
    iterations = 0

def change_pause() :
    global pause
    global b_pause
    pause = 1 if pause == 0 else 0
    b_pause.destroy()
    b_pause = Button(cadre,text=[" | | "," > "][pause],command=change_pause)
    b_pause.pack(side=TOP,anchor="w",padx=5,pady=5)
    if pause == 0 : mouv()

def crea_grille() :
    global grille
    grille = [0 for i in range (taille**2)]
    affich()

def affich() :
    canvas.delete("all")
    [canvas.create_rectangle(j*(500/taille)+2,i*(500/taille)+2,(j+1)*(500/taille)+2,(i+1)*(500/taille)+2,fill="black",outline="black") for i in range (taille) for j in range (taille) if grille[i*taille+j] == 1]
    if compteur == 1 : canvas.create_text(250,10,text=str(iterations),font="Consolas 12",fill="purple")

def mouv() :
    global grille
    global taille
    global iterations
    if taille < limite and 1 in grille[:taille]+grille[taille**2-taille:]+[grille[i] for i in range (0,taille**2-taille,taille)]+[grille[i] for i in range (taille-1,taille**2,taille)] :
        for i in range (taille) :
            grille = grille[:i*(taille+2)]+[0]+grille[i*(taille+2):i*(taille+2)+taille]+[0]+grille[i*(taille+2)+taille:]
        grille = [0 for i in range (taille+2)]+grille+[0 for i in range (taille+2)]
        taille += 2
    l = []
    for i in range (taille**2) :
        total = 0
        if i > taille and i%taille != 1 and grille[i-taille-1] == 1 : total += 1
        if i > taille and grille[i-taille] == 1 : total += 1
        if i > taille and i%taille != taille-1 and grille[i-taille+1] == 1 : total += 1
        if i%taille != 1 and grille[i-1] == 1 : total += 1
        if i%taille != taille-1 and grille[i+1] == 1 : total += 1
        if i < taille**2-taille and i%taille != 1 and grille[i+taille-1] == 1 : total += 1
        if i < taille**2-taille and grille[i+taille] == 1 : total += 1
        if i < taille**2-taille and i%taille != taille-1 and grille[i+taille+1] == 1 : total += 1
        if grille[i] == 1 and total in [2,3] or grille[i] == 0 and total == 3 : l += [1]
        else : l += [0]
    grille = list(l)
    iterations += 1
    affich()
    if pause == 0 : canvas.after(delai,mouv)

fenetre = Tk()
fenetre.title("Le jeu de la Vie")
fenetre.resizable(width=False,height=False)

menubar = Menu(fenetre)
menu = Menu(menubar,tearoff=0)
menu.add_command(label="Ouvrir...",command=open_file,accelerator="Ctrl+o")
menu.add_command(label="Enregistrer sous...",command=save_as,accelerator="Ctrl+Shift+s")
menu.add_separator()
menu.add_command(label="Quitter",command=fermeture,accelerator="Alt+F4")
menubar.add_cascade(label="Fichier",menu=menu)
fenetre.bind("<Control-o>",raccourci_open_file)
fenetre.bind("<Control-Alt-s>",raccourci_save_as)
fenetre.bind("<Alt-F4>",raccourci_fermeture)

canvas = Canvas(fenetre,width=500,height=500,bg="white")
canvas.pack(side=LEFT,padx=5,pady=5)
canvas.bind("<Button-1>",mouse_button_down)
canvas.bind("<B1-Motion>",mouse_button_down)

cadre = LabelFrame(fenetre,text="",padx=5,pady=5,borderwidth=0)
cadre.pack(side=LEFT,fill="both",expand="no")

cadre2 = LabelFrame(cadre,text="Largeur de l'écran :",padx=5,pady=5)
cadre2.pack(side=TOP,fill="both",expand="no")
taille = 50
entree = Entry(cadre2,width=30)
entree.pack(side=TOP,anchor="w",padx=0,pady=0)
entree.bind("<Return>",key_down_return)

cadre3 = LabelFrame(cadre,text="Limite :",padx=5,pady=5)
cadre3.pack(side=TOP,fill="both",expand="no")
limite = 50
entree2 = Entry(cadre3,width=30)
entree2.pack(side=TOP,anchor="w",padx=0,pady=0)
entree2.bind("<Return>",key_down_return2)

cadre4 = LabelFrame(cadre,text="Outils :",padx=0,pady=0)
cadre4.pack(side=TOP,fill="both",expand="no")
outil = StringVar()
b_outil1,b_outil2,b_clear_ecran = Radiobutton(cadre4,text="Ajouter",variable=outil,value=1,state=ACTIVE).pack(side=LEFT,padx=0,pady=0),Radiobutton(cadre4,text="Retirer",variable=outil,value=0,state=ACTIVE).pack(side=LEFT,padx=0,pady=0),Button(cadre4,text=" X ",command=crea_grille).pack(side=LEFT,padx=5,pady=5)
outil.set("1")

cadre5 = LabelFrame(cadre,text="Compteur :",padx=0,pady=0)
cadre5.pack(side=TOP,fill="both",expand="no")
compteur,iterations = 0,0
b_compteur = Checkbutton(cadre5,text="Compteur d'itérations",command=change_compteur).pack(side=LEFT,padx=5,pady=5)
b_clear_compteur = Button(cadre5,text=" X ",command=clear_compteur).pack(side=LEFT,padx=5,pady=5)

cadre6 = LabelFrame(cadre,text="Délai entre chaque itération (en ms) :",padx=5,pady=5)
cadre6.pack(side=TOP,fill="both",expand="no")
delai = 100
entree3 = Entry(cadre6,width=30)
entree3.pack(side=TOP,anchor="w",padx=0,pady=0)
entree3.bind("<Return>",key_down_return3)

pause = 1
b_pause = Button(cadre,text=" > ",command=change_pause)
b_pause.pack(side=TOP,anchor="w",padx=5,pady=5)

crea_grille()

fenetre.config(menu=menubar)
fenetre.mainloop()