import pyodbc

password = "Bg4,2ciK2SX19"

cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};Server=tcp:sqlserver-trading.database.windows.net,1433;Database=financial;Uid=MasterTrader;Pwd="+password+";Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
cursor = cnxn.cursor()

cursor.execute("SELECT * FROM {}".format('SP500')) 
# row = cursor.fetchone()
rows = cursor.fetchall()

print(rows)

# while row:
#     print (str(row[0]) + " " + str(row[1]))
#     row = cursor.fetchone()


# for row in cursor.execute("select user_id, user_name from users"):
# print(row.user_id, row.user_name)

# row  = cursor.execute("select * from tmp").fetchone()
# rows = cursor.execute("select * from tmp").fetchall()

# count = cursor.execute("update users set last_logon=? where user_id=?", now, user_id).rowcount
# count = cursor.execute("delete from users where user_id=1").rowcount



# from azure.identity import DefaultAzureCredential
# from azure.keyvault.secrets import SecretClient

# credential = DefaultAzureCredential()

# secret_client = SecretClient(vault_url="https://my-key-vault.vault.azure.net/", credential=credential)
# secret = secret_client.get_secret("secret-name")

# print(secret.name)
# print(secret.value)