from Util import commonUtil
def readFromFileToList(fileInput: str) -> list:
    fileInput = commonUtil.getPath(fileInput)
    try:
        f = open(fileInput, "r")
        return list(f.read().splitlines())
    except Exception as e:
        # TODO error catch
        raise (e)

def readFromFileToListWithoutHead(fileInput: str) -> list:
    fileInput = commonUtil.getPath(fileInput)
    try:
        f = open(fileInput, "r")
        return list(f.read().splitlines())[1:]
    except Exception as e:
        # TODO error catch
        raise (e)


def saveListToCSV(fileOutput: str, srcList: list):
    fileOutput = commonUtil.getPath(fileOutput)
    try:
        f = open(fileOutput, "w")
        for idx, item in enumerate(srcList):
            if idx < len(srcList) - 1:
                f.write(str(item) + '\n')
            else:
                f.write(str(item))
        f.close()
    except Exception as e:
        # TODO error catch
        raise (e)


def readFromFileToData(fileInput: str, row='a'):
    fileInput = commonUtil.getPath(fileInput)

    import pandas as pd
    try:
        if row == 'a':
            data = pd.read_csv(fileInput, encoding='utf-8', delimiter=',')  # nrows=1000
        else:
            data = pd.read_csv(fileInput, encoding='utf-8', delimiter=',', nrows=int(row))
        if (len(data) < 1):
            pass
        else:
            return data
    except Exception as e:
        # TODO error catch
        raise (e)


def saveDataToCSV(fileOutput: str, data: dict):
    fileOutput = commonUtil.getPath(fileOutput)
    import pandas as pd
    dataframe = pd.DataFrame(data)
    try:
        dataframe.to_csv(fileOutput, index=False, sep=',')
    except Exception as e:
        # TODO error catch
        raise (e)


def deleteAllFolder(folderName: str):
    import shutil
    import os
    folderName = commonUtil.getPath(folderName)
    del_list = os.listdir(folderName)
    for f in del_list:
        file_path = os.path.join(folderName, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)


def addLabelToCSV(srcFile: str, labelFile: str, row='a'):
    import os

    srcFile = commonUtil.getPath(srcFile)
    labelFile = commonUtil.getPath(labelFile)

    srcData = readFromFileToData(srcFile, row)
    lbData = readFromFileToData(labelFile, row)
    srcData['label'] = lbData['label']
    saveDataToCSV(srcFile, srcData)
    os.remove(labelFile)

def retainTimeColumnsInCSV(srcFile: str, row='a'):
    srcFile = commonUtil.getPath(srcFile)
    srcData = readFromFileToData(srcFile, row)

    cols = srcData.columns[:].tolist()
    cols1 = cols[:2]
    cols2 = cols[-1:]

    srcData.drop(cols1 + cols2, axis=1, inplace=True)
    return srcData

def getTimeLabelColumns(srcFile: str, row='a'):
    srcFile = commonUtil.getPath(srcFile)
    srcData = readFromFileToData(srcFile, row)

    cols = srcData.columns[:].tolist()
    cols1 = cols[:0]
    cols2 = cols[-1:]

    return cols1 + cols2

def addLinesToCSV(fileInput: str, lines:list):
    import csv
    try:
        fileInput = commonUtil.getPath(fileInput)
        out_f = open(fileInput, 'a', newline='')
        writer = csv.writer(out_f)
        writer.writerows(lines)
        out_f.close()
    except Exception as e:
        # TODO error catch
        raise (e)
