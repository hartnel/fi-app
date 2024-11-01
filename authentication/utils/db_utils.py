import os
from django.conf import settings


def get_user_profile_path(instance, filename):
    """
    Returns the path to save user profile image

    """

    ext = filename.split(".")[-1]

    return os.path.join(
        settings.USER_PROFILE_FOLDER, f"profile-{instance.id}.{ext}"
    )