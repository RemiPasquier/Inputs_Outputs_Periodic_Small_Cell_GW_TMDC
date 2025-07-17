import os

# Define which filenames or extensions to keep
KEEP_FILES = {"GW.inp", "cp2k.out","bandstructure_SCF_and_G0W0","bandstructure_SCF_and_G0W0_plus_SOC"}

def is_deepest_leaf_dir(path):
    """Return True if a directory has no subdirectories."""
    return all(
        not os.path.isdir(os.path.join(path, entry))
        for entry in os.listdir(path)
    )

def clean_directory(path):
    """Delete unwanted files from a directory, keeping specified ones."""
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isfile(full_path):
            # Keep if filename is in the keep list or extension matches
            if entry not in KEEP_FILES:
                os.remove(full_path)
                print(f"Deleted: {full_path}")

def find_and_clean_deepest_leaves(root_path):
    """Walk directory tree and clean only deepest folders, skipping .git folders."""
    for dirpath, dirnames, filenames in os.walk(root_path, topdown=False):
        # Skip any .git folder and don't even descend into it
        if '.git' in dirpath.split(os.sep):
            continue

        # Also remove .git from child directory list to prevent walk
        dirnames[:] = [d for d in dirnames if d != '.git']

        # Clean only if it's a leaf (no subdirectories)
        if not dirnames:
            clean_directory(dirpath)

def preview_leaf_directory(path):
    """Print contents of the leaf directory."""
    print(f"\n📁 Leaf Directory: {path}")
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isfile(full_path):
            print(f"  - {entry}")


# Replace this with your actual root folder
root_directory = os.getcwd()
find_and_clean_deepest_leaves(root_directory)
