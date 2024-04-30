import os
from typing import List, Optional, Any

from aqt import mw
from aqt.addons import AddonManager


def __get_addon_manager() -> AddonManager:
    if mw is None:
        raise Exception("Anki is not running")
    return mw.addonManager


def get_addon_path():
    addon_package = __get_addon_manager().addonFromModule(__name__)
    addon_path = __get_addon_manager().addonsFolder(addon_package)
    return addon_path


def get_user_files_folder() -> str:
    addon_id = __get_addon_manager().addonFromModule(__name__)
    user_files_folder = os.path.join(__get_addon_manager().addonsFolder(), addon_id, 'user_files')
    os.makedirs(user_files_folder, exist_ok=True)
    return user_files_folder


def set_default_document_id(doc_id: int) -> None:
    config = get_config()
    config['default_document_id'] = doc_id
    __get_addon_manager().writeConfig(__name__, config)


def remove_default_document() -> None:
    config = get_config()
    config.pop('default_document_id', None)
    __get_addon_manager().writeConfig(__name__, config)


def get_default_document_id() -> Optional[int]:
    config = get_config()
    return config.get('default_document_id')


# New functions to handle scan paths in the configuration
def get_scan_paths() -> List[str]:
    config = get_config()
    return config.get('scan_paths', [])


def add_scan_path(path: str) -> None:
    config = get_config()
    scan_paths = config.get('scan_paths', [])
    if path not in scan_paths:
        scan_paths.append(path)
        config['scan_paths'] = scan_paths
        __get_addon_manager().writeConfig(__name__, config)


def remove_scan_path(path: str) -> None:
    config = get_config()
    scan_paths = config.get('scan_paths', [])
    if path in scan_paths:
        scan_paths.remove(path)
        config['scan_paths'] = scan_paths
        __get_addon_manager().writeConfig(__name__, config)


def get_config() -> dict[str, Any]:
    config = __get_addon_manager().getConfig(__name__)
    return config if config is not None else {}
