# Scan open ports
Программа для обнаружения открытых портов за NAT (firewall).

* [Описание](#Описание)
* [Алгоритм](#Алгоритм)
* [Опции](#Опции)
* [FAQ](#FAQ) 

## Описание
Программа создавалась для собственных нужд, для обнаружение открытых портов за сетевым экраном.
Дело в том что многие люди путают понятие открытого порта и сервиса работающего на открытом порту.
Для того что бы внешний сканер смог определить открытый порт,на нем должен быть запущен сервис
который слушает данный порт. Если на сетевом экране проброшен порт (настроен DNAT), но сервиса
на данном порту не запущено сканер покажет что порт закрыт, что не соответствует действительности.

## Алгоритм
Запуск, на сканируемом сервере должен быть получен доступ по ssh и установлен `python3-minimal`.

```
python3 run.py -b8000 -e8100 -i81.120.102.55
```
Данная команда скопирует сервернную часть на 81.120.102.55 в /tmp/Server.py
и будет запускать её на указанном диапазоне портов.
Клиентская часть будет пытаться установить соединение с сервером и обменятся данными через сокет.
Если обмен произошел успешно, то порт считается открытым. Результат пишется в файл `openports.txt`.


## Опции
Доступные опции:

    '-b', '--port_begin'
    '-e', '--port_end'
    '-p', '--ssh_port'
    '-z', '--chunk_size'
    '-s', '--server_timeout'
    '-s', '--client_timeout'
    '-i', '--ip_address'
    '-u', '--user'
    '-w', '--password'
    '-h', '--help'
    
Опции интуитивно понятные, комментировать не имеет смысла.

## FAQ
- Q: Зачем нужна эта программа, ведь есть nmap и т.д.?
- A: У программ подобных nmap, отстутствует серверная часть и они могут просканировать 
   только сервисы запущенные на сканируемых портах.

- Q: Разьве нельзя использовать связку `nc -l port ; nc -vn host port`?
- A: Конечно можно, но такое решение хорошо работает когда нужно просканировать 2-3 порта, 
   но не диапазон 1024-65535. Скрипты на bash с nc у меня стабильно не заработали. 

- Q: Не исчерпает ли программа системные ресурсы во время сканирования?
- A: Нет, не исчерпает. Сканирование вдется порциями (chunk), по умолчанию 500 портов за раз.
     Размер чанка регулируется через опции.
     
- Q: Насколько быстро работает программа?
- A: Все зависит от таймаутов и удаленности сервера. У меня пиг до сервера 60-80мс. 
     Таймауты дефолтные.  Занял в районе 10 минут на полный перебор 1024-65535.
     
- Q: А разьве нельзя посмотреть проброшенные порты на сетевом экране?
- A: Конечно можно, если у вас есть к нему доступ. В моем случае не было.