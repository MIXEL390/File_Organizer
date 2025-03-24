import os
import shutil
import sys

File_categories = {
    "Images": [".jpg", ".jpeg", ".png", ".bmp", ".svg", ".tiff"],
    "Video": [".mov", ".mp4", ".gif", ".avi", ".flv", ".wmv", ".mkv"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".rtf", ".xlsx", ".xls", ".ppt", ".pptx", ".odt", ".txt", ".rtf"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code files": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".php", ".json"],
    "Design files": [".psd", ".ai", ".indd", ".blend", ".vsd", ".mpp", ".max", ".fbx", ".prproj", ".stl", ".glx", ".obj"],
    "Executables": [".exe", ".msi", ".deb", ".dmg", ".cmd"]
}

def file_organizer(directory): ##directory check
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return
    ## Get all files in the directory
    files = [ 
        file for file in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, file)) and file != os.path.basename(__file__)
    ]

    if not files:
        print("No files to organize")
        return False

    for file_name in files: ##Organize
        file_path = os.path.join(directory, file_name)
        file_extension = os.path.splitext(file_name)[1].lower()

       ## For categories not from the list
        category = "Other"
        for cats_, exts_ in File_categories.items():
            if file_extension in exts_:
                category = cats_
                break

        ##create category
        category_dir = os.path.join(directory, category)
        os.makedirs(category_dir, exist_ok=True)

        try:
            destination = os.path.join(category_dir, file_name)
            if not os.path.exists(destination):
                shutil.move(file_path, destination)
                print(f"Moved '{file_name}' to '{category}/'")
            else:
                print(f"File '{file_name}' already exists in '{category}'")
        except Exception as e:
            print(f"Error moving '{file_name}': {str(e)}")
    return True

def main():
    print("Write the directory path to organize (or 'exit' to exit the program )\n\n" )

    while True:
        path = input("Path is: ").strip()
        
        if path.lower() == 'exit':
            print("Thank you for using")
            break
            
        if not path:
            path = os.getcwd()
        
        if not os.path.exists(path):
            print(f"\nError: Directory '{path}' doesn't exist!")
            print("Try again or use 'exit'\n")
            continue

        if not os.path.isdir(path):
            print(f"\nError: '{path}' Is not the directory")
            continue
            
        print(f"\nOrganizing in: {path}")
        success = file_organizer(path)
        
        if success:
            print("\nOrganization complete!")
        else:
            print("\nOrganization is impossible to be done!")
        
        choice = input("\nDo you want to organize another? (y/n): ").lower()
        if choice != 'y':
            print("Good bye")
            break


if __name__ == '__main__':
    main()
