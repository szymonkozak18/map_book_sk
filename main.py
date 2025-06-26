from tkinter import *

import tkintermapview

users: list = []


class User:
    def __init__(self, name, surname, location, post):
        self.name = name
        self.surname = surname
        self.location = location
        self.post = post
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1])

    def get_coordinates(self) -> list:
        import requests
        from bs4 import BeautifulSoup
        url = f"https://pl.wikipedia.org/wiki/{self.location}"
        response = requests.get(url).text
        response_html = BeautifulSoup(response, "html.parser")
        longitude = float(response_html.select(".longitude")[1].text.replace(",", "."))
        latitude = float(response_html.select(".latitude")[1].text.replace(",", "."))
        print(longitude, latitude)
        return [latitude, longitude]


def add_user():
    zmienna_imie = entry_name.get()
    zmienna_nazwisko = entry_surname.get()
    zmienna_miejscowosc = entry_locaction.get()
    zmienna_post = entry_post.get()
    user = User(name=zmienna_imie, surname=zmienna_nazwisko, location=zmienna_miejscowosc, post=zmienna_post)
    users.append(user)

    entry_name.delete(0, END)
    entry_surname.delete(0, END)
    entry_locaction.delete(0, END)
    entry_post.delete(0, END)

    entry_name.focus()

    show_users()


def show_users():
    listbox_lista_obiektow.delete(0, END)
    for idx, user in enumerate(users):
        listbox_lista_obiektow.insert(idx, f'{idx + 1}. {user.name} {user.surname}')


def remove_user():
    i = listbox_lista_obiektow.index(ACTIVE)
    users[i].marker.delete()
    users.pop(i)
    show_users()


def edit_user():
    i = listbox_lista_obiektow.index(ACTIVE)
    name = users[i].name
    surname = users[i].surname
    location = users[i].location
    post = users[i].post

    entry_name.insert(0, name)
    entry_surname.insert(0, surname)
    entry_locaction.insert(0, location)
    entry_post.insert(0, post)

    button_dodaj_obiekt.config(text='zapisz', command=lambda: update_user(i))


def update_user(i):
    new_name = entry_name.get()
    new_surname = entry_surname.get()
    new_location = entry_locaction.get()
    new_post = entry_post.get()

    users[i].name = new_name
    users[i].surname = new_surname
    users[i].location = new_location
    users[i].post = new_post

    users[i].marker.delete()
    users[i].coordinates = users[i].get_coordinates()
    users[i].marker = map_widget.set_marker(users[i].coordinates[0], users[i].coordinates[1])

    entry_name.delete(0, END)
    entry_surname.delete(0, END)
    entry_locaction.delete(0, END)
    entry_post.delete(0, END)
    entry_name.focus()

    button_dodaj_obiekt.config(text='Dodaj uzytkownika', command=add_user)
    show_users()


def show_user_details():
    i = listbox_lista_obiektow.index(ACTIVE)
    name = users[i].name
    surname = users[i].surname
    location = users[i].location
    post = users[i].post
    label_szczegoly_name_wartosc.config(text=name)
    label_szczegoly_surname_wartosc.config(text=surname)
    label_szczegoly_location_wartosc.config(text=location)
    label_szczegoly_post_wartosc.config(text=post)

    map_widget.set_position(users[i].coordinates[0], users[i].coordinates[1])
    map_widget.set_zoom(15)


root = Tk()
root.geometry('1200x760')
root.title("map book SD")

ramka_lista_obiektow = Frame(root)
ramka_formularz = Frame(root)
ramka_szczegoly_obiektow = Frame(root)
ramka_mapa = Frame(root)
ramka_lista_obiektow.grid(row=0, column=0)
ramka_formularz.grid(row=0, column=1)
ramka_szczegoly_obiektow.grid(row=1, column=0, columnspan=2)  # colorspam= rozciagnięcie
ramka_mapa.grid(row=2, column=0, columnspan=2)

# ramka_lista_obiektow
label_lista_obiektow = Label(ramka_lista_obiektow, text="lista użytkowników")
label_lista_obiektow.grid(row=0, column=0)
listbox_lista_obiektow = Listbox(ramka_lista_obiektow, width=50, height=10)
listbox_lista_obiektow.grid(row=1, column=0, columnspan=3)
button_pokaz_szczegoly_obiektu = Button(ramka_lista_obiektow, text="Pokaż szczegóły", command=show_user_details)
button_pokaz_szczegoly_obiektu.grid(row=2, column=0)
button_usun_obiekt = Button(ramka_lista_obiektow, text="Usuń użytkownika", command=remove_user)
button_usun_obiekt.grid(row=2, column=1)
button_edytuj_obiekt = Button(ramka_lista_obiektow, text="Edytuj użytkownika", command=edit_user)
button_edytuj_obiekt.grid(row=2, column=2)

# ramka_formularz
label_formularz = Label(ramka_formularz, text="Formularz")
label_formularz.grid(row=0, column=0, columnspan=2)
label_name = Label(ramka_formularz, text="Imie")
label_name.grid(row=1, column=0, sticky=W)
label_surname = Label(ramka_formularz, text="Nawisko")
label_surname.grid(row=2, column=0, sticky=W)
label_locaction = Label(ramka_formularz, text="Miejscowość ")
label_locaction.grid(row=3, column=0, sticky=W)
label_post = Label(ramka_formularz, text="Ilość postów ")
label_post.grid(row=4, column=0)

entry_name = Entry(ramka_formularz)
entry_name.grid(row=1, column=1)
entry_surname = Entry(ramka_formularz)
entry_surname.grid(row=2, column=1)
entry_locaction = Entry(ramka_formularz)
entry_locaction.grid(row=3, column=1)
entry_post = Entry(ramka_formularz)
entry_post.grid(row=4, column=1)

button_dodaj_obiekt = Button(ramka_formularz, text="Dodaj użytkownika", command=add_user)
button_dodaj_obiekt.grid(row=5, column=0, columnspan=2)

# ramka_szczegoly_obiektu
label_szczegoly_obiektow = Label(ramka_szczegoly_obiektow, text="Szczegóły obiektu")
label_szczegoly_obiektow.grid(row=0, column=0)
label_szczegoly_name = Label(ramka_szczegoly_obiektow, text="Imie")
label_szczegoly_name.grid(row=1, column=0)
label_szczegoly_name_wartosc = Label(ramka_szczegoly_obiektow, text="....")
label_szczegoly_name_wartosc.grid(row=1, column=1)
label_szczegoly_surname = Label(ramka_szczegoly_obiektow, text="Nazwisko")
label_szczegoly_surname.grid(row=1, column=2)
label_szczegoly_surname_wartosc = Label(ramka_szczegoly_obiektow, text="....")
label_szczegoly_surname_wartosc.grid(row=1, column=3)
label_szczegoly_location = Label(ramka_szczegoly_obiektow, text="Miejscowość")
label_szczegoly_location.grid(row=1, column=4)
label_szczegoly_location_wartosc = Label(ramka_szczegoly_obiektow, text="....")
label_szczegoly_location_wartosc.grid(row=1, column=5)
label_szczegoly_post = Label(ramka_szczegoly_obiektow, text="Posty")
label_szczegoly_post.grid(row=1, column=6)
label_szczegoly_post_wartosc = Label(ramka_szczegoly_obiektow, text="....")
label_szczegoly_post_wartosc.grid(row=1, column=7)

# ramka_mapa
map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1200, height=500, corner_radius=5)
map_widget.grid(row=0, column=0, columnspan=2)
map_widget.set_position(52.23, 21.0)
map_widget.set_zoom(6)

root.mainloop()

















