from app import ma
from app.models import Farmer, Admin, Client, ProductBatch, ClientOrder, OrderedItem, Payout

# 1. Farmer Schema
class FarmerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Farmer
        load_instance = True

farmer_schema = FarmerSchema()
farmers_schema = FarmerSchema(many=True)


# 2. Admin Schema
class AdminSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Admin
        load_instance = True

admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)


# 3. Client Schema
class ClientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Client
        load_instance = True

client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)


# 4. ProductBatch Schema
class ProductBatchSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProductBatch
        load_instance = True

batch_schema = ProductBatchSchema()
batches_schema = ProductBatchSchema(many=True)


# 5. ClientOrder Schema
class ClientOrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ClientOrder
        load_instance = True

order_schema = ClientOrderSchema()
orders_schema = ClientOrderSchema(many=True)


# 6. OrderedItem Schema (Many-to-Many Join Table)
class OrderedItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderedItem
        load_instance = True

ordered_item_schema = OrderedItemSchema()
ordered_items_schema = OrderedItemSchema(many=True)


# 7. Payout Schema
class PayoutSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Payout
        load_instance = True

payout_schema = PayoutSchema()
payouts_schema = PayoutSchema(many=True)