import random
import string
from faker import Faker

fake = Faker()


def mutate_url(url):
    # Генерируем новый URL
    new_url = fake.uri()
    return new_url


def mutate_method(method):
    # Список допустимых методов
    methods = ['GET', 'POST', 'PUT', 'DELETE']
    # Случайным образом выбираем другой метод
    while True:
        new_method = random.choice(methods)
        if new_method != method:
            break
    return new_method


def mutate_headers(headers):
    # Изменяем некоторые заголовки
    headers['Content-Type'] = random.choice(['application/json', 'application/x-www-form-urlencoded'])
    headers['User-Agent'] = fake.user_agent()
    return headers


def mutate_body(body):
    # Пример мутации тела запроса
    body_params = {
        'csrfmiddlewaretoken': fake.uuid4(),
        'newpass1': ''.join(random.choices(string.ascii_letters + string.digits, k=8)),
        'newpass2': ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    }
    new_body = "&".join([f"{k}={v}" for k, v in body_params.items()])
    return new_body.encode()


def mutate_status_code(status_code):
    # Возможные коды состояния
    status_codes = [200, 201, 400, 401, 403, 404, 500]
    # Выбираем случайно
    new_status_code = random.choice(status_codes)
    return str(new_status_code)


def mutate_response_headers(headers):
    # Изменяем заголовки ответа
    headers['Content-Type'] = random.choice(['text/html; charset=utf-8', 'application/json'])
    return headers


def augment_record(record, n_augmentations=100):
    augmented_records = []
    for _ in range(n_augmentations):
        mutated_record = record.copy()

        # Мутация полей
        mutated_record['request']['url'] = mutate_url(mutated_record['request']['url'])
        mutated_record['request']['method'] = mutate_method(mutated_record['request']['method'])
        mutated_record['request']['headers'] = mutate_headers(mutated_record['request']['headers'].copy())
        mutated_record['request']['body'] = mutate_body(mutated_record['request']['body'])
        #mutated_record['response']['status_code'] = mutate_status_code(mutated_record['response']['status_code'])
        mutated_record['response']['headers'] = mutate_response_headers(mutated_record['response']['headers'].copy())

        augmented_records.append(mutated_record)

    return augmented_records


# Пример использования
record = {
    'context_id': 102,
    'vulnerable': True,
    'request': {
        'url': '/users/changepass',
        'method': 'POST',
        'headers': {
            'Content-Length': '110',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'test:8000',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Referer': 'http://test:8000/users/changepass',
            'Cookie': 'csrftoken=dDNhwY8UKTqLrHn1QAUXurAh6N1OuSGq'
        },
        'body': b'csrfmiddlewaretoken=tGMEw5jcUAJdsOCyWSwquECCgBkLtvmqw9pLSThWujZOJlPpCigdOV2JcebpNdSG&newpass1=ZAP&newpass2=ZAP'
    },
    'control_flow': {
        0: 'context = { "navinfo": config[\'DEFAULT\'][\'CSRF\'] }',
        1: "if request.method == 'POST':",
        2: "password1 = request.POST.get('newpass1')",
        3: "password2 = request.POST.get('newpass2')",
        4: 'if (password1 == password2):',
        5: 'context = { "msg": \'Your new password is \' + password1,',
        6: '"navinfo": config[\'DEFAULT\'][\'CSRF\']',
        7: 'context = { "msg": \'Your new password is \' + password1,',
        8: "return render(request, 'user/changepass.html', context)"
    },
    'response': {
        'status_code': '200',
        'headers': {
            'Content-Type': 'text/html; charset=utf-8'
        }
    }
}

augmented_records = augment_record(record, n_augmentations=100)
print(augmented_records[:2])
print(len(augmented_records))
