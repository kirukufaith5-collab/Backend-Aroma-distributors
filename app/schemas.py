from app import ma
from app.models import User, Batch,Order

#Schema to serialize Batch data
class BatchSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Batch
        load_instance = True

#Schema to serialize Order data
class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model =Order
        load_instance =True

#Instantiate schemas
batch_schema =BatchSchema()
batches_schema =BatchSchema(many=True)

order_schema =OrderSchema()
orders_schema =OrderSchema(many =True)