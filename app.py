from flask import Flask
from flask import render_template

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

import pyodbc


app = Flask(__name__)

@app.route("/")
def home():
    
    # url du key vault sur Azure
    vault_url = "https://tradingkeyvault.vault.azure.net/"
    # récupération des accés au key vault dans le context d'Azure
    credential = DefaultAzureCredential()

    # récupération des accés à la database depuis le key vault
    secret_client = SecretClient(vault_url=vault_url, credential=credential)
    secret = secret_client.get_secret("sqlserver-trading")

    # connexion au sql server depuis une machine linux
    cnxn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:sqlserver-trading.database.windows.net,1433;Database=financial;Uid=MasterTrader;Pwd="+secret.value+";Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
    cursor = cnxn.cursor()

    cursor.execute("SELECT TOP(200) * FROM XGBoost_BSH_1H ORDER BY DatePrediction DESC") 
    # row = cursor.fetchone()
    rows = cursor.fetchall()
    rows.reverse()

    new_rows =[]
    for row in rows:
        # row_list = [elem for elem in row]
        # row_list.append(max(row_list[1:]))

        row_list = [row[0]]
        row_list_rounded = list(map(lambda x: round(x, ndigits=4), row[1:]))
        row_list.extend(row_list_rounded)
        row_list.append(max(row_list[1:]))
        new_rows.append(row_list)

    return render_template('index.html', data=new_rows)
