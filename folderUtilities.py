import os
import shutil
import platform
from pathlib import Path

class FolderUtilities:
    # =====================================================
    # ============= SYSTEM FOLDER HELPERS =================
    # =====================================================
    @staticmethod
    def get_user_folder():
        """Return user home folder."""
        return str(Path.home())

    @staticmethod
    def get_documents_folder():
        """Cross-platform Documents folder detection."""
        home = Path.home()
        system = platform.system()

        if system == "Windows":
            return str(home / "Documents")
        elif system == "Darwin":  # macOS
            return str(home / "Documents")
        else:  # Linux and others
            xdg_documents = os.environ.get("XDG_DOCUMENTS_DIR")
            if xdg_documents:
                return os.path.expandvars(xdg_documents)
            return str(home / "Documents")

    @staticmethod
    def get_downloads_folder():
        """Cross-platform Downloads folder detection."""
        home = Path.home()
        system = platform.system()

        if system == "Windows":
            return str(home / "Downloads")
        elif system == "Darwin":  # macOS
            return str(home / "Downloads")
        else:  # Linux and others
            xdg_download = os.environ.get("XDG_DOWNLOAD_DIR")
            if xdg_download:
                return os.path.expandvars(xdg_download)
            return str(home / "Downloads")

    @staticmethod
    def get_desktop_folder():
        """Cross-platform Desktop folder detection."""
        home = Path.home()
        system = platform.system()

        if system == "Windows":
            return str(home / "Desktop")
        elif system == "Darwin":  # macOS
            return str(home / "Desktop")
        else:  # Linux and others
            xdg_desktop = os.environ.get("XDG_DESKTOP_DIR")
            if xdg_desktop:
                return os.path.expandvars(xdg_desktop)
            return str(home / "Desktop")

    @staticmethod
    def get_appdata_folder():
        """Windows AppData\Roaming or ~/.config for Linux/macOS."""
        system = platform.system()

        if system == "Windows":
            return os.environ.get("APPDATA", str(Path.home() / "AppData" / "Roaming"))
        else:
            return str(Path.home() / ".config")

    @staticmethod
    def get_local_appdata_folder():
        """Windows LocalAppData or ~/.local/share for Linux/macOS."""
        system = platform.system()

        if system == "Windows":
            return os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData" / "Local"))
        else:
            return str(Path.home() / ".local" / "share")

    @staticmethod
    def get_temp_folder():
        """Return temp folder (cross-platform)."""
        return str(Path(os.getenv("TEMP") or Path(os.getenv("TMPDIR", "/tmp"))))
        


    # =====================================================
    # ============= BASIC FOLDER UTILITIES ================
    # =====================================================

    @staticmethod
    def create_folder(path: str, exist_ok: bool = True):
        """Create a folder (with parents)."""
        Path(path).mkdir(parents=True, exist_ok=exist_ok)
        return str(Path(path).resolve())

    @staticmethod
    def delete_folder(path: str):
        """Delete folder and all contents."""
        if Path(path).exists() and Path(path).is_dir():
            shutil.rmtree(path)
            return True
        return False

    @staticmethod
    def rename_folder(old_path: str, new_path: str):
        """Rename/move a folder."""
        if Path(old_path).exists() and Path(old_path).is_dir():
            Path(old_path).rename(new_path)
            return str(Path(new_path).resolve())
        return None
    
    @staticmethod
    def copy_folder(src, dst):
        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
            return True
        return False

    @staticmethod
    def move_folder(src, dst):
        if os.path.isdir(src):
            shutil.move(src, dst)
            return True
        return False
    
    # =====================================================
    # ============= More FOLDER UTILITIES ================
    # =====================================================    


    @staticmethod
    def is_empty_folder(path: str):
        """Check if folder exists and is empty."""
        p = Path(path)
        return p.exists() and p.is_dir() and not any(p.iterdir())

    @staticmethod
    def get_folder_size(path: str):
        """Get total folder size in bytes (recursive)."""
        total_size = 0
        p = Path(path)
        if p.exists() and p.is_dir():
            for f in p.rglob("*"):
                if f.is_file():
                    total_size += f.stat().st_size
        return total_size

    @staticmethod
    def ensure_folder(path: str):
        """Ensure folder exists, create if not."""
        return FolderUtilities.create_folder(path, exist_ok=True)

    @staticmethod
    def join_path(*args):
        """Join path parts safely."""
        return str(Path(*args))

    @staticmethod
    def is_folder_exist(path):
        return os.path.isdir(path)
    # =====================================================
    # ============= SCAN DATA UTILITIES ===================
    # =====================================================
    @staticmethod
    def scan_folder(
        path: str,
        recursive: bool = False,
        fullpath: bool = True,
        mode: str = "all",
        extensions: list[str] | None = None,
        keyword: str | None = None,
        sort_by: str | None = "name",  # new parameter
        reverse: bool = False           # ascending / descending
    ):
        """
        Scan folder contents dengan filter ekstensi & keyword, plus sorting.

        Params:
            path (str)       : path folder target
            recursive (bool) : True -> rekursif (seperti os.walk)
            fullpath (bool)  : True -> hasil berupa full path, False -> hanya nama
            mode (str)       : "all", "files", "dirs"
            extensions (list): filter berdasarkan ekstensi, ex: [".jpg", ".png"]
            keyword (str)    : filter nama file/folder mengandung string ini
            sort_by (str)    : None, "name", "ctime", "mtime", "size"
            reverse (bool)   : True -> descending, False -> ascending

        Return:
            - recursive=False -> list sederhana
            - recursive=True  -> list of dict {root, dirs, files}
        """
        p = Path(path)
        if not p.exists() or not p.is_dir():
            return []

        def match_filter(entry: Path):
            if extensions and entry.is_file():
                if entry.suffix.lower() not in [e.lower() for e in extensions]:
                    return False
            if keyword and keyword.lower() not in entry.name.lower():
                return False
            return True

        def sort_items(items: list[Path]):
            if not sort_by:
                return items
            if sort_by == "name":
                items.sort(key=lambda x: x.name.lower(), reverse=reverse)
            elif sort_by == "ctime":
                items.sort(key=lambda x: x.stat().st_ctime, reverse=reverse)
            elif sort_by == "mtime":
                items.sort(key=lambda x: x.stat().st_mtime, reverse=reverse)
            elif sort_by == "size":
                items.sort(key=lambda x: x.stat().st_size, reverse=reverse)
            return items

        # --- non recursive ---
        if not recursive:
            items = []
            children = sort_items([c for c in p.iterdir() if match_filter(c)])
            for child in children:
                if mode == "files" and not child.is_file():
                    continue
                if mode == "dirs" and not child.is_dir():
                    continue
                items.append(str(child) if fullpath else child.name)
            return items

        # --- recursive ---
        result = []
        for root, dirs, files in os.walk(path):
            entry = {"root": root, "dirs": [], "files": []}

            dir_paths = [Path(root) / d for d in dirs]
            file_paths = [Path(root) / f for f in files]

            if mode in ("all", "dirs"):
                dirs_filtered = [d for d in dir_paths if match_filter(d)]
                dirs_sorted = sort_items(dirs_filtered)
                entry["dirs"] = [str(d) if fullpath else d.name for d in dirs_sorted]

            if mode in ("all", "files"):
                files_filtered = [f for f in file_paths if match_filter(f)]
                files_sorted = sort_items(files_filtered)
                entry["files"] = [str(f) if fullpath else f.name for f in files_sorted]

            result.append(entry)
        return result


    @staticmethod
    def iter_scan_folder(
        path: str,
        recursive: bool = False,
        fullpath: bool = True,
        mode: str = "all",
        extensions: list[str] | None = None,
        keyword: str | None = None,
        ):
        """
        Iterate folder contents (generator version of scan_folder) dengan filter.

        Params:
            path (str)       : target folder
            recursive (bool) : True -> recursive (like os.walk)
            fullpath (bool)  : True -> return full path, False -> only name
            mode (str)       : "all", "files", "dirs"
            extensions (list): filter ekstensi (misalnya [".jpg", ".png"])
            keyword (str)    : filter nama file/folder mengandung string

        Yield:
            - recursive=False -> item by item (str)
            - recursive=True  -> dict {root, dirs, files} per step
        """
        p = Path(path)
        if not p.exists() or not p.is_dir():
            return

        def match_filter(entry: Path):
            if extensions and entry.is_file():
                if entry.suffix.lower() not in [e.lower() for e in extensions]:
                    return False
            if keyword and keyword.lower() not in entry.name.lower():
                return False
            return True

        # --- non recursive ---
        if not recursive:
            for child in p.iterdir():
                if mode == "files" and not child.is_file():
                    continue
                if mode == "dirs" and not child.is_dir():
                    continue
                if not match_filter(child):
                    continue
                yield str(child) if fullpath else child.name
            return

        # --- recursive ---
        for root, dirs, files in os.walk(path):
            entry = {"root": root, "dirs": [], "files": []}

            if mode in ("all", "dirs"):
                entry["dirs"] = [
                    str(Path(root) / d) if fullpath else d
                    for d in dirs
                    if match_filter(Path(root) / d)
                ]
            if mode in ("all", "files"):
                entry["files"] = [
                    str(Path(root) / f) if fullpath else f
                    for f in files
                    if match_filter(Path(root) / f)
                ]

            yield entry


    @staticmethod
    def find_in_folder(path: str, pattern="*", recursive=True):
        p = Path(path)
        if not p.exists() or not p.is_dir():
            return []
        if recursive:
            return [str(f) for f in p.rglob(pattern)]
        else:
            return [str(f) for f in p.glob(pattern)]

    @staticmethod
    def count_items(path: str, recursive: bool = True):
        """
        Hitung jumlah file & folder dalam sebuah direktori.

        Params:
            path (str)       : path target
            recursive (bool) : True -> hitung semua subfolder (rekursif)
                            False -> hanya level 1

        Return:
            dict -> {"files": int, "dirs": int, "total": int}
        """
        p = Path(path)
        if not p.exists() or not p.is_dir():
            return {"files": 0, "dirs": 0, "total": 0}

        if recursive:
            files = sum(1 for _ in p.rglob("*") if _.is_file())
            dirs = sum(1 for _ in p.rglob("*") if _.is_dir())
        else:
            files = sum(1 for _ in p.iterdir() if _.is_file())
            dirs = sum(1 for _ in p.iterdir() if _.is_dir())

        return {"files": files, "dirs": dirs, "total": files + dirs}

    # =====================================================
    # ============= NEW EXTRA UTILITIES ===================
    # =====================================================
    @staticmethod
    def get_parent_folder(path: str):
        """Return parent folder of given path."""
        return str(Path(path).parent.resolve())

    @staticmethod
    def get_cwd():
        """Get current working directory."""
        return str(Path.cwd())

    @staticmethod
    def change_cwd(path: str):
        """Change current working directory."""
        os.chdir(path)
        return str(Path.cwd())

    @staticmethod
    def get_absolute_path(path: str):
        """Return absolute normalized path."""
        return str(Path(path).resolve())



