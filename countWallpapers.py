import os

folders = ['clear', 'cloud', 'fog', 'rain']

def main():
    current = os.getcwd()
    relative = "Wallpapers"
    path = os.path.join(current, relative)

    dirs = os.listdir(path)

    for dir in dirs:
        if os.path.isdir(os.path.join(path, dir)):
            print()
            print(dir.upper())
            for folder in folders:
                f = os.path.join(os.path.join(path, dir), folder)
                print("{}\t".format(os.path.join(os.path.join(relative, dir), folder)))
                files = os.listdir(f)
                count = 0
                for file in files:
                    count += 1 if "jp" in file.split(".")[-1] else 0
                print("\t\t{} files".format(count))
        


if __name__ == "__main__":
    main()
