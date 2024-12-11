# Predicció del Preu dels Jugadors de LaLiga Fantasy Relevo

Aquest projecte té com a objectiu predir el preu actual dels jugadors en el joc *LaLiga Fantasy Relevo* utilitzant tècniques de *machine learning*. El model es basa en un conjunt de dades que inclou diverses estadístiques dels jugadors i el seu preu de mercat.

## Contingut

- **Exploratory Data Analysis (EDA):** Anàlisi de les dades per entendre la distribució, correlacions i identificar possibles anomalies.
- **Preprocessament de dades:** Transformació de les dades per preparar-les per a la construcció del model.
- **Modelització:** Diferents tècniques de modelització s'apliquen per predir el preu dels jugadors, com ara regressió lineal, *Lasso*, *Ridge*, *Random Forest*, *XGBoost*, entre altres.
- **Selecció de característiques:** S'apliquen tècniques com RFE (Recursive Feature Elimination) i SFS (Sequential Feature Selection) per identificar les característiques més rellevants.
- **Avaluació del model:** Utilització de mètriques com R², MAE, i MSE per avaluar el rendiment del model en conjunts de dades d'entrenament i prova.

## Requisits

Abans d'executar el projecte, assegura't de tenir instal·lades les següents biblioteques:

- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- lightgbm
- xgboost
- mlxtend
- statsmodels (per a models ARIMA)

Pots instal·lar aquestes biblioteques amb pip:

```
pip install pandas numpy matplotlib seaborn scikit-learn lightgbm xgboost mlxtend statsmodels
```

## Com executar el codi

1. **Carregar les dades:** El conjunt de dades ha de ser un arxiu CSV amb les estadístiques dels jugadors. El codi es carrega amb `pandas.read_csv()`.
   
2. **Exploració de dades (EDA):** El primer bloc del codi realitza una anàlisi exploratòria de les dades per comprendre millor les estadístiques i detectar possibles valors nuls o anomalies. 

3. **Preprocessament:** El codi transforma les variables categòriques a numèriques, elimina les columnes irrellevants i aplica enginyeria de característiques per millorar la predicció del preu.

4. **Entrenament del model:** S'entrenen diversos models de *machine learning* per predir el preu actual del jugador, incloent regressió lineal, *Lasso*, *Ridge*, *Random Forest*, *XGBoost*, etc.

5. **Avaluació i selecció de característiques:** S'analitza el rendiment dels models utilitzant mètriques com R², MAE, MSE. També s'utilitzen tècniques de selecció de característiques com RFE i SFS per identificar quines variables tenen més influència sobre el preu del jugador.

## Resultats

Els resultats inclouen les mètriques de rendiment per cada model, que ajuden a identificar quin model proporciona les millors prediccions per al conjunt de dades. També es genera una visualització dels errors i de les prediccions comparades amb els valors reals.

## Possibles millores futures

- **Incorporar sèries temporals:** Es podria millorar el model tractant els preus com una sèrie temporal, actualitzant el model diàriament segons l'evolució del preu dels jugadors.
- **Models més avançats:** Provar models més complexos com xarxes neuronals, RNNs o LSTMs per a problemes temporals.

## Autor

- Santi Miquel Coll

- Héctor Álvarez Pérez
---
