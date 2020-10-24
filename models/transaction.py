import peewee as pw
from models.base_model import BaseModel
from models.user import User
from models.image import Image


class Transaction(BaseModel):
    user = pw.ForeignKeyField(User, backref="donations", on_delete="CASCADE")
    image = pw.ForeignKeyField(Image, backref="donations", on_delete="CASCADE")
    amount = pw.DecimalField(null=False)
