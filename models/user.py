from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash
import re
from flask_login import UserMixin
from playhouse.hybrid import hybrid_property

class User(BaseModel, UserMixin):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password_hash = pw.CharField(unique=False)
    image_path= pw.CharField(null=True)
    password=None
    is_private= pw.BooleanField(default=False)

    def follow(self,idol):
        from models.fan_idol import FanIdol
        # check whether current user follow idol before
        # relationship = FanIdol.get_or_none(fan=self.id, idol=idol.id)
        if self.follow_status(idol) == None:
            new_rel = FanIdol(fan=self.id, idol=idol.id)
            if idol.is_private == False:  # public idol
                new_rel.is_approved = True
            return new_rel.save()
        else:
            return 0

    def unfollow(self, idol):
        from models.fan_idol import FanIdol
        return FanIdol.delete().where(FanIdol.idol==idol.id, FanIdol.fan==self.id).execute()

    def follow_status(self, idol):
        from models.fan_idol import FanIdol
        return FanIdol.get_or_none(fan=self.id,idol=idol.id)

    @hybrid_property
    def idols(self):
        # return a list of idol user instances that only approved
        from models.fan_idol import FanIdol
        idols_id = FanIdol.select(FanIdol.idol).where(FanIdol.fan==self.id, FanIdol.is_approved==True)
        idols = User.select().where(User.id.in_(idols_id))
        return idols

    @hybrid_property
    def fans(self):
        # return a list of fan user instances that only approved
        from models.fan_idol import FanIdol
        fans_id = FanIdol.select(FanIdol.fan).where(FanIdol.idol==self.id, FanIdol.is_approved==True)
        fans = User.select().where(User.id.in_(fans_id))
        return fans

    @hybrid_property
    def idol_requests(self):
        from models.fan_idol import FanIdol
        idols_id = FanIdol.select(FanIdol.idol).where(FanIdol.fan==self.id, FanIdol.is_approved==False)
        return User.select().where(User.id.in_(idols_id))

    @hybrid_property
    def fan_requests(self):
        from models.fan_idol import FanIdol
        fans_id = FanIdol.select(FanIdol.fan).where(FanIdol.idol==self.id, FanIdol.is_approved==False)
        return User.select().where(User.id.in_(fans_id))

    def approve(self, fan):
        from models.fan_idol import FanIdol
        relationship = FanIdol.get_or_none(idol=self.id,fan=fan.id)
        relationship.is_approved = True
        return relationship.save()

    @hybrid_property
    def image_feed(self):
        from models.fan_idol import FanIdol
        from models.image import Image
        approved_idols_id = FanIdol.select(FanIdol.idol).where(FanIdol.fan==self.id, FanIdol.is_approved==True)
        idols_with_me = [x.idol for x in approved_idols_id]  # return a list of idols' id
        idols_with_me.append(self.id) # add your own id
        return Image.select().where(Image.user.in_(idols_with_me)).order_by(Image.created_at.desc())

    @hybrid_property
    def profile_image_path(self):
        from app import app
        if not self.image_path:
            return app.config.get("AWS_S3_DOMAIN") + "mickey.jpg"
        return app.config.get("AWS_S3_DOMAIN") + self.image_path

    def validate(self):
        existing_email = User.get_or_none(User.email == self.email)
        existing_username = User.get_or_none(User.username == self.username)
        print("User validation in process")
        if existing_email and self.id != existing_email.id:
            self.errors.append("Email must be unique")
        
        if existing_username  and self.id != existing_username.id:
            self.errors.append("Username must be unique")

        if self.password:
            if len(self.password) < 6:
                self.errors.append("Password must be at least 6 characters")

            if not re.search("[a-z]", self.password):
                self.errors.append("Password must include lowercase")

            if not re.search("[A-Z]", self.password):
                self.errors.append("Password must include uppercase")

            if not re.search("[\[\]\*\^\%]", self.password):
                self.errors.append("Password must include special characters")

            if len(self.errors) == 0:
                print("No errors detected")
                self.password_hash = generate_password_hash(self.password)
        
        if not self.password_hash:
            self.errors.append("Password must be present")