from pathlib import Path


def create_directory():
    Path(".\\Decks\\").mkdir(parents=True, exist_ok=True)


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
        # elif choose == 1:
        #     with open("Decks\\jund.txt") as file:
        #         print(file.read())
        # elif choose == 2:
        #     with open("Decks\\Izzet.txt") as file:
        #         print(file.read())
        elif choose > 0:
            print("mazzo non ancora disponibile")


def scelta_utente():
    while True:
        try:
            return int(input("\ncosa scegli? "))
        except ValueError:
            print("Problema: carettere non disponibile inserire solo numeri")


def add_deck():
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

        with open("Decks\\" + my_deck["nome"], "w") as file:
            file.write(f"{my_deck['nome']}\n{my_deck['formato']}\n{my_deck['prezzo']}")

        break


def read_decks_from_disk():
    deck_list = []
    basepath = Path("Decks\\")

    for filename in basepath.iterdir():
        if filename.is_file():
            with filename.open() as file:
                deck_info = file.read().splitlines()
                d = {
                    "nome": deck_info[0],
                    "formato": deck_info[1],
                    "prezzo": deck_info[2]
                }
            deck_list.append(d)

    return deck_list


def print_deck_index(decks):
    for index, deck in enumerate(decks, 1):
        print(f"{index}) nome: {deck['nome']}, formato: {deck['formato']}, prezzo: {deck['prezzo']}")
    print("---")


def print_deck_no_index(decks):
    for deck in decks:
        print(f"nome: {deck['nome']}, formato: {deck['formato']}, prezzo: {deck['prezzo']}")
    print("---")


def remove_deck():
    while True:
        print("\nLista dei mazzi disponibili")
        exit_mode()
        decks = read_decks_from_disk()
        print_deck_index(decks)
        index = int(input('scegli il mazzo il mazzo: '))
        if index == 0:
            return
        try:
            deck_to_be_deleted = decks[index - 1]
        except IndexError as e:
            print('il mazzo non esiste!', e)
        else:
            full_file_path = Path('Decks\\' + deck_to_be_deleted['nome'])
            full_file_path.unlink()

    # while True:
    #     print("\nLista dei mazzi disponibili")
    #     exit_mode()
    #     decks = read_decks_from_disk()
    #     print_deck_index(decks)
    #     #           REMOVE BY NAME
    #     deck_folder = Path("Decks\\")
    #     delete_deck = input("\nInserisci il numero per togliere il mazzo: ")  # aggiungere int se lo rimetto come prima
    #     delete_deck = delete_deck.title()
    #     for deck in deck_folder.iterdir():
    #         if deck.is_file():
    #             if deck.name == delete_deck:
    #                 deck.unlink()
    #                 break
    #             elif "0" == delete_deck:
    #                 return
    #     else:
    #         print("Mazzo non disponibile")

    #       REMOVE BY INDEX
    # for index, filename in enumerate(deck_folder.iterdir(), 1):
    #     if filename.is_file():
    #         if index == delete_deck:
    #             filename.unlink()
    #             break
    #         elif 0 == delete_deck:
    #             break
    # else:
    #     print("mazzo non disponibile")


def choose_format_deck(decks, formato):
    my_list = []
    for deck in decks:
        if deck["formato"] == formato:
            my_list.append(deck)
    return my_list


def choose_1_deck(decks, number):
    my_list = []
    for index, deck in enumerate(decks, 1):
        if index == number:
            my_list.append(deck)
    return my_list


def modify_name():
    print("\nLista dei file disponibili")
    exit_mode()
    basepath = Path("Decks\\")

    for index, deck_file in enumerate(basepath.iterdir(), 1):
        if deck_file.is_file():
            print(str(index) + ")", deck_file.name)

    number_file = int(input("Inserire il numero del file da modificare: "))
    for index, deck_file in enumerate(basepath.iterdir(), 1):
        if deck_file.is_file():
            if 0 == number_file:
                return
            elif index == number_file:
                print(f"Nome del file: {deck_file.name} ")
                print("Info deck:")
                decks = read_decks_from_disk()
                deck_data = choose_1_deck(decks, index)
                print_deck_no_index(deck_data)
                print("""1) Nome File
2) Nome Mazzo
3) Formato
4) Prezzo"""
                      )
                question = int(input("Inserire numero per modifica: "))   # problemi con le lettere
                question2 = input("modifica da fare: ").title()  # .title() da sistemare se da problemi con i numeri
                if question == 1:
                    if index == number_file:
                        # a = Path("Decks\\" + deck_file.name)  # da sistemare
                        # print(a.cwd())
                        # a.replace(question2)
                        break
                    # se il file è = al numero selezionato
                    # file.name.replace(question2)
            #             # se si vuole modificare il nnome del file
            #         elif question == 2:
            #             # se si vuole modificare il nome deck
            #             pass
            #         elif question == 3:
            #             # se si vuole modificare il formato
            #             pass
            #         elif question == 4:
            #             # se si vule modificare il prezzo
            #             pass

    else:
        print("file non disponibile")
        return



def elabora_scelta_utente(choose):
    if choose == 1:
        show_menu1()
    elif choose == 2 or choose > 8:
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
        pass


while True:
    create_directory()
    show_main_menu()
    scelta = scelta_utente()
    if scelta == 0:
        break
    else:
        elabora_scelta_utente(scelta)
