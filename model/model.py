# new terminal
# cd model
# python model.py -u 'MONGO_DB_CONNECTION_STRING'

import argparse

import matplotlib.pyplot as plt
import pandas as pd
from pymongo import MongoClient
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Normalizer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
import plotly.express as px
import plotly.graph_objects as go
from sklearn.impute import SimpleImputer
import seaborn as sns

parser = argparse.ArgumentParser(description='Create Model')
parser.add_argument('-u', '--uri', required=True, help="mongodb uri with username/password")
args = parser.parse_args()

mongo_uri = args.uri
mongo_db = "produkte"
mongo_collection = "produkte"

client = MongoClient(mongo_uri)
db = client[mongo_db]
collection = db[mongo_collection]


# fetch a single document
produkt = collection.find_one(projection={'rating': 0})
values = [produkt.values() for produkt in collection.find(projection={'rating': 0})]

df = pd.DataFrame(columns=produkt.keys(), data=values).set_index("_id")

# Wechselkurs CHF
exchange_rate = 0.012

# Anwenden der Korrekturfunktion und Umrechnung in CHF
df['price'] = df['price'].str.replace('₹', '').str.replace(',', '').str.replace(' ', '').astype(float) * exchange_rate

# drop na values
df.dropna()

# Boxplot
fig_boxplot=px.box(df,x='price')

# Teuerstes und Billigstes Handy
max_price = df['price'].idxmax()
min_price = df['price'].idxmin()


# 5G UND NFC ANALYSE
df['Has 5G'] = df['sim'].str.contains('5G|5g', case=False, na=False)
df['Has NFC'] = False

for column in df.columns:
    df['Has NFC'] = df['Has NFC'] | df[column].astype(str).str.contains('NFC', case=False, na=False)

_5g_count = df['Has 5G'].sum()
nfc_count = df['Has NFC'].sum()
both_count = df[(df['Has NFC']) & (df['Has 5G'])].shape[0]

results_df = pd.DataFrame({
    'Feature': ['5G', 'NFC', 'Both NFC and 5G'],
    'Number of Phones': [_5g_count, nfc_count, both_count]
})

fig = go.Figure(data=[go.Bar(
    x=results_df['Feature'], 
    y=results_df['Number of Phones'],
    text=results_df['Number of Phones'],  # Setzt die Textwerte gleich den y-Werten
    textposition='inside',  # Positioniert den Text mittig im Balken
    marker_color=['blue', 'orange', 'green'],
    textfont=dict(size=16, color='white')  # Angepasste Texteigenschaften: Größe und Farbe
)])

fig.update_layout(
    title_text='Number of Phones by Feature',
    xaxis_title='Feature',
    yaxis_title='Number of Phones',
    plot_bgcolor='rgb(230, 230, 230)'
)





################################

print("##########")
print("##########")
print("##########")

print("Anzahl Zeilen und Spalten: " + str(df.shape))

print("Column information: ")
print(df.info())

print("Univariate Analyse der Spalte Preis: ")
print(df['price'].describe().round(2))
print("Schwierigkeiten sich das besser vorzustellen? Probieren wir es mit einem Boxplot: ")
#print(fig_boxplot.show())

# Ausgabe der Tabelle
print("Tabelle der Handy-Features 5G und NFC:")
print(results_df)
fig.show()

################################



# Dual Sim und 5G Unterstützung als binäre Spalten
df['Dual Sim'] = df['sim'].str.contains('Dual Sim', case=False, na=False)
df['Has 5G'] = df['sim'].str.contains('5G', case=False, na=False)

# GHz aus der Prozessor-Spalte extrahieren
df['GHz'] = df['processor'].str.extract(r'(2.8|2.2|2.4|1.77|100|208)').astype(float)

# RAM in numerischer Form extrahieren
df['RAM_GB'] = df['ram'].str.extract(r'(8|16|32|64|128)').astype(float)

# Batterie-Kapazität in mAh extrahieren
df['Battery_mAh'] = df['battery'].str.extract(r'(5000|5100|2800|4000|4500|2500|1000|1100|1200)').astype(float)

# Display-Rate extrahieren und binär machen
df['Display_60Hz'] = df['display'].str.contains('60 Hz', case=False, na=False)
df['Display_120Hz'] = df['display'].str.contains('120 Hz', case=False, na=False)

# Betriebssystem als binär nach 'Android' extrahieren
df['OS_Android'] = df['os'].str.contains('Android', case=False, na=False)

# Nicht benötigte Spalten entfernen
df = df.drop(['model', 'sim', 'processor', 'ram', 'battery', 'display', 'camera', 'card', 'os'], axis=1)

# Teile den Datensatz in Features und Target
X = df.drop('price', axis=1)
y = df['price']

# Teile die Daten in Trainings- und Testsets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Imputer erstellen, der NaN-Werte durch den Median der jeweiligen Spalte ersetzt
imputer = SimpleImputer(strategy='median')

# Imputer auf die Trainingsdaten anwenden
X_train_imputed = imputer.fit_transform(X_train)
X_test_imputed = imputer.transform(X_test)

# Lineare Regression
lr = LinearRegression()
lr.fit(X_train_imputed, y_train)
y_pred_lr = lr.predict(X_test_imputed)

# Gradient Boosting Regressor
gbr = GradientBoostingRegressor(random_state=42)
gbr.fit(X_train_imputed, y_train)
y_pred_gbr = gbr.predict(X_test_imputed)

# Berechne Metriken
r2_lr = r2_score(y_test, y_pred_lr)
mse_lr = mean_squared_error(y_test, y_pred_lr)
r2_gbr = r2_score(y_test, y_pred_gbr)
mse_gbr = mean_squared_error(y_test, y_pred_gbr)

# Ergebnisse in einem DataFrame
results_LR_GBR = pd.DataFrame({
    'Model': ['Linear', 'GBR'],
    'R2': [r2_lr, r2_gbr],
    'MSE': [mse_lr, mse_gbr]
})

print(results_LR_GBR)

'''
# Wir erstellen eine Korrelationsmatrix nur für den 'price'
price_corr = df.corrwith(df['price']).iloc[:-1].to_frame()
price_corr.columns = ['Correlation with Price']

# Sortiere die Korrelationen für eine bessere Visualisierung
price_corr = price_corr.sort_values(by='Correlation with Price', ascending=False)

# Erstelle die Heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(price_corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, cbar_kws={"shrink": .82})

# Titel für die Heatmap
plt.title('Feature Correlation with Price')

# Zeige die Heatmap an
plt.show()
'''






