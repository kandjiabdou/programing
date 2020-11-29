from random import  randint
from tkinter import *
display = Tk()
display.title("Kandji")
display.minsize(400, 600)
display.maxsize(400, 600)
display.iconbitmap("klogo.ico")
display.config(background='#4C93E5')
titre = Frame(display, bd=5, relief=RAISED, width=100, height=20,)
titre.pack()
text1 = Label(titre, text="Jeu Threes", font=("Arial", 15), fg="black")
text1.pack()
#text2 = Label(titre, text="kandji", font=("Arial", 15), fg="black")
#text2.pack()

plateauFond = Frame(display, width=225, height=275, bd=3, bg="#41B87F", relief=SUNKEN)
plateauFond.pack()

def init_play():
    plateau={}
    plateau['n']=4
    # Le nombre de case libre au début est 16 évidement
    plateau['nb_case_libre']=16
    # Initialisation d'un tableau de 16 cases ayant des valeurs nulles
    table_init=[]
    i=0
    while i<16:
        table_init.append(0)
        i+=1
    plateau['tiles']=table_init
    return plateau

def is_game_over(plateau):
    if get_nb_empty_rooms(plateau)!=0:
        return False
    else:
        i=0
        while i<4:
            j=0
            while j<3:
                x=get_value(plateau,i,j)
                y=get_value(plateau,i,j+1)
                if (x==1 and y==2) or (x==2 and y==1):
                    return False
                elif x%3==0 and x==y:
                    return False
                j+=1
            i+=1
        i=0
        while i<4:
            j=0
            while j<3:
                x=get_value(plateau,j,i)
                y=get_value(plateau,j+1,i)
                if (x==1 and y==2) or (x==2 and y==1):
                    return False
                elif x%3==0 and x==y:
                    return False
                j+=1
            i+=1
    return True


def check_indice(plateau, indice):
    if indice >= 0 and indice <= plateau['n'] - 1:
        return True
    return False


def check_room(plateau, lig, col):
    if check_indice(plateau, lig) and check_indice(plateau, col):
        return True
    return False


def get_value(plateau, lig, col):
    assert check_room(plateau, lig, col), "La case est invalide"

    val = plateau['tiles'][4 * lig + col]
    return val


def set_value(plateau, lig, col, val):
    assert check_room(plateau, lig, col), "La case est invalide"
    assert val > 0, "Erreur sur la valeur"
    plateau['tiles'][4 * lig + col] = val
    nb = 0
    i = 0
    while i < 16:
        if plateau['tiles'][i] == 0:
            nb += 1
        i += 1
    plateau['nb_case_libre'] = nb


def is_room_empty(plateau, i, j):
    assert check_room(plateau, i, j), "La case est invalide"
    if get_value(plateau, i, j) == 0:
        return True
    return False


def get_nb_empty_rooms(plateau):
    # On parcours le tableau tiles et on compte le nombre de case contenant la valeur 0 à l'aide d'un variable nb
    nb = 0
    i = 0
    while i < 16:
        if plateau['tiles'][i] == 0:
            nb += 1
        i += 1
    plateau['nb_case_libre'] = nb
    return nb

def get_next_alea_tiles(plateau, mode):
    assert mode in ['init',
                    'encours'], "Deux modes sont possibles 'init' et 'encours' (voir commentaire de la fonction)"
    if mode == 'init':
        tableau = list(range(16))
        x = randint(0, 15)
        del (tableau[x])
        i = randint(0, 14)
        y = tableau[i]
        tile = {'mode': 'init',
                '0': {'val': 2, 'lig': x // 4, 'col': x % 4},
                '1': {'val': 1, 'lig': y // 4, 'col': y % 4},
                }
        tile['check'] = not is_game_over(plateau)
    else:
        tableau = []
        i = 0
        while i < 16:
            if plateau['tiles'][i] == 0:
                tableau.append(i)
            i += 1
        if len(tableau) != 0:
            indice = randint(0, len(tableau) - 1)
            x = tableau[indice]
            val = randint(1, 3)
            tile = {'mode': 'encours',
                    '0': {'val': val, 'lig': x // 4, 'col': x % 4},
                    }
            tile['check'] = not is_game_over(plateau)
        else:
            tile = {'mode': 'encours', }
            tile['check'] = not is_game_over(plateau)
    return tile


def put_next_tiles(plateau, tile):
    if tile['mode'] == 'init':
        set_value(plateau, tile['0']['lig'], tile['0']['col'], tile['0']['val'])
        set_value(plateau, tile['1']['lig'], tile['1']['col'], tile['1']['val'])
    elif tile['mode'] == 'encours' and len(tile) != 2:
        set_value(plateau, tile['0']['lig'], tile['0']['col'], tile['0']['val'])
    else:
        plateau = plateau


def line_pack(plateau, num_lig, debut, sens):
    assert check_room(plateau, num_lig, debut), "Erreur sur l'indice"
    assert sens in [0, 1], "le sens est incorrect (O et 1 valeurs possibles)"
    if sens == 1:
        i = debut
        while i < 3:
            plateau['tiles'][4 * num_lig + i] = plateau['tiles'][4 * num_lig + i + 1]
            i += 1
        plateau['tiles'][4 * num_lig + 3] = 0
    else:
        i = debut
        while i > 0:
            plateau['tiles'][4 * num_lig + i] = plateau['tiles'][4 * num_lig + i - 1]
            i -= 1
        plateau['tiles'][4 * num_lig] = 0


def colum_pack(plateau, num_col, debut, sens):
    assert check_room(plateau, num_col, debut), "Erreur sur l'indice"
    assert sens in [0, 1], "le sens est incorrect (O et 1 valeurs possibles)"
    if sens == 1:
        i = debut
        while i < 3:
            plateau['tiles'][4 * i + num_col] = plateau['tiles'][4 * i + num_col + 4]
            i += 1
        plateau['tiles'][12 + num_col] = 0
    else:
        i = debut
        while i > 0:
            plateau['tiles'][4 * i + num_col] = plateau['tiles'][4 * i + num_col - 4]
            i -= 1
        plateau['tiles'][num_col] = 0


def line_move(plateau, num_lig, sens):
    if sens == 1:
        debut = 0
        test = False
        while debut < 3 and test == False:
            x = get_value(plateau, num_lig, debut)
            y = get_value(plateau, num_lig, debut + 1)
            if is_room_empty(plateau, num_lig, debut):
                line_pack(plateau, num_lig, debut, 1)
                test = True
            elif (x == 2 and y == 1) or (x == 1 and y == 2):
                line_pack(plateau, num_lig, debut, 1)
                set_value(plateau, num_lig, debut, 3)
                test = True
            elif x % 3 == 0 and x == y:
                line_pack(plateau, num_lig, debut, 1)
                set_value(plateau, num_lig, debut, 2 * x)
                test = True
            debut += 1

    else:
        debut = 3
        test = False
        while debut > 0 and test == False:
            x = get_value(plateau, num_lig, debut)
            y = get_value(plateau, num_lig, debut - 1)
            if is_room_empty(plateau, num_lig, debut):
                line_pack(plateau, num_lig, debut, 0)
                test = True
            elif (x == 2 and y == 1) or (x == 1 and y == 2):
                line_pack(plateau, num_lig, debut, 0)
                set_value(plateau, num_lig, debut, 3)
                test = True
            elif x % 3 == 0 and x == y:
                line_pack(plateau, num_lig, debut, 0)
                set_value(plateau, num_lig, debut, 2 * x)
                test = True
            debut -= 1


def colum_move(plateau, num_col, sens):
    if sens == 1:
        debut = 0
        test = False
        while debut < 3 and test == False:
            x = get_value(plateau, debut, num_col)
            y = get_value(plateau, debut + 1, num_col)
            if is_room_empty(plateau, debut, num_col) == True:
                colum_pack(plateau, num_col, debut, 1)
                test = True
            elif (x == 2 and y == 1) or (x == 1 and y == 2):
                colum_pack(plateau, num_col, debut, 1)
                set_value(plateau, debut, num_col, 3)
                test = True
            elif x % 3 == 0 and x == y:
                colum_pack(plateau, num_col, debut, 1)
                set_value(plateau, debut, num_col, 2 * x)
                test = True
            debut += 1

    elif sens == 0:
        debut = 3
        test = False
        while debut > 0 and test == False:
            x = get_value(plateau, debut, num_col)
            y = get_value(plateau, debut - 1, num_col)
            if is_room_empty(plateau, debut, num_col) == True:
                colum_pack(plateau, num_col, debut, 0)
                test = True
            elif (x == 2 and y == 1) or (x == 1 and y == 2):
                colum_pack(plateau, num_col, debut, 0)
                set_value(plateau, debut, num_col, 3)
                test = True
            elif x % 3 == 0 and x == y:
                colum_pack(plateau, num_col, debut, 0)
                set_value(plateau, debut, num_col, 2 * x)
                test = True
            debut -= 1


def lines_move(plateau, sens):
    for i in range(4):
        line_move(plateau, i, sens)


def colums_move(plateau, sens):
    for i in range(4):
        colum_move(plateau, i, sens)


p = init_play()
tile = get_next_alea_tiles(p, 'init')
put_next_tiles(p, tile)

def debut_jeu():

    i = 0
    y = 2
    while i < 4:
        x = 2
        j = 0
        while j < 4:
            nb = get_value(p, i, j)
            couleur = "white"
            fond = "black"
            if nb == 1:
                couleur = "blue"
                fond = "white"
            elif nb == 2:
                couleur = "red"
                fond = "white"
            if nb == 0:
                nb = " "
                couleur = "#B0C4DE"
            case_0_0 = Frame(plateauFond, bd=10, bg="#41B87F")
            case_0_0.place(x=x, y=y)
            txt_0_0 = Label(case_0_0, text=nb, font=("Arial", 13), bd=5, width=3, height=2, relief=RAISED, fg=fond,
                            bg=couleur)
            txt_0_0.grid()
            x += 50
            j += 1
        y += 60
        i += 1

def ver_haut():
    colums_move(p,1)
    i=0
    y=2
    while i<4:
        x = 2
        j=0
        while j<4:
            nb=get_value(p,i,j)
            couleur="white"
            fond="black"
            if nb==1:
                couleur = "blue"
                fond="white"
            elif nb==2:
                couleur = "red"
                fond = "white"
            if nb==0:
                nb=" "
                couleur="#B0C4DE"
            case_0_0 = Frame(plateauFond, bd=10, bg="#41B87F")
            case_0_0.place(x=x, y=y)
            txt_0_0 = Label(case_0_0, text=nb, font=("Arial", 13), bd=5, width=3, height=2, relief=RAISED,fg=fond,bg=couleur)
            txt_0_0.grid()
            x+=50
            j+=1
        y+=60
        i+=1
    tile = get_next_alea_tiles(p, "encours")
    put_next_tiles(p, tile)

def ver_bas():
    colums_move(p,0)
    i=0
    y=2
    while i<4:
        x = 2
        j=0
        while j<4:
            nb=get_value(p,i,j)
            couleur="white"
            fond="black"
            if nb==1:
                couleur = "blue"
                fond="white"
            elif nb==2:
                couleur = "red"
                fond = "white"
            if nb==0:
                nb=" "
                couleur="#B0C4DE"
            case_0_0 = Frame(plateauFond, bd=10, bg="#41B87F")
            case_0_0.place(x=x, y=y)
            txt_0_0 = Label(case_0_0, text=nb, font=("Arial", 12), bd=5, width=3, height=2, relief=RAISED,fg=fond,bg=couleur)
            txt_0_0.grid()
            x+=50
            j+=1
        y+=60
        i+=1
    tile = get_next_alea_tiles(p, "encours")
    put_next_tiles(p, tile)

def vers_gauche():
    lines_move(p,1)
    i=0
    y=2
    while i<4:
        x = 2
        j=0
        while j<4:
            nb=get_value(p,i,j)
            couleur="white"
            fond="black"
            if nb==1:
                couleur = "blue"
                fond="white"
            elif nb==2:
                couleur = "red"
                fond = "white"
            if nb==0:
                nb=" "
                couleur="#B0C4DE"
            case_0_0 = Frame(plateauFond, bd=10, bg="#41B87F")
            case_0_0.place(x=x, y=y)
            txt_0_0 = Label(case_0_0, text=nb, font=("Arial", 13), bd=5, width=3, height=2, relief=RAISED,fg=fond,bg=couleur)
            txt_0_0.grid()
            x+=50
            j+=1
        y+=60
        i+=1
    tile = get_next_alea_tiles(p, "encours")
    put_next_tiles(p, tile)

def vers_droite():
    lines_move(p,0)
    i=0
    y=2
    while i<4:
        x = 2
        j=0
        while j<4:
            nb=get_value(p,i,j)
            couleur="white"
            fond="black"
            if nb==1:
                couleur = "blue"
                fond="white"
            elif nb==2:
                couleur = "red"
                fond = "white"
            if nb==0:
                nb=" "
                couleur="#B0C4DE"
            case_0_0 = Frame(plateauFond, bd=10, bg="#41B87F")
            case_0_0.place(x=x, y=y)
            txt_0_0 = Label(case_0_0, text=nb, font=("Arial", 13), bd=5, width=3, height=2, relief=RAISED,fg=fond,bg=couleur)
            txt_0_0.grid()
            x+=50
            j+=1
        y+=60
        i+=1
    tile = get_next_alea_tiles(p, "encours")
    put_next_tiles(p, tile)



fleche1=PhotoImage(file="haut.png")
framebtn1=Frame(display,bd=5,bg="#41B87F",relief=RAISED)
framebtn1.place(x=175,y=390)
btn1=Button(framebtn1,image=fleche1,command=ver_haut)
btn1.grid()

fleche2=PhotoImage(file="bas.png")
framebtn2=Frame(display,bd=5,bg="#41B87F",relief=RAISED)
framebtn2.place(x=175,y=490)
btn2=Button(framebtn2,image=fleche2,command=ver_bas)
btn2.grid()

fleche3=PhotoImage(file="gauche.png")
framebtn3=Frame(display, bd=5, bg="#41B87F", relief=RAISED)
framebtn3.place(x=120,y=440)
btn3=Button(framebtn3,image=fleche3,command=vers_gauche)
btn3.grid()

fleche4=PhotoImage(file="droite.png")
framebtn4=Frame(display,bd=5,bg="#41B87F",relief=RAISED)
framebtn4.place(x=230,y=440)
btn4=Button(framebtn4,image=fleche4,command=vers_droite)
btn4.grid()


debut_jeu()

display.mainloop()

# from random import randint
# from tiles.tile_acces import *
# import game
# #########################################
# ####       Foncton de la partie     #####
# ####        get_nb_empty_rooms      #####
# #########################################

# def get_nb_empty_rooms(plateau):
#     """Met à jour le dictionnaire avec le nombre de case libre (s)
#     et renvoie le nombre de case libre du plateau"""
#     # On parcours le tableau tiles et on compte le nombre de case contenant la valeur 0 à l'aide d'un variable nb
#     nb=0
#     for i in range(16):
#         if plateau['tiles'][i]==0:
#             nb+=1
#     plateau['nb_case_libre']=nb
#     return nb

# #########################################
# ####       Foncton de la partie     #####
# ####        get_next_ale_tiles      #####
# #########################################

# def get_next_alea_tiles(plateau,mode):
#     """Retounre une ou deux tuiles(s) dont la position est triée
#     aléatoirement et correspont à une emplacement libre du plateau

#     plateau : dictinnaire contenant le plateau de jeu
#     mode : deux modes possibles 'init' et 'encours'

#         - 'init' : Un dictionnaire contenant deux tuiles de valeur 1 et 2.
#                    La position de chaque tuile est tiré aléatoirement à un emplacelent du plateau.
#                    Ce mode est utilisé lors de l'initialisation du jeu.

#         - 'encours' : Un dictionnaire contenant une tuile de valeur comprise entre 1 et 3 est retournée.
#                       La position du tuile est tiré aléatoirement et correspond à un emplacelent libre du plateau.
#                       Ce mode est utilisé en cours du jeu.

#     """
#     # Teste si le mode est bien définit c-à-d deux modes sont possibles 'init' et 'encours'
#     assert mode in ['init' ,'encours'], "Deux modes sont possibles 'init' et 'encours' (voir commentaire de la fonction)"
#     if mode=='init':
#         #En mode 'init' deux valeurs sont introdiutes dans le plateau
#         # Création d'un tableau de 16 case  dont les valeurs sont ceux des indices du tableau tile dans le plateau
#         tableau=list(range(16))
#         # On prend aléatoirement un premier indice stocké dans un variable x
#         x=randint(0,15)
#         # On supprime cette valeur dans le tableau pour ne pas le reprendre
#         del(tableau[x])
#         # On prend aléatoirement un deuxième indice dans le tableau stocké dans un variable i
#         i=randint(0,14)
#         # On prend aléatoirement un premier indice stocké dans un variable x
#         y=tableau[i]
#         # Pour accéder aux cases: l'indice de la ligne est la division entière et la colonne reste de la division
#         return {'mode':'init', '0':{'val':2,'lig':x//4,'col':x%4}, '1':{'val':1,'lig':y//4,'col':y%4},
#               'check': not game.play.is_game_over(plateau)}
#     else:
#         # En mode 'encours' On récupère les indices du tableau tiles ayant la valeur 0
#         tableau=[]
#         for i in range(16):
#             if plateau['tiles'][i]==0:
#                 tableau.append(i)
#         if len (tableau)!=0:
#             # S'il y a au moins une case libre, on choisi de manière aléatoire une de ces valeurs du tableau crée
#             indice = randint(0,len(tableau)-1)
#             x, val = tableau[indice], randint(1,3)
#             return {'mode':'encours','0':{'val':val,'lig':x//4,'col':x%4},'check': not game.play.is_game_over(plateau)}
#         else:
#             return {'mode':'encours','check': not game.play.is_game_over(plateau)}

# #########################################
# ####       Foncton de la partie     #####
# ####          put_next_tiles        #####
# #########################################

# def put_next_tiles(plateau,tile):
#     """
#     Permet de placer une ou deux tuile(s) dans le plateau
#     et qui dépend du plateau tiles retourné par la fonction get_next_ale_tile
#     """
#     if tile['mode']=='init':
#         set_value(plateau,tile['0']['lig'],tile['0']['col'],tile['0']['val'])
#         set_value(plateau,tile['1']['lig'],tile['1']['col'],tile['1']['val'])
#     elif tile['mode']=='encours' and len(tile)!=2:
#         set_value(plateau,tile['0']['lig'],tile['0']['col'],tile['0']['val'])


# #########################################
# ####       Foncton de la partie     #####
# ####            line_pack           #####
# #########################################

# def line_pack(plateau,num_lig, debut, sens):
#     """Tasse les tuiles d'une ligne dans un sens donné
#        plateau : dictionnaire contant le plateau du jeu
#        num_lig : indice de la ligne à tasser
#        debut :  l'indice à partir du quel se fait le tassement
#        sens : sens du tassement 1 vers la guache et O vers la droite"""
#     assert check_room(plateau,num_lig,debut) , "Erreur sur l'indice"
#     assert sens in [0,1], "le sens est incorrect (O et 1 valeurs possibles)"
#     if sens==1:
#         for i in range(debut,3,1):
#             plateau['tiles'][4*num_lig+i] = plateau['tiles'][4*num_lig+i+1]
#         plateau['tiles'][4*num_lig+3] = 0
#     else:
#         for i in range(debut,-1,-1):
#             plateau['tiles'][4*num_lig+i]= plateau['tiles'][4*num_lig+i-1]
#         plateau['tiles'][4*num_lig]=0

# def colum_pack(plateau, num_col, debut, sens):
#     """Tasse les tuiles d'une ligne dans un sens donné
#        plateau : dictionnaire contant le plateau du jeu
#        num_lig : indice de la ligne à tasser
#        debut :  l'indice à partir du quel se fait le tassement
#        sens : sens du tassement 1 vers le haut et O vers le bas"""
#     assert check_room(plateau,num_col,debut) , "Erreur sur l'indice"
#     assert sens in [0,1], "le sens est incorrect (O et 1 valeurs possibles)"
#     if sens==1:
#         for i in range(debut,3,1):
#             plateau['tiles'][4*i+num_col]= plateau['tiles'][4*i+num_col+4]
#         plateau['tiles'][12+num_col]=0
#     else:
#         for i in range(debut,-1,-1):
#             plateau['tiles'][4*i+num_col]= plateau['tiles'][4*i+num_col-4]
#         plateau['tiles'][num_col]=0


# def line_move(plateau, num_lig, sens):
#     """Déplace les tuiles d'une ligne donnée dans un sens donné
#        en appliquant les règle du jeu Threes
#        palateau : dictionnaire contenant le plateau du jeu
#        num_lig : indice de la ligne pour laquelle il faut déplacer les tuiles
#        sens : sens du tassement 1 vers la guache et O vers la droite
#     """
#     if sens==1:
#         debut=0
#         test=False
#         while debut<3 and not test:
#             x,y = get_value(plateau,num_lig,debut), get_value(plateau,num_lig,debut+1)
#             if is_room_empty(plateau,num_lig,debut):
#                 line_pack(plateau,num_lig, debut, 1)
#                 test=True
#             elif (x==2 and y==1) or (x==1 and y==2):
#                 line_pack(plateau,num_lig, debut, 1)
#                 set_value(plateau,num_lig, debut,3)
#                 test=True
#             elif x%3==0 and x==y:
#                 line_pack(plateau,num_lig, debut, 1)
#                 set_value(plateau,num_lig,debut,2*x)
#                 test=True
#             debut+=1
#     else:
#         debut=3
#         test=False
#         while debut>0 and not test:
#             x, y = get_value(plateau,num_lig,debut), get_value(plateau,num_lig,debut-1)
#             if is_room_empty(plateau,num_lig,debut):
#                 line_pack(plateau,num_lig, debut, 0)
#                 test=True
#             elif (x==2 and y==1) or (x==1 and y==2):
#                 line_pack(plateau,num_lig, debut, 0)
#                 set_value(plateau,num_lig, debut,3)
#                 test=True
#             elif x%3==0 and x==y:
#                 line_pack(plateau,num_lig, debut, 0)
#                 set_value(plateau,num_lig,debut,2*x)
#                 test=True
#             debut-=1

# def colum_move(plateau, num_col, sens):
#     """Déplace les tuiles d'une colonne donnée dans un sens donné
#        en appliquant les règle du jeu Threes
#        palateau : dictionnaire contenant le plateau du jeu
#        num_col : indice de la ligne pour laquelle il faut déplacer les tuiles
#        sens : sens du tassement 1 vers le haut et O vers le bas"""
#     if sens==1:
#         debut=0
#         test=False
#         while debut<3 and not test:
#             x, y = get_value(plateau,debut,num_col), get_value(plateau,debut+1,num_col)
#             if is_room_empty(plateau,debut,num_col)==True:
#                 colum_pack(plateau, num_col, debut, 1)
#                 test=True
#             elif (x==2 and y==1) or (x==1 and y==2):
#                 colum_pack(plateau, num_col, debut, 1)
#                 set_value(plateau,debut,num_col,3)
#                 test=True
#             elif x%3==0 and x==y:
#                 colum_pack(plateau, num_col, debut, 1)
#                 set_value(plateau, debut, num_col, 2*x)
#                 test=True
#             debut+=1

#     elif sens==0:
#         debut=3
#         test=False
#         while debut>0 and not test:
#             x, y = get_value(plateau,debut,num_col), get_value(plateau,debut-1,num_col)
#             if is_room_empty(plateau,debut,num_col)==True:
#                 colum_pack(plateau, num_col, debut, 0)
#                 test=True
#             elif (x==2 and y==1) or (x==1 and y==2):
#                 colum_pack(plateau, num_col, debut, 0)
#                 set_value(plateau,debut,num_col,3)
#                 test=True
#             elif x%3==0 and x==y:
#                 colum_pack(plateau, num_col, debut, 0)
#                 set_value(plateau, debut, num_col, 2*x)
#                 test=True
#             debut-=1

# def lines_move(plateau,sens):
#     """Déplace les tuiles de toutes les lignes dans un sens donné
#        en appliquant les règle du jeu Threes
#        palateau : dictionnaire contenant le plateau du jeu
#        sens : sens du tassement 1 vers la guache et O vers la droite
#     """
#     for i in range(4):
#         line_move(plateau, i, sens)

# def colums_move(plateau,sens):
#     """Déplace les tuiles de toutes les collonnes dans un sens donné
#        en appliquant les règle du jeu Threes
#        palateau : dictionnaire contenant le plateau du jeu
#        sens : sens du tassement 1 vers le haut et O vers le bas
#     """
#     for i in range(4):
#         colum_move(plateau, i, sens)

# def play_move(plateau,sens):
#     """
#     Permet de jouer le coups du joueur dans le sens voulu
#     plateau : plateau contenant les tuiles
#     sens : le sens de tachement des tuiles du plateu
#     """
#     if sens=="h":
#         colums_move(plateau,1)
#     elif sens=="b":
#         colums_move(plateau,0)
#     elif sens=="g":
#         lines_move(plateau,1)
#     else:
#         lines_move(plateau,0)


