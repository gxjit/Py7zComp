# Copyright (c) 2020 Gurjit Singh

# This source code is licensed under the MIT license that can be found in
# the accompanying LICENSE file or at https://opensource.org/licenses/MIT.


import argparse
import math
import pathlib
import subprocess
import sys
import os


def parseArgs():
    def dirPath(pth):
        pthObj = pathlib.Path(pth)
        if pthObj.is_dir():
            return pthObj
        else:
            raise argparse.ArgumentTypeError("Invalid Directory path")

    parser = argparse.ArgumentParser(
        description="Compress all child directories in specified folder using 7z."
    )
    parser.add_argument(
        "-d", "--dir", required=True, help="Directory path", type=dirPath
    )
    parser.add_argument(
        "-s",
        "--split",
        nargs="?",
        default=None,
        const=300,
        type=int,
        help="Maximum split size in MB, default is 300 MB",
    )
    parser.add_argument(
        "-a",
        "--abs",
        action="store_true",
        help=r"Use absolute 7z.exe path C:\Program Files\7-Zip\7z.exe",
    )
    pargs = parser.parse_args()

    return pargs


getCmd = lambda dirPath, abs: [
    "7z.exe" if not abs else r"C:\Program Files\7-Zip\7z.exe",
    "a",
    f"{str(dirPath)}.zip",
    str(dirPath),
]

getDirList = lambda dirPath: [x for x in dirPath.iterdir() if x.is_dir()]

bytesToMB = lambda bytes: math.ceil(bytes / float(1 << 20))


def getSize(totalSize, maxSplit):
    fSize = 0
    for i in range(2, 35):
        splitSize = math.ceil(totalSize / i)
        if totalSize <= splitSize:
            continue
        if splitSize <= maxSplit:
            fSize = splitSize
            return i, splitSize
    if fSize == 0:
        return 1, totalSize


def getDirSize(dirPath):
    totalSize = 0
    for childpath, _, childfiles in os.walk(dirPath):
        for file in childfiles:
            totalSize += os.stat(os.path.join(childpath, file)).st_size
    return totalSize


def main(pargs):

    dirPath = pargs.dir.resolve()

    dirList = getDirList(dirPath)

    if not dirList:
        print("Nothing to do.")
        sys.exit()

    splitAboveMB = 50

    for folder in dirList:
        totalSize = bytesToMB(getDirSize(folder))

        cmd = getCmd(folder, pargs.abs)

        if pargs.split and totalSize > splitAboveMB:
            splitSize = getSize(totalSize, pargs.split)[1]
            cmd.append(f"-v{splitSize}m")

        print("\n--------------------------------------")
        print("\n", cmd)
        print(f"\nTotal size of source files { (totalSize) } MB")
        if pargs.split and totalSize > splitAboveMB:
            print(f"\nSplit size: {splitSize} MB")
        print("\n---------------------------------------\n")
        subprocess.run(cmd)
        input("\nPress Enter to continue...")


main(parseArgs())