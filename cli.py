import importlib
import core

def clsr():
    core.os.system("cls")

core.detect_face()
inp = -1
while inp != 3:
    clsr()
    print("Recognizer App")
    print("=================")
    print("1. Face Recognition")
    print("2. Live Recognition lock")
    print("3. Live Recognition unlock")
    print("3. Exit")
    print(">> ", end="")
    inp = int(input())

    if(inp == 1):
        clsr()
        core.test()
    elif(inp == 2):
        clsr()
        core.live('lock')
    elif(inp == 3):
        clsr()
        core.live('unlock')
        
        
        
    