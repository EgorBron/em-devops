# em-devops

Тестовое задание на позицию Junior DevOps.

Построено на стеке из Python 3.14 и Docker.


## Сборка и запуск

### Предварительная подготовка

Для запуска требуется Debian 12+ или основанный на нём дистрибутив Linux, с systemd в качестве подсистемы инициализации и apt в качестве пакетного менеджера.

1. Установите зависимости:

  sudo apt update && sudo apt install -y ca-certificates curl gnupg lsb-release

2. Установите Docker Engine:

  curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  sudo apt update && sudo apt install -y docker-ce docker-ce-cli containerd.io
  sudo systemctl enable --now docker
  sudo usermod -aG docker $USER
  newgrp docker

3. Установите Git (необязательно):

  sudo apt update && sudo apt install -y git


### Скачивание репозитория

Склонируйте репозиторий командой ниже:

  git clone https://github.com/EgorBron/em-devops

Или скачайте следующей командой, если присутствуют проблемы с Git:

  curl -L https://github.com/EgorBron/em-devops/archive/refs/heads/master.tar.gz | tar -xz

Затем перейдите в директорию репозитория.


### Запуск сервисов в Docker

Команды в этом разделе должны выполняться *от корня репозитория*.

0. Скопируйте пример файла с переменными окружения и отредактируйте его при надобности:

  cp .env.example .env

1. Проверьте корректность конфигурации:

  docker compose config --quiet && echo "docker-compose.yml is valid"

2. Запустите приложение со включенной сборкой образов:

  docker compose up --build

3. При последующих запусках можно использовать следующую команду, если код или Dockerfile бэкенда не изменялись:

  docker compose up -d

  > Флаг `-d` "отвязывает" терминал от окна журналов Compose. Чтобы просмотреть их, стоит использовать команду `docker compose logs`.

4. Вы можете сменить адрес и порт, на котором слушает приложение и обратный прокси, задав переменные окружения через файл `.env` или через параметр `-e`:

  docker compose up -e PROXY_PORT=8090 -e BACKEND_PORT=9000 -e BACKEND_HOST=0.0.0.0

  > Поскольку nginx напрямую не поддерживает подстановку из переменных окружения, при смене порта приложения также измените его в конфигурации nginx!

5. Проверьте работоспособность приложения с помощью `curl`:

  curl localhost -v

6. По окончании работы остановите и удалите контейнеры:

  docker copose down

  > Если вы по каким-то причинам не хотите удалять контейнеры, а просто приостановить, воспользуйтесь командами `docker compose stop/start` для управления этим состоянием.


## Архитектура приложения

1. Запрос от клиента попадает на указанный порт обратного прокси (по умолчанию это порт HTTP 80), который слушается Docker.
2. Docker перенаправляет запрос в контейнер с nginx.
3. nginx обрабатывает запрос и проксирует на порт контейнера (8080) через Docker-сеть `backend`, добавляя необходимые заголовки к запросу.
4. Docker направляет запрос в контейнер приложения.
5. Веб-сервер на базе модуля `http.server` возвращает строку `Hello from Effective Mobile!` в качестве ответа со статусным кодом 200.

Для настройки используются переменные окружения `PROXY_PORT`, `BACKEND_PORT` и `BACKEND_HOST`. Все из них могут быть опущены в текущей конфигурации, но могут быть полезны для:
- смены порта, на котором будет слушать приложение во время разработки или при переконфигурации nginx;
- смены адреса, на котором будет слушать приложение во время разработки.
