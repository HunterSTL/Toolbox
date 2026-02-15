import os, subprocess, platform
from tkinter import messagebox

def read_text_file(path) -> str:
    encodings_to_try = ["utf-8", "utf-8-sig", "cp1252", "latin-1"]

    for encoding in encodings_to_try:
        try:
            with open(path, "r", encoding=encoding, errors="strict") as f:
                return f.read()
        except Exception:
            pass

    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception:
        return None

def open_in_notepad(path) -> None:
    try:
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":     #mac
            subprocess.run(["open", path])
        else:
            subprocess.run(["xdg-open", path])  #linux
    except Exception as e:
        messagebox.showinfo("Hint", f"Result saved at:\n{path}\n\nCould not open directly: {e}")

def get_file_extensions_from_string(string) -> list:
    return split_multiline_text_into_terms(string, starts_with='.')

def get_search_terms_from_string(search_term_string) -> list:
    return split_multiline_text_into_terms(search_term_string)

def split_multiline_text_into_terms(string, starts_with: str = None) -> list:
    """Split multiline `string` into a list of unique, stripped terms.

    -Ignores empty lines.
    -Preserves original order while removing duplicates.
    -If `starts_with` is provided, only lines beginning with that prefix are kept.
    """
    seen = set()
    terms = []
    for line in string.splitlines():
        line = line.strip()
        if not line:
            continue
        if starts_with is not None and not line.startswith(starts_with):
            continue
        if line not in seen:
            seen.add(line)
            terms.append(line)
    return terms