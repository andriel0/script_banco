range_string = []
for i in range(13, 14):
    cod = str(i)
    if len(cod) < 3:
        cod = ('0' * (3 - len(cod))) + cod
    range_string.append(cod)
    
meses = []
for mes in range(1,13):
    str_mes = str(mes)
    if len(str_mes) < 2:
        str_mes = ('0' * (2 - len(str_mes))) + str_mes
    meses.append(str_mes)
