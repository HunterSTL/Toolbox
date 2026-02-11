import tkinter
from tkinter import filedialog, messagebox, ttk
import ctypes
import os
from time import gmtime, strftime

#GUI colors
TITLE_BAR_COLOR ="#202020"
BACKGROUND_COLOR = "#404040"
BUTTON_COLOR = "#505050"
INPUT_COLOR = "#606060"
TEXT_COLOR = "#FFFFFF"
LINE = "-" * 150

def select_source_directory(source_entry, target_entry):
    directory_path = filedialog.askdirectory()
    if directory_path:
        source_entry.delete(0, tkinter.END)
        source_entry.insert(0, directory_path)

        if target_entry.get() == "":
            target_entry.insert(0, directory_path)

def select_target_directory(target_entry):
    directory_path = filedialog.askdirectory()
    if directory_path:
        target_entry.delete(0, tkinter.END)
        target_entry.insert(0, directory_path)

def open_in_notepad(path):
    try:
        os.startfile(path)
    except Exception as e:
        messagebox.showinfo("Hint", f"Result saved at:\n{path}\n\nCould not open notepad directly: {e}")

def get_search_terms_from_string(search_term_string):
    seen_lines = set()
    lines = []
    for line in search_term_string.splitlines():
        line = line.strip() #remove spaces before/after term
        if not line:        #ignore empty lines
            continue
        if line not in seen_lines:
            seen_lines.add(line)
            lines.append(line)
    return lines

def read_text_file(path):
    encodings_to_try = ["utf-8", "utf-8-sig", "cp1252", "latin-1"]
    last_error = None

    for enc in encodings_to_try:
        try:
            with open(path, "r", encoding=enc, errors="strict") as f:
                return f.read(), None
        except Exception as e:
            last_error = f"{type(e).__name__}: {e}"

    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read(), None
    except Exception as e:
        specific = last_error or f"{type(e).__name__}: {e}"
        return None, f"Read error. Last attempt failed: {specific}"


def find_occurrences(text, search_term, case_sensitive):
    text_to_search = text if case_sensitive else text.lower()
    search_term_to_find = search_term if case_sensitive else search_term.lower()

    positions = []
    for line_num, line in enumerate(text_to_search.splitlines(), start=1):
        start = 0
        while True:
            idx = line.find(search_term_to_find, start)
            if idx == -1:
                break
            positions.append((line_num, idx + 1))
            start = idx + 1
    return positions

def add_positions_to_results(results, search_term, file, positions):
    """
    dictionary of dictionaries of list of tuples (lol)
    results = {
        "search_term": {
            "file": [(line, column), (line, column),...]
        }
    }
    """

    if search_term not in results:
        results[search_term] = {}

    if len(positions) == 0:
        return results

    if file not in results[search_term]:
        results[search_term][file] = []

    for position in positions:
        results[search_term][file].append(position)

    return results

def start_search(source_directory_string, target_directory_string, search_terms_string, case_sensitive, progress_bar):
    if source_directory_string == "":
        messagebox.showerror("Input error", "Source directory is empty")
        return
    if target_directory_string == "":
        messagebox.showerror("Input error", "Target directory is empty")
        return
    if search_terms_string == "":
        messagebox.showerror("Input error", "No search terms specified")
        return
    if not os.path.isdir(source_directory_string):
        messagebox.showerror("Input error", f"Source directory doesn't exist:\n{source_directory_string}")
        return
    if not os.path.isdir(target_directory_string):
        messagebox.showerror("Input error", f"Target directory doesn't exist:\n{target_directory_string}")
        return

    results = {}
    errors = []

    #each line in the “Search terms” field becomes a search term.
    search_terms = get_search_terms_from_string(search_terms_string)

    #attempt to read directory
    try:
        files = os.listdir(source_directory_string)
        file_count = len(files)
    except Exception as e:
        messagebox.showerror("Error", f"Directory contents could not be read:\n{e}")
        return

    last_progress = -1

    #go through every file in the directory
    for index, file in enumerate(files, start=1):
        #update progress bar
        progress = int((index * 100) / file_count)
        if progress != last_progress:
            progress_bar["value"] = progress
            progress_bar.update_idletasks()
            last_progress = progress

        full_path = os.path.join(source_directory_string, file)

        #skip directories
        if not os.path.isfile(full_path):
            continue

        #skip files that don't end with ".txt", ".csv", ".log", ".md" or ".rtf"
        _, ext = os.path.splitext(file)
        if ext.lower() not in [".txt", ".csv", ".log", ".md", ".rtf"]:
            continue

        #read file
        text, err = read_text_file(full_path)
        if text is None:
            errors.append((full_path, err or "Unknown error while reading"))
            continue

        #search for occurrences of the search term and write them in the results dictionary
        for search_term in search_terms:
            positions = find_occurrences(text, search_term, case_sensitive)
            results = add_positions_to_results(results, search_term, file, positions)

    #reset progress bar
    progress_bar["value"] = 0

    #assemble results
    report_lines = [
        LINE,
        f" Directory:\t{source_directory_string}\n",
        LINE
    ]

    for search_term, file_dictionary in results.items():
        report_lines.append(f"Search term:\t{search_term}\n")

        if len(file_dictionary) == 0:
            report_lines.append("no matches")
            report_lines.append(LINE)
            continue

        total_count = 0
        tmp_report_lines = []

        for file, positions in file_dictionary.items():
            tmp_report_lines.append(f"{file}:")
            for line, column in positions:
                tmp_report_lines.append(f"\tLine {line}, Column {column}")
                total_count += 1
        tmp_report_lines.append(LINE)

        report_lines.append(f"{total_count} Matches:\n")
        report_lines.extend(tmp_report_lines)

    #print errors
    if errors:
        report_lines.append("\nError reading the following files:")
        for path, message in errors:
            report_lines.append(f"\t{path}\nReason: {message}\n")
        report_lines.append(LINE)

    #create and open result file
    result_file_path = target_directory_string + "\\Result_" + strftime("%Y%m%d_%H_%M_%S", gmtime()) + ".txt"
    open(result_file_path, "x")

    with open(result_file_path, "w") as f:
        f.write("\n".join(report_lines))

    open_in_notepad(result_file_path)

def initialize_ui():
    #create GUI window with tkinter
    GUI_window = tkinter.Tk()
    GUI_window.config(bg=BACKGROUND_COLOR)
    GUI_window.title("Search files")
    icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
    GUI_window.iconbitmap(icon_path)

    #force dark mode for the title bar
    ctypes.windll.dwmapi.DwmSetWindowAttribute(
        ctypes.windll.user32.GetParent(GUI_window.winfo_id()),
        20,
        ctypes.byref(ctypes.c_int(1)),
        ctypes.sizeof(ctypes.c_int(1))
    )

    #label source directory
    label_source_directory = tkinter.Label(
        GUI_window,
        text="Source directory:",
        bg=BACKGROUND_COLOR,
        fg=TEXT_COLOR
    )
    label_source_directory.grid(row=0, column=0, padx=5, sticky="E")

    #input source directory
    entry_source_directory = tkinter.Entry(
        GUI_window,
        bg=INPUT_COLOR,
        fg=TEXT_COLOR,
        width=50
    )
    entry_source_directory.grid(row=0, column=1, sticky="EW")

    #select source directory button
    select_source_directory_button = tkinter.Button(
        GUI_window,
        text="Select",
        bg=BUTTON_COLOR,
        fg=TEXT_COLOR,
        width=10,
        command=lambda: select_source_directory(entry_source_directory, entry_target_directory)
    )
    select_source_directory_button.grid(row=0, column=2, padx=5, pady=2)

    #label search terms
    label_search_terms = tkinter.Label(
        GUI_window,
        text="Search terms:",
        bg=BACKGROUND_COLOR,
        fg=TEXT_COLOR
    )
    label_search_terms.grid(row=1, column=0, padx=5, sticky="NE")

    #input search terms
    entry_search_terms = tkinter.Text(
        GUI_window,
        bg=INPUT_COLOR,
        fg=TEXT_COLOR,
        height=10,
        width=20
    )
    entry_search_terms.grid(row=1, column=1, sticky="EW")

    #checkbox case sensitive
    case_sensitive_var = tkinter.BooleanVar(value=False)
    checkbox_case_sensitive = tkinter.Checkbutton(
        GUI_window,
        text="Case sensitive",
        onvalue=True,
        offvalue=False,
        variable=case_sensitive_var,
        bg=BACKGROUND_COLOR,
        fg=TEXT_COLOR,
        activebackground=BACKGROUND_COLOR,
        selectcolor=BACKGROUND_COLOR
    )
    checkbox_case_sensitive.grid(row=2, column=1, sticky="W")

    #label target directory
    label_target_directory = tkinter.Label(
        GUI_window,
        text="Target directory:",
        bg=BACKGROUND_COLOR,
        fg=TEXT_COLOR
    )
    label_target_directory.grid(row=3, column=0, padx=5, sticky="E")

    #input target directory
    entry_target_directory = tkinter.Entry(
        GUI_window,
        bg=INPUT_COLOR,
        fg=TEXT_COLOR,
        width=50
    )
    entry_target_directory.grid(row=3, column=1, sticky="EW")

    #select target directory button
    select_target_directory_button = tkinter.Button(
        GUI_window,
        text="Select",
        bg=BUTTON_COLOR,
        fg=TEXT_COLOR,
        width=10,
        command=lambda: select_target_directory(entry_target_directory)
    )
    select_target_directory_button.grid(row=3, column=2, padx=5, pady=2)

    #progress bar
    progress_bar_style = ttk.Style(GUI_window)
    progress_bar_style.theme_use("default")
    progress_bar_style.configure("Custom.Horizontal.TProgressbar", background="green", troughcolor=INPUT_COLOR)
    tk_progress_bar = ttk.Progressbar(GUI_window, style="Custom.Horizontal.TProgressbar")
    tk_progress_bar.grid(row=4, column=1, columnspan=1, sticky="EW")

    #start search button
    search_button = tkinter.Button(
        GUI_window,
        text="Start",
        bg=BUTTON_COLOR,
        fg=TEXT_COLOR,
        width=10,
        command=lambda: start_search(
            entry_source_directory.get(),
            entry_target_directory.get(),
            entry_search_terms.get("1.0", "end-1c"),
            case_sensitive_var.get(),
            tk_progress_bar
        )
    )
    search_button.grid(row=4, column=0, padx=5, pady=2, sticky="EW")

    return GUI_window

if __name__ == "__main__":
    GUI_Window = initialize_ui()
    GUI_Window.mainloop()