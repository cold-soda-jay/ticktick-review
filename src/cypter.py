import random
weight=20
move = 50

def enCode(code):
    key = int(random.random()*15) #create a random key
    engbk=bytearray(code.encode('utf-8')) #encode into utf-8
    result = bytearray(len(engbk)*3) #result is a list with 3 elements, two of value and one is key
    for i in range(len(engbk)): #encode every symbol
        origi = engbk[i]
        firsrencode = origi^key
        rest = firsrencode%weight
        scale = firsrencode//weight
        result[i*3]=rest+move
        result[i*3+1]=scale+move
        result[i*3+2]=key
    return result.decode('utf-8')


def deCode(code):
    degbk = bytearray(code.encode('utf-8'))
    result = bytearray(int(len(degbk)/3))
    for i in range(len(result)):
       code =  degbk[i*3]-move+(degbk[i*3+1]-move)*weight
       result[i] = code^degbk[i*3+2]
    return result.decode('utf-8')