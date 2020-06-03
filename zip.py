# Copyright (c) 2019 Gurjit Singh

# This source code is licensed under the MIT license that can be found in
# the accompanying LICENSE file or at https://opensource.org/licenses/MIT.


import sys
import os
import pathlib
import subprocess
import argparse


def parseArgs():
    def dirPath(pth):
        pthObj = pathlib.Path(pth)
        if pthObj.is_dir():
            return pthObj
        else:
            raise argparse.ArgumentTypeError("Invalid Directory path")

    parser = argparse.ArgumentParser(
        description="Compress all child \
                                     directories in specified folder."
    )
    parser.add_argument("dir", metavar="DirPath", help="Directory path", type=dirPath)
    parser.add_argument(
        "-s", "--split", action="store_true", help="Split output in multiple files"
    )
    parser.add_argument(
        "-a", "--abs", action="store_true", help="Use absolute 7z.exe path"
    )
    pargs = parser.parse_args()

    return pargs


def main(pargs):

    dirpath = pargs.dir.resolve()

    dirlist = [x for x in dirpath.iterdir() if x.is_dir()]

    if not dirlist:
        print("Nothing to do.")
        sys.exit()

    for folder in dirlist:
        totalSize = 0
        for childpath, _, childfiles in os.walk(folder):
            for file in childfiles:
                totalSize += os.stat(os.path.join(childpath, file)).st_size
        filestr = str(folder)
        cmd = ["7z.exe", "a", f"{ filestr }.zip", filestr]
        if totalSize > 314572800 and pargs.split:
            cmd.append("-v300m")
        if pargs.abs:
            cmd[0] = r"C:\Program Files\7-Zip\7z.exe"

        print("--------------------------------------------")
        print(cmd)
        print(f"{ totalSize } bytes")
        print("--------------------------------------------")
        subprocess.run(cmd)
        input("\nPress Enter to continue...")


main(parseArgs())
