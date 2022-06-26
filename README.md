# Oasis Network Whale Detector

The reason of this project is to analyze **in live** the Oasis Network Blockchain to find the most valuable transactions and report it instantly. This could help to the community and investors to find the behaviour of the network daily.

This project was made by kamiras. Feel free to use, change and ask everything that you want.

## Features

**Monitoring of the Oasis Network Blockchain**

- Every second the script checks 2 times the Blockchain with the staking.Transfer method, which is the quivalent of a transaction.

**API's**

- Twitter API
- Coinbase API
- oasisscan API

**Automated Tweets**

- The bot tweets transactions over 100000 dollars by default.
- Every 24 Hours the bot tweets a rank of the 3 highest transactions of the Network (22:00 EU).

**Database and example.py**

- 1 Databse
- 1 Table
- 3 Columns

example.py: As the name says it is an example that you could follow to create the database. Rather than doing an .sql script I chose to do it with python for its simplicity.

## What do you consider a whale?

If we look at the next picture we can see the Bitcoin column with the supply, amount of bitcoins to become a whale and the percentage of 1000 Bitcoins compared to the supply. If we do the simple math we will find out that the amount of ROSE to become a whale is 470.000 ROSE's, which is 25.380 USD ~ (26/06/2022).

![representation](https://user-images.githubusercontent.com/80554217/175822280-a0243cd3-ff98-4992-8332-d403d11ca64c.png)


## Installation

```
pip install -r .\requirements.txt
```

## Usage

Execute the **whale.py**

```
python3 whale.py
```   
