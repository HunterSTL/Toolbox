##################################################################################################################################
Concatenate files tool
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
This tool combines the contents of many text‑based files into a single aggregated output file.
The user selects a source directory, defines which file extensions to include, and optionally enables recursive processing of subdirectories.
The tool scans all matching files, reads them using robust multi‑encoding fallback logic, and appends their contents into one structured result file.
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
How it operates:

You select a source directory and target directory.
You enter one or more file extensions (each on its own line).
The tool collects all files that match the extensions, including subdirectories if enabled.
Each file is read safely with multi‑encoding attempts (utf‑8, utf‑8‑sig, cp1252, latin‑1).
A combined output file is generated, including a header before each file’s content.
The result is automatically saved with a timestamp and opened in Notepad.
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Intended use:

Ideal for aggregating logs, exports, markdown notes, code snippets, or any large batch of text‑based files into one unified document.
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Features:

*GUI for selecting source/target folders and specifying extensions
*Optional scanning of all subdirectories
*Progress bar for long file collections
*Robust text‑reading with multi‑encoding fallback
*Concatenates files with clear separation headers
*Saves timestamped output and opens it automatically
##################################################################################################################################
Search files tool
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
This tool scans supported text‑based files in a directory and searches for user‑defined terms.
You can specify multiple search terms (one per line) and optionally enable case‑sensitive searching.
The tool reads each file safely using the same multi‑encoding fallback system and identifies all matches with line and column precision.
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
How it operates:

You select a source directory and target directory.
You enter one or more search terms (each on its own line).
The tool scans all supported text files (.txt, .csv, .log, .md, .rtf).
Each file is read using multi‑encoding fallback.
For each search term, the tool locates all occurrences across all files.
A structured report is generated, including filenames, line numbers, column numbers, and match counts.
The result file is automatically saved and opened in Notepad.
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Intended use:

Ideal for identifying keywords, markers, error messages, timestamps, identifiers, or patterns across large collections of logs, exports, or documentation files.
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Features:

*GUI for selecting source/target folders and defining search terms
*Optional case‑sensitive matching
*Progress bar for large file sets
*Safe text‑reading with multiple encoding attempts
*Searches standard text formats and reports exact match locations
Generates a structured, timestamped match report and opens it automatically
##################################################################################################################################