# gas-fees-predictor
Predict Ethereum gas fees using an ARIMA statistical model

## Files
In order to start tinkering, you need to run the following files in the exact order:

*init_db.py*
creates the sqlite3 db

*importer.py*
imports the CSV dataset inside the database

*ml.py*
contains the statistical analysis code producing a visual output graph
