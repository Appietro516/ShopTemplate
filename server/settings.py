from dotenv import load_dotenv
import os

load_dotenv()

STRIPE_KEY = os.getenv('STRIPE_SECRET_KEY')

POSTGRES_URL = os.getenv("POSTGRES_URL")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PW = os.getenv("POSTGRES_PW")
POSTGRES_DB = os.getenv("POSTGRES_DB")

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)

# Shhhhhh its a secret
SECRET_KEY = os.getenv('SECRET_KEY')