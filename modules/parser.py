from bs4 import BeautifulSoup
import os

def select_conversations_from_file(*, my_id, file=None):
    #TODO Написать doc-строку
    if file is None:
        files = list(filter(lambda x: x.endswith(".html"), os.listdir()))
        if len(files) == 0:
            print("Файл для извлечения ID бесед не найден.")
            return 0
        elif len(files) == 1:
            file = files[0]
        else:
            print("Выберите файл для извлечения ID бесед, написав его номер:")
            for i, file in enumerate(files):
                print(f"{i+1}) {file}")
            return select_conversations_from_file(my_id=my_id, file=files[int(input()) - 1])


    with open(file) as file, open(f"data/{my_id}_conversations_ids.txt", "w") as c_file:
        soup = BeautifulSoup(file, "lxml")
        for conv in soup.find("ul", {"id": "im_dialogs"}).find_all("li"):
            c_file.write(conv.get("data-list-id") + "\n")
    return 1
