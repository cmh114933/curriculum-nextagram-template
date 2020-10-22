from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from models.image import Image
from flask_login import login_required, current_user
from helpers import upload_to_s3


images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')


@images_blueprint.route('/new', methods=['GET'])
@login_required
def new():
    return render_template('images/new.html')


@images_blueprint.route('/', methods=['POST'])
@login_required
def create():
    if "user_image" not in request.files:
        return "No user_image key in request.files"

    file = request.files["user_image"]

    if file.filename == "":
        return "Please select a file"

    if file:
        file_path = upload_to_s3(file, current_user.id)

        new_image = Image(image_url=file_path, user=current_user.id)

        if new_image.save():
            flash("Upload successfully.")
            return redirect(url_for("users.show", username=current_user.username))
        else:
            return "Could not upload profile image, please go back and try again!"
    else:
        return redirect(url_for("images.new"))
