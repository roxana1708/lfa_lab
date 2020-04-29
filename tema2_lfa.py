"""
    $ NFA TO NFA
"""
def citireDateLambdaNfaToNfa():
    f = open("lambdaNfaToNfa.in")  # preluam datele din fisier
    lines = f.readlines()   # citim liniile
    n = int(lines[0])   # numar stari
    m = int(lines[1])  # numar caractere din alfabet
    alfabet = lines[2]  # alfabetul
    q0 = int(lines[3])  # starea initiala
    k = int(lines[4])  # numar stari finale
    st_fin = [int(x) for x in lines[5].split()]  # vector stari finale
    l = int(lines[6])  # numar tranzitii
    transitions = [[[] for x in range(m+1)] for y in range(n)]  # matricea de tranzitii
    alfabet = alfabet.strip("\n") + '$'  # adaugam in alfabet caracterul lambda pentru a crea matricea de tranzitii
    poz_lambda = len(alfabet) - 1  # retinem ca lambda e pe ultima coloana

    # formam matricea cu datele citite din fisier
    for i in range(l):
        trnz = lines[7 + i].strip('\n')
        transitions[int(trnz[0])][alfabet.index(trnz[2])].append(int(trnz[4]))

    # setam o valoare pentru "casutele" din matrice unde nu exista tranzitie intre rand si coloana
    for i in range(n):
        for j in range(m + 1):
            if len(transitions[i][j]) == 0:
                transitions[i][j] = -1

    automat = [0] * 8
    automat[0] = n
    automat[1] = m
    automat[2] = alfabet
    automat[3] = q0
    automat[4] = k
    automat[5] = st_fin
    automat[6] = l
    automat[7] = transitions

    return automat

def inchidereLambda(automatIn, tabel, stare, stare_curenta):
    if stare_curenta not in tabel[0][stare]:
        tabel[0][stare].append(stare_curenta)
        if automatIn[7][stare_curenta][2] != -1:
            for i in automatIn[7][stare_curenta][2]:
                inchidereLambda(automatIn, tabel, stare, i)

def tranzitiiCaracter(automatIn, tabel, chr):
    for x in range(automatIn[0]):
        for y in tabel[0][x]:
            stari = automatIn[7][y][automatIn[2].index(chr)]
            if stari != -1:
                for z in stari:
                    if z not in tabel[automatIn[2].index(chr)+1][x]:
                        tabel[automatIn[2].index(chr)+1][x].append(z)

def inchidereMultimi(automatIn, tabelInch, tabelTranz):
    for chr in range(len(automatIn[2])-1):
        for i in range(automatIn[0]):
            listeReuniune = []
            for x in tabelInch[chr+1][i]:
                listeReuniune = listeReuniune + list(set(tabelInch[0][x]) - set(listeReuniune))
            tabelTranz[chr+1].append(sorted(listeReuniune))

def stFin(automatIn, stInAF, tabelInch):
    rez = []
    for x in range(automatIn[0]):
        if x != stInAF:
            for st in automatIn[5]:
                if st in tabelInch[0][x] and x not in rez:
                    rez.append(x)
    return rez

def inlocuire(automatIn, tabelTranz, a, b, dim):
    index = tabelTranz[0].index(b)
    tabelTranz[0] = tabelTranz[0][:index] + tabelTranz[0][index+1:]
    for i in range(dim):
        for chr in range(len(automatIn[2])-1):
            if b in tabelTranz[chr+1][i]:
                tabelTranz[chr+1][i][tabelTranz[chr+1][i].index(b)] = a
                tabelTranz[chr+1][i] = list(set(tabelTranz[chr+1][i]))

def elimStariRedundante(automatIn, stFinAF, tabelTranz):
    copie_n = automatIn[0]
    i = 0
    while i < copie_n:
        j = i+1
        while j < copie_n:
            ok = 1
            if ((i in stFinAF and j in stFinAF) or (i not in stFinAF and j not in stFinAF)):
                for chr in range(len(automatIn[2])-1): #alphabet[0:len(alphabet)-1]:
                    if tabelTranz[chr+1][i] != tabelTranz[chr+1][j]:
                        ok = 0
                if ok:
                    aux_i = tabelTranz[0][i]
                    aux_j = tabelTranz[0][j]
                    for chr in range(len(automatIn[2])-1):
                        tabelTranz[chr+1] = tabelTranz[chr+1][:j] + tabelTranz[chr+1][j+1:]
                    copie_n -= 1
                    inlocuire(automatIn, tabelTranz, aux_i, aux_j, copie_n)
                else:
                    j+=1
            else:
                j += 1
        i += 1
    return copie_n

def lambdaNfaToNfa(automatInitial):
    tabelInchideri = [[[] for x in range(automatInitial[0])] for y in range(automatInitial[1]+1)]
    automatFinal = [0] * 8
    tranzitiiAutomatFinal = [[] for y in range(automatInitial[1]+1)]

    # Pasul 1: Calcularea lambda-inchiderii
    for x in range(automatInitial[0]):
        inchidereLambda(automatInitial, tabelInchideri, x, x)

    # Pasul 2: Calcularea functiei de tranzitie
    for chr in automatInitial[2][0:len(automatInitial[2]) - 1]:
        tranzitiiCaracter(automatInitial, tabelInchideri,chr)
    for i in range(automatInitial[0]):
        tranzitiiAutomatFinal[0].append(i)
    inchidereMultimi(automatInitial, tabelInchideri, tranzitiiAutomatFinal)

    # Pasul 3: Calcularea starilor finale si initiale
    stareInitialaAutomatFinal = automatInitial[3]
    stariFinaleAutomatFinal = stFin(automatInitial, stareInitialaAutomatFinal, tabelInchideri)

    # Pasul 4: Eliminarea starilor redundante
    nrStariAutomatFinal = elimStariRedundante(automatInitial, stariFinaleAutomatFinal, tranzitiiAutomatFinal)

    automatFinal[0] = nrStariAutomatFinal
    automatFinal[1] = automatInitial[1]
    automatFinal[2] = automatInitial[2]
    automatFinal[3] = stareInitialaAutomatFinal
    automatFinal[4] = len(stariFinaleAutomatFinal)
    automatFinal[5] = stariFinaleAutomatFinal
    automatFinal[6] = 0
    for x in tranzitiiAutomatFinal[1:]:
        for y in x:
            automatFinal[6] += len(y)
    automatFinal[7] = tranzitiiAutomatFinal
    return automatFinal
"""
    $ NFA TO NFA
"""

"""
    NFA TO DFA
"""
def citireDateNfaToDfa():
    f = open("nfaToDfa.in")  # preluam datele din fisier
    lines = f.readlines()  # citim liniile
    n = int(lines[0])  # numar stari
    m = int(lines[1])  # numar caractere din alfabet
    alfabet = lines[2]  # alfabetul
    q0 = int(lines[3])  # starea initiala
    k = int(lines[4])  # numar stari finale
    st_fin = [int(x) for x in lines[5].split()]  # vector stari finale
    l = int(lines[6])  # numar tranzitii
    tranzitii = [[[] for x in range(m)] for y in range(n)]  # matricea de tranzitii
    alfabet = alfabet.strip("\n")

    for i in range(l):
        trnz = lines[7 + i].strip('\n')
        tranzitii[int(trnz[0])][alfabet.index(trnz[2])].append(int(trnz[4]))

    automat = [0] * 8
    automat[0] = n
    automat[1] = m
    automat[2] = alfabet
    automat[3] = q0
    automat[4] = k
    automat[5] = st_fin
    automat[6] = l
    automat[7] = tranzitii

    return automat

def elimNedet(automatIn, dict, st):
    if len(st) > 1:
        for chr in range(len(automatIn[2])):
            v = []
            for l in st:
                v = v + list(set(automatIn[7][int(l)][chr]) - set(v))
            a = "".join(str(x) for x in v)
            dict[st].append(a)
            if a not in dict.keys() and a != '':
                dict.update({a: []})
                elimNedet(automatIn, dict, a)
    else:
        for chr in range(len(automatIn[2])):
            a = "".join(str(x) for x in automatIn[7][int(st)][chr])
            dict[st].append(a)
            if a not in dict.keys() and a != '':
                dict.update({a: []})
                elimNedet(automatIn, dict, a)

def stF(stFinIn, dict):
    stFinaleNoi = []
    for key in dict.keys():
        for a in key:
            if int(a) in stFinIn:
                stFinaleNoi.append(key)
    return stFinaleNoi

def redenumireStari(dict, nrStariIn):
    poz = nrStariIn
    keys = list(dict.keys())
    for key in keys:
        if len(key) > 1:
            v = dict[key]
            dict.pop(key)
            dict.update({str(poz): v})

            for key2 in dict.keys():
                for val in dict[key2]:
                    if val == key:
                        dict[key2][dict[key2].index(val)] = poz
            poz += 1

def nfaToDfa(automatInitial):
    dictTranzitiiAutomatFinal = {str(automatInitial[3]): []}

    #Pasul 1: Eliminarea nedeterminismului
    for chr in range(len(automatInitial[2])):
        a = "".join(str(x) for x in automatInitial[7][automatInitial[3]][chr])
        dictTranzitiiAutomatFinal[str(automatInitial[3])].append(a)
        if a not in dictTranzitiiAutomatFinal.keys() and a != '':
            dictTranzitiiAutomatFinal.update({a: []})
    for i in dictTranzitiiAutomatFinal[str(automatInitial[3])]:
        if i != '':
            elimNedet(automatInitial, dictTranzitiiAutomatFinal, i)

    #Pasul 2: Calcularea starilor initiale si finale
    stareInitialaAutomatFinal = automatInitial[3]
    stariFinaleAutomatFinal = stF(automatInitial[5], dictTranzitiiAutomatFinal)

    #Pasul 3: Redenumirea starilor
    redenumireStari(dictTranzitiiAutomatFinal, automatInitial[0])

    automatFinal = [0]*10
    automatFinal[0] = len(dictTranzitiiAutomatFinal.keys())
    automatFinal[1] = automatInitial[1]
    automatFinal[2] = automatInitial[2]
    automatFinal[3] = stareInitialaAutomatFinal
    automatFinal[4] = len(stariFinaleAutomatFinal)
    automatFinal[5] = stariFinaleAutomatFinal
    automatFinal[6] = 0
    for item in dictTranzitiiAutomatFinal.values():
        for x in item:
            if x != '':
                automatFinal[6] += 1
    automatFinal[7] = dictTranzitiiAutomatFinal
    return automatFinal

"""
    NFA TO DFA
"""
"""
    DFA TO DFA Min
"""
def citireDateDfaToDfaMin():
    f = open("dfaToDfaMin.in")  # preluam datele din fisier
    lines = f.readlines()  # citim liniile
    n = int(lines[0])  # numar stari
    m = int(lines[1])  # numar caractere din alfabet
    alfabet = lines[2].strip("\n")  # alfabetul
    q0 = int(lines[3])  # starea initiala
    k = int(lines[4])  # numar stari finale
    st_fin = [int(x) for x in lines[5].split()]  # vector stari finale
    l = int(lines[6])  # numar tranzitii
    tranzitii = [[-1 for x in range(m)] for y in range(n)]  # matricea de tranzitii

    for i in range(l):
        trnz = lines[7 + i].strip('\n')
        tranzitii[int(trnz[0])][alfabet.index(trnz[2])] = int(trnz[4])

    automat = [0] * 10
    automat = [0] * 8
    automat[0] = n
    automat[1] = m
    automat[2] = alfabet
    automat[3] = q0
    automat[4] = k
    automat[5] = st_fin
    automat[6] = l
    automat[7] = tranzitii

    return automat

def stEchiv(tbEchiv, automatIn):
    for i in range(automatIn[0]):
        for j in range(automatIn[0]):
            if tbEchiv[i][j] != -1:
                if (i in automatIn[5] and j not in automatIn[5]) or (i not in automatIn[5] and j in automatIn[5]):
                    tbEchiv[i][j] = False
    for i in range(automatIn[0]):
        for j in range(automatIn[0]):
            if tbEchiv[i][j] == True:
                for chr in automatIn[2]:
                    if tbEchiv[automatIn[7][i][automatIn[2].index(chr)]][automatIn[7][j][automatIn[2].index(chr)]] == False:
                        tbEchiv[i][j] = False

def grupareStariEchiv(automatIn, tbEchiv, lstStEchiv):
    i = automatIn[0]-1
    vizitate = []
    while i > 0:
        if i not in vizitate:
            cuv = str(i)
            for j in range(automatIn[0]):
                if tbEchiv[i][j] == True:
                    cuv = str(j) + cuv
                    vizitate.append(j)
            lstStEchiv.insert(0, cuv)
        i -= 1

def tranzAutomatFinal(automatIn, tranzAF, lstStEchiv):
    for key in tranzAF.keys():
        for chr in automatIn[2]:
            a = automatIn[7][int(key[0])][automatIn[2].index(chr)]
            for i in lstStEchiv:
                if str(a) in i:
                    tranzAF[key].append(i)

def stInit(q0, lstStEchiv):
    for key in lstStEchiv:
        if str(q0) in key:
            return key

def stFinale(stFinIn, lstStEchiv):
    stFinNoi = []
    for key in lstStEchiv:
        for x in stFinIn:
            if str(x) in key and key not in stFinNoi:
                stFinNoi.append(key)
    return stFinNoi

def drumStFin(alfabet, stFinAF, tranzAF, stCrt, chrIndex):
    if stCrt in stFinAF:
        return 1
    rez = 0
    if tranzAF[stCrt][chrIndex] and tranzAF[stCrt][chrIndex] != stCrt:
        rez = drumStFin(alfabet, stFinAF, tranzAF, tranzAF[stCrt][chrIndex], 0)

    if chrIndex < len(alfabet)-1 and rez == 0:
        rez = drumStFin(alfabet, stFinAF, tranzAF, stCrt, chrIndex+1)

    return 0 or rez

def elimStDeadEnd(alfabet, stFinAF, tranzAF):
    v = []
    for key in tranzAF.keys():
        if drumStFin(alfabet, stFinAF, tranzAF, key, 0) == 0:
            v.append(key)
    for key in v:
        tranzAF.pop(key)
        for key2 in tranzAF.keys():
            for val in tranzAF[key2]:
                if val == key:
                    tranzAF[key2][tranzAF[key2].index(val)] = ''

def elimStNeacesibile(stInAF, tranzAF):
    v = []
    for key1 in tranzAF.keys():
        if key1 != str(stInAF):
            ok = 0
            for key2 in tranzAF.keys():
                if key2 != key1:
                    if key1 in tranzAF[key2]:
                        ok = 1
            if ok == 0:
                v.append(key1)
    for key in v:
        tranzAF.pop(key)
        for key2 in tranzAF.keys():
            for val in tranzAF[key2]:
                if val == key:
                    tranzAF[key2][tranzAF[key2].index(val)] = ''

def redenumireSt(dict):
    poz = 0
    keys = list(dict.keys())
    for key in keys:
        if len(key) > 1:
            v = dict[key]
            dict.pop(key)
            dict.update({str(poz): v})

            for key2 in dict.keys():
                for val in dict[key2]:
                    if val == key:
                        dict[key2][dict[key2].index(val)] = poz
            poz += 1

def dfaToDfaMin(automatInitial):
    #Pasul 1: Determinarea starilor echivalente
    tabelEchiv = [[-1 for x in range(automatInitial[0])] for y in range(automatInitial[0])]
    for i in range(automatInitial[0]):
        for j in range(automatInitial[0]):
            if i > j:
                tabelEchiv[i][j] = True
    stEchiv(tabelEchiv, automatInitial)

    #Pasul 2: Gruparea starilor echivalente si calcularea functiei de tranzitie
    listaStariEchiv = []
    grupareStariEchiv(automatInitial, tabelEchiv, listaStariEchiv)

    tranzitiiAutomatFinal = {listaStariEchiv[i]: [] for i in range(len(listaStariEchiv))}
    tranzAutomatFinal(automatInitial, tranzitiiAutomatFinal, listaStariEchiv)

    #Pasul 3: Calcularea starilor finale si initiale
    stareInitialaAutomatFinal = stInit(automatInitial[3], listaStariEchiv)
    stariFinaleAutomatFinal = stFinale(automatInitial[5], listaStariEchiv)

    #Pasul 4: Eliminarea starilor dead-end
    elimStDeadEnd(automatInitial[2], stariFinaleAutomatFinal, tranzitiiAutomatFinal)

    #Pasul 5: Eliminarea starilor neaccesibile
    elimStNeacesibile(stareInitialaAutomatFinal, tranzitiiAutomatFinal)

    #Redenumire stari
    redenumireSt(tranzitiiAutomatFinal)

    automatFinal = [0] * 10
    automatFinal[0] = len(tranzitiiAutomatFinal.keys())
    automatFinal[1] = automatInitial[1]
    automatFinal[2] = automatInitial[2]
    automatFinal[3] = stareInitialaAutomatFinal
    automatFinal[4] = len(stariFinaleAutomatFinal)
    automatFinal[5] = stariFinaleAutomatFinal
    for item in tranzitiiAutomatFinal.values():
        for x in item:
            if x != '':
                automatFinal[6] += 1
    automatFinal[7] = tranzitiiAutomatFinal
    return automatFinal

"""
    DFA TO DFA Min
"""


"""
    $ NFA TO NFA
"""
#"""
#Citim datele din fisier
automat01 = citireDateLambdaNfaToNfa()

#Transformam $_NFA in NFA
automat1 = lambdaNfaToNfa(automat01)

#Afisare tranzitii automat final
print("$ NFA -> NFA")
for i in range(automat1[0]):
    print(automat1[7][0][i])
    for chr in range(len(automat1[2])-1):
        print(automat1[2][chr])
        print(automat1[7][chr+1][i])
print('\n')
"""
    NFA TO DFA
"""
#"""
#Citim datele din fisier
automat02 = citireDateNfaToDfa()

#Transformam NFA in DFA
automat2 = nfaToDfa(automat02)

#Afisare tranzitii automat final
print("NFA -> DFA")
print(automat2[7])
print('\n')
#"""

"""
    DFA TO DFA Min
"""
#Citim datele din fisier
automat03 = citireDateDfaToDfaMin()

#Transformam NFA in DFA
automat3 = dfaToDfaMin(automat03)

#Afisare automat final
print("DFA -> DFA Min")
print(automat3[7])
