import os
import argparse
import pathspec

# Function to load ignore patterns from .gitignore
def load_gitignore_patterns(gitignore_path):
    if os.path.isfile(gitignore_path):
        with open(gitignore_path, 'r') as gitignore_file:
            patterns = gitignore_file.read().splitlines()
        return pathspec.PathSpec.from_lines('gitwildmatch', patterns)
    return None

# Function to combine files into one txt file
def combine_files(directory, extensions, exclude_files=None, exclude_dirs=None, gitignore=None, output_file=None):
    # Set default values if not provided
    exclude_files = exclude_files or []
    exclude_dirs = exclude_dirs or []

    # Load .gitignore patterns if provided
    gitignore_spec = load_gitignore_patterns(gitignore) if gitignore else None

    # Determine the output file path
    if output_file is None:
        output_file = os.path.join(directory, 'combined.txt')
    else:
        output_file = os.path.join(directory, output_file)

    # Exclude output file
    exclude_files.append(os.path.basename(output_file))

    # Start file processing
    files_combined = 0
    files_skipped = 0

    print(f"Starting to combine files from `{directory}` into `{output_file}`.")
    print(f"Including extensions: {extensions}")
    if exclude_files:
        print(f"Excluding files: {exclude_files}")
    if exclude_dirs:
        print(f"Excluding directories: {exclude_dirs}")
    if gitignore_spec:
        print("Using patterns from `.gitignore`")

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(directory):
            # Skip directories matched by .gitignore or explicitly excluded
            dirs[:] = [d for d in dirs if os.path.join(root, d) not in exclude_dirs and
                       (not gitignore_spec or not gitignore_spec.match_file(os.path.join(root, d)))]

            for filename in files:
                filepath = os.path.join(root, filename)

                # Skip files matched by .gitignore, excluded files, or without matching extensions
                if filename in exclude_files or \
                   (gitignore_spec and gitignore_spec.match_file(filepath)) or \
                   not any(filename.endswith(ext) for ext in extensions):
                    files_skipped += 1
                    print(f"Skipping: {filepath}")
                    continue

                # Process the file
                print(f"Combining: {filepath}")
                files_combined += 1
                relative_path = os.path.relpath(filepath, directory)

                with open(filepath, 'r', encoding='utf-8') as infile:
                    # Write the relative path to the file as a title
                    outfile.write(f"{relative_path}:\n")
                    # Write the contents of the file
                    content = infile.read()
                    outfile.write(content)
                    # Add double line breaks to separate files
                    outfile.write('\n\n')

    print(f"\nCombined files successfully written to `{os.path.abspath(output_file)}`")
    print(f"Total files combined: {files_combined}")
    print(f"Total files skipped: {files_skipped}")

# Basic code for working with command-line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Combine file contents from a directory into a single file.")
    parser.add_argument('directory', nargs='?', default='.', help='The directory to scan. Defaults to the current directory.')
    parser.add_argument('-e', '--extensions', nargs='+', default=['.txt', '.py', '.java', '.js', '.md'], help='List of file extensions to include. Defaults to .txt, .py, .java, .js, and .md')
    parser.add_argument('-x', '--exclude-files', nargs='*', default=[], help='List of file names to exclude from combining.')
    parser.add_argument('-X', '--exclude-dirs', nargs='*', default=[], help='List of directory names to exclude from scanning.')
    parser.add_argument('-g', '--gitignore', action='store_true', help='Exclude files and directories listed in the .gitignore file.')
    parser.add_argument('-o', '--output', default=None, help='The name of the output file. Defaults to combined.txt in the scanned directory.')

    args = parser.parse_args()

    # Convert excluded directories to absolute paths
    exclude_dirs = [os.path.abspath(os.path.join(args.directory, d)) for d in args.exclude_dirs]

    # Determine the current directory for scanning
    scan_directory = os.path.abspath(args.directory)

    # Determine .gitignore path if requested
    gitignore_path = os.path.join(scan_directory, '.gitignore') if args.gitignore else None

    # Run the function with arguments
    combine_files(scan_directory, args.extensions, args.exclude_files, exclude_dirs, gitignore_path, args.output)
