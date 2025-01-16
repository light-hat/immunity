import requests
import pandas as pd
from sklearn.model_selection import train_test_split
from datasets import Dataset, DatasetDict
from huggingface_hub import HfApi, HfFolder
import random
import string
from faker import Faker

fake = Faker()

# Настройки
API_ENDPOINT = "http://127.0.0.1:85/api/users/dataset/?page_size=100000"
HF_DATASET_REPO = "l1ghth4t/iast-python3-django-flask"
LOCAL_TRAIN_PATH = "./train_set.csv"
LOCAL_VALIDATION_PATH = "./validation_set.csv"

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

# 1. Выгрузка данных с API
def fetch_and_parse_data(api_endpoint):
    # Запрос к API
    print("Делаем запрос к API...")
    response = requests.get(api_endpoint)

    # Проверяем статус ответа
    if response.status_code == 200:
        data = response.json()

        # Преобразуем данные в DataFrame
        print("Парсим данные...")
        df = pd.DataFrame(data["data"])

        # Проверяем наличие нужных колонок
        if not {"text", "label"}.issubset(df.columns):
            raise ValueError("Ответ API не содержит обязательных колонок 'text' и 'label'.")

        print(f"Получено {len(df)} записей.")
        return df
    else:
        raise Exception(f"Ошибка при запросе данных: {response.status_code}")

# 2. Очистка данных
def clean_data(df):
    print("Чистим данные...")
    # Удаление дубликатов
    df = df.drop_duplicates()
    # Оставляем только текст и метки
    df = df[["text", "label"]]

    # Применяем аугментацию к каждому экземпляру данных
    augmented_data = []
    for _, row in df.iterrows():
        original_json = eval(row['text'])  # Предполагаем, что text содержит строку JSON
        augmented_records = augment_record(original_json)
        for record in augmented_records:
            augmented_data.append({'text': str(record), 'label': row['label']})

    # Создаем новый DataFrame из аугментированных данных
    augmented_df = pd.DataFrame(augmented_data)

    # Разделение на обучающий и валидационный наборы
    train_df, validation_df = train_test_split(
        augmented_df,
        test_size=0.3,  # 30% данных для валидации
        random_state=42,  # Фиксируем случайность для воспроизводимости результатов
        stratify=augmented_df['label']  # Стратифицированное разделение по меткам
    )

    return train_df, validation_df

# 3. Преобразование данных и сохранение
def save_and_upload_dataset(train_df, validation_df, dataset_repo, train_path, validation_path):
    print("Сохраняем датасеты...")
    # Сохраняем обучающий набор в CSV
    train_df.to_csv(train_path, index=False)
    # Сохраняем валидационный набор в CSV
    validation_df.to_csv(validation_path, index=False)

    print("Создаем Hugging Face Datasets...")
    train_dataset = Dataset.from_pandas(train_df)
    validation_dataset = Dataset.from_pandas(validation_df)

    print("Загружаем датасеты на Hugging Face Hub...")
    dataset = DatasetDict({
        "train": train_dataset,
        "validation": validation_dataset
    })
    dataset.push_to_hub(f"{dataset_repo}")

# Основная функция
def main():
    # Шаг 1: Получаем данные
    df = fetch_and_parse_data(API_ENDPOINT)

    # Шаг 2: Чистим данные и делим на обучающий и валидационный наборы
    train_df, validation_df = clean_data(df)

    print(train_df)
    print(validation_df)

    # Шаг 3: Проверка на наличие данных
    if train_df.empty or validation_df.empty:
        print("Данные пустые после очистки. Завершаем выполнение.")
        return

    # Шаг 4: Сохранение и загрузка на HF Hub
    save_and_upload_dataset(train_df, validation_df, HF_DATASET_REPO, LOCAL_TRAIN_PATH, LOCAL_VALIDATION_PATH)
    print("Обучающий и валидационный наборы успешно загружены на Hugging Face Hub.")

if __name__ == "__main__":
    main()
