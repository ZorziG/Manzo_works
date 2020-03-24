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
7) Name modify
8) Search
   ---"""
    print(menu)


def exit_mode():
    print("0) Exit")


def show_menu1():
    while True:
        print_deck(read_decks_from_disk())
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
    legal_format = ["Modern", "Standard", "Pioneer", "Legacy", "Vintage", "Commander", "Pauper"]
    print("\nI Formati disponibili sono:")
    for index, deck in enumerate(legal_format, 1):
        print(str(index) + ')', deck)

    print("Il mazzo non può valere 0")
    while True:
        insert_deck = input("Inserisci il nome del mazzo: ").title()
        my_deck["nome"] = insert_deck

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
    exit_mode()
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


def print_deck(decks):
    for index, deck in enumerate(decks, 1):
        print(f"{index}) nome: {deck['nome']}, formato: {deck['formato']}, prezzo: {deck['prezzo']}")
    print("---")


def remove_deck():
    while True:
        print("\nLista dei mazzi disponibili")
        decks = read_decks_from_disk()
        print_deck(decks)
        #           REMOVE BY NAME
        deck_folder = Path("Decks\\")
        delete_deck = input("\nInserisci il numero per togliere il mazzo: ")  # aggiungere int se lo rimetto come prima
        delete_deck = delete_deck.title()
        for deck in deck_folder.iterdir():
            if deck.is_file():
                if deck.name == delete_deck:
                    deck.unlink()
                    break
                elif "0" == delete_deck:
                    return
        else:
            print("Mazzo non disponibile")

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


def choose_deck(decks, formato):
    my_list = []
    for deck in decks:
        if deck["formato"] == formato:
            my_list.append(deck)
    return my_list


def modify_name():
    print("\nLista dei mazzi disponibili")
    decks = read_decks_from_disk()
    print_deck(decks)
    deck = input("Mazzo da modificare: ").title()
    new_deck = input("Nuovo nome del mazzo: ").title()
    basepath = Path("Decks\\")
    for file in basepath.iterdir():
        if file.is_file():
            if file == deck:  # problema da qua
                file.rename(new_deck)
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
        format_modern = choose_deck(decks, "Modern")
        print_deck(format_modern)
    elif choose == 6:
        decks = read_decks_from_disk()
        format_pioneer = choose_deck(decks, "Pioneer")
        print_deck(format_pioneer)
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
