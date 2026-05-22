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

3. Установите Git:

  sudo apt update && sudo apt install -y git

4. Установите nginx:

  sudo apt update && sudo apt install -y nginx
  sudo systemctl enable --now nginx


### Скачивание репозитория

Склонируйте репозиторий командой ниже:

  git clone https://github.com/EgorBron/em-devops

Или скачайте следующей командой, если присутствуют проблемы с Git:

  curl -L https://github.com/EgorBron/em-devops/archive/refs/heads/master.tar.gz | tar -xz

Затем перейдите в директорию репозитория.


### Запуск Backend в Docker

Команды в этом разделе должны выполняться *от корня репозитория*.

1. Соберите образ приложения перед запуском:

  docker build -f backend/Dockerfile -t em-devops:1.0.0 backend/

3. Запустите приложение:

  docker run -p 8080:8080 em-devops:1.0.0

4. Вы можете сменить адрес и порт, на котором слушает приложение, передав переменные окружения через параметр `-e`:

  docker run -p 9000:9000 -e BACKEND_PORT=9000 -e BACKEND_HOST=0.0.0.0 em-devops:1.0.0

5. Проверьте работоспособность приложения с помощью `curl`:

  curl localhost:8080 -v


### Настройка nginx

Команды в этом разделе должны выполняться *от корня репозитория*.

1. Удалите ссылку на сайт по умолчанию перед изменением конфига:
  
    sudo rm /etc/nginx/sites-enabled/default

2. Замените стандартный конфиг:

  sudo cp nginx/nginx.conf /etc/nginx/nginx.conf

3. Протестируйте конфиг:

  sudo nginx -t

  > Тест считается *успешным*, если код выхода (`echo $?`) равен нулю, а последние две строки вывода таковы:
  >   nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
  >   nginx: configuration file /etc/nginx/nginx.conf test is successful

4. Если тест прошёл успешно, перезапустите службу:

  sudo systemctl reload nginx

5. Проверьте работоспособность nginx при запущенном контейнере из предыдущего раздела:

  curl localhost -v


## Архитектура приложения

1. Запрос от клиента попадает на стандартный порт HTTP (80).
2. nginx обрабатывает запрос и проксирует на порт контейнера (8080), добавляя необходимые заголовки к запросу.
3. Docker направляет запрос в контейнер приложения.
4. Веб-сервер на базе модуля `http.server` возвращает строку `Hello from Effective Mobile!` в качестве ответа со статусным кодом 200.
5. Для настройки сервер использует переменные окружения `BACKEND_PORT` и `BACKEND_HOST`. Обе из них могут быть опущены в текущей конфигурации, но могут быть полезны для:
  - смены порта, на котором будет слушать приложение во время разработки или при переконфигурации nginx;
  - смены адреса, на котором будет слушать приложение во время разработки.
