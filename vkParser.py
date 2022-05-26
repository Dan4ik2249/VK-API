import time
import requests
from config import *

token = mytoken
v = versApi
    
#получает инфу о пользователе по его id или короткому имени
def get_users(user_id): 
    name_field = 'about, activities, books, career, home_town, interests, last_seen, military, movies, music, occupation, online, personal, quotes, relatives, relation, sex, status, tv, universities'
    response = requests.get('https://api.vk.com/method/users.get', 
                            params = {'user_ids': user_id,
                                    'fields': name_field,
                                    'access_token': token,
                                    'v': v})
    
    last_user_info  = response.json()
    if 'response' in last_user_info:
        last_user_info = response.json()['response'][0] 
        global real_id
        real_id = last_user_info['id']
        return (last_user_info)
    else:
        error_code = response.json()['error']['error_code']
        error_msg = response.json()['error']['error_msg']
        print('Error', error_code)
        print(f'"{error_msg}"')
        return 0
    
    
 

#получает список групп на которые подписан пользователь
def get_user_groups(real_id):
    response = requests.get('https://api.vk.com/method/groups.get', 
                            params= {'user_id': real_id,
                            'extended': 0,
                            'access_token': token,
                            'v': v
                            })
    items_group = response.json()
    if 'response' in items_group:
        items_group = response.json()['response']['items']
        count_group = response.json()['response']['count']
        return (items_group, count_group)
    else:
        error_code = response.json()['error']['error_code']
        error_msg = response.json()['error']['error_msg']
        print('Error', error_code)
        print(f'"{error_msg}"')
        return 0
    
#получает доп информацию о полученных ранее группах
def get_info_to_group(owner_id):
    fields_name = 'activity, age_limits, city, contacts, description, members_count, status'
    response = requests.get('https://api.vk.com/method/groups.getById', 
                            params= {'group_id': owner_id,
                            'fields': fields_name,
                            'access_token': token,
                            'v': v
                            })
    
    info_to_group = response.json()
    
    if 'response' in info_to_group:
        info_to_group = response.json()['response'][0]
        return (info_to_group)
    else:
        error_code = response.json()['error']['error_code']
        error_msg = response.json()['error']['error_msg']
        print('Error', error_code)
        print(f'"{error_msg}"')
        return 0


#анализ активност пользователя в группах(выводит количество лайков пользователя в группах)
def group_analysis(owner_id, c_1):
    analysis_group_likes = {}
     
    response = requests.get('https://api.vk.com/method/wall.get',
                             params={'owner_id': -owner_id,
                            'count': c_1,
                            'offset': 0,
                            'extended' : 1,
                            'access_token': token,
                             'v': v
                             })
    info_for_posts = response.json()
        
    if 'response' in info_for_posts: 
        info_for_posts = response.json()['response']['items']
        response = None
    else:
        error_code = response.json()['error']['error_code']
        error_msg = response.json()['error']['error_msg']
        print('Error', error_code)
        print(f'"{error_msg}"')
        
    likes_counter = 0
    k = 0
    for i in info_for_posts:
        item_id = info_for_posts[k]['id']
        response = requests.get('https://api.vk.com/method/likes.isLiked',
                                    params={'user_id': real_id,
                                    'type': 'post',
                                    'owner_id': -owner_id,
                                    'item_id': item_id,
                                    'access_token': token,
                                    'v': v
                                    })
        likes = response.json()['response']['liked']
        if likes == 1:
            likes_counter = likes_counter + 1
        k = k + 1
        time.sleep(0.3)

    analysis_group_likes[f'{owner_id}'] = likes_counter
    del info_for_posts
    time.sleep(0.3)
    
    return(analysis_group_likes)

def friends_get(real_id):
    response = requests.get('https://api.vk.com/method/friends.get',
                            params = {'user_id': real_id,
                            'access_token': token,
                            'v': v    
                            })
    get_friends = response.json()
    if 'response' in get_friends:
        get_friends = response.json()['response']['items']
        count_friends = response.json()['response']['count']
        return(get_friends, count_friends)
    else:
        error_code = response.json()['error']['error_code']
        error_msg = response.json()['error']['error_msg']
        print('Error', error_code)
        print(f'"{error_msg}"')
        return 0


def friends_analysis(friend_id, d_1):
    analysis_friend_likes = {}
    response = requests.get('https://api.vk.com/method/wall.get',
                            params={'owner_id': friend_id,
                            'count': d_1,
                            'offset': 0,
                            'extended' : 1,
                            'access_token': token,
                             'v': v
                             })
    friend_post = response.json()
        
    if 'response' in friend_post: 
        friend_post = response.json()['response']['items']
        response = None
    else:
        error_code = response.json()['error']['error_code']
        error_msg = response.json()['error']['error_msg']
        print('Error', error_code)
        print(f'"{error_msg}"')
  
    likes_counter = 0
    k = 0
    for i in friend_post:
        item_id = friend_post[k]['id']
        response = requests.get('https://api.vk.com/method/likes.isLiked',
                                    params={'user_id': real_id,
                                    'type': 'post',
                                    'owner_id': friend_id,
                                    'item_id': item_id,
                                    'access_token': token,
                                    'v': v
                                    })
        likes = response.json()
        
        if 'response' in likes: 
            likes = response.json()['response']['liked']
        else:
            error_code = response.json()['error']['error_code']
            error_msg = response.json()['error']['error_msg']
            print('Error', error_code)
            print(f'"{error_msg}"')
            continue
            
        if likes == 1:
            likes_counter = likes_counter + 1
        k = k + 1
        time.sleep(0.3)

    analysis_friend_likes[f'{friend_id}'] = likes_counter
    return (analysis_friend_likes)

    
def main():
    if token == '':
        print('Error: Введите токен доступа в файле config.py чтобы продолжить.')
        return 0
    if v == '':
        print('Error: Введите версию используемого API в файле config.py чтобы продолжить.')
        return 0
    
    a = input('Введите ссылку на пользователя: ')
    if a.find('/') != -1:
        user_id = a.split('/')[3]
    else:
        user_id = a
        
    get_users(user_id)
    
    print('Выберите, что искать')
    print('1. Сбор информации о пользователе')
    print('2. Сбор информации о группе')
    print('3. Анализ активности пользователя в группе(максисум за 100 последних постов)')
    print('4. Анализ активности пользователя на странице друга')
    print('0. Выход')
    
    choise = input()
    
    if (choise != '1' and choise != '2' and choise != '3' and choise != '4' and choise != '0'):
       while (choise != '1' and choise != '2' and choise != '3' and choise != '4' and choise != '0'):
            print('Error: Выберите пункт из списка')
            choise = input()
            
    while choise != 0:
        match choise:
            
            case '1':
                print(get_users(user_id))
                print()
                items, count = get_user_groups(real_id)
                print('Колчество подписок: ', count)
                print()
                print('Группы на которые подписан пользователь: \n', items)
                print()
        
                choise = input()
                
                
            case '2':
                g = input('Введите ссылку или id группы: ')
                if g.find('/') != -1:
                    group_id = g.split('/')[3]
                else:
                    group_id = g
                info_group = get_info_to_group(group_id)
                print(info_group)
                int(group_id)
                print()
                print('Ссылка на группу: ')
                print('https://vk.com/' + info_group['screen_name'])
                print()
                
                choise = input()
        
        
            case '3':
                group_id = int(input('Введите id группы: '))
                
                c = int(input('Выберите количество последних постов, которые необходимо проверть на отметку нравится(до 100): '))
                
                while c > 100:
                    print('Error: максимальное число записей 100')
                    c = int(input('Выберите количество последних постов, которые необходимо проверть на отметку нравится(до 100): '))
                    
                likes = group_analysis(group_id, c)
                if likes[f'{group_id}'] == 1:
                    print('Пользователь оценил: ', likes[f'{group_id}'], ' запись.')
                elif 2<= likes[f'{group_id}'] <=4:
                    print('Пользователь оценил: ', likes[f'{group_id}'], ' записи.')
                else:
                    print('Пользователь оценил: ', likes[f'{group_id}'], ' записей.')
                    
                print()
                
                choise = input()
            
            
            case '4':
                friend_id = int(input('Введите id человека: '))
                
                d = int(input('Выберите количество последних постов, которые необходимо проверть на отметку нравится(до 100): '))
                
                while d > 100:
                    print('Error: максимальное число записей 100')
                    d = int(input('Выберите количество последних постов, которые необходимо проверть на отметку нравится(до 100): '))
                    
                likes_friend = friends_analysis(friend_id, d)
                if likes_friend[f'{friend_id}'] == 1:
                    print('Пользователь оценил: ', likes_friend[f'{friend_id}'], ' запись.')
                elif 2<= likes_friend[f'{friend_id}'] <=4:
                    print('Пользователь оценил: ', likes_friend[f'{friend_id}'], ' записи.')
                else:
                    print('Пользователь оценил: ', likes_friend[f'{friend_id}'], ' записей.')
                    
                print()
                
                choise = input()
            
                
            case '0':
                print()
                print('Спасибо за использование;)')
                break
            
            
#https://vk.com/danilshulgin
#57143976
#115066430
#https://vk.com/dnlshlgn
if __name__=="__main__":
    main()