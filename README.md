# Online Auction GraphQL API

This project is a **GraphQL Online Auction System** built using:

* Flask
* GraphQL (Graphene)
* MongoDB
* PyMongo

It supports:

* Active auction items query
* Bidding system
* Closing auction
* Payment completion

The API runs on:

http://localhost:5000/graphql

---

## PROJECT FILES

app.py
Runs the Flask server and GraphQL endpoint.
Uses GraphQLView to expose `/graphql`.
See implementation in app.py.

database.py
Connects to MongoDB and creates collections.

schema.py
Contains GraphQL Types, Queries, and Mutations.

---

## REQUIREMENTS

Install Python packages:

pip install flask
pip install flask-graphql
pip install graphene
pip install pymongo
pip install bson

---

## MONGODB SETUP

Start MongoDB locally

mongod

Database used:

auctionDB

Collections used:

users
items
bids
transactions
categories

---

## HOW TO RUN PROJECT

Step 1 — Open project folder

cd online-auction-graphql

Step 2 — Activate virtual environment

source venv/bin/activate

Step 3 — Run server

python3 app.py

Server will start at:

http://localhost:5000/graphql

---

## INSTALL ALTAIR GRAPHQL CLIENT

Install Altair extension in browser

Chrome:
https://chrome.google.com/webstore/detail/altair-graphql-client

OR use desktop version:
https://altairgraphql.dev

Open Altair

Enter URL:

http://localhost:5000/graphql

Click SEND

---

## GRAPHQL QUERY

Get active auction items

query {
activeItems {
id
title
currentPrice
endTime
}
}

---

## MUTATION — CREATE BID

mutation {
createBid(
itemId: "ITEM_ID"
bidderId: "USER_ID"
bidAmount: 35000
){
bid{
id
bidAmount
}
}
}

---

## MUTATION — CLOSE AUCTION

mutation {
closeAuction(itemId:"ITEM_ID"){
item{
id
status
currentPrice
}
}
}

---

## MUTATION — COMPLETE PAYMENT

mutation {
completePayment(transactionId: "TRANSACTION_ID") {
transaction {
id
paymentStatus
amount
}
}
}

---

## HOW SYSTEM WORKS

1. User queries activeItems
2. User places bid using createBid
3. Admin closes auction using closeAuction
4. Transaction created automatically
5. Payment done using completePayment

---

## NOTES

• itemId must exist in items collection
• bidderId must exist in users collection
• transactionId is created after closing auction
• Bid must be higher than current price

---
