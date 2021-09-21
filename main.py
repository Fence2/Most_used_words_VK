from modules.console import *
import modules.vk_module as vk
import modules.parser as parser

if __name__ == '__main__':
    my_id = vk.MY_ID
    print_conversations(vk.get_conversations_from_file())