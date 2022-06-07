import time
import sys
import pyAesCrypt
import PySimpleGUI as sg

from os import stat, remove
sizeof = 20
sizein = 2
sg.theme('DarkBlack')
def encrypt(data, password, y):
    with open(data, "rb") as fIn:
        with open("{}.aes".format(data), "wb") as fOut:
            pyAesCrypt.encryptStream(fIn, fOut, password, bufferSize)
    if y == False:

        print('\nok')
        time.sleep(1)
        sys.exit()

    remove("{}".format(data))
    print('Arquivo removido')
    time.sleep(2)
    sys.exit()

def decrypt(data, password):
    # get encrypted file size
    encFileSize = stat("{}".format(data)).st_size
    # decrypt
    with open(data, "rb") as fIn:
        try:
            data = data.replace('.aes', '')
            with open(data, "wb") as fOut:
                # decrypt file stream
                pyAesCrypt.decryptStream(fIn, fOut, password, bufferSize, encFileSize)

        except ValueError:
            print('senha incorreta')
            # remove output file on error
            remove("{}".format(data))

    time.sleep(3)
    sys.exit()

def menuencrypt():
    window.close()
    layoutencryptmenu = [[
        sg.Text('Senha')],
        [sg.Input(password_char="*")],
        [sg.Text('Arquivo para ser criptografado')],
        [sg.Input(), sg.FileBrowse()],
        [sg.Checkbox('SIM')],
        [sg.Text('Voce quer deletar o arquivo original ?')],
        [sg.OK(), sg.Exit()]]

    menuencrypt1 = sg.Window('ENCRIPTER DE ARQUIVOS', layoutencryptmenu)
    event, values = menuencrypt1.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        menuencrypt1.close()
    else:
        encrypt(values[1], values[0], values[2])
def menudecrypt():
    window.close()
    layoutdecryptmenu = [[
        sg.Text('Senha')],
        [sg.Input(password_char="*")],
        [sg.Text('Arquivo para ser criptografado')],
        [sg.Input(), sg.FileBrowse()],
        [sg.OK(), sg.Exit()]
    ]
    menudecrypt1 = sg.Window('DECRIPTER DE ARQUIVOS', layoutdecryptmenu)
    event, values = menudecrypt1.read()
    print(event)
    if event == sg.WIN_CLOSED or event == 'Exit':
        menudecrypt1.close()
    else:
        decrypt(values[1], values[0])


# encryption/decryption buffer size - 64K
bufferSize = 100 * 1024

layout = [[
            sg.Button('Encriptar', key=lambda: menuencrypt(), size=(sizeof, sizein)),
            sg.Button('Decriptar', key=lambda: menudecrypt(), size=(sizeof, sizein))]]
window = sg.Window('CRIPTER DE ARQUIVOS').Layout(layout)
event, values = window.read()
if callable(event):
    event()
if event == sg.WIN_CLOSED or event == 'Cancel':
    window.close()
