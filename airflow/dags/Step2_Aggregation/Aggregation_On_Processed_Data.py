import re
import time

from Util import fileUtil, commonUtil

# write & read
timeFormat = '%Y-%m-%d %H:%M:%S'
appendColumns = ['Minute', 'Hour', 'Day', 'Month', 'Year']

def rwCSV(fileInput: str, fileOutput: str,
          timeIntervalList: list,
          timeFormat=timeFormat, pivot='datetime', appendColumns=appendColumns) -> list:
    if len(timeIntervalList) == 0:
        timeIntervalList = ['1hour']

    raw_name = fileOutput

    path = commonUtil.getPath(fileInput)
    fileOutput = commonUtil.getPath(fileOutput)
    data = fileUtil.readFromFileToData(path)

    data_len = len(data)

    # No order
    allColumns = data.columns.tolist()
    time_col = data[pivot]

    len_timeIntervals_sorted, timeIntervals_sorted = commonUtil.getIntervalList(timeIntervalList)
    selecColumns = []
    for col in allColumns:
        if col != pivot and (re.findall('id', col, flags=re.IGNORECASE) == []):
            selecColumns.append(col)

    vals = commonUtil.d(timeIntervals_sorted)
    for i in range(len_timeIntervals_sorted):
        vals[i] = commonUtil.d(selecColumns, appendColumns)

    # Not recommend to write inline function like this, but in order to get high speed
    def timeAggregate(startHourTimeStamp, startLine, endLine, interval: int):

        localTime = time.localtime(startHourTimeStamp[interval])

        timeSpan = endLine - startLine + 1
        alertLevel = int(timeSpan * 0.75)

        print(f"aggregating")

        # (1)AVERAGE VALUE CAL
        # (2)75 percent is 0, then 0
        for attr in selecColumns:
            # scan from startLine to endLine
            vList = data[attr][startLine:endLine + 1]
            counter = vList.tolist().count(0)

            if counter < alertLevel:
                value = sum(vList / timeSpan)
                vals[interval][attr].append(value)
            else:
                vals[interval][attr].append(0)

        # HARDCODE
        # TODO Currently no need to modify, not sure in the future version
        vals[interval]['Minute'].append(localTime.tm_min)
        vals[interval]['Hour'].append(localTime.tm_hour)
        vals[interval]['Day'].append(localTime.tm_mday)
        vals[interval]['Month'].append(localTime.tm_mon)
        vals[interval]['Year'].append(localTime.tm_year)

    startLine = [0 for i in range(len_timeIntervals_sorted)]
    lastStartLine = [0 for i in range(len_timeIntervals_sorted)]
    lastEndLine = [0 for i in range(len_timeIntervals_sorted)]

    data_raw_time = time_col[0]
    lastHourTimeStamp = [time.mktime(time.strptime(data_raw_time, timeFormat)) for i in range(len_timeIntervals_sorted)]
    currentHour = 0
    for lineIdx in range(data_len):

        data_raw_time = time_col[lineIdx]
        currentHour = time.mktime(time.strptime(data_raw_time, timeFormat))

        # Layer combination
        # Start a new time set
        for idx, timeInterval in enumerate(timeIntervals_sorted):
            if currentHour - lastHourTimeStamp[idx] >= timeInterval * 60:
                startLine[idx] = lineIdx
                lastEndLine[idx] = lineIdx - 1
                timeAggregate(lastHourTimeStamp, lastStartLine[idx], lastEndLine[idx], idx)
                lastHourTimeStamp[idx] = currentHour

            lastStartLine[idx] = startLine[idx]

    timeAggregate(lastHourTimeStamp, lastStartLine[idx], data_len - 1, idx)

    files = []
    for idx, timeInterval in enumerate(timeIntervals_sorted):
        fileUtil.saveDataToCSV(fileOutput + f"_{timeInterval}.csv", vals[idx])

        files.append(raw_name + f"_{timeInterval}.csv")

    return files
