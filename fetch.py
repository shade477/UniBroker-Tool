import csv
import requests
import os
import zipfile
import io


datasets = {
    "fyers": {
        "NSE – Currency Derivatives": "https://public.fyers.in/sym_details/NSE_CD.csv",
        "NSE – Equity Derivatives": "https://public.fyers.in/sym_details/NSE_FO.csv",
        "NSE – Capital Market": "https://public.fyers.in/sym_details/NSE_CM.csv",
        "BSE – Capital Market": "https://public.fyers.in/sym_details/BSE_CM.csv",
        "BSE - Equity Derivatives": "https://public.fyers.in/sym_details/BSE_FO.csv",
        "MCX - Commodity": "https://public.fyers.in/sym_details/MCX_COM.csv"
    },
    "angel_one": "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json",
    "icici": "https://directlink.icicidirect.com/NewSecurityMaster/SecurityMaster.zip",
    "zerodha": {
        "url": "https://api.kite.trade/instruments",
        "headers": {
            "X-Kite-Version": "3",
            "Authorization": "token api_key:access_token"
        }
    },
    "kotak": {
        "cash": "https://preferred.kotaksecurities.com/security/production/TradeApiInstruments_Cash_01_04_2022.txt",
        "futures": "https://preferred.kotaksecurities.com/security/production/TradeApiInstruments_FNO_01_04_2022.txt"
    }
}

def rename_files_ext(path, from_ext, to_ext):
    for filename in os.listdir(path):
        if filename.endswith(from_ext):
            base = os.path.splitext(filename)[0]  # Get the file name without extension
            new_filename = f"{base}{to_ext}"
            os.rename(
                os.path.join(path, filename),
                os.path.join(path, new_filename)
            )
            print(f"Renamed {filename} to {new_filename}")

def extract_zip(response, extract_to='datasets'):
    os.makedirs(extract_to, exist_ok=True)

    try:
        with zipfile.ZipFile(io.BytesIO(response)) as z:
            z.extractall(path=extract_to)
            print(f"Files Extracted to {extract_to}")
            rename_files_ext(extract_to, '.txt', '.csv')
    except Exception as e:
        print(e)




def export_data(path, data='', headers=None, is_json=False):
    dir_path = path.split('/')[:-1]
    dir_path = '/'.join(dir_path)
    filename = path.split('/')[-1]
    if not data:
        print(f'{filename} is empty')
        return
    
    
    os.makedirs(f'datasets/{dir_path}', exist_ok=True)
    path = f'datasets/{path}.csv'

    print(f'Writing to file {filename}...')
    
    try:
        if is_json:
            print('Converting JSON to CSV...')
            with open(path, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()
                for row in data:
                    writer.writerow(row)
        else:
            with open(path, 'w', newline='') as file:
                file.write(data)
        print(f'Write to {filename} is successful')
    except Exception as e:
        print(e)

def fyers():
    headers = ['fytoken','symbol_details','exchange_instrument_type',
                'minimum_lot_size','tick_size','isin',
                'trading_session','last_update_date','expiry_date',
                'symbol_ticker','exchange','segment',
                'scrip_code','underlying_symbol','underlying_scrip_code',
                'strike_price','option_type','underlying_fytoken',
                'reserved1','reserved2','reserved3']
    
    filenames = ['NSE_CD', 'NSE_FO', 'NSE_CM', 'BSE_CM', 'BSE_FO', 'MCX_COM']
    
    print("Fetching master scrip from Fyers Trading...")

    for filename, url in zip(filenames, datasets["fyers"].values()):
        print(f"Fetching data from {url}...")
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            if response.status_code == 200:
                print("Success")
                # Combine headers with CSV data
                csv_data = ','.join(headers) + '\n' + response.text
                path = f'fyers/{filename}'
                
                export_data(path, csv_data)
                
        except requests.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            continue

def angelOne():
    headers = ['token', 'symbol', 'name',
                'expiry', 'strike', 'lotsize',
                'instrumenttype', 'exch_seg', 'tick_size']

    url = datasets['angel_one']
    filename = 'angel_one'

    print('Fetching data from Angel One')
    try:
        response = requests.get(url)
        response.raise_for_status()
        if response.status_code == 200:
            print("Fetching successful...")
            data = response.json()
            export_data(filename, data, headers, True)
    except requests.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
                    
def icici_smart():
    url = datasets['icici']
    # filename = 'icici_master_scrip'
    print('Fetching data from ICICI Direct Breeze')
    try:
        response = requests.get(url)
        response.raise_for_status()
        extract_zip(response.content, extract_to='datasets/icici')
    except requests.RequestException as e:
        print(f'Error fetching data from {url}: {e}')

def zerodha():
    request = datasets['zerodha']
    url = request['url']
    headers = request['headers']
    filename = 'zerodha_master_scrip'
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        export_data(filename, response.text)
    except requests.RequestException as e:
        print(f"Error fetching data from {url}: {e}")

def kotak():
    request = datasets['kotak']
    print('Fetching from Kotak')
    for filename, url in request.items():
        path = 'Kotak/'+filename
        print(f"Starting {filename}")
        try:
            response = requests.get(url)
            response.raise_for_status()
            export_data(path, response.text.replace('|', ','))
        except requests.RequestException as e:
            print(f"Error fetching data from {url}: {e}")



def fetch_all():
    fyers()
    angelOne()
    icici_smart()
    zerodha()
    kotak()

def fetch(key):
    fetch_map = {
        'Fyers': fyers,
        'Angel': angelOne,
        'ICICI': icici_smart,
        'Zerodha': zerodha,
        'Kotak': kotak,
    }
    if key in fetch_map:
        fetch_map[key]()
    else:
        print(f"Unknown broker: {key}")
