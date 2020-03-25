def DFA(word, st_crt):
    for letter in word:
        if transitons[st_crt][alphabet.index(letter)] != -1:
            st_crt = transitons[st_crt][alphabet.index(letter)][0] #pentru ca am pastrat modul de creare al matricei de la Lambda-NFA,
            # care presupune a initializa ca vector de stari tranzitiile,
            # specificam a treia dimensiune chiar daca avem doar un element
        else:
            return 0
    if st_crt in st_fin:
        return 1

def lambda_NFA(word, ind, st_crt):  # functia este recursiva pentru a verifica toate posibilitatile
    # ind reprezinta indexul din cuvant al literei curente, il retinem pentru recursivitate
    # st_crt reprezinta starea curenta
    if ind == len(word): #conditia de oprire a recursivitatii
        if st_crt in st_fin:
            return 1
        else:
            return 0
    else:
        chr_crt = word[ind] #daca am avem litere de parcurs, chr_crt ia litera indicata de indice
    if transitons[st_crt][alphabet.index(chr_crt)] == -1:  # daca din starea curenta nu putem sa trecem in alta stare cu litera curenta
        if transitons[st_crt][poz_lambda] != -1: # verificam daca avem posibilitatea unei lambda tranzitii
            st_crt = transitons[st_crt][poz_lambda][0]
            if ind == len(word):    #in cazul in care lambda tranzitia este ultima tranzitie (dintre ultima litera si strea curenta),
                # caz in care trebuie sa oprim recursivitate,
                # altfel va continua sa apeleze pentru aceeasi litera si starea curenta (setata in urma tranzitiei lambda)
                if st_crt in st_fin:   # verificam daca stare in care am ajuns prin lambda tranzitie e finala
                    return 1
                else:
                    return 0
            else:
                rez = lambda_NFA(word, ind, st_crt)  # daca nu este tranzitie finala atunci verficam si aceasta cale
        else:
            return 0
    else:
        # daca avem stare/stari in care sa trecem
        rez = 0
        for i in transitons[st_crt][alphabet.index(chr_crt)]:
            rez = rez or lambda_NFA(word, ind+1, i) # rez = 1 daca gasim macar o varianta valida de tranzitii spre o stare finala,
            # rez = 0 daca nu exista nicio posibilitate
        if transitons[st_crt][poz_lambda] != -1:  # adaugam si posibilitatea unei/unor lambda-tranzitii pe care sa o verificam
            for i in transitons[st_crt][poz_lambda]:
                rez = rez or lambda_NFA(word, ind, i)
    return rez


def evaluate(automata, word):
    if automata == "lambda NFA":
        evaluation = lambda_NFA(word, 0, q0)
    else:
        evaluation = DFA(word, q0)
    return bool(evaluation)


f = open("lambda-nfa-ex.in")  # preluam datele din fisier
lines = f.readlines()   # citim liniile
n = int(lines[0])   # numar stari
m = int(lines[1])  # numar caractere din alfabet
alphabet = lines[2]  # alfabetul
q0 = int(lines[3])  # starea initiala
k = int(lines[4])  # numar stari finale
st_fin = [int(x) for x in lines[5].split()]  # vector stari finale
l = int(lines[6])  # numar tranzitii
transitons = [[[] for x in range(m+1)] for y in range(n)]  # matricea de tranzitii
alphabet = alphabet.strip("\n") + '$'  # adaugam in alfabet caracterul lambda pentru a crea matricea de tranzitii
poz_lambda = len(alphabet) - 1  # retinem ca lambda e pe ultima coloana

# formam matricea cu datele citite din fisier
for i in range(l):
    trnz = lines[7+i].strip('\n')
    transitons[int(trnz[0])][alphabet.index(trnz[2])].append(int(trnz[4]))

# setam o valoare pentru "casutele" din matrice unde nu exista tranzitie intre rand si coloana
for i in range(n):
    for j in range(m+1):
        if len(transitons[i][j]) == 0:
            transitons[i][j] = -1


#rez0 = evaluate("DFA", "bacyaaac")
#print(rez0)

rez1 = evaluate("lambda NFA", "abxyyyxyby")
print(rez1)
rez2 = evaluate("lambda NFA", "bcax")
print(rez2)
rez3 = evaluate("lambda NFA", "bcbxxy")
print(rez3)
rez4 = evaluate("lambda NFA", "abyyxz")
print(rez4)
rez5 = evaluate("lambda NFA", "abyyxyx")
print(rez5)
