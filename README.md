# `FolderUtilities`

**FolderUtilities** adalah library Python untuk memudahkan manipulasi dan scanning folder, cross-platform (Windows/macOS/Linux).
Mendukung operasi dasar folder, scan, filter, dan informasi folder.

## Fitur Utama

1. **System folder helpers**

   * `get_user_folder()`
   * `get_documents_folder()`
   * `get_downloads_folder()`
   * `get_desktop_folder()`
   * `get_appdata_folder()`
   * `get_local_appdata_folder()`
   * `get_temp_folder()`

2. **Basic folder operations**

   * `create_folder(path, exist_ok=True)`
   * `delete_folder(path)`
   * `rename_folder(old_path, new_path)`
   * `copy_folder(src, dst)`
   * `move_folder(src, dst)`
   * `is_empty_folder(path)`
   * `get_folder_size(path)`
   * `ensure_folder(path)`
   * `join_path(*args)`
   * `is_folder_exist(path)`

3. **Scan & Iterasi folder**

   * `scan_folder(...)` → filter berdasarkan ekstensi, keyword, mode (`all/files/dirs`), sorting, recursive
   * `iter_scan_folder(...)` → versi generator, hemat memori untuk folder besar
   * `find_in_folder(path, pattern="*", recursive=True)`

4. **Utility tambahan**

   * `count_items(path, recursive=True)` → hitung jumlah file & folder
   * `get_parent_folder(path)`
   * `get_cwd()` / `change_cwd(path)`
   * `get_absolute_path(path)`

---

## Instalasi

Library ini **pure Python**, tidak ada dependensi eksternal.
Cukup copy file `folder_utilities.py` ke project Anda:

```bash
git clone https://github.com/riffasoft/folder-utilities.git
```

Atau langsung copy `folder_utilities.py` ke project Anda.

---

## Contoh Penggunaan

```python
from folder_utilities import FolderUtilities

# Scan folder Documents, hanya file, recursive, filter ekstensi .txt
files = FolderUtilities.scan_folder(
    FolderUtilities.get_documents_folder(),
    recursive=True,
    mode="files",
    extensions=[".txt"]
)
print(files)

# Iterasi folder Downloads, generator, hemat memori
for f in FolderUtilities.iter_scan_folder(
    FolderUtilities.get_downloads_folder(),
    recursive=False,
    mode="all"
):
    print(f)

# Hitung jumlah file & folder di Desktop
count = FolderUtilities.count_items(FolderUtilities.get_desktop_folder())
print(count)

# Buat folder baru
FolderUtilities.create_folder("D:/TestFolder")

# Hapus folder
FolderUtilities.delete_folder("D:/TestFolder")
```

---

## Lisensi

Lisensi bebas (MIT) – bisa digunakan untuk proyek pribadi maupun komersial.


