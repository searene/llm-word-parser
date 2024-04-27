import os
from typing import List, Optional

from aqt import mw


def get_addon_path():
    addon_package = mw.addonManager.addonFromModule(__name__)
    addon_path = mw.addonManager.addonsFolder(addon_package)
    return addon_path


def get_user_files_folder():
    addon_id = mw.addonManager.addonFromModule(__name__)
    user_files_folder = os.path.join(mw.addonManager.addonsFolder(), addon_id, 'user_files')
    os.makedirs(user_files_folder, exist_ok=True)
    return user_files_folder


def set_default_document_id(doc_id):
    config = mw.addonManager.getConfig(__name__)
    config['default_document_id'] = doc_id
    mw.addonManager.writeConfig(__name__, config)


def remove_default_document():
    config = mw.addonManager.getConfig(__name__)
    config.pop('default_document_id', None)
    mw.addonManager.writeConfig(__name__, config)


def get_default_document_id() -> Optional[int]:
    config = mw.addonManager.getConfig(__name__)
    return config.get('default_document_id')


# New functions to handle scan paths in the configuration
def get_scan_paths() -> List[str]:
    config = mw.addonManager.getConfig(__name__)
    return config.get('scan_paths', [])


def add_scan_path(path: str):
    config = mw.addonManager.getConfig(__name__)
    scan_paths = config.get('scan_paths', [])
    if path not in scan_paths:
        scan_paths.append(path)
        config['scan_paths'] = scan_paths
        mw.addonManager.writeConfig(__name__, config)


def remove_scan_path(path: str):
    config = mw.addonManager.getConfig(__name__)
    scan_paths = config.get('scan_paths', [])
    if path in scan_paths:
        scan_paths.remove(path)
        config['scan_paths'] = scan_paths
        mw.addonManager.writeConfig(__name__, config)
