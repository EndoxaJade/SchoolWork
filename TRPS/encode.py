import base64

# password = "f7c199a97f90fe7ca09756ab3fc5b01d"
password = None
try:
    password = open(".pwd", "r").read()
except IOError:
    pass

pwd = "G!thuB"

# An encoding similar to Vigenere cipher

def encode(string, key=pwd):
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        # Encoding symbols
        encoded_c = chr((ord(string[i]) + ord(key_c)) % 256)  # исправить расчет
        encoded_chars.append(encoded_c)
    encoded_string = "".join(encoded_chars)
    return base64.urlsafe_b64encode(encoded_string.encode('utf-8')).decode('utf-8')

def decode(string, key=pwd):
    decoded_chars = []
    string = base64.urlsafe_b64decode(string.encode('utf-8')).decode('utf-8')
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr((ord(string[i]) - ord(key_c)) % 256)  # исправить расчет
        decoded_chars.append(encoded_c)
    decoded_string = "".join(decoded_chars)
    return decoded_string
