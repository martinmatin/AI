# Author: Martin Crappe


import random
import copy
from tkinter import *
racine= Tk()

zone_dessin = Canvas(racine, width=500, height=500)

zone_dessin.pack()



CARDS = (
    # (AP King, AP Knight, Fetter, AP Population/Assassins)
    (1, 6, True, 5),
    (1, 5, False, 4),
    (1, 6, True, 5),
    (1, 6, True, 5),
    (1, 5, True, 4),
    (1, 5, False, 4),
    (2, 7, False, 5),
    (2, 7, False, 4),
    (1, 6, True, 5),
    (1, 6, True, 5),
    (2, 7, False, 5),
    (2, 5, False, 4),
    (1, 5, True, 5),
    (1, 5, False, 4),
    (1, 5, False, 4)
)

POPULATION = {
    'monk', 'plumwoman', 'appleman', 'hooker', 'fishwoman', 'butcher',
    'blacksmith', 'shepherd', 'squire', 'carpenter', 'witchhunter', 'farmer'
}

BOARD = [
    ['R', 'R', 'R', 'R', 'R', 'G', 'G', 'R', 'R', 'R'],
    ['R', 'R', 'R', 'R', 'R', 'G', 'G', 'R', 'R', 'R'],
    ['R', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'R'],
    ['R', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G'],
    ['R', 'G', 'G', 'G', 'G', 'R', 'R', 'G', 'G', 'G'],
    ['G', 'G', 'G', 'G', 'G', 'R', 'R', 'G', 'G', 'G'],
    ['R', 'R', 'G', 'G', 'G', 'R', 'R', 'G', 'G', 'G'],
    ['R', 'R', 'G', 'G', 'G', 'R', 'R', 'G', 'G', 'G'],
    ['R', 'R', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G'],
    ['R', 'R', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G']
]
# Coordinates of pawns on the board
KNIGHTS = {(1, 3), (3, 0), (7, 8), (8, 7), (8, 8), (8, 9), (9, 7)}
VILLAGERS = {
    (1, 1), (1, 2), (1, 0), (3, 6), (5, 2), (5, 5),
    (5, 7), (5, 9), (7, 1), (7, 5), (8, 3), (9, 5)
}
CASTLES = {(2,2), (4,1)}

#ASSASSINS déjà dévoilés
ASSASSINS = {'monk'}

#Dans le cas le rôle est 'assassins', mettre ici les trois villageois assassins
ASSASSINS_VILLAGER = {'monk', 'plumwoman', 'appleman'}

# Separate board containing the position of the pawns
PEOPLE = [[None for column in range(10)] for row in range(10)]

PEOPLE[9][9] = 'king'

# Place the knights on the board
for coord in KNIGHTS:
    PEOPLE[coord[0]][coord[1]] = 'knight'

for villager, coord in zip(random.sample(POPULATION, len(POPULATION)), VILLAGERS):
    PEOPLE[coord[0]][coord[1]] = villager


KA_INITIAL_STATE = {
    'board': BOARD,
    'people': PEOPLE,
    'castle': [(2, 2, 'N'), (4, 1, 'W')],
    'card': None,
    'king': 'healthy',
    'lastopponentmove': [],
    'arrested': [],
    'killed': {
        'knights': 0,
        'assassins': 0
    }
}

#Definition du rôle
role = 'assassins'

#Defintion utile pour trouver les positions de pièces,
#'nametype' représente quel personnoage chercher et  'position' représente
#le plateau sur lequel vous travaillez actuellement
def findpos(nametype, position):
    global ASSASSINS_VILLAGER
    global ASSASSINS
    r=0
    if nametype == 'knight':
        KNIGHTS.clear()
        for row in position:
            c=0
            for col in row:
                if col == 'knight':
                    a= r,c
                    KNIGHTS.add(a)
                c+=1
            r+=1

        return KNIGHTS

    if nametype == 'villagers':
        VILLAGERS = {}
        for row in position:
            c=0
            for col in row:
                if col is not 'knight' and col is not None and col is not 'assassins':
                    a= r,c
                    VILLAGERS[col]=a
                c+=1
            r+=1
        return VILLAGERS

    if nametype == 'assassins':
        ASSASSINS_pos= {}
        for a in ASSASSINS:

            for row in position:
                c=0
                for col in row:
                    if col is a:
                        a= r,c
                        ASSASSINS_pos[col]=a
                    c+=1
                r+=1

        return ASSASSINS_pos
    elif nametype=='hidden_assassins': #que pour le rôle assassin, il retourne les positions des assains cachés ou non
        ASSASSINS_HIDDEN={}
        A1,A2, A3 = ASSASSINS_VILLAGER
        for row in position:
            c=0
            for col in row:
                if col is A1 or col is A2 or col is A3:
                    a= r,c
                    ASSASSINS_HIDDEN[col]=a
                c+=1
            r+=1
        return ASSASSINS_HIDDEN


#petit supplément pas indispenseble au fonctionnement du jeu mais utile lorsqu'on veut une
#une visualisation avec couleurs d'une board. La librairie utilsée est tkinter.
def drawboard(liste):
    color = {'king':"orange",'villagers':"steelBlue1",'knight':"blue2",'A':"saddle brown"}


    #TOITS QUADILLAGE DOORS *****************

    roofs = {   (0,0,250,100),
                (0,100,50,250),
                (0,300,100,502),
                (250,200,350,400),
                (350,0,500,100),
                (450,100,500,150)}
    doors={(100,100,150,107),(50,200,57,250)}

    for section in roofs: #dessinne les toits
        zone_dessin.create_rectangle(section,fill='LightSalmon2', width=0)
    for section in doors: #dessinne les portes
        zone_dessin.create_rectangle(section,fill='saddle brown', width=0)
    i=0
    while i<10: #dessinne le quadrillage
        zone_dessin.create_line(i*50, 0, i*50, 500) #verticale
        zone_dessin.create_line(0, i*50, 500, i*50) #horizontale
        i+=1

    #POSITIONS  *****************
    r=0
    for row in liste:
        c=0
        for piece in row:
            if piece is not None:
                if piece == 'knight' or piece =='king':
                    zone_dessin.create_oval((c*50)+10,(r*50)+10,
                                            (c*50)+40,(r*50)+40,fill=color[piece], width=0)
                else: #villagers
                    zone_dessin.create_oval((c*50)+10,(r*50)+10,
                                            (c*50)+40,(r*50)+40,fill=color['villagers'], width=0)
                    # l.place(x = 20, y = 30 , width=120, height=25)

            c+=1
        r+=1
    bouton_sortir = Button(racine,text="Next",command=racine.destroy)
    bouton_sortir.pack()

#On envoie une board ici, la fonction va calculer un ensemble de paramètres telle
#que des distances, le nombre de villageois, etc
# la fonction revnoie alors une liste avec des points.
def calcpoints(anboard): #analysed board

    people = findpos('villagers',anboard)
    knights= findpos('knight', anboard)
    assassins=findpos('assassins',anboard)
    king_row, king_col = people['king']
    global CASTLES
    doors = CASTLES
    globalpoints = []
    #Distance king to doors: king_door
    king_door= 0
    for i in doors:
        door_row, door_col = i
        distance= abs(king_row - door_row) + abs(king_col - door_col)
        if distance > king_door:
            king_door = distance

    #Total distance knights to doors: nights_door
    knights_door= 0
    for i in knights:
        knight_row, knight_col = i
        dist=99 #to check wich doors is closest
        for a in doors:
            door_row, door_col = a
            distance= abs(knight_row - door_row) + abs(knight_col - door_col)

            if distance < dist:
                dist = distance

        knights_door += dist

    #Total distance knights to king
    king_knight =0
    for i in knights:
        knight_row, knight_col = i
        distance= abs(king_row - knight_row) + abs(king_col - knight_col)
        king_knight+=distance

    #Distance between the king and the 2 closest villagers
    king_villagers = 0
    dist1 =99
    dist2 =99
    for i in people:
        villager_row, villager_col = people[i]
        distance= abs(king_row - villager_row) + abs(king_col - villager_col)
        if distance != 0: #pour éviter de prendre le roi comme un villageois
            if distance < dist1:
                dist1=distance
            elif distance < dist2:
                dist2 = distance
    king_villagers = dist1+dist2

    #Nombre de chevaliers
    knight_numb = len(knights)

    #Numbers of villagers
    villages_numb = len(people) -1 #-1 pour enlever le roi

    #Number of assassins
    assassins_numb = len(assassins)
    for i in king_door,knights_door, king_knight,king_villagers,knight_numb, villages_numb, assassins_numb:
        globalpoints.append(i)
    return globalpoints


#cette fonction recoit la liste des points calculés avec calcpoints et multiplie chaque points avec un coeffecient
#en fonction qu'on soit un roi ou un assassin
def king_decision(boards_ap):
    king_coef =[-0.90,-0.10,-0.20,1,1,-1,-5]
    point_list = []
    boards = boards_ap[0]
    ap = boards_ap[1]
    for board in boards:
        points = calcpoints(board)
        i=0
        while i < len(points):
            points[i]=points[i]*king_coef[i]
            i+=1
        point_list.append(sum(points))
    maxi =max(point_list)
    i =0
    while i < len(point_list): #trouver quel board est le mieux
        if point_list[i] == maxi:
            numberboard = i
        i +=1
    return boards[numberboard], ap[numberboard]


#cette fonction recoit la liste des points calculés avec calcpoints et multiplie chaque points avec un coeffecient
#en fonction qu'on soit un roi ou un assassin
def assasin_decision(boards,kinglive,ap):
    assassin_coef =[0,0,0,1,0.8,0,0,2]
    point_list = []
    # ap = boards_ap[1]
    a=0
    while a < len(boards):
        points = calcpoints(boards[a])
        points.append(kinglive[a])

        i=0
        while i < len(points):
            points[i]=points[i]*assassin_coef[i]

            i+=1
        point_list.append(sum(points))

        a+=1
    maxi =max(point_list)
    i =0
    while i < len(point_list): #trouver quel board est le mieux
        if point_list[i] == maxi:
            numberboard = i
        i +=1
    return boards[numberboard], ap[numberboard]

#Cette fonction génère toutes les boards possibles
def gener_board(actualboard,ap,): #generate board with the number of positon available
    delta = {'N':(1,0), 'O':(0,-1),'S':(-1,0),'E':(0,1)}
    knights= findpos('knight', actualboard)
    people = findpos('villagers',actualboard)
    assassins=findpos('assassins',actualboard)

    print(assassins)
    king_row, king_col = people['king']
    del people['king'] # j'enlève le roi de la liste des villageois
    print(people)
    boardbuffer = []
    boardbufferap = []
    kinglivebuffer = [2]
    devoile = []
    global BOARD
    ground_roof = BOARD
    global role
    global ASSASSINS
    if role == 'king':
        for knight in knights: #all possibilities for
            knight_row, knight_col=knight
            level_state1 = ground_roof[knight_row][knight_col]
            for move in delta:
                y, x= delta[move]
                shove_row = y+knight_row
                shove_col=x+knight_col
                statut = move_acceptation(shove_row, shove_col,y,x, actualboard,0)
                if statut == 'right':
                    level_state2 = ground_roof[shove_row][shove_col]
                    if level_state2 =='G' or (level_state2=='R' and level_state1=='R'):
                        boardcach = copy.deepcopy(actualboard)
                        boardcach[shove_row][shove_col]= 'knight'
                        boardcach[knight_row][knight_col]= None
                        boardbuffer.append(boardcach)
                        cost = ap -1
                        boardbufferap.append(cost)
                    if level_state2 =='R' and level_state1=='G' and cost>1:
                        boardcach = copy.deepcopy(actualboard)
                        boardcach[shove_row][shove_col]= 'knight'
                        boardcach[knight_row][knight_col]= None
                        boardbuffer.append(boardcach)
                        cost = ap -2
                        boardbufferap.append(cost)
                elif statut == 'wrong':
                    pass
                elif statut == 'arrest':
                    level_state2 = ground_roof[shove_row][shove_col]
                    if level_state2 =='G' or (level_state2=='R' and level_state1=='R'):
                        boardcach = copy.deepcopy(actualboard)
                        boardcach[shove_row][shove_col]= None
                        boardbuffer.append(boardcach)
                        cost = ap -1
                        boardbufferap.append(cost)

                else: #have to deplace
                    deplace_row, deplace_col = statut
                    level_state2 = ground_roof[deplace_row][deplace_col]
                    if level_state2 == 'G' or (level_state2=='R' and level_state1=='R'):
                        boardcach = copy.deepcopy(actualboard)
                        shove_row = deplace_row -y
                        shove_col = deplace_col -x
                        while shove_row != knight_row or shove_col != knight_col: #on déplace tous les pions pour arriver au chevalier
                            to_deplace = boardcach[shove_row][shove_col]
                            boardcach[shove_row][shove_col] = None
                            boardcach[deplace_row][deplace_col] = to_deplace
                            shove_row +=  -y
                            shove_col +=  -x
                            deplace_row += -y
                            deplace_col += -x
                        to_deplace = boardcach[shove_row][shove_col] #on déplace le chevalier
                        boardcach[shove_row][shove_col] = None
                        boardcach[deplace_row][deplace_col] = to_deplace
                        boardbuffer.append(boardcach)
                        cost = ap -1
                        boardbufferap.append(cost)
        level_state1 = ground_roof[king_row][king_col]
        for move in delta: #pour le roi
            y, x= delta[move]
            shove_row = y+king_row
            shove_col=x+king_col
            statut = kingmove_acceptation(shove_row, shove_col,y,x, actualboard)
            if statut == 'right' and ground_roof[shove_row][shove_col] !='R':
                boardcach = copy.deepcopy(actualboard)
                boardcach[shove_row][shove_col]= 'king'
                boardcach[king_row][king_col]= None
                boardbuffer.append(boardcach)
                cost = ap -1
                boardbufferap.append(cost)
            else:
                pass
        return (boardbuffer, boardbufferap)
    if role =='assassins':
        hidden_assassins = findpos('hidden_assassins',actualboard) # je regarde quels sont les assassins
        print(hidden_assassins,'------')
        for villager in people: #all possibilities for assassins
            hidden = False
            for a in hidden_assassins: #
                if villager ==a:
                    hidden = True
            villager_row, villager_col=people[villager]
            level_state1 = ground_roof[villager_row][villager_col]
            for move in delta:
                y, x= delta[move]
                shove_row = y+villager_row
                shove_col=x+villager_col

                statut = villagermove_acceptation(shove_row, shove_col,hidden, actualboard)
                if statut == 'right':
                    level_state2 = ground_roof[shove_row][shove_col]
                    if  (level_state2==level_state1):
                        boardcach = copy.deepcopy(actualboard)
                        boardcach[shove_row][shove_col]= villager
                        boardcach[villager_row][villager_col]= None
                        boardbuffer.append(boardcach)
                        devoile.append(None)
                        cost = ap -1
                        boardbufferap.append(cost)
                        kinglivebuffer.append(2)
                    if  level_state2=='G' and level_state1=='R': #climb
                        boardcach = copy.deepcopy(actualboard)
                        boardcach[shove_row][shove_col]= villager
                        boardcach[villager_row][villager_col]= None

                        if villager in ASSASSINS:
                            cost = ap-1
                            boardbuffer.append(boardcach)
                            devoile.append(None)
                            boardbufferap.append(cost)
                            kinglivebuffer.append(2)
                        elif ap>1:
                            cost = ap-2
                            boardbuffer.append(boardcach)
                            devoile.append(None)
                            boardbufferap.append(cost)
                            kinglivebuffer.append(2)

                    if  level_state2=='R' and level_state1=='G': #go down
                        boardcach = copy.deepcopy(actualboard)
                        boardcach[shove_row][shove_col]= villager
                        boardcach[villager_row][villager_col]= None
                        if villager in ASSASSINS:
                            cost = ap
                            boardbuffer.append(boardcach)
                            devoile.append(None)
                            boardbufferap.append(cost)
                            kinglivebuffer.append(2)
                        else:
                            cost = ap-1
                            boardbuffer.append(boardcach)
                            devoile.append(None)
                            boardbufferap.append(cost)
                            kinglivebuffer.append(2)

                elif statut == 'wrong':
                    pass
                elif statut == 'knight': #on peut tuer un chevalier
                    level_state2 = ground_roof[shove_row][shove_col]
                    if level_state2 =='G' or (level_state2=='R' and level_state1=='R'):
                        if villager not in ASSASSINS:
                            devoile.append(villager)
                        boardcach = copy.deepcopy(actualboard)
                        boardcach[shove_row][shove_col]= None
                        boardbuffer.append(boardcach)
                        devoile.append(None)
                        kinglivebuffer.append(2)
                        cost = ap -1
                        boardbufferap.append(cost)
                elif statut == 'king': #on peut tuer un chevalier
                    level_state2 = ground_roof[shove_row][shove_col]
                    if level_state2 =='G' and ap >1:
                        if villager not in ASSASSINS:
                            devoile.append(villager)
                        boardcach = copy.deepcopy(actualboard)
                        boardbuffer.append(boardcach)
                        cost = ap -2
                        boardbufferap.append(cost)
                        kinglivebuffer.append(1)
                # hidden = False
                # if villager in ASSASSINS:
                #     hidden = True
                # print(villager,'move>>>', shove_row,shove_col,'assins?>>>',hidden,'statut>>',statut,'*****')
                # print((boardbuffer, boardbufferap, kinglivebuffer,devoile))
        return (boardbuffer, boardbufferap, kinglivebuffer,devoile)


#fonction utilisée par la fonction gener_board pour voir si on peut déplacer ou non le chevalier

def move_acceptation(shove_row, shove_col,y,x, actualboard,ideplace): #for the knigths!
    if -1<shove_row <10 and -1<shove_col <10:
        shovedplayer = actualboard[shove_row][shove_col]
        #conditions d'acceptation du move
        if shovedplayer == 'knight':
            return 'wrong'
        elif shovedplayer == 'king':
            return 'wrong'
        elif shovedplayer is not None and ideplace ==0: #est un villageois
            statut = 'villager'
            while statut == 'villager':
                shove_row += y
                shove_col+= x
                ideplace+=1
                statut = move_acceptation(shove_row, shove_col,y,x, actualboard,ideplace)
            if statut == 'wrong':
                return 'arrest'
            else:
                return shove_row, shove_col
        elif shovedplayer is not None and ideplace != 0:
            return 'villager'
            if statut == 'wrong':
                return 'wrong'
            else:
                return 'deplace', shove_row, shove_col
        elif shovedplayer is None:
            return 'right'
    else:
        return 'wrong'

#fonction utilisée par la fonction gener_board pour voir si on peut déplacer ou non le roi
def kingmove_acceptation(shove_row, shove_col,y,x, actualboard): #for the king!
    if -1<shove_row <10 and -1<shove_col <10:
        shovedplayer = actualboard[shove_row][shove_col]
        #conditions d'acceptation du move
        if shovedplayer is None:
            return 'right'
        else: return 'wrong'
    else:
        return 'wrong'

#fonction utilisée par la fonction gener_board pour voir si on peut déplacer ou non un villageois
def villagermove_acceptation(shove_row, shove_col,hidden,actualboard): #for the villager!

    if -1<shove_row <10 and -1<shove_col <10:
        shovedplayer = actualboard[shove_row][shove_col]
        #conditions d'acceptation du move
        if shovedplayer is None:
            return 'right'
        elif hidden == True: #dans le cas ou c'est un assassin dévoilé, enfait hidden dit s'il est dévoilé ou non
            if shovedplayer is 'king':
                return 'king'
            if shovedplayer is 'knight':
                return 'knight'
            else:
                return 'wrong'
        else: # je ne suis pas un assassin donc je ne peux pas tuer
            return 'wrong'

    else:
        return 'wrong'

#SCRIPT:::
if role =='king':
    newboard,newap =king_decision(gener_board(PEOPLE,4 ))
    print('FINAL BOARD')
    for i in newboard:
        print(i)
if role =='assassins':
    newboard,ap,liveking,devoile = gener_board(PEOPLE,4)
    finalboard, finalap =assasin_decision(newboard,liveking,ap)
    print('FINAL BOARD:')
    for i in finalboard:
        print(i)
    drawboard(finalboard)
    racine.mainloop()
