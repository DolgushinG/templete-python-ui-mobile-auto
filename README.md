TEMPLETE PROJECT UI MOBILE AUTOMATION - UAM  

1. Как установить проект автоматизации:
- git clone https://
- mkdir app || true
- python3 -m venv virtual-env
- source virtual-env/bin/activate
- pip install --upgrade pip
- pip install -r requirements.txt
- Cкопировать приложения в папке app с расширениями для android apk, для iOS app, по одному приложению из каждой платформы,
- При старте они ищутся автоматически в этой папке по расширениям
установка
- NodeJs → brew install node
- Appium Desktop → https://github.com/appium/appium-desktop/releases/ 
- Appium Doctor → npm install appium-doctor -g
- Appium Inspector → https://github.com/appium/appium-inspector/releases 
- Appium [npm], → npm install appium -g 
- Xcode latest version for iOS, → App Store install xcode
- Android Studio для Android → https://developer.android.com/studio#downloads
Запустить командой:
- appium-doctor 
- после этого он подскажет что необходимо доустановить для запуска и управления симуляторами и эмуляторами

2. Структура:
- tests - директория с тестами
- screenshots -  директория для скриншотов
- pages - пейдж-объекты для эankкранов приложения
- main - вспомогательные методы и методы работы через апи
- app - директория для приложений
- allure-results-* / allure-results-* - директория результатов для аллюр репорта соответствующих тестов android/ios
- logs - логи эмуляторов и appium
- conftest.py - содержит общие фикстуры для всех тестов, инициализацию аппиум сервера и драйвера
- options.py - содержит метод получения приложений для теста и методы получения опций для запуска аппиум-сессии
- pytest.ini - параметры запуска pytest
- requirements.stable.txt - зависимости, устанавливающиеся при создании виртуального окружения, имеющие последние протестированные версии
- requirements.txt - те же зависимости, но без версии - для установки последних доступных версий
- tox.ini - параметры запуска виртуальных окружений

3. Опции в tox ini 
- По умолчанию, командой tox запускаются только тесты 
- Для запуска и остановки эмулятора вместе с тестами используются команды tox -e android tox -e ios
- tox -e android , tox -e ios
- подчеркнутые параметры находятся в tox.ini под тегом [testenv:android] и [testenv:ios]
Тесты не создают эмулятор android / симулятор ios, а лишь запускают созданные ранее.
Для запуска эмуляторов обязательно указать параметры предварительно созданных в системе эмуляторов в переменных окружения в tox.ini
- APPIUM_PORT = 4723(любой порт главное чтобы не совпадал с другим [testenv:android или iOS] ) 
- PLATFORM_NAME = android или ios(android или ios) 
- DEVICE_NAME = Pixel_4_API_31 или iPhone 11 (указывается имя девайса строго как в созданном эмуляторе)
- UDID = emulator-5554 (adb devices команда либо emulator-%port% порт показывается в запущенном эмуляторе в title) или для iOS 6493F621-AB03-4480-A0FD-3C324CB35142 
- команда для поиска
- xcrun simctl list 
- AVD_PORT = 5554 (тот же самый порт что выше, служит для запуска эмулятора на указанном порте, для дальнейшего закрытия эмулятора после завершения тестов)
- WDA_PORT = 8101 (любой порт 81** служит для установки webDriverAgent или driver на ios, чтобы appium server смог подключиться и слушать указанный порт)
- BOOTSTRAP_PORT = 8201 (любой порт 82** служит для установки Appium setting или driver на android, чтобы appium server смог подключиться и слушать указанный порт)
- AVD_PORT - только для ANDROID
- WDA_PORT - только для IOS
- Все эти значения параметров должны быть уникальные за исключением platform_name тут либо iOS или android
- Симулятор ios возможно запустить только на macos окружении
- В каждом отдельном виртуальном окружении tox запускается своя версия аппиум сервера на отдельном порте
4. Особенности тестов
- Селекторы для ios или android выбираются по параметру platformName из options аппиум-сессии
- Селекторы автоматически определяют тип элемента xpath,id и так далее
- Селекторы автоматически выбираются в зависимости от платформы
- Этапы запуска тестов - tox - установка зависимостей tox - установка соединения - запуск симуляторов/эмуляторов - запуск тестов - остановка симуляторов/эмуляторов - отправка отчетов при флаге allure