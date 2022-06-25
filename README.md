
# Flask RestAPI attendance
## System requirements
- Python3
- pip
- Database MySQL

## How to install
- copy .env.example .env
- run
```bash
python generate_secret.py
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
