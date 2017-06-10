from subprocess import call
from os import listdir
import random

def main ():
    print("Starting randomizer script")
    dirlist = listdir()
    dirlist.remove("randomizer.py");
    bob = [" ", "(", ")", "[", "]", "{", "}", "'", "&"]
    total = 0
    renamed = 0
    failed = 0
    for j in dirlist:
        try:
            filelist = listdir(j)
            for c in bob:
                j = j.replace(c, "\\" + c)
            for l in range(len(filelist)):
                for c in bob:
                    filelist[l] = filelist[l].replace(c, "\\" + c)
            indexlist = [i for i in range(len(filelist))]
            random.shuffle(indexlist)
            for f,i in zip(filelist, range(len(filelist))):
                name = f;
                while (name[0] >= "0" and name[0] <= "9"):
                    name = name[1:]
                if (name[0] == "-"):
                    name = name[1:]
                script = ("mv " + j + "/" + f + " " + j + "/%02d-" + name) % indexlist[i]
                if (call(script, shell=True) == 0):
                    renamed += 1
                else:
                    failed += 1
            total += len(filelist)
        except NotADirectoryError:
            continue
    print("Tried to rename " + str(total) + " files")
    print("Successfully renamed " + str(renamed) + " files")
    print("Failed to rename " + str(failed) + " files")

if __name__ == '__main__':
    main()
