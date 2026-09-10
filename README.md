# File Organizer

A little automation script that sorts a messy folder (mine was Downloads,
obviously) into subfolders by file type. Started this because I was tired of
manually dragging files into folders every couple weeks, and it turned into
a decent excuse to actually use `watchdog` for something.

Runs either as a one-off (`sort`) or as a background watcher that sorts new
files the moment they show up (`watch`).

## What it does

- Sorts files into folders like `Images/`, `Documents/`, `Code/`, etc. based
  on extension
- Rules live in `config.yaml` — easy to edit, doesn't require touching code
  to add a new extension or category
- `--dry-run` shows you exactly what it would do before it touches anything
  (I built this after almost dropping a bunch of files into the wrong place
  the first time I ran it)
- Won't overwrite files — if `Documents/notes.txt` already exists, the new
  one becomes `notes (1).txt` instead of clobbering it
- Ignores its own log file and OS junk files like `.DS_Store`
- `watch` mode keeps running and sorts files as soon as they land in the
  folder, using `watchdog` under the hood

## Setup

```bash
git clone <your-repo-url>
cd file-organizer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

See what would happen first (always do this before pointing it at a real
folder):

```bash
python main.py sort ~/Downloads --dry-run -v
```

Then actually sort it:

```bash
python main.py sort ~/Downloads
```

Or leave it running in the background and let it sort things as they
download:

```bash
python main.py watch ~/Downloads
```

Using a custom rule set instead of the default `config.yaml`:

```bash
python main.py sort ~/Downloads --config my-rules.yaml
```

## Customizing the rules

`config.yaml` maps folder names to a list of extensions:

```yaml
categories:
  Images:
    - jpg
    - png
  Documents:
    - pdf
    - docx

fallback_folder: Other
```

Anything with an extension that's not listed anywhere goes into
`fallback_folder`.

## Tests

```bash
pytest tests/ -v
```

Tests run against real temp folders (`tmp_path`), no mocking the filesystem,
since the whole point of this thing is what it does to real files.

## Known limitations

- Only sorts the top level of a folder, doesn't recurse into subfolders
  (on purpose — I didn't want it reorganizing folders I'd already sorted
  by hand)
- `watch` mode has a 1-second delay before sorting a new file, to avoid
  grabbing something mid-download. Works fine for normal file sizes but a
  huge file that's still transferring could still get grabbed too early.
- No undo command yet — if you want to reverse a run, the log tells you
  exactly what moved where, just no automated "put it back" button.

## License

MIT
