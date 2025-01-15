import requests
import pandas as pd
from datasets import Dataset
from huggingface_hub import HfApi, HfFolder

# Настройки
API_ENDPOINT = "http://127.0.0.1:81/api/users/dataset/?page_size=100000"
HF_DATASET_REPO = "l1ghth4t/iast-python3-django-flask"
LOCAL_DATA_PATH = "./dataset.csv"

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
    return df

# 3. Преобразование данных и сохранение
def save_and_upload_dataset(df, dataset_repo, local_path):
    print("Сохраняем датасет...")
    # Сохраняем в CSV
    df.to_csv(local_path, index=False)

    print("Создаем Hugging Face Dataset...")
    dataset = Dataset.from_pandas(df)

    print("Загружаем датасет на Hugging Face Hub...")
    dataset.push_to_hub(dataset_repo)

# Основная функция
def main():
    # Шаг 1: Получаем данные
    df = fetch_and_parse_data(API_ENDPOINT)

    # Шаг 2: Чистим данные
    df_cleaned = clean_data(df)

    # Шаг 3: Проверка на наличие данных
    if df_cleaned.empty:
        print("Данные пустые после очистки. Завершаем выполнение.")
        return

    # Шаг 4: Сохранение и загрузка на HF Hub
    save_and_upload_dataset(df_cleaned, HF_DATASET_REPO, LOCAL_DATA_PATH)
    print("Датасет успешно загружен на Hugging Face Hub.")

if __name__ == "__main__":
    main()
