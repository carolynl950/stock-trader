"""
User Strategy Template

Users define their trading logic here.
This script is uploaded to Firebase Storage.
Paper trading only.
"""


from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import OrderSide, OrderStatus, TimeInForce
from firebase_admin import firestore
from datetime import date
import json
import os
api_key = "YOUR API KEY HERE"
secret_key = "YOUR SECRET KEY HERE"
name = "YOUR NAME HERE"
groupID = "YOUR GROUP ID HERE"
today = date.today()
trading_client = TradingClient(api_key, secret_key, paper=True)




def accountInfo(trading_client):
  account = trading_client.get_account()
  return account.equity


def lastequity(trading_client):
  account = trading_client.get_account()
  return account.last_equity

def format_number(number):
  if number >= 0:
    return "${:.2f}".format(abs(number))
  else:
    return "-${:.2f}".format(abs(number))

def percentage(number):
  number *= 100
  if number >= 0:
    return "{:.3f}".format(abs(number)) + "%"
  else:
    return "-{:.3f}".format(abs(number)) + "%"

equity = accountInfo(trading_client)



equity = accountInfo(trading_client)

output_list = {
  "account_equity": "$" + equity,
  "name": name,
  "daily_change": format_number(float(accountInfo(trading_client)) - float(lastequity(trading_client))),
  "last_runtime": str(today),
  "lifetime_changes": percentage((float(equity) - 100000) / 100000),
  "groupID": groupID
}
db = firestore.client()
db.collection("output").document(str(name)).set(output_list)

