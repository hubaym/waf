import os
PROD = True if 'false'== os.environ['DJANGO_DEVELOPMENT'] else False
#Postgres settings
DEV_POSTG_DBNAME="farehunter"
DEV_POSTG_USER="postgres"
DEV_POSTG_PSW="postgres"
DEV_POSTG_HOST="127.0.0.1"
DEV_POSTG_PORT="5432"

PROD_POSTG_DBNAME="waf_p"
PROD_POSTG_USER="postgres"
PROD_POSTG_PSW="postgres"
PROD_POSTG_HOST="127.0.0.1"
PROD_POSTG_PORT="5432"

#Mongo settings
DEV_MONGO_DBNAME='waf'
DEV_MONGO_TWITTER_COLLECTION = "twitter"
DEV_MONGO_HOST ="localhost"
DEV_MONGO_PORT =21017

PROD_MONGO_DBNAME='waf'
PROD_MONGO_TWITTER_COLLECTION = "twitter"
PROD_MONGO_HOST ="localhost"
PROD_MONGO_PORT =21017
#Neo settings

DEV_NEO_USER="neo4j"
DEV_NEO_PSW="admin"
DEV_NEO_HOST="http://localhost:7474"

PROD_NEO_USER="neo4j"
PROD_NEO_PSW="neo4j_prod"
PROD_NEO_HOST="http://localhost:7474"

#Twitter settings
ckey = 'T19UvYBTwcB9N8BDuoBvJMlGr'
consumer_secret = 'UlqyCOl46CISZ5EWZYIffsu3MzGasZf7SmUY8dEOXvBjwnmiFR'
access_token_key = '733344359689687040-uX8YKfkxNm1HOUlYbKKNBkdw9VdI8yb'
access_token_secret = 'O6MBZNVB2GV4KMUAn8G5SqyxMykRm2GJILqYTYrqhhHzX'

#File settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DROPDOWN_JSON = BASE_DIR + '/static/files/dropdown_list.json'



# SET THE VARIABLE based on the environment type
if PROD:
    POSTG_DBNAME = PROD_POSTG_DBNAME
    POSTG_USER = PROD_POSTG_USER
    POSTG_PSW = PROD_POSTG_PSW
    POSTG_HOST = PROD_POSTG_HOST
    POSTG_PORT = PROD_POSTG_PORT
    MONGO_DBNAME = PROD_MONGO_DBNAME
    MONGO_TWITTER_COLLECTION = PROD_MONGO_TWITTER_COLLECTION 
    MONGO_HOST = PROD_MONGO_HOST 
    MONGO_PORT = PROD_MONGO_PORT
    NEO_USER = PROD_NEO_USER
    NEO_PSW = PROD_NEO_PSW
    NEO_HOST = PROD_NEO_HOST
else:
    POSTG_DBNAME = DEV_POSTG_DBNAME
    POSTG_USER = DEV_POSTG_USER
    POSTG_PSW = DEV_POSTG_PSW
    POSTG_HOST = DEV_POSTG_HOST
    POSTG_PORT = DEV_POSTG_PORT
    MONGO_DBNAME = DEV_MONGO_DBNAME
    MONGO_TWITTER_COLLECTION = DEV_MONGO_TWITTER_COLLECTION 
    MONGO_HOST = DEV_MONGO_HOST 
    MONGO_PORT = DEV_MONGO_PORT 
    NEO_USER = DEV_NEO_USER
    NEO_PSW = DEV_NEO_PSW
    NEO_HOST = DEV_NEO_HOST
    