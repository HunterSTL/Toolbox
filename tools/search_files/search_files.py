import os, sys, ctypes, tkinter
from tkinter import filedialog, messagebox, ttk
from time import gmtime, strftime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from core import UI_COLORS
from core import TextUtilities as TU

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

    #each line in the “Search terms” field becomes a search term.
    search_terms = TU.split_multiline_text_into_terms(search_terms_string)

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
        text = TU.read_text_file(full_path)

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

    #create and open result file
    result_file_name = "Result_" + strftime("%Y%m%d_%H_%M_%S", gmtime()) + ".txt"
    result_file_path = os.path.join(target_directory_string, result_file_name)

    with open(result_file_path, "w") as f:
        f.write("\n".join(report_lines))

    TU.open_in_notepad(result_file_path)

def initialize_ui():
    #create GUI window with tkinter
    GUI_window = tkinter.Tk()
    GUI_window.config(bg=UI_COLORS["background"])
    GUI_window.title("Search files")

    #load icon
    icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
    if os.path.exists(icon_path):
        icon_image = tkinter.PhotoImage(file=icon_path)
        GUI_window.iconphoto(True, icon_image)

    if sys.platform == "win32":
        try:
            #force dark mode for the title bar
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                ctypes.windll.user32.GetParent(GUI_window.winfo_id()),
                20,
                ctypes.byref(ctypes.c_int(1)),
                ctypes.sizeof(ctypes.c_int(1))
            )
        except Exception:
            pass

    #label source directory
    label_source_directory = tkinter.Label(
        GUI_window,
        text="Source directory:",
        bg=UI_COLORS["background"],
        fg=UI_COLORS["text"]
    )
    label_source_directory.grid(row=0, column=0, padx=5, sticky="E")

    #input source directory
    entry_source_directory = tkinter.Entry(
        GUI_window,
        bg=UI_COLORS["input"],
        fg=UI_COLORS["text"],
        width=50
    )
    entry_source_directory.grid(row=0, column=1, sticky="EW")

    #select source directory button
    select_source_directory_button = tkinter.Button(
        GUI_window,
        text="Select",
        bg=UI_COLORS["button"],
        fg=UI_COLORS["text"],
        width=10,
        command=lambda: select_source_directory(entry_source_directory, entry_target_directory)
    )
    select_source_directory_button.grid(row=0, column=2, padx=5, pady=2)

    #label search terms
    label_search_terms = tkinter.Label(
        GUI_window,
        text="Search terms:",
        bg=UI_COLORS["background"],
        fg=UI_COLORS["text"]
    )
    label_search_terms.grid(row=1, column=0, padx=5, sticky="NE")

    #input search terms
    entry_search_terms = tkinter.Text(
        GUI_window,
        bg=UI_COLORS["input"],
        fg=UI_COLORS["text"],
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
        bg=UI_COLORS["background"],
        fg=UI_COLORS["text"],
        activebackground=UI_COLORS["background"],
        selectcolor=UI_COLORS["background"]
    )
    checkbox_case_sensitive.grid(row=2, column=1, sticky="W")

    #label target directory
    label_target_directory = tkinter.Label(
        GUI_window,
        text="Target directory:",
        bg=UI_COLORS["background"],
        fg=UI_COLORS["text"]
    )
    label_target_directory.grid(row=3, column=0, padx=5, sticky="E")

    #input target directory
    entry_target_directory = tkinter.Entry(
        GUI_window,
        bg=UI_COLORS["input"],
        fg=UI_COLORS["text"],
        width=50
    )
    entry_target_directory.grid(row=3, column=1, sticky="EW")

    #select target directory button
    select_target_directory_button = tkinter.Button(
        GUI_window,
        text="Select",
        bg=UI_COLORS["button"],
        fg=UI_COLORS["text"],
        width=10,
        command=lambda: select_target_directory(entry_target_directory)
    )
    select_target_directory_button.grid(row=3, column=2, padx=5, pady=2)

    #progress bar
    progress_bar_style = ttk.Style(GUI_window)
    progress_bar_style.theme_use("default")
    progress_bar_style.configure("Custom.Horizontal.TProgressbar", background="green", troughcolor=UI_COLORS["input"])
    tk_progress_bar = ttk.Progressbar(GUI_window, style="Custom.Horizontal.TProgressbar")
    tk_progress_bar.grid(row=4, column=1, columnspan=1, sticky="EW")

    #start search button
    search_button = tkinter.Button(
        GUI_window,
        text="Start",
        bg=UI_COLORS["button"],
        fg=UI_COLORS["text"],
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