from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash
import re


class User(BaseModel):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password_hash = pw.CharField(unique=False)
    password=None

    def validate(self):
        existing_email = User.get_or_none(User.email == self.email)
        existing_username = User.get_or_none(User.username == self.username)
        print("User validation in process")
        if existing_email:
            self.errors.append("Email must be unique")
        
        if existing_username:
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