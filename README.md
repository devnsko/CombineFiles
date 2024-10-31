# CombineFiles Script

This Python script combines the contents of specified file types from a directory into a single output file, allowing for the exclusion of specific files, directories, and `.gitignore` entries.

## Features

- Combines text content from files in a directory and outputs to a single file.
- Allows file and directory exclusion based on custom lists or `.gitignore`.
- Customizable file extensions, output file name, and other options.
- Supports Windows, Linux, and macOS.

## Requirements

- **Python 3.6+**
- **Libraries**: `pathspec` (install with `pip install pathspec`)

## Setup

### 1. Clone the Repository and Install Dependencies

```bash
git clone https://github.com/yourusername/CombineFiles.git
cd CombineFiles
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Create an Easy-to-Use Command

For quick access to the script from any location, you can set up a shortcut.

#### Windows

1. Create a `comf.bat` file in the root directory with the following contents:

   ```bat
   @echo off
   call C:\Path\To\CombineFiles\.venv\Scripts\activate  # Update this path
   python C:\Path\To\CombineFiles\main.py %*  # Update this path
   deactivate
   ```

2. Add the directory containing `comf.bat` to your system PATH:
   - Go to **Control Panel** > **System and Security** > **System** > **Advanced system settings** > **Environment Variables**.
   - Under **System variables**, find the **Path** variable, and add the path to the directory containing `comf.bat`.

You can now use the script from any directory with the command:
```bash
comf [options]
```

#### Linux / macOS

1. Create a shortcut script `comf` in `/usr/local/bin` or another directory in your PATH:

   ```bash
   #!/bin/bash
   source /path/to/CombineFiles/.venv/bin/activate  # Update this path
   python /path/to/CombineFiles/main.py "$@"  # Update this path
   deactivate
   ```

2. Make the script executable and ensure it’s in your PATH:

   ```bash
   chmod +x /usr/local/bin/comf
   ```

You can now use the command in the terminal:
```bash
comf [options]
```

## Usage

The script has various options for customizing how files are combined.

```bash
comf [directory] [-e extensions] [-x exclude-files] [-X exclude-dirs] [-g] [-o output]
```

### Arguments

- `directory` - Directory to scan (defaults to current directory).
- `-e, --extensions` - List of file extensions to include (e.g., `.txt .py`).
- `-x, --exclude-files` - List of file names to exclude.
- `-X, --exclude-dirs` - List of directories to exclude.
- `-g, --gitignore` - Exclude files listed in `.gitignore`.
- `-o, --output` - Name of the output file.

### Examples

Combine all `.txt` and `.md` files in `src/` directory, excluding files in `.gitignore`:

```bash
comf src -e .txt .md -g
```

Specify an output file name and exclude specific files:

```bash
comf -o combined_output.txt -x README.md LICENSE
```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
