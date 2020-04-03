from pathlib import Path


def create_directory():  # creare una cartella
    Path("Decks").mkdir(parents=True, exist_ok=True)


def decks_path():
    basepath = Path("Decks")
    return basepath


def show_main_menu():
    menu = """   ---
0) Exit
1) View all decks
2) Collection
3) Add Deck
4) Delete Deck
5) Modern Decks
6) Pionner Decks
7) Modify
8) Search
   ---"""
    print(menu)


def exit_mode():
    print("0) Exit")


def show_menu1():
    while True:
        exit_mode()
        print_deck_index(read_decks_from_disk())
        choose = scelta_utente()
        if choose == 0:
            break
        elif choose > 0:
            print("mazzo non ancora disponibile")


def scelta_utente():
    while True:
        try:
            return int(input("\ncosa scegli? "))
        except ValueError:
            print("Problema: carettere non disponibile inserire solo numeri")


def add_deck():  # creare un file e aggiungere mazzo,formato,prezzo uno per linea
    my_deck = {}

    while True:
        insert_deck = input("Inserisci il nome del mazzo: ").title()
        my_deck["nome"] = insert_deck

        legal_format = ["Modern", "Standard", "Pioneer", "Legacy", "Vintage", "Commander", "Pauper"]
        print("\nI Formati disponibili sono:")
        for index, deck in enumerate(legal_format, 1):
            print(str(index) + ')', deck)

        try:
            add_format = int(input("Inserisci il formato: "))
        except ValueError:
            print("Problema: inseriere solo numeri")
            continue

        for index, deck in enumerate(legal_format, 1):
            if index == add_format:
                my_deck["formato"] = deck
                break
        else:
            print("Formato non disponibile")
            continue

        print("Il valore del mazzo non può essere 0")
        try:
            add_price = int(input("Inserisci valore del mazzo: "))
        except ValueError:
            print("Problema: inseriere solo numeri")
            continue
        if add_price > 0:
            my_deck["prezzo"] = add_price
        else:
            print("Prezzo non Valido")
            continue

        # basepath = decks_path()
        #
        # i = 0
        # while basepath.joinpath(my_deck['nome'] + str(i)).exists():
        #     i += 1

        with open(incrementing_filename(my_deck["nome"]), "w") as file:
            file.write(f"{my_deck['nome']}\n{my_deck['formato']}\n{my_deck['prezzo']}")
        # with open(basepath.joinpath(my_deck["nome"] + str(i)), "w") as file:
        #     file.write(f"{my_deck['nome']}\n{my_deck['formato']}\n{my_deck['prezzo']}")

        break


def incrementing_filename(nome):
    basepath = decks_path()
    i = 1
    if not basepath.joinpath(nome).exists():
        return basepath.joinpath(nome)
    else:
        while basepath.joinpath(nome + str(i)).exists():
            i += 1
        return basepath.joinpath(nome + str(i))


def read_decks_from_disk():  # leggere un file e aggiungere a un dizionario le 3 linee
    deck_list = []
    basepath = decks_path()

    for filename in basepath.iterdir():
        if filename.is_file():
            with filename.open() as file:
                deck_info = file.read().splitlines()
                d = {
                    "nome_file": filename.name,
                    "nome": deck_info[0],
                    "formato": deck_info[1],
                    "prezzo": deck_info[2]
                }
            deck_list.append(d)

    return deck_list


def print_deck_index(decks):  # printare i mazzi con l'indice
    for index, deck in enumerate(decks, 1):
        print(f"{index}) nome: {deck['nome']}, formato: {deck['formato']}, prezzo: {deck['prezzo']}")
    print("---")


def print_deck_no_index(decks):  # printare mazzi senza indice
    for deck in decks:
        print(f"nome: {deck['nome']}, formato: {deck['formato']}, prezzo: {deck['prezzo']}")
    print("---")


def remove_deck():  # rimuovere un file dalla cartella in base al numero del mazzo sul display
    while True:
        print("\nLista dei mazzi disponibili")
        exit_mode()
        decks = read_decks_from_disk()
        print_deck_index(decks)
        try:
            index = int(input('scegli il mazzo il mazzo da cancellare: '))
            if index == 0:
                return
            deck_to_be_deleted = decks[index - 1]
        except IndexError as e:
            print('il mazzo non esiste!', e)
        else:
            basepath = decks_path()
            full_file_path = basepath.joinpath(deck_to_be_deleted["nome_file"])
            full_file_path.unlink()


def choose_format_deck(decks, formato):  # printare i mazzi in base al formato
    my_list = []
    for deck in decks:
        if deck["formato"] == formato:
            my_list.append(deck)
    return my_list


def searched_word(decks, choose):  # printare i mazzi n base alla parola scelta
    my_list = []
    for deck in decks:
        if choose in deck["nome"]:
            my_list.append(deck)
        elif choose in deck["formato"]:
            my_list.append(deck)
        elif choose in deck["prezzo"]:
            my_list.append(deck)
    return my_list


def choose_deck(decks):
    index = int(input("mazzo da scegliere:"))
    if index == 0:
        return index

    try:
        print_deck_no_index([decks[index - 1]])
        return decks[index - 1]
    except IndexError as err:
        print("mazzo non disponibile", err)


def choose_field_to_edit():
    print("""1) Nome Mazzo
2) Formato
3) Prezzo""")
    question = int(input("Quale campo modificare: "))
    return question


def edit_name(deck):
    basepath = decks_path()
    question1 = input("Rinnominare il mazzo: ").title()
    with basepath.joinpath(deck["nome_file"]).open() as file:
        data = file.readlines()
        data[0] = question1 + "\n"
    with basepath.joinpath(deck["nome_file"]).open("w") as file1:
        file1.writelines(data)

    new_name = incrementing_filename(question1)  # rinnominare il nome del file
    basepath.joinpath(deck["nome_file"]).rename(new_name)


def modity_format(deck):
    basepath = decks_path()
    legal_formats = ["Modern", "Standard", "Pioneer", "Legacy", "Vintage", "Commander", "Pauper"]
    print("\nI Formati disponibili sono:")
    for i, legal_format in enumerate(legal_formats, 1):  # itera tutti i formati di sponibli
        print(str(i) + ')', legal_format)  # me li stampa
    question2 = int(input("Scegliere formato: "))  # quale formato devo sceglire

    try:
        if legal_formats[question2 - 1]:
            with basepath.joinpath(deck["nome_file"]).open() as file:
                data = file.readlines()
                data[1] = legal_formats[question2 - 1] + "\n"
            with basepath.joinpath(deck["nome_file"]).open("w") as file1:
                file1.writelines(data)
    except IndexError as err:
        print("formato non disponibile", err)


def edit_price(deck):
    basepath = decks_path()
    question3 = input("Modificare prezzo: ")
    with basepath.joinpath(deck["nome_file"]).open() as file:
        data = file.readlines()
        data[2] = question3 + "\n"
    with basepath.joinpath(deck["nome_file"]).open("w") as file1:
        file1.writelines(data)


def modify_name():  # modificare il nome del file, nome del mazzo, formato o il prezzo, bisogna capire come uscire
    while True:
        print("\nLista dei mazzi disponibili")
        exit_mode()
        decks = read_decks_from_disk()
        print_deck_index(decks)
        deck = choose_deck(decks)
        if deck == 0:
            return
        if deck:
            modify_choice = choose_field_to_edit()
            # modifico parametro
            if modify_choice == 1:

                edit_name(deck)
            elif modify_choice == 2:

                modity_format(deck)
            elif modify_choice == 3:
                edit_price(deck)

            else:
                print("campo non disponibile")


def looking_for_a_word():  # cercare una parola specifica in ogni file e printare le varie info
    while True:
        word = input("Digitare cosa cercare: ").lower()
        basepath = decks_path()
        for file in basepath.iterdir():
            if file.is_file():
                with file.open() as deck:
                    if word == "Exit" or word == "exit" or word == "EXIT":
                        return
                    elif word in deck.read():
                        decks = read_decks_from_disk()
                        show = searched_word(decks, word)
                        return print_deck_index(show)
        else:
            print("nessuna riscontro trovato")


def elabora_scelta_utente(choose):
    if choose == 1:
        show_menu1()
    elif choose == 2 or choose > 9:
        print("scelta al momento non disponibile")
    elif choose == 3:
        add_deck()
    elif choose == 4:
        remove_deck()
    elif choose == 5:
        decks = read_decks_from_disk()
        format_modern = choose_format_deck(decks, "Modern")
        print_deck_index(format_modern)
    elif choose == 6:
        decks = read_decks_from_disk()
        format_pioneer = choose_format_deck(decks, "Pioneer")
        print_deck_index(format_pioneer)
    elif choose == 7:
        modify_name()
    elif choose == 8:
        looking_for_a_word()
    elif choose == 9:
        print(read_decks_from_disk())


while True:
    create_directory()
    show_main_menu()
    scelta = scelta_utente()
    if scelta == 0:
        break
    else:
        elabora_scelta_utente(scelta)
