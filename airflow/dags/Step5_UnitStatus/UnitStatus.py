import csv
import os
import random
import time

from Util import commonUtil, fileUtil

# This file does not have id column
# heads: 'Date','Attr', '0', '1', ... , '23'
APPENDIX = ['Minute', 'Hour', 'Day', 'Month', 'Year']
timeFormat = '%M-%H-%d-%m-%Y'


def rwCSV(filesAggregated, fileOutput, UserInputColumns: list, APPENDIX, timeFormat, timeIntervalList: list):
    len_timeIntervals_sorted, timeIntervals_sorted = commonUtil.getIntervalList(timeIntervalList)
    for fidx, f in enumerate(filesAggregated):
        func(f, fileOutput, UserInputColumns, APPENDIX, timeFormat, timeIntervals_sorted[fidx])


def func(fileinput, fileOutput, UserInputColumns: list, APPENDIX, timeFormat, timeInterval):
    createNewCSV(fileOutput, timeInterval)
    data = fileUtil.readFromFileToData(fileInput=fileinput)
    processCSV(data, fileOutput, UserInputColumns, APPENDIX, timeFormat, timeInterval)


def createNewCSV(fileOutput, timeInterval: int):
    heads = []
    heads.append('Date')
    heads.append('Attr')

    counter = int(24 * 60 / timeInterval)
    # Minute style
    if timeInterval < 60:
        for i in range(counter):
            tmpM = (i * timeInterval) % 60
            tmpH = (i * timeInterval) / 60
            if tmpM == 0:
                heads.append(f"{int(tmpH)}:00")
            else:
                heads.append(f"{int(tmpH)}:{tmpM}")
    # Hour style
    else:
        for i in range(counter):
            heads.append(f"{i}:00")

    heads.append('label')
    vals = commonUtil.d(heads)

    #tmpName = raw_name.split(os.sep)[1]
    fileUtil.saveDataToCSV(fileOutput, vals)


def processCSV(data, fileOutput, UserInputColumns, APPENDIX, timeFormat, timeInterval: int):
    startMinute, startHour, startDay, startMonth, startYear = combineAppendixItem(data, APPENDIX, rowIndex=0)

    tString = f'{startDay}-{startMonth}-{startYear}'
    startTimeStamp = time.mktime(time.strptime(tString, '%d-%m-%Y'))

    prevStartRow = 0

    slots = int(24 * 60 / timeInterval)
    dataPlots = [False for i in range(slots)]

    curTimeStamp = startTimeStamp

    #tmpName = raw_name.split(os.sep)[1]
    location = commonUtil.getPath(fileOutput)

    out_f = open(location, 'a', newline='')
    writer = csv.writer(out_f)
    for idx in range(len(data)):
        curMinute, curHour, curDay, curMonth, curYear = combineAppendixItem(data, APPENDIX, rowIndex=idx)
        curTime = f'{curMinute}-{curHour}-{curDay}-{curMonth}-{curYear}'

        curTimeStamp = time.mktime(time.strptime(curTime, timeFormat))

        if curTimeStamp - startTimeStamp < 86400:
            dataPlots[int((curHour * 60 + curMinute) / timeInterval)] = True

        else:
            startTimeStamp = curTimeStamp
            writeToDigestCSV(data, UserInputColumns, APPENDIX, prevStartRow, dataPlots, writer, timeInterval)

            dataPlots = [False for i in range(slots)]
            dataPlots[int((curHour * 60 + curMinute) / timeInterval)] = True
            prevStartRow = idx

    writeToDigestCSV(data, UserInputColumns, APPENDIX, prevStartRow, dataPlots, writer, timeInterval)
    out_f.close()


def writeToDigestCSV(data, UserInputColumns, APPENDIX, prevStartRow, dataPlots, writer, timeInterval: int):
    # Data and Attr
    additionColumns = 2

    slots = int(24 * 60 / timeInterval)

    tmp = []
    for attr in sorted(UserInputColumns):
        # Date
        preMinute, preHour, preDay, preMonth, preYear = combineAppendixItem(data=data,
                                                                            APPENDIX=APPENDIX,
                                                                            rowIndex=prevStartRow)
        preTime_beautify = ' ' + f'{preYear}-{preMonth}-{preDay}'
        tmpRes = [preTime_beautify]
        # Attr
        tmpRes.append(attr)

        counter = prevStartRow
        tmpRes.extend([0 for i in range(slots)])

        for flagIndex in range(slots):
            if dataPlots[flagIndex]:
                tmpRes[flagIndex + additionColumns] = data[attr][counter]
                counter += 1

        tmp.append(tmpRes)
    writer.writerows(tmp)


def combineAppendixItem(data, APPENDIX, rowIndex=0):
    curMinute = data[APPENDIX[0]][rowIndex]
    curHour = data[APPENDIX[1]][rowIndex]
    curDay = data[APPENDIX[2]][rowIndex]
    curMonth = data[APPENDIX[3]][rowIndex]
    curYear = data[APPENDIX[4]][rowIndex]

    return curMinute, curHour, curDay, curMonth, curYear