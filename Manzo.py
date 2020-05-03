from pathlib import Path
import uuid


def create_directory():  # creare una cartella
    Path("Decks").mkdir(parents=True, exist_ok=True)
    Path("Tournaments").mkdir(parents=True, exist_ok=True)


def tournaments_path():
    return Path("Tournaments")


def decks_path():
    return Path("Decks")


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
9) Enter deck result
10) View all tournament
11) Remove Tournament
   ---"""
    print(menu)


def exit_mode():
    print("0) Exit")


def show_menu1():
    while True:
        exit_mode()
        decks = read_decks_from_disk()
        print_deck_index(decks)
        tournament_path = tournaments_path()
        tournament = read_tournament_from_disk()
        deck = choose_deck(decks)
        if deck == 0:
            return
        elif deck:
            if tournament_path.joinpath(deck["nome_file"]).exists():
                print_tournament(tournament, decks)  # devo trovare il modo di printare solo queli scelti


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

        while True:
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
            break

        while True:
            print("Il valore del mazzo non può essere 0")
            try:
                add_price = int(input("Inserisci valore del mazzo: "))
            except ValueError:
                print("Problema: inseriere solo numeri")
                continue
            if add_price > 0:
                my_deck["prezzo"] = add_price
                break
            else:
                print("Prezzo non Valido")
                continue

        with open(deck_filename(my_deck["nome"]), "w") as file:
            file.write(f"{my_deck['nome']}\n{my_deck['formato']}\n{my_deck['prezzo']}")

        break


def deck_filename(nome):
    deck_path = decks_path()
    random_name = str(uuid.uuid4())
    right_name = nome + "_" + random_name
    return deck_path.joinpath(right_name)


def incrementing_tournament_filename(nome):
    tournament_path = tournaments_path()
    i = 1
    if not tournament_path.joinpath(nome).exists():
        return tournament_path.joinpath(nome)
    else:
        while tournament_path.joinpath(nome + "_" + str(i)).exists():
            i += 1
        return tournament_path.joinpath(nome + "_" + str(i))


def read_decks_from_disk():  # leggere un file e aggiungere a un dizionario le 3 linee
    deck_list = []
    deck_path = decks_path()

    for filename in deck_path.iterdir():
        if filename.is_file():
            with filename.open() as file:
                deck_info = file.read().splitlines()
                d = {
                    "nome_file": filename.name,
                    "nome": deck_info[0],
                    "formato": deck_info[1],
                    "prezzo": deck_info[2],
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
            deck_path = decks_path()
            full_file_path = deck_path.joinpath(deck_to_be_deleted["nome_file"])
            full_file_path.unlink()


def remove_tournament():
    while True:
        print("\nLista dei mazzi disponibili")
        exit_mode()
        decks = read_decks_from_disk()
        tournament = read_tournament_from_disk()
        print_tournament_with_index(tournament, decks)
        try:
            index = int(input('scegli il mazzo il mazzo da cancellare: '))
            if index == 0:
                return
            tournament_to_be_deleted = tournament[index - 1]
        except IndexError as e:
            print('il mazzo non esiste!', e)
        else:
            tournament_path = tournaments_path()
            full_file_path = tournament_path.joinpath(tournament_to_be_deleted["nome_file"])
            full_file_path.unlink()


def choose_format_deck(decks, formato):  # printare i mazzi in base al formato
    my_list = []
    for deck in decks:
        if deck["formato"] == formato:
            my_list.append(deck)
    return my_list


def choose_deck(decks):
    index = int(input("mazzo da scegliere:"))
    if index == 0:
        return index
    try:
        return decks[index - 1]
    except IndexError as err:
        print("mazzo non disponibile", err)


def choose_deck_with_print(decks):
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
    deck_path = decks_path()
    question1 = input("Rinnominare il mazzo: ").title()
    with deck_path.joinpath(deck["nome_file"]).open() as file:
        data = file.readlines()
        data[0] = question1 + "\n"
    with deck_path.joinpath(deck["nome_file"]).open("w") as file1:
        file1.writelines(data)

        # rinnominare il nome file
    # new_name = incrementing_deck_filename(question1)
    # deck_path.joinpath(deck["nome_file"]).rename(new_name)


def edit_format(deck):
    deck_path = decks_path()
    legal_formats = ["Modern", "Standard", "Pioneer", "Legacy", "Vintage", "Commander", "Pauper"]
    print("\nI Formati disponibili sono:")
    for i, legal_format in enumerate(legal_formats, 1):  # itera tutti i formati di sponibli
        print(str(i) + ')', legal_format)  # me li stampa
    question2 = int(input("Scegliere formato: "))  # quale formato devo sceglire

    try:
        if legal_formats[question2 - 1]:
            with deck_path.joinpath(deck["nome_file"]).open() as file:
                data = file.readlines()
                data[1] = legal_formats[question2 - 1] + "\n"
            with deck_path.joinpath(deck["nome_file"]).open("w") as file1:
                file1.writelines(data)
    except IndexError as err:
        print("formato non disponibile", err)


def edit_price(deck):
    deck_path = decks_path()
    question3 = input("Modificare prezzo: ")
    with deck_path.joinpath(deck["nome_file"]).open() as file:
        data = file.readlines()
        data[2] = question3 + "\n"
    with deck_path.joinpath(deck["nome_file"]).open("w") as file1:
        file1.writelines(data)


def modify_info():  # modificare il nome del file, nome del mazzo, formato o il prezzo, bisogna capire come uscire
    while True:
        print("\nLista dei mazzi disponibili")
        exit_mode()
        decks = read_decks_from_disk()
        print_deck_index(decks)
        deck = choose_deck_with_print(decks)
        if deck == 0:
            return
        if deck:
            modify_choice = choose_field_to_edit()
            if modify_choice == 1:
                edit_name(deck)
            elif modify_choice == 2:
                edit_format(deck)
            elif modify_choice == 3:
                edit_price(deck)
            else:
                print("campo non disponibile")


def searched_word(decks, choose):
    my_list = []
    for deck in decks:
        if choose in deck["nome"]:
            my_list.append(deck)
        elif choose in deck["formato"]:
            my_list.append(deck)
        elif choose in deck["prezzo"]:
            my_list.append(deck)

    return my_list


def looking_for_a_word():  # cercare una parola specifica in ogni file e printare le varie info
    while True:
        word = input("Digitare cosa cercare: ")
        deck_path = decks_path()
        for file in deck_path.iterdir():
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


def tournament_result(deck):
    tournament = {}
    while True:
        tournament_name = input("inserisci il nome del torneo: ").title()
        tournament["tournament_name"] = tournament_name

        while True:
            try:
                win, lose, tie = input("Inserire win-lose-tie:").split("-")
                win, lose, tie = int(win), int(lose), int(tie)
            except ValueError as err:
                print("formato disponibile è win-lose-tie: ", err)
                continue
            tournament["win"] = win
            tournament["lose"] = lose
            tournament["tie"] = tie
            break

        while True:
            try:
                position = int(input("Posizione finale del torneo: "))
            except ValueError as err:
                print("inserire solo numeri: ", err)
                continue
            tournament["position"] = position
            break

        with open(incrementing_tournament_filename(deck["nome_file"]), "w") as file:
            file.write(f"{tournament['tournament_name']}"
                       f"\n{tournament['win']}"
                       f"\n{tournament['lose']}"
                       f"\n{tournament['tie']}"
                       f"\n{tournament['position']}\n")

        break


def read_tournament_from_disk():
    tournament_path = tournaments_path()
    tournament_list = []
    for filename in tournament_path.iterdir():
        if filename.is_file():
            with filename.open() as file:
                tournament_info = file.read().splitlines()
                d = {
                    "nome_file": filename.name,
                    "torneo": tournament_info[0],
                    "win": tournament_info[1],
                    "lose": tournament_info[2],
                    "tie": tournament_info[3],
                    "posizione": tournament_info[4]
                }
                tournament_list.append(d)

    return tournament_list


def print_tournament(tornei, decks):
    for t in tornei:
        for d in decks:
            if d["nome_file"] in t["nome_file"]:
                print(f"torneo: {t['torneo']},"
                      f" win-lose-tie: {t['win']}-{t['lose']}-{t['tie']},"
                      f" prezzo: {t['posizione']},"
                      f" mazzo: {d['nome']} ")

    print("   ---")


def print_tournament_with_index(tornei, decks):
    for index, t in enumerate(tornei, 1):
        for d in decks:
            if d["nome_file"] in t["nome_file"]:
                print(f"{index})"
                      f"torneo: {t['torneo']},"
                      f" win-lose-tie: {t['win']}-{t['lose']}-{t['tie']},"
                      f" prezzo: {t['posizione']},"
                      f" mazzo: {d['nome']} ")

    print("   ---")


def elabora_scelta_utente(choose):
    if choose == 1:
        show_menu1()
    elif choose == 2 or choose > 16:
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
        modify_info()
    elif choose == 8:
        looking_for_a_word()
    elif choose == 9:
        decks = read_decks_from_disk()
        print_deck_index(decks)
        deck = choose_deck_with_print(decks)
        tournament_result(deck)
    elif choose == 10:
        decks = read_decks_from_disk()
        tournament = read_tournament_from_disk()
        print_tournament(tournament, decks)
    elif choose == 11:
        remove_tournament()


while True:
    create_directory()
    show_main_menu()
    scelta = scelta_utente()
    if scelta == 0:
        break
    else:
        elabora_scelta_utente(scelta)
