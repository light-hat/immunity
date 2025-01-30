<p align="center">
<img src="assets/head.png">
</p>

<hr/>

<p align="center">
<img src="https://img.shields.io/badge/nVIDIA-%2376B900.svg?style=for-the-badge&logo=nVIDIA&logoColor=white">
<img src="https://img.shields.io/badge/cuda-000000.svg?style=for-the-badge&logo=nVIDIA&logoColor=green">
<img src="https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white">
<img src="https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white">
<img src="https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white">
<img src="https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white">
<img src="https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white">
<img src="https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E">
<img src="https://img.shields.io/badge/vuejs-%2335495e.svg?style=for-the-badge&logo=vuedotjs&logoColor=%234FC08D">
<img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">
<img src="https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white">
<img src="https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray">
<img src="https://img.shields.io/badge/celery-%23a9cc54.svg?style=for-the-badge&logo=celery&logoColor=ddf4a4">
<img src="https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white">
<img src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white">
<img src="https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white">
<img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white">
</p>

<p align="center">
Система интерактивного анализа веб-приложений на Python (Interactive Application Security Testing, IAST), разработанная в рамках моего дипломного проекта.
</p>

## Содержание

<!-- TOC -->
  * [Содержание](#содержание)
  * [Результаты работы](#результаты-работы)
  * [Демо](#демо)
  * [Развёртывание системы](#развёртывание-системы)
    * [Характеристики сервера](#характеристики-сервера)
    * [Подготовка сервера](#подготовка-сервера)
    * [Запуск системы](#запуск-системы)
  * [Концепция](#концепция)
  * [Агент интерактивного анализа](#агент-интерактивного-анализа)
  * [Управляющий сервер](#управляющий-сервер)
  * [Модель машинного обучения](#модель-машинного-обучения)
  * [Тестовый DevSecOps-стенд](#тестовый-devsecops-стенд)
  * [Результаты сравнительного тестирования](#результаты-сравнительного-тестирования)
<!-- TOC -->

## Результаты работы

- разработан [агент интерактивного анализа](https://github.com/light-hat/immunity-python-agent);
- разработан управляющий сервер (данный репозиторий);
- собран [обучающий набор данных](https://huggingface.co/datasets/l1ghth4t/iast-python3-django-flask), а также выполнено [трансферное обучение модели BERT](https://huggingface.co/l1ghth4t/immunity) для задачи выявления уязвимостей;
- разработан [тестовый стенд](https://github.com/light-hat/devsecops-stand), описывающий внедрение системы в процессы DevSecOps;
- проведено сравнительное тестирование разработанной системы с инструментами SAST и DAST.

## Демо

...

## Развёртывание системы

### Характеристики сервера

> [!NOTE]
> Сервер с указанными характеристиками использовался для разработки и тестирования системы.

| Параметр             | Значение                 |
|----------------------|--------------------------|
| Операционная система | Ubuntu 22.04 LTS 64-bit  |
| CPU                  | 4 ядра                   |
| RAM                  | 32 ГБ                    |
| GPU                  | 1 × Tesla T4  16 ГБ      |

### Подготовка сервера

Установите Docker и Docker Compose на сервер, используя данную [инструкцию](https://docs.docker.com/engine/install/ubuntu/) с официального сайта Docker.

Когда установлен Docker, проверьте драйвера видеокарты:

```shell
nvidia-smi
```

<details>
  <summary>👀 Что примерно должно быть в ответе</summary>

<hr />

```
Sat Jan  4 01:37:28 2025       
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 535.183.01             Driver Version: 535.183.01   CUDA Version: 12.2     |
|-----------------------------------------+----------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
|                                         |                      |               MIG M. |
|=========================================+======================+======================|
|   0  Tesla T4                       Off | 00000000:00:06.0 Off |                  Off |
| N/A   49C    P0              28W /  70W |    783MiB / 16384MiB |      0%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+
```

<hr />

</details>

<details>
  <summary>👀 Как поставить драйвера на GPU</summary>

<hr />

Устанавливаем инструменты для компиляции драйверов и заголовки ядра:

```shell
sudo apt update
sudo apt-get install build-essential linux-headers-$(uname -r)
```

Ищем доступные версии драйвера:

```shell
ubuntu-drivers devices
```

Находим в выводе похожую строчку:

```text
...
driver   : nvidia-driver-535 - distro non-free recommended
...
```

Это версия драйвера, которую вам нужно установить. Делаем это:

```shell
sudo apt-get install nvidia-driver-535
```

Затем перезапускаем сервер:

```shell
sudo reboot
```

После перезагрузки снова проверяем драйвера GPU:

```shell
nvidia-smi
```

<hr />

</details>

После этого проверьте, установлен ли на сервере `NVIDIA Container Toolkit`:

```shell
dpkg -l | grep nvidia-container-toolkit
```

<details>
  <summary>👀 Что примерно должно быть в ответе</summary>

<hr />

```
ii  nvidia-container-toolkit          1.17.3-1          amd64     NVIDIA Container toolkit
ii  nvidia-container-toolkit-base     1.17.3-1          amd64     NVIDIA Container Toolkit Base

```

<hr />

</details>

> [!TIP]
> Если в этом ответе пусто, вот [мануал](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) c официального сайта как установить NVIDIA Container Toolkit.

### Запуск системы

1. Клонируйте репозиторий:

```shell
git clone https://github.com/light-hat/immunity-iast
cd immunity-iast
```

2. Настройте проект перед запуском:

```shell
make config
```

Переменные окружения в конфигурации:

- `API_URL`: адрес, на котором будет развёрнут сервис;

- `API_PORT`: порт, на котором будет принимать запросы сервис;

- `POSTGRES_HOST`: хост базы данных (имя сервиса в стеке приложений);

- `POSTGRES_PORT`: порт базы данных;

- `POSTGRES_USER`: пользователь базы данных;

- `POSTGRES_PASSWORD`: пароль от базы данных;

- `POSTGRES_DB`: имя базы данных, используемой сервисом;

3. Запустите стек приложений:

```shell
make up
```

4. Проверьте логи:

```shell
make logs | grep immunity
make logs | grep worker
```

<details>
  <summary>👀 Как выглядит здоровый лог при запуске</summary>

<hr />

Лог основного приложения (immunity):

```shell
sudo docker compose logs api
```

```text
...
```

Лог асинхронного воркера (worker):

```shell
sudo docker compose logs worker
```

```text
...
```

<hr />

</details>

## Концепция

`IAST (Interactive Application Security Testing)` – это метод тестирования безопасности приложений, который сочетает в себе статический анализ кода (`SAST`) и динамический анализ (`DAST`). Основная концепция заключается в том, чтобы объединить эти два подхода для получения более точных результатов и повышения эффективности процесса тестирования.

В контексте интерактивного анализа (`IAST`), классификация может включать две категории: активный и пассивный анализ.

## Агент интерактивного анализа

...

## Управляющий сервер

...

## Модель машинного обучения

...

## Тестовый DevSecOps-стенд

...


## Результаты сравнительного тестирования

...
