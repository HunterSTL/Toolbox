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

def get_file_extensions_from_string(file_extensions_string):
    seen_lines = set()
    lines = []
    for line in file_extensions_string.splitlines():
        line = line.strip() #remove spaces before/after term
        if not line:        #ignore empty lines
            continue
        if line[:1] != ".": #disregard lines that don't start with "."
            continue
        if line not in seen_lines:
            seen_lines.add(line)
            lines.append(line)
    return lines

def read_text_file(path):
    encodings_to_try = ["utf-8", "utf-8-sig", "cp1252", "latin-1"]

    for enc in encodings_to_try:
        try:
            with open(path, "r", encoding=enc, errors="strict") as f:
                return f.read()
        except Exception:
            pass

    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception:
        return None

def collect_valid_files_from_directory(directory, include_subdirs, file_extensions):
    collected_files = []
    if include_subdirs:
        for root, dirs, files in os.walk(directory):
            for file in files:
                _, file_extension = os.path.splitext(file)
                if file_extension.lower() in file_extensions:
                    collected_files.append(os.path.join(root, file))
    else:
        for file in os.listdir(directory):
            path = os.path.join(directory, file)
            if os.path.isfile(path):
                _, file_extension = os.path.splitext(path)
                if file_extension.lower() in file_extensions:
                    collected_files.append(path)
    return collected_files

def start(source_directory_string, target_directory_string, file_extensions_string, include_subdirs, progress_bar):
    if source_directory_string == "":
        messagebox.showerror("Input error", "Source directory is empty")
        return
    if target_directory_string == "":
        messagebox.showerror("Input error", "Target directory is empty")
        return
    if file_extensions_string == "":
        messagebox.showerror("Input error", "No file extensions specified")
        return
    if not os.path.isdir(source_directory_string):
        messagebox.showerror("Input error", f"Source directory doesn't exist:\n{source_directory_string}")
        return
    if not os.path.isdir(target_directory_string):
        messagebox.showerror("Input error", f"Target directory doesn't exist:\n{target_directory_string}")
        return

    #each line in the “File extensions” field is split into a file extension
    file_extensions = get_file_extensions_from_string(file_extensions_string)
    if len(file_extensions) == 0:
        messagebox.showerror("File extensions", f"No valid file extensions specified\n(e.g. \".txt\", \".json\", \".py\"...)")
        return

    #read valid files from directory
    try:
        files = collect_valid_files_from_directory(source_directory_string, include_subdirs, file_extensions)
    except Exception as e:
        messagebox.showerror("Error", f"Directory contents could not be read:\n{e}")
        return

    file_count = len(files)

    if file_count == 0:
        messagebox.showerror("Error", f"No files with the following file extensions found:\n{str(file_extensions)}")
        return

    last_progress = -1

    concatenated_text = "#" * 150

    #go through every file in the directory
    for index, file in enumerate(files, start=1):
        #update progress bar
        progress = int((index * 100) / file_count)
        if progress != last_progress:
            progress_bar["value"] = progress
            progress_bar.update_idletasks()
            last_progress = progress

        #read file
        text = read_text_file(file)
        if text is None:
            continue

        #Append file contents to entire text
        concatenated_text += "\n" + file + ":\n\n"
        concatenated_text += text + "\n"
        concatenated_text += "#" * 150

    #reset progress bar
    progress_bar["value"] = 0

    #create and open result file
    result_file_path = target_directory_string + "\\Result_" + strftime("%Y%m%d_%H_%M_%S", gmtime()) + ".txt"

    with open(result_file_path, "w", encoding="utf-8") as f:
        f.write(concatenated_text)

    open_in_notepad(result_file_path)

def initialize_ui():
    #create GUI window with tkinter
    GUI_window = tkinter.Tk()
    GUI_window.config(bg=BACKGROUND_COLOR)
    GUI_window.title("Concatenate files")
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

    #label file extensions
    label_file_extensions = tkinter.Label(
        GUI_window,
        text="File extensions:",
        bg=BACKGROUND_COLOR,
        fg=TEXT_COLOR
    )
    label_file_extensions.grid(row=1, column=0, padx=5, sticky="NE")

    #input file extensions
    entry_file_extensions = tkinter.Text(
        GUI_window,
        bg=INPUT_COLOR,
        fg=TEXT_COLOR,
        height=10,
        width=20
    )
    entry_file_extensions.grid(row=1, column=1, sticky="EW")

    #checkbox include subdirectories
    include_subdirs_var = tkinter.BooleanVar(value=False)
    checkbox_include_subdirs = tkinter.Checkbutton(
        GUI_window,
        text="Include subdirectories",
        onvalue=True,
        offvalue=False,
        variable=include_subdirs_var,
        bg=BACKGROUND_COLOR,
        fg=TEXT_COLOR,
        activebackground=BACKGROUND_COLOR,
        selectcolor=BACKGROUND_COLOR
    )
    checkbox_include_subdirs.grid(row=2, column=1, sticky="W")

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

    #selct target directory button
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

    #start button
    start_button = tkinter.Button(
        GUI_window,
        text="Start",
        bg=BUTTON_COLOR,
        fg=TEXT_COLOR,
        width=10,
        command=lambda: start(
            entry_source_directory.get(),
            entry_target_directory.get(),
            entry_file_extensions.get("1.0", "end-1c"),
            include_subdirs_var.get(),
            tk_progress_bar
        )
    )
    start_button.grid(row=4, column=0, padx=5, pady=2, sticky="EW")

    return GUI_window

if __name__ == "__main__":
    GUI_Window = initialize_ui()
    GUI_Window.mainloop()