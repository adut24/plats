import os
import shutil

def move_images_to_subdirs(directory: str):
    # Ensure the directory exists
    if not os.path.isdir(directory):
        print(f"Directory '{directory}' does not exist.")
        return

    # Loop through files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # Skip if not a file
        if not os.path.isfile(file_path):
            continue

        # Extract filename without extension
        name, _ = os.path.splitext(filename)

        # Target subdirectory path
        subdir_path = os.path.join(directory, name)
        os.makedirs(subdir_path, exist_ok=True)

        # Destination file path (always plat.jpg)
        dest_file_path = os.path.join(subdir_path, "plat.jpg")

        # Move + rename
        shutil.move(file_path, dest_file_path)
        print(f"Moved '{filename}' -> '{dest_file_path}'")

if __name__ == "__main__":
    images_dir = "."  # change to your folder
    move_images_to_subdirs(images_dir)
