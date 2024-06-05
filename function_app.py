import azure.functions as func
import logging
import requests
import pandas as pd
from sqlalchemy import create_engine
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

def fetch_stores(url):
    # Fetches products from the specified URL.
    res = []
    i = 1
    while True:
        modify_url = f"{url}?page={i}"
        payload = json.dumps({
            "keyword": "India",
            "perPage": "200"
        })
        headers = {
            'Xstoreaccesskey': 'pNRq8BGvIHk/G9AwlBxKG5lz97eYDaxnWO0YYs+VrMY=',
            'Content-Type': 'application/json',
            'Cookie': '__cf_bm=KEAixb72Bc8hjHLmY_q7JPV8syOcyBcFwVzMjxTCz7o-1712582604-1.0.1.1-obPC7mQkJxe5Y1cQD8BNwXMCgl4ERUNFINfaPHRk4dDKyozHHls8hGPimxvcK4UXSgjUJ2O7DcQwvZGJKPuoaA; __cfruid=7052bdf419223514a10b2bdf083656457e17024f-1712582604'
        }
        response = requests.post(modify_url, headers=headers, data=payload)
        data = response.json()
        store_data = data.get("data", {})
        store_list = store_data.get("data", [])
        res.extend(store_list)
        if store_data.get("to") >= store_data.get("total"):
            break
        i += 1
    return res


def fetch_products(url, page_size=200):
    # Fetches products from the specified URL.
    res = []
    i = 0
    while True:
        modify_url = f"{url}?page={i}&page-size={page_size}"
        headers = {
            'Cookie': '__cf_bm=UZCHF6cOgeuULfONIAa.XNAZ6IllNtFKgzq8YGFX9pU-1712136928-1.0.1.1-eMKZMtvVrCMoAyJruxJHBIh3Mst7lcAISw9D4aa1nH.hxCw9rGWHuD2mPaYQV7px3GB1cpVQl34LE7yBm9dEJw; __cfruid=c98ccf8cd0e73db1e52d1638ba026ceac192796b-1712136928'
        }
        response = requests.get(modify_url, headers=headers)
        data = response.json()
        product_list = data.get("result", {}).get("product_list", [])
        res.extend(product_list)
        if len(product_list) < page_size:
            break
        i += 1
    return res

def scrape_categories(base_url, category_ids):
    # Scrapes products from multiple categories and combines them.
    all_products = []
    for category_id in category_ids:
        category_url = f"{base_url}/{category_id}"
        products = fetch_products(category_url)
        all_products.extend(products)
    return all_products

@app.route(route="func_product_scrap")
def func_product_scrap(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    base_api_url = "https://api-gateway.juno.lenskart.com/v2/products/category"
    category_ids = ["3363", "3362", "16631", "16633", "16634", "16641", "16637", "16640", "16639", "16635", "16638", "16607"]
    logging.info("Scraping product data...")
    all_products = scrape_categories(base_api_url, category_ids)
    logging.info(f"Total products scraped: {len(all_products)}")
    
    logging.info("Removing duplicates based on 'id' column...")
    df = pd.json_normalize(all_products)
    df = df.drop_duplicates(subset=['id'])
    logging.info(f"Total unique products: {len(df)}")
    
    df['price'] = df['prices'].apply(json.dumps)
    df.drop(columns=['prices'], inplace=True)
    df['hastags'] = df['hashtagList'].apply(json.dumps)
    df.drop(columns=['hashtagList'], inplace=True)
    
    try:
        conn_str = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:lenskart.database.windows.net,1433;Database=lenskartdb;Uid=lenskart;Pwd=1234@Bcd;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
        engine = create_engine(f"mssql+pyodbc:///?odbc_connect={conn_str}")
        df.to_sql('products', schema='lenskart', con=engine, if_exists='replace', index=False)
    except Exception as e:
        return func.HttpResponse(
            f"Failed {e} ",
            status_code=400
         )
    return func.HttpResponse(
            f"Success products added to db ",
            status_code=200
    )

@app.route(route="func_store_scrap", auth_level=func.AuthLevel.FUNCTION)
def func_store_scrap(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    base_api_url = "https://locator-stores.lenskart.com/api/v3/store/list"
    logging.info("Scraping store data...")
    store_list = fetch_stores(base_api_url)
    logging.info(f"Total stores scraped: {len(store_list)}")
    # Convert list of dictionaries to DataFrame
    df = pd.json_normalize(store_list)
    try:
        conn_str = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:lenskart.database.windows.net,1433;Database=lenskartdb;Uid=lenskart;Pwd=1234@Bcd;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
        engine = create_engine(f"mssql+pyodbc:///?odbc_connect={conn_str}")
        df.to_sql('stores', schema='lenskart', con=engine, if_exists='replace', index=False)
    except Exception as e:
        return func.HttpResponse(
            f"Failed {e} ",
            status_code=400
         )
    return func.HttpResponse(
            f"Success stores added to db ",
            status_code=200
    )