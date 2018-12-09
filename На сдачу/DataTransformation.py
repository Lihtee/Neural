import csv
import pandas as pd

baseDir = 'D:/Users/Дрей/Desktop/Neural/Neural-master'
baseSetName = 'Data.xls'
resSetName = 'DataTestV5.xlsx'
factorSetName = 'FactorsV5.xlsx'

baseSet = '{0}/{1}'.format(baseDir, baseSetName)
resSet = '{0}/{1}'.format(baseDir, resSetName)
factorSet = '{0}/{1}'.format(baseDir, factorSetName)

grid = pd.read_excel(baseSet)
resSetWriter = pd.ExcelWriter(resSet)
factorsWriter = pd.ExcelWriter(factorSet)

colToFactorise = ['N', 'WW', 'W1', 'W2', 'Cl', 'Nh', 'H', 'Cm', 'Ch', 'E', 'DD', 'sss']

#Drop too empty columns.
for colName in grid:
    col = grid[colName]
    if (col.isna().sum() / col.size > 0.2 or col.isnull().sum() / col.size > 0.2):
        if (colName in colToFactorise):
            colToFactorise.remove(colName)
        grid.drop(columns=colName, inplace=True)

#Remove rows with empty cells.
grid = grid.dropna()

#Narrowing output.
y1 = grid['WW']
replace =  {'нет осадков':['нет осадков'], 'ливень': ['ливень', 'ливнев','ливни'], 'дождь':['дожд'], 'снег':['снег','снежн','град'], 'метель':['метел'], 'морось':['морос'], 'туман':['туман'], 'облака':['облак', 'облач'], 'гроза':['гроз']}
newY1 = []
for v in y1:
     f = False
     for r in replace:
         for rr in replace[r]:
             if (v.lower().find(rr) >= 0):
                newY1.append(r)
                f = True
                break
         if (f):
             break
     if (not f):
        newY1.append('нет осадков')
grid.drop(columns='WW', inplace = True)
grid.insert(column = 'WW', value = newY1, loc = 0)

for colName in colToFactorise:
    col = grid[colName]
    labels, uniques = pd.factorize(col)
    grid.drop(columns=colName, inplace=True)
    grid.insert(column=colName, value=labels, loc=0)
    codes = {'code': range(0, uniques.size), 'labels': uniques}
    codesGrid = pd.DataFrame(codes)
    codesGrid.to_excel(factorsWriter, colName)

#Split datetime into 4 columns
dtCol = pd.to_datetime(grid['Местное время в Перми'])
grid.drop(columns='Местное время в Перми', inplace = True)
grid.insert(column = 'year', value = dtCol.dt.year, loc = 0)
grid.insert(column = 'month', value = dtCol.dt.month, loc = 0)
grid.insert(column = 'day', value = dtCol.dt.day, loc = 0)
grid.insert(column = 'hour', value = dtCol.dt.hour, loc = 0)

#Move desirable cols to the end.
colT = grid.pop('WW')
grid['WW'] = colT;

grid.to_excel(resSetWriter, 'ResSet', index = False)
resSetWriter.save()
factorsWriter.save()