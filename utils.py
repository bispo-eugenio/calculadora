#Valida se é número ou não
def is_valid_number(string: str) :
    flag = bool()
    try:
        float(string) 
        flag = True
    except ValueError:
        flag = False
    return flag

#Verifica se a string está vazia
def is_empty(string):
    return len(string) == 0

#Verifica se a entrada é um número:
def is_numeric_or_dont(request):
    if request in "1234567890.":
        return request
    return 