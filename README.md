
# Flask RestAPI attendance
## System requirements
- Python3.8 and up
- pip
- virtualenv (optional)
- Database MariaDB/MySQL

## How to install
- copy .env.example .env
- run
```bash
1. virtualenv venv
2. python generate_secret.py
```
- after running that command, copy secret and jwt_secret value, configure .env file
- configure database info in .env file
- run the following command:
```bash
  1. pip install -r requirements.txt
  2. flask db migrate -m "Migrate."
  3. flask db upgrade 
  4. flask run
```
