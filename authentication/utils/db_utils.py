import os
from django.conf import settings
from django.core.exceptions import ValidationError

from common.key_manager import KeyManager
from django.utils.translation import gettext as _


def get_user_profile_path(instance, filename):
    """
    Returns the path to save user profile image

    """

    ext = filename.split(".")[-1]

    return os.path.join(
        settings.USER_PROFILE_FOLDER, f"profile-{instance.id}.{ext}"
    )


def validate_profile_size(value):
    filesize = value.size
    filesize_in_mb = filesize / (1024 * 1024)
    max_file_size = KeyManager.get(name="MAX_PROFILE_SIZE_MB" , default=5.0, value_type=float)

    if filesize_in_mb > max_file_size:
        raise ValidationError(
            _("the max size of file is :{}MB").format(max_file_size)
        )
    else:
        return value