'''
Pokedex module
----------------------------------------------------------------------------
'''

from app.mac import mac, signals
import requests
from modules.pokedex import pykemon

'''
Main funciton, all happens after this
'''
@signals.message_received.connect
def handle(message):
    if message.command == "pokemon":
        if message.predicate == "-h":
            show_help(message)
        else:
            handle_command(message)
        
    
'''
Handles command
!pokemon <id>

'''
def handle_command(message):
    arg = message.predicate.split(' ')[0]
    if is_int_number(arg):
        try:
            client = pykemon.V1Client()
            pokemon = client.get_pokemon(uid=int(arg))[0]
            mac.send_message(pokemon.name.capitalize(), message.conversation)
            #mac.send_image(message.conversation, get_image(pokemon.sprites["front_default"], "1.png"), pokemon.name)
        except Exception as ex:
            print(ex)
            mac.send_message("Couldn't find the pokemon", message.conversation)
    else:
        mac.send_message("Invalid argument", message.conversation)
    
def is_int_number(arg):
    try: 
        int(arg)
        return True
    except ValueError:
        return False

'''
Prints help (how to use example)
'''
def show_help(message):
    answer = "*Pokemon*\n*Usage:* !pokemon [id]\n*Example:* !pokemon 1️"
    mac.send_message(answer, message.conversation)
    
    
'''
Downloads image from url
returns image file path
'''
def get_image(url, file_name):
    path = "app/assets/images/" + file_name
    file = open(path, 'wb')
    file.write(requests.get(url).content)
    file.close()
    return path