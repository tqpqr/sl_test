import hashlib #для получения хэша
import requests #для запроса к Gravatar
import json #для работы с json форматом


url = 'https://ru.gravatar.com/'
email='example@mail.ru'

# Будем исходить из отсутствия необходимости валидации e-mail.

def grav_changer(email):
    # Получаем MD5 хэш с помощью hashlib
    email_hash = hashlib.md5(email.encode('utf-8')).hexdigest()
    #print(email_hash)

    # Направляем запрос, чтобы получить .json от Gravatar
    r = requests.get(url+email_hash+'.json')
    print(r.text)

    # Простая замена работая со строкой:
    r_changed = r.text.replace('hash', 'email_hash').replace('profileUrl', 'url').replace('preferredUsername', 'alias').replace('thumbnailUrl','thumb').replace('name', 'person').replace('currentLocation', 'location')
    r_jsoned = json.loads(r_changed)
    #print(r_jsoned)
    # Добавляем e-mail, которого нет в явном виде в ответе от Gravatar
    r_jsoned['entry'][0]['email']=email
    #print(r_jsoned['entry'])
    # Собираем всё в требуемом виде
    res = {"result":r_jsoned['entry'][0]}
    return res

# Более сложная замена с json (замену нельзя производить сразу в самом словаре -
# нужно работать с его копией, иначе при смене ключа Python справедливо будет
# ругаться):
def grav_changer_json(email):
    # Аналогично получаем хэш и отправляем запрос
    email_hash = hashlib.md5(email.encode('utf-8')).hexdigest()
    r = requests.get(url+email_hash+'.json')
    # загружаем json для работы с ним
    r_jsoned = json.loads(r.text)
    # Составляем словарик с тем, что на что меняется:
    changes = {'id':'id',
               'photos':'photos',
               'emails':'emails',
               'accounts':'accounts',
               'urls':'urls',
               'requestHash':'requestHash',
               'displayName':'displayName',
               'hash':'email_hash',
               'profileUrl':'url',
               'preferredUsername':'alias',
               'thumbnailUrl':'thumb',
               'name' : 'person',
               'currentLocation' : 'location'}
    result = {'result':dict((changes[key], value) for (key,value) in r_jsoned['entry'][0].items())}
    #Не забываем добавить 'email'
    result['result']['email']=email
    return result

# Если нас интересует чёткий порядок ключей в .json (мы работаем с версией
# Python > 3.7, словарь у нас упорядочен и требования к порядку ключей жесткие)
def grav_changer_ordered(email):
    # Аналогично получаем хэш и отправляем запрос
    email_hash = hashlib.md5(email.encode('utf-8')).hexdigest()
    r = requests.get(url+email_hash+'.json')
    # загружаем json для работы с ним
    r_jsoned = json.loads(r.text)
    # А теперь прямо указываем что и куда ставим:
    res = {'result':{
            'id':r_jsoned['entry'][0]['id'],
            'email':email,
            'email_hash':r_jsoned['entry'][0]['hash'],
            'person':r_jsoned['entry'][0]['name'],
            'url':r_jsoned['entry'][0]['profileUrl']}}
            # ...и так далее.
    return res


print(grav_changer(email))
print(grav_changer_json(email))
print(grav_changer_ordered(email))
