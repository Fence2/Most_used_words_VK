from modules.console import *
import modules.vk_module as vk
import modules.parser as parser
from time import sleep

import modules.settings as settings

if __name__ == '__main__':
    main_acc = vk.Acc(settings.main)
    print_conversations(main_acc.conversations)
    print("\n\n")
    sleep(0.4)
    old_acc = vk.Acc(settings.old)
    print_conversations(old_acc.conversations)
