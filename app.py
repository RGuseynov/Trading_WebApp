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

    cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};Server=tcp:sqlserver-trading.database.windows.net,1433;Database=financial;Uid=MasterTrader;Pwd="+secret+";Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
    cursor = cnxn.cursor()

    cursor.execute("SELECT * FROM {}".format('SP500')) 
    # row = cursor.fetchone()
    rows = cursor.fetchall()

    print(rows)


    table = [[1,2,3],[4,5,6],[7,8,9]]
    return render_template('index.html', data=table)

