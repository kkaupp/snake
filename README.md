# Setup with virtual environment

1. Move into project folder

```properties
snake@game:~$ cd 'path_to_snake_folder'
```

2. Setup & activate virtual environment 

```properties 
snake@game:~$ python3 -m venv ./venv 
snake@game:~$ source ./venv/bin/activate (Windows: venv\Scripts\activate)
``` 

3. Install pygame & numpy

```properties
snake@game:~$ pip install -r requirements.txt
``` 

4. Start program

```properties
snake@game:~$ python3 main.py
```

5. Disable virtual environment when finished (optional)

```properties
snake@game:~$ deactivate
```

# Setup without virtual environment

```properties
snake@game:~$ cd 'path_to_snake_folder' && pip install -r requirements.txt 
snake@game:~$ python3 main.py
```

<br>Unfinished Parts will be deliverd in the day one patch *cough*