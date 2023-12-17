import os
import shutil

# Import customized libraries
from new_subprocess_cmd import subprocess_cmd
from new_progress_bar import progress_bar

import new_utils


def rename(filename):
    newFilename = filename[:filename.rfind(".")] + ".Z"
    os.rename(os.path.join(new_utils.TEMPPath, filename), os.path.join(new_utils.TEMPPath, newFilename))


def copyFileToDatas(year, month, filename):
    try:
        filename = filename.replace("updates.", "").replace(".gz", "")
        file1 = new_utils.DATARoot + "/" + year + month + "/" + filename + ".txt"
        file2 = new_utils.DATARoot + "/" + year + month + "/" + filename + "M.txt"
        DUMP = new_utils.TEMPPath + "/DUMP"
        shutil.copy2(DUMP, new_utils.DATARoot + "/" + year + month + "/" + filename + "M.txt")
        DUMP_out = new_utils.TEMPPath + "/DUMP_out.txt"
        shutil.copy2(DUMP_out, new_utils.DATARoot + "/" + year + month + "/" + filename + ".txt")
        return file1, file2
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def handleFile(year, month, filename):
    rename(filename)
    subprocess_cmd("cd " + new_utils.TEMPPath + "; \
                            chmod +x zebra-script.sh ;\
                            sh ./zebra-script.sh")
    progress_bar(time_sleep=0.02, status_p='Converting')
    subprocess_cmd("cd " + new_utils.TEMPPath + "; \
                            mono ConsoleApplication1.exe >/dev/null ; ")
    return copyFileToDatas(year, month, filename)
