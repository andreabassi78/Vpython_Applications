a = 2.1
b = 3
c = a * b
d = "text"

e = [a,3.0,b,d]



for index,element in enumerate(e):
    if index >=2:
        print("l'elemento", index, "vale:", element)
    else:
        print("l'indice è minore di 2")
    print("sono nel ciclo for ma il ciclo if è finito")    


print("qui il ciclo for è finito")



