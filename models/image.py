import peewee as pw
from models.base_model import BaseModel
from models.user import User
from playhouse.hybrid import hybrid_property


class Image(BaseModel):
    user = pw.ForeignKeyField(User, backref="images", on_delete="CASCADE")
    image_url = pw.TextField(null=False)

    @hybrid_property
    def full_image_url(self):
        from app import app
        return app.config.get("AWS_S3_DOMAIN") + self.image_url