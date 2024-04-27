import os

from aqt import mw


def get_addon_path():
    addon_package = mw.addonManager.addonFromModule(__name__)
    addon_path = mw.addonManager.addonsFolder(addon_package)
    return addon_path


def get_user_files_folder():
    # Using __name__ to find the module from which this function is called
    addon_id = mw.addonManager.addonFromModule(__name__)
    # Compute the path to the user_files folder within the add-on's directory
    user_files_folder = os.path.join(mw.addonManager.addonsFolder(), addon_id, 'user_files')
    # Ensure the directory exists
    os.makedirs(user_files_folder, exist_ok=True)
    return user_files_folder


def set_default_document_id(doc_id):
    config = mw.addonManager.getConfig(__name__)
    config['default_document_id'] = doc_id
    mw.addonManager.writeConfig(__name__, config)
