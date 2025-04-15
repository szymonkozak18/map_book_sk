

users:list=[
    {'name' :'maciej','location':'Łódź','posts':100},
    {'name' :'mateusz','location':'Poznań','posts':200},
    {'name' :'maciej01','location':'Siedlce','posts':300},
    {'name' :'konrad','location':'Grudziądz','posts':400}
]


def gets_user_info(users_data:list)->None:
    for user in users_data:
        print(f'twój znajomy {user['name']} z miejscowości {user["location"]} opublikował {user["posts"]} postów')

gets_user_info(users)