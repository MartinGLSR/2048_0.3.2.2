"""
Auteur      :Martin Glauser
Date        :03.02.2023
Version     :0.3.3
Description  :Création du jeu 2048 en tkinter
"""
# moduls
from tkinter import *
from random import *
from tkinter.messagebox import *
import platform
import copy
import os

# constants
table_color = "#555555"
colors = {"0": "#777777", "2": "#8a8add", "4": "#7979ff", "8": "#1070e0", "16": "#005ded", "32": "#5a17cd", "64": "#7a19e1", "128": "#8a19e1", "256": "#9011CE", "512": "#9000A5", "1024": "#B10A75", "2048": "#D00060", "4096": "#F01070", "8192": "#FF7700"}
colors_next_case = {"2": "red", "4": "red"}
# tableau logique
table = [[1024, 0, 0, 0],
         [0, 0, 1024, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]

# tableau visuel
button_case = [[None, None, None, None],
               [None, None, None, None],
               [None, None, None, None],
               [None, None, None, None]]

background = "#222222"
font_color = "#ffffff"
active_font_color = "#fafafa"
font_family = ""
# paramétrer la police en fonction de l'OS
if platform.system() == "Ubuntu":
    font_family = "Ubuntu"
else:
    font_family = "Arial Rouded HD Blod"
font_settings = (font_family, 30)
font_settings_score = (font_family, 20)
best_score_folder = open("best_score.txt", "r+")
# variables
game_over = False
if_new_case_color = True
str_case_number = ""
score = 0
next_case = [0, 0]
color_case = ""
win = 0
# functions

# fonction pour faire apparaitre une messagebox en cas de victoire

def Win_screen():
    if askyesno("","Vous avez gagné \n Continuer ?"):
        print("continuer")
    else:
        window.quit()
# fonction pour mettre à jour les couleurs de fond
def refresh_ground():
    frame_text.config(bg=background)
    frame_score.config(bg=background)
    label_score.config(bg=background)
    label_title.config(bg=background)
    label_best_score.config(bg=background)
    button_setting.config(bg=background)
    window.config(bg=background)

# fonction permetant de réinitialiser les meilleur score
def reboot_best_score():
    if askyesno("", "Voulez vous vraiment réinitialiser votre meilleur score"):
        with open(r"best_score.txt", 'w') as folder:
                folder.write("0")
                folder.close()
        display()
# cette fonction permet d'afficher une fenêtre pour les paramêtres
def Settings_box():
    global swindows
    try:
        swindows.destroy()
    except:
        swindows = Tk()
        swindows.geometry("300x500")
        swindows.iconbitmap("settings-10-32.ico")
        swindows.config(bg=background)
        swindows.title("settings")
        frame_reboot_score = Frame(swindows)
        frame_reboot_score.pack()
        button_reboot_score = Button(frame_reboot_score, text="réinitialiser le meilleur score", background=background, activebackground=background, bd=0, foreground=font_color, activeforeground=font_color, command=reboot_best_score)
        button_reboot_score.pack()
        swindows.mainloop()

# fonction pour afficher un message de fin
def end_window():
    global colors, colors_next_case, background, game_over, table, score
    if askyesno("","Vous avez fini. \n recommencer?"):
        colors = {"0": "#777777", "2": "#8a8add", "4": "#7979ff", "8": "#1070e0", "16": "#005ded", "32": "#5a17cd", "64": "#7a19e1", "128": "#8a19e1", "256": "#9011CE", "512": "#9000A5", "1024": "#B10A75", "2048": "#D00060", "4096": "#F01070", "8192": "#FF7700"}
        colors_next_case = {"2": "red", "4": "red"}
        background = "#222222"
        game_over = False
        table = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        refresh_ground()
        reload_table()
        display()

    else:
        exit()
# fonction pour mettre à jour les couleurs de fin
def end_screen():
    global colors, background, colors_next_case
    colors = {"0": "#aaaaaa", "2": "#aaaaaa", "4": "#aaaaaa", "8": "#aaaaaa", "16": "#aaaaaa", "32": "#aaaaaa", "64": "#aaaaaa", "128": "#aaaaaa", "256": "#aaaaaa", "512": "#aaaaaa", "1024": "#aaaaaa", "2048": "#aaaaaa", "4096": "#aaaaaa", "8192": "#aaaaaa"}
    background = "#666666"
    colors_next_case = {"2": "#aaaaaa", "4": "#aaaaaa"}

#calcule si les cases d'un tableau sont les mêmes
def Get_if_same(table_memory):
    global game_over
    for i in range(4):
        for j in range(len(table_memory) - 1):
            if table_memory[i][j] == table_memory[i][j + 1]:
                game_over = False

# vérifie s'il y a un mouvement possible
def Get_if_end(table):
    global game_over
    game_over = True
    # vérification horizontale
    table_memory = copy.deepcopy(table)
    Get_if_same(table_memory)
    # vérification verticale
    table_memory = [[], [], [], []]
    for i in range(4):
        for j in range(4):
            table_memory[i].append(table[j][i])
    Get_if_same(table_memory)
    if game_over:
        end_screen()
def reload_table():
    global table, score
    for x in range(2):
        new_case_variable = New_case([], table)
        table = new_case_variable[0]
    score = 0
def Get_key(event):
    if event.keysym in ["Left", "Right", "Up", "Down", "a", "w", "s", "d"]:
        tour(event)
    elif event.keysym == "Escape":
        if askyesno("","êtes vous sûr de vouloir quitter ?"):
            exit()

# fonction pour tasser dans tous les senses
def Tass(sense, score, table_memory, table):
    global win
    for i in range(4):
        list_cases = []
        if sense == "Right" or sense == "Left":
            list_cases = table[i]
        if sense == "Up" or sense == "Down":
            for j in range(4):
                list_cases.append(table[j][i])
        # enlever les 0
        for k in range(4):
            if 0 in list_cases:
                list_cases.remove(0)
        # fusionner les cases si besoins
        if sense == "Right" or sense == "Down":
            list_cases.reverse()
        for k in range(len(list_cases) - 1):
            if list_cases[k] == list_cases[k + 1]:
                list_cases[k + 1] = 0
                list_cases[k] = list_cases[k] * 2
                if list_cases[k] == 2048:
                    win += 1
                score += list_cases[k] * 2
        if sense == "Right" or sense == "Down":
            list_cases.reverse()
        for k in range(len(list_cases)):
            if 0 in list_cases:
                list_cases.remove(0)
        if sense == "Left" or sense == "Up":
            list_cases = tass_4(list_cases)
        if sense == "Right" or sense == "Down":
            list_cases.reverse()
            list_cases = tass_4(list_cases)
            list_cases.reverse()
        # ajouter la ligne au tableau en mémoire
        if sense == "Right" or sense == "Left":
            table_memory.append(list_cases)
        if sense == "Up" or sense == "Down":
            for m in range(4):
                table_memory[m].append(list_cases[m])
    return table_memory, score

# fonction pour faire apparaître une nouvelle case
def New_case(table_base, table_memory):
    free_cases_x = []
    free_cases_y = []
    not_free_cases = False
    if table_base != table_memory:
        for x in range(4):
            for y in range(4):
                if table_memory[x][y] == 0:
                    free_cases_x.append(x)
                    free_cases_y.append(y)
        random_number = randint(0, len(free_cases_x) - 1)
        random_number2 = randint(0, 10)
        if len(free_cases_x) == 1:
            not_free_cases = True
        if random_number2 != 10:
            table_memory[free_cases_x[random_number]][free_cases_y[random_number]] = 2
        else:
            table_memory[free_cases_x[random_number]][free_cases_y[random_number]] = 4
        next_case = [free_cases_x[random_number], free_cases_y[random_number]]
    else:
        next_case = [10,10]
    return table_memory, next_case, not_free_cases

# fonction pour afficher le tableau et les scores
def display():
    global win
    for x in range(4):
        for y in range(4):
            if table[x][y] == 0:
                str_case_number = ""
                color_case = colors[str(table[x][y])]
            else:
                str_case_number = str(table[x][y])
                color_case = colors[str(table[x][y])]
                if x == next_case[0] and y == next_case[1]:
                    str_case_number = str(table[x][y])
                    color_case = colors_next_case[str(table[x][y])]
            button_case[x][y].config(text=str_case_number,activebackground=color_case, bg=color_case)
    label_score.config(text=f"score:{str(score)}")
    with open("best_score.txt", 'r') as folder:
        label_best_score.config(text=f"meilleur score:{folder.read()}")
        folder.close()
    if win == 1:
        Win_screen()
        win += 1
    if game_over:
        end_window()

# fonction pour enlever les 0
def tass_4(list_c):
    for k in range(4 - len(list_c)):
        list_c.append(0)
    return list_c

# fonction globale d'action l'or d'un mouvement
def tour(event):
    # définition des variables
    global table, score, next_case
    sense = ""
    table_memory = []
    table_base = []
    lst = []
    for i in range(4):
        for j in range(4):
            nb = int(table[i][j])
            lst.append(nb)
        table_base.append(lst)
        lst = []
    # definir la direction selont les touches
    if event.keysym == "Left" or event.keysym == "a":
        sense = "Left"
    elif event.keysym == "Right" or event.keysym == "d":
        sense = "Right"
    elif event.keysym == "Up" or event.keysym == "w":
        sense = "Up"
        table_memory = [[], [], [], []]
    elif event.keysym == "Down" or event.keysym == "s":
        sense = "Down"
        table_memory = [[], [], [], []]
    # ajouter les valeurs du tableau à la liste list_case
    tass_variable = Tass(sense, score, table_memory, table)
    table_memory = tass_variable[0]
    score = tass_variable[1]
    # ajouter une cases aléatoirement aux endroits vides
    new_case_variable = New_case(table_base, table_memory)
    table = new_case_variable[0]
    next_case = new_case_variable[1]
    if new_case_variable[2]:
        Get_if_end(table)
    # ajouter et charger les modifications au tableau
    table = table_memory
    with open(r"best_score.txt", 'r') as folder:
        if score > int(folder.read()):
            folder.close()
            with open(r"best_score.txt", 'w') as folder:
                    folder.write(str(score))
                    folder.close()
    display()
# ajout des deux premières cases
reload_table()
# window structure
window = Tk()
window.title("2048")
window.configure(bg=background)
window.geometry("850x850")
frame_text = Frame(window, bg=background)
frame_text.pack(fill=BOTH, expand=True)
frame_table = Frame(window, bg=table_color, bd=5)
frame_table.pack(padx=15, pady=15)
frame_score = Frame(frame_text, bg=background)
frame_score.pack(side=RIGHT, fill=Y)
label_title = Label(frame_text, text="2048", fg="white", bg=background, font=font_settings)
label_title.pack(side=LEFT, padx=60)
label_score = Label(frame_score, text=f"score:{score}", fg="white", bg=background, font=font_settings_score)
label_score.pack(side=LEFT, padx=30)
setting_icon = PhotoImage(file="settings-10-64.png")
button_setting = Button(frame_score, image=setting_icon, background=background, bd=0, activebackground=background, command=Settings_box)
button_setting.pack(side=RIGHT, padx=30)
# définition des scores
with open("best_score.txt", 'r') as folder:
    label_best_score = Label(frame_score, text=f"meilleur score:{folder.read()}", fg="white", bg=background, font=font_settings_score)
    label_best_score.pack(side=RIGHT, padx=30)
    folder.close()
for x in range(4):
    for y in range(4):
        if table[x][y] == 0:
            str_case_number = ""
        else:
            str_case_number = str(table[x][y])
        button_case[x][y] = Button(frame_table, bg=colors[str(table[x][y])], width=4, height=2, text=str_case_number,
                             font=("Ubuntu", 40), fg="white",
                             activebackground=colors[str(table[x][y])], activeforeground="white", bd=0)
        button_case[x][y].grid(row=x, column=y, padx=4, pady=4)
# key events
window.bind_all("<Key>", Get_key)
window.mainloop()
# TODO
# ajouter l'apparition aléatoire des 4                                                              fait
# ajouter la les meilleurs scores                                                                   fait
# aficher la case qui vient d'apparaître                                                            fait
# ajouter des paramètres                                                                            fait
# aficher un écran de fin lorsque il n'y a plus de possibilités ou que le joueur a ateint 8192      fait
# optionnel:
#   ajouter une annimation de déplacement                                                           à faire
#   ajouter des coins arrondis aux cases                                                            à faire
