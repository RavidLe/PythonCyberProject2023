

def encrypt(message, key):
    encrypted_msg = ""
   
    if len(list(key)) != 16:
        return 
    
    j = 0
    for c in message:
        char = c
        char = chr((c + key[j]) % 126)
        encrypted_msg += char

        j += 1
        if j == len(key):
            j = 0
    
    

    return str(encrypted_msg)


def decrypt(encrypted_msg, key):
    if len(list(key)) != 16:
        return 
    
    clear_msg = ""

    j = 0
    for c in encrypted_msg:
        char = c
        char = chr((c - key[j]) % 126)
        clear_msg += char

        j += 1
        if j == len(key):
            j = 0
    return clear_msg
