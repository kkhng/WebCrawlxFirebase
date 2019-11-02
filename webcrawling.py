# Tasks
#1. crawler(url, selector): INPUT: url, selector; OUTPUT: html_elements
#2. clean_up(html_elements): use pyquery to crawl elements, arrange as dictionary; INPUT: html_elements; OUTPUT: dict
#3. save_to_firebase(collection_name, data): save crawled info into firebase; INPUT dict; OUTPUT: info in firebase
#4. query_exchange_rate(ccy,type): inquire firebase; INPUT: ccy, type; OUTPUT: number


#1. Create crawler function
#1.1 install pyquery pip install pyquery
#1.2 import PyQuery
from pyquery import PyQuery as pq 

#1.3 define crawler function
def crawler(url, selector):
    html = pq(url)
    html_elements = html(selector)
    return html_elements

#1.4 use crawler
url = "https://rate.bot.com.tw/xrt?Lang=en-US"
selector = "td[class^='rate-content-']"
html_elements = crawler(url, selector)
print(html_elements.text())

#2. Create clean_up function
#2.1 define clean up function
def clean_up(html_elements):
    #transforming html_elements to text
    html_elements_text = html_elements.text()
    #create list for the currencies
    currency_list = ["USD", "HKD", "GBP", "AUD", "CAD", "SGD", "CHF", "JPY", "ZAR", "SEK", "NZD", "THB", "PHP", "IDR", "EUR", "KRW", "VND", "MYR", "CNY"]
    #split html_elements_text to get the exchange rates
    rates_list = html_elements_text.split(' ')
    #create an empty dictionary file as a data set
    data_set = {}
    #for each index in the currency list
    for index in range (len(currency_list)):
        #get the name of the currency
        currency_name = currency_list[index]
        #Calculate the location of the exchange rate list based on the index of the currency list and keep the relevant data in the variables
        cash_buy   = rates_list[index * 4]
        cash_sell  = rates_list[index * 4 + 1]
        spot_buy  = rates_list[index * 4 + 2]
        spot_sell = rates_list[index * 4 + 3]
        #in the dictionary, add a key, the content is another dictionary, responsible for putting four exchange rate values
        data_set[currency_name] = {
        'CASH_BUY'  : cash_buy,
        'CASH_SELL' : cash_sell,
        'SPOT_BUY' : spot_buy,
        'SPOT_SELL': spot_sell
         }

    #return the dataset
    return data_set

#3. Create save_to_firebase function
#3.1 install firebase_admin pip install --upgrade firebase-admin
#3.2 import firebase_admin packages
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

#the private key downloaded in the project must be changed to your own
serviceAccount = {
  "type": "service_account",
  "project_id": "your_project_id",
  "private_key_id": "your_private_key_id",
  "private_key": "your_private_key",
  "client_email": "your_client_email",
  "client_id": "your_client_id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "your_cert_url"
}

#generate authorized objects
cred = credentials.Certificate(serviceAccount)

#initialize firebase and will only be initialized once
try:
  firebase_admin.delete_app(firebase_admin.get_app())
except:
  print('have not initialized firebase_admin')
else:
  print('initialized firebase_admin')
firebase_admin.initialize_app(cred)
  
print('done initialized firebase_admin!')

#Initialize the database object
db = firestore.client()

#3.3 Define save_to_firebase function to store data
def save_to_firebase(collection_name, doc_name, data_set):
  
  #pass back the firebase stored message
  return db.collection(collection_name).document(doc_name).set(data_set)

#3.4 Use save_to_firebase function
collection_name = "exchange_rates"
date = "2019-10-02"
data_set = clean_up(html_elements)
#save the exchange rate and return system message
save_to_firebase(collection_name, date, data_set)

#4. Create query_exchange_rate function
# Go to database check 
def query_exchange_rate(date, ccy, type):
  #create a reference to doc, collection is folder
  doc_ref = db.collection('exchange_rates').document(date)
  try:
    #try to read the data
    doc = doc_ref.get()
    #convert data to a dictionary
    data = pd.Series(doc.to_dict())
    #return crawled result
    return data[ccy][type]
  #exception incident?
  except:
    #print message
    print('something is wrong!')

#4.2 Use query_exchange_rate function
date = "2019-10-02" 
ccy = "KRW" 
type = "CASH_SELL" 
rate = query_exchange_rate(date, ccy, type)
print(rate)








