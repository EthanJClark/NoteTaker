# Streamlit NoteTaker

A simple, organized note-taking web app built with Streamlit. Supports multiple notes, auto-saving, text transformation tools, and file import/export.

## Features
- Sidebar list of notes with create/select/delete
- Auto-save on edit (stored locally in `notes/` as Markdown)
- Editor tab with Markdown-friendly textarea and editable title
- Text Tools tab with:
  - Uppercase / Lowercase / Title Case / Trim Spaces
  - Find & Replace
  - Live word/char/line counts
- File tab with:
  - Download current note as `.md`
  - Import `.txt` or `.md` (appends to current note)
- Notes metadata persisted in `notes/index.json`

## Project Structure
```
app.py                # Streamlit application
notes/                # Created automatically; stores note .md files and index.json
requirements.txt      # Python dependencies
```

## Quick Start
Create and activate your virtual environment if not already:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
Install dependencies:
```powershell
pip install -r requirements.txt
```
Run the app:
```powershell
streamlit run app.py
```
Open the URL shown in the terminal (usually http://localhost:8501).

## Importing Files
Use the File tab to upload `.txt` or `.md` files. Imported content is appended to the current note.

## Exporting Notes
Use the Download button in the File tab to save the current note as a Markdown file.

## Extending
You can integrate AI-based summarization or formatting by adding new tabs or buttons. The code is structured for easy modification.

## License
MIT (Add a LICENSE file if distributing.)
