def getDiffSet(A, B) -> list:
    return list(set(list(A)).difference(set(list(B))))


def d(*args):
    res = {}
    for lst in args:
        if isinstance(lst, list):
            for item in lst:
                res[item] = []
    return res


def createPNGTags(inputCSVFile: str, outputPNGTagsFolderPrefix='data_temperature'):
    import os
    import matplotlib.pyplot as plt
    from Util import fileUtil

    data = fileUtil.readFromFileToData(inputCSVFile)
    outputPNGTagsFolderPrefix = getPath(outputPNGTagsFolderPrefix)
    os.makedirs(outputPNGTagsFolderPrefix, exist_ok=True)

    cols = data.columns.tolist()
    data = data[cols[2:-1]][:]

    Axis = [i for i in range(24)]
    plt.margins(0, 0)
    plt.gcf().set_size_inches(100 / 100, 100 / 100)
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    plt.axis('off')
    for index in range(len(data)):
        print(f"Tag {index} processed")
        place = os.path.join(outputPNGTagsFolderPrefix, f'{index}.png')
        plt.plot(Axis, data.iloc[index][:], linewidth=1)
        plt.savefig(place, dpi=200)
        plt.clf()

def createPNGTags_1(inputCSVFile: str,OUTPUT_FOLDER_TAG = 'data_temperature'):
    import os
    import matplotlib.pyplot as plt
    from Util import fileUtil
    OUTPUT_FOLDER = 'data_temperature'
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    data = fileUtil.readFromFileToData(inputCSVFile)

    cols = data.columns.tolist()
    data = data[cols[2:-1]][:]

    Axis = [i for i in range(48)]
    plt.margins(0, 0)
    plt.gcf().set_size_inches(100 / 100, 100 / 100)
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    plt.axis('off')
    for index in range(len(data)):
        print(f"Tag {index} processed")
        place = os.path.join(OUTPUT_FOLDER, f'{index}.png')
        plt.plot(Axis, data.iloc[index][:], linewidth=1)
        plt.savefig(place, dpi=200)
        plt.clf()


def getPath(curPath: str):
    import os
    rootPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(rootPath, curPath)


def getIntervalList(timeIntervalList: list):
    import operator
    # Not recommend to write inline function like this, but in order to get high speed
    # Currently, can only process the time interval by 'minute', 'hour'
    def picker():
        picker = []
        for timeInterval in timeIntervalList:
            if operator.contains(timeInterval, 'min'):
                picker.append(int(timeInterval[:timeInterval.rfind('m')]))
            if operator.contains(timeInterval, 'hour'):
                picker.append(int(timeInterval[:timeInterval.rfind('h')]) * 60)
        return picker

    # from small to big
    timeIntervals_sorted = sorted(picker())
    len_timeIntervals_sorted = len(timeIntervals_sorted)
    return len_timeIntervals_sorted, timeIntervals_sorted

def getSelectedColumns(UserInputSettingFile:str,HeadFile:str,NAME:str):
    import re
    from Util import LoadYAML,fileUtil

    userInput = LoadYAML.rSelectColumns(UserInputSettingFile)
    intervals = userInput['INTERVAL']
    commons = userInput['COMMON']
    queries:list = userInput['DEVICE']
    devices=""
    for queryIdx, queryItem in enumerate(queries):
        if queryItem.__contains__(NAME.lower()):
            devices = queryItem
            break

    src = fileUtil.readFromFileToList(HeadFile)
    res = set()

    if isinstance(intervals,list) and isinstance(commons,list) and isinstance(devices,str):
        for item in commons:
            for s in src:
                if item != '' and item != 'none' and re.findall(item, s, re.IGNORECASE) != []:
                    res.add(s)

        pattern = re.compile(devices)
        for s in src:
            if (re.search(pattern, s) != None):
                res.add(s)

        return intervals, list(res)
    else:
        raise("UserInput is wrong!")
