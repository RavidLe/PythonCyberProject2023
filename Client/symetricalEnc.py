# function to encrypt message with key
def encrypt(message, key):
    encrypted_msg = ""
   
   # checking that the is in the correct length
    if len(list(key)) != 16: 
        return  # return if not
    
    j = 0 # index for the key

    # loop to encrypt each char in the message one by one
    for c in message:
        char = c 
        char = chr((c + key[j]) % 126) # moving each char with one chuck of the key and moulding it with 126 so it fits the ascii
        encrypted_msg += char # adding the char to the encrypted message

        j += 1 # inc the index

        # if the index has reach the end of the key resetting it
        if j == len(key): 
            j = 0
    
    

    return str(encrypted_msg)

def decrypt(encrypted_msg, key):

       # checking that the is in the correct length
    if len(list(key)) != 16:
        return # return if not
    
    clear_msg = "" # the message that will be returned in the end

    j = 0 # index for the key

    # loop to decrypt each char in the message one by one
    for c in encrypted_msg:
        char = c
        char = chr((c - key[j]) % 126) # reversing the action of the encryption with the key
        clear_msg += char

        j += 1
        if j == len(key):
            j = 0
    return clear_msg