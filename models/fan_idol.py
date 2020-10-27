from models.base_model import BaseModel
import peewee as pw
from models.user import User

class FanIdol(BaseModel):
    idol = pw.ForeignKeyField(User,on_delete='CASCADE')
    fan = pw.ForeignKeyField(User,on_delete='CASCADE')
    is_approved = pw.BooleanField(default=False)

