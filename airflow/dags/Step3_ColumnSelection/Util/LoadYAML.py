import re
import os
import yaml

from Util import commonUtil

yaml.warnings({'YAMLLoadWarning': False})

commonQuerySetting = os.path.join('Setting','Queries.yml')
selectColumnsSetting = os.path.join('Setting','UserInputRules.yml')


def loadYAML(fileInput: str) -> dict:
    yamlPath = commonUtil.getPath(fileInput)
    try:
        f = open(yamlPath, 'r', encoding='utf-8')
        cfg = f.read()
        # convert to dict
        d = yaml.safe_load(cfg)
        return d
    except Exception as e:
        raise(e)


def rDatabaseSetting(databaseSetting):
    d = loadYAML(databaseSetting)

    items = list(d.keys())
    host = d[items[0]]
    port = d[items[1]]
    user = d[items[2]]
    password = str(d[items[3]])
    database = d[items[4]]
    tablenames = d[items[5]]
    return [host, port, user, password, database, tablenames]


def rCommonQueries(Query='SHOWALLDATABASES', parameters=[]):
    d = loadYAML(commonQuerySetting)

    res = str(d[Query])
    parlist = re.findall('([A-Z]+)', res)

    if (not parameters) or (not parlist) or (type(parameters).__name__ != 'list') or (len(parameters) != len(parlist)):
        # TODO set a reasonable return value
        pass
    else:
        for idx, parameter in enumerate(parameters):
            res = res.replace(parlist[idx], parameter)
    return res


def rSelectColumns(selectColumnsSetting):
    d = loadYAML(selectColumnsSetting)
    return d
