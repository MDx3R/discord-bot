import requests

header = {'accept': 'application/json'}
url = 'http://127.0.0.1:8000/api'

def get_discord_users():
    response = requests.get(url + '/discord/users', headers=header)

    if response.status_code == 200:
        return response.json()

def get_discord_user(id):
    response = requests.get(url + '/discord/users/' + id, headers=header)

    if response.status_code == 200:
        return response.json()
    
def post_discord_user(id):
    query = {'id': id}
    response = requests.post(url + '/discord/users', headers=header, data=query)

    if response.status_code == 200:
        return response.json()   

def get_faceit_users():
    response = requests.get(url + '/faceit/users', headers=header)

    if response.status_code == 200:
        return response.json()

def get_faceit_user_by_id(id):
    response = requests.get(url + '/faceit/users/' + id, headers=header)

    if response.status_code == 200:
        return response.json()

def get_faceit_user_by_nickname(nickname):
    query = {'nickname': nickname}
    response = requests.get(url + '/faceit/users', headers=header, data=query)
    
    if response.status_code == 200:
        return response.json()

def post_faceit_user(id, nickname):
    query = {'id': id, 'nickname': nickname}
    response = requests.post(url + '/faceit/users', headers=header, data=query)

    if response.status_code == 200:
        return response.json()

def post_faceit_user_by_id(id):
    query = {'id': id}
    response = requests.post(url + '/faceit/users', headers=header, data=query)

    if response.status_code == 200:
        return response.json()

def post_faceit_user_by_nickname(nickname):
    query = {'nickname': nickname}
    response = requests.post(url + '/faceit/users', headers=header, data=query)

    if response.status_code == 200:
        return response.json() 
    
def patch_faceit_user_by_id(id):
    stats = get_unsaved_faceit_user_by_id(id)
    query = {'stats': stats if stats is not None else 0}
    response = requests.patch(url + '/faceit/users/' + id, headers=header, data=query)

    if response.status_code == 200:
        return response.json()

def get_unsaved_faceit_user_by_id(id):
    query = {'id': id}
    response = requests.get(url + '/faceit/unsaved/users', headers=header, data=query)   

    if response.status_code == 200:
        return response.json()

def get_unsaved_faceit_user_by_nickname(nickname):
    query = {'nickname': nickname}
    response = requests.get(url + '/faceit/unsaved/users', headers=header, data=query)

    if response.status_code == 200:
        return response.json()

def get_faceit_linked_users():
    response = requests.get(url + '/faceitlinked/users', headers=header)

    if response.status_code == 200:
        return response.json()
    
def get_faceit_linked_user_by_discord_id(id):
    query = {'discord_id': id}
    response = requests.get(url + '/faceitlinked/users', headers=header, data=query)

    if response.status_code == 200:
        return response.json()
    
def get_faceit_linked_user_by_faceit_id(id):
    query = {'faceit_id': id}
    response = requests.get(url + '/faceitlinked/users', headers=header, data=query)

    if response.status_code == 200:
        return response.json()
    
def get_faceit_linked_user_by_faceit_nickname(nickname):
    query = {'faceit_nickname': nickname}
    response = requests.get(url + '/faceitlinked/users', headers=header, data=query)

    if response.status_code == 200:
        return response.json()
    
def post_faceit_linked_user(discord_id, faceit_id):
    query = {'discord_id': discord_id, 'faceit_id': faceit_id}
    response = requests.post(url + '/faceitlinked/users', headers=header, data=query)

    if response.status_code == 200:
        return response.json()
    
def delete_faceit_linked_user_by_discord_id(id):
    query = {'discord_id': id}
    response = requests.delete(url + '/faceitlinked/users', headers=header, data=query)

    return response.status_code

def delete_faceit_linked_user_by_faceit_id(id):
    query = {'faceit_id': id}
    response = requests.delete(url + '/faceitlinked/users', headers=header, data=query)

    return response.status_code

def delete_faceit_linked_user_by_faceit_nickname(nickname):
    query = {'faceit_nickname': nickname}
    response = requests.delete(url + '/faceitlinked/users', headers=header, data=query)

    return response.status_code