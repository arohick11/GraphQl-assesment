import graphene
from database import users, items, bids, transactions
from bson.objectid import ObjectId
from datetime import datetime

# ----------------------
# GraphQL Types
# ----------------------

class UserType(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    email = graphene.String()
    role = graphene.String()

class ItemType(graphene.ObjectType):
    id = graphene.String()
    title = graphene.String()
    description = graphene.String()
    startingPrice = graphene.Float()
    currentPrice = graphene.Float()
    status = graphene.String()
    endTime = graphene.String()

class BidType(graphene.ObjectType):
    id = graphene.String()
    itemId = graphene.String()
    bidderId = graphene.String()
    bidAmount = graphene.Float()
    bidTime = graphene.String()

class TransactionType(graphene.ObjectType):
    id = graphene.String()
    itemId = graphene.String()
    buyerId = graphene.String()
    amount = graphene.Float()
    paymentStatus = graphene.String()

class Query(graphene.ObjectType):

    activeItems = graphene.List(ItemType)

    def resolve_activeItems(self, info):
        data = items.find({"status": "active"})
        result = []

        for i in data:
            result.append(ItemType(
                id=str(i["_id"]),
                title=i["title"],
                description=i["description"],
                startingPrice=i["starting_price"],
                currentPrice=i["current_price"],
                status=i["status"],
                endTime=str(i["end_time"])
            ))

        return result

class CreateBid(graphene.Mutation):

    class Arguments:
        itemId = graphene.String()
        bidderId = graphene.String()
        bidAmount = graphene.Float()

    bid = graphene.Field(lambda: BidType)

    def mutate(self, info, itemId, bidderId, bidAmount):

        item = items.find_one({"_id": ObjectId(itemId)})

        if bidAmount <= item["current_price"]:
            raise Exception("Bid must be higher than current price")

        items.update_one(
            {"_id": ObjectId(itemId)},
            {"$set": {"current_price": bidAmount}}
        )

        bid_data = {
            "item_id": itemId,
            "bidder_id": bidderId,
            "bid_amount": bidAmount,
            "bid_time": datetime.now()
        }

        bid_id = bids.insert_one(bid_data).inserted_id

        return CreateBid(
            bid=BidType(
                id=str(bid_id),
                itemId=itemId,
                bidderId=bidderId,
                bidAmount=bidAmount,
                bidTime=str(datetime.now())
            )
        )

class CloseAuction(graphene.Mutation):

    class Arguments:
        itemId = graphene.String()

    item = graphene.Field(lambda: ItemType)

    def mutate(self, info, itemId):

        item = items.find_one({"_id": ObjectId(itemId)})

        highest_bid = bids.find_one(
            {"item_id": itemId},
            sort=[("bid_amount", -1)]
        )

        if highest_bid:
            transactions.insert_one({
                "item_id": itemId,
                "buyer_id": highest_bid["bidder_id"],
                "amount": highest_bid["bid_amount"],
                "payment_status": "pending"
            })

        items.update_one(
            {"_id": ObjectId(itemId)},
            {"$set": {"status": "closed"}}
        )

        item = items.find_one({"_id": ObjectId(itemId)})

        return CloseAuction(
            item=ItemType(
                id=str(item["_id"]),
                title=item["title"],
                description=item["description"],
                startingPrice=item["starting_price"],
                currentPrice=item["current_price"],
                status=item["status"],
                endTime=str(item["end_time"])
            )
        )

class CompletePayment(graphene.Mutation):

    class Arguments:
        transactionId = graphene.String()

    transaction = graphene.Field(lambda: TransactionType)

    def mutate(self, info, transactionId):

        transactions.update_one(
            {"_id": ObjectId(transactionId)},
            {"$set": {"payment_status": "completed"}}
        )

        tx = transactions.find_one({"_id": ObjectId(transactionId)})

        return CompletePayment(
            transaction=TransactionType(
                id=str(tx["_id"]),
                itemId=tx["item_id"],
                buyerId=tx["buyer_id"],
                amount=tx["amount"],
                paymentStatus=tx["payment_status"]
            )
        )

class Mutation(graphene.ObjectType):
    createBid = CreateBid.Field()
    closeAuction = CloseAuction.Field()
    completePayment = CompletePayment.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)