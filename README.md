I. Instalare tehnologii
    1) Python 3.6
        - configurare variabila de enviroment
    2) PostgreSql 10
        - configurare
            host: localhost
            port: 5432
        - creare bază de date
            nume bază de date: library
            nume admin: admin
            parolă admin: admin
    3) RabbitMq 3.7.14
        - configurare
            setări default
    4) Erlang OTP 21.3
        - configurare 
            setări default  
    5) Pycharm
        - configurare
    
II. Configurare enviroment proiect
    1) Se deschide proiectul cu PyCharm
    2) Setare interpretor proiect: python 3.6
    3) Instalare dependențe din requirements.txt executând comanda:
        pip install -r /path/to/requirements.txt
    4) Initializare bază de date:
        - in fisierul __init__.py se comentează importurile de pe intervalul de linii 49-58
        - se execută models.py
        - se decomentează randurile 49-58 din __init__.py 
        
III. Rulare aplicație   
    1) se execută run.py
    2) se execută run_celery.py
    3) se execută run_beat.py

IV. Utilizare
    1) cont admin:
        - username: admin@gmail.com
        - parolă: admin
    2) cont utilizator:
        - username: user1@gmail.com
        - parolă: user1@gmail.com
        