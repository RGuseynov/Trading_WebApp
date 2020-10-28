from flask import Flask
from flask import render_template

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

import pyodbc


app = Flask(__name__)

@app.route("/")
def home():
    
    credential = DefaultAzureCredential()

    secret_client = SecretClient(vault_url="https://tradingkeyvault.vault.azure.net/", credential=credential)
    secret = secret_client.get_secret("sqlserver-trading")

    print(f"secret name is: {secret.name}")

    cnxn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:sqlserver-trading.database.windows.net,1433;Database=financial;Uid=MasterTrader;Pwd="+secret.value+";Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
    cursor = cnxn.cursor()

    cursor.execute("SELECT TOP(50) * FROM XGBoost_BSH_1H ORDER BY DatePrediction DESC") 
    # row = cursor.fetchone()
    rows = cursor.fetchall()
    rows.reverse()

    new_rows =[]
    for row in rows:
        row_list = [elem for elem in row]
        row_list.append(max(row_list[1:]))
        print(row_list)
        new_rows.append(row_list)

    return render_template('index.html', data=new_rows)
