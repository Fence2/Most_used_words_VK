from modules.console import *
import modules.vk_module as vk
import modules.parser as parser

if __name__ == '__main__':
    my_id = vk.MY_ID
    help = """"""
    # if parser.select_conversations_from_file(my_id=1):
    #     print("YES")
    # else:
    #     print("NO")
    print_conversations(vk.get_conversations_from_file())
