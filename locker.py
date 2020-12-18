from cryptography.fernet import Fernet
import os
import sys
from pathlib import Path

KEY = ''
PATH = ''

LIST_FILE_PROTECT =('listName.json','key.key')

def write_key():
    global KEY
    KEY = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(KEY)

def remove_list_json(list_file):
    # jika ada yang mau gak di encrypt / decrypt
    for i in list_file:
        for j in LIST_FILE_PROTECT:
            if i.name == j:
                list_file.remove(i)
    return list_file

def load_key():
    global KEY
    KEY =  open("key.key", "rb").read()

def decrypt():
    try:
        list_file = list(Path(PATH).rglob("*"))
        list_file = remove_list_json(list_file)
        f = Fernet(KEY)
        for current_file in list_file:
            try:
                encrypted_file = current_file.read_bytes()
                decrypt_file = f.decrypt(encrypted_file)
                with open(current_file, "wb") as file:
                    file.write(decrypt_file)
                    print("Success decrypt {}".format(current_file.name))
            except Exception as e:
                print("Failed because {}".format(e))
    except Exception as e :
        print("Failed because {}".format(e))
        return False

def encrypt_file():
    try:
        list_file = list(Path(PATH).rglob("*"))
        list_file = remove_list_json(list_file)
        f = Fernet(KEY)
        for current_file in list_file:
            try:
                encrypted_data = f.encrypt(current_file.read_bytes())
                with open(current_file, "wb") as file:
                    file.write(encrypted_data)
                    file.close()
                    print("Success encrypt {}".format(current_file.name))
            except Exception as e:
                print("Failed because {}".format(e))
    except Exception as e:
        print("Failed because {}".format(e))
        return False

def main():
    global KEY, PATH
    try:
        PATH = sys.argv[1]
    except:
        PATH = None

    if PATH is None:
        print("Input must run with 'python {} [Path] [e|d]'".format(sys.argv[0]))
        return

    if os.path.exists('./key.key') is False:
        print("Generating key...")
        write_key()
    else:
        print("Loading key..")
        load_key()
    
    try:
        if sys.argv[2] is 'e':
            print("Encrypting...")    
            encrypt_file()
        elif sys.argv[2] is 'd':
            print("Decrypting...")    
            decrypt()
    except:
        print("Input must run with 'python {} [Path] [e|d]'".format(sys.argv[0]))
        return

if __name__ == "__main__":
    main()
