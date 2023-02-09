def conditionals_year(varSheetname_GS,varIndxValueToCompare,rowValues,varRDF_to_write,varRD_to_write,pd):
        varRDF_to_write = '2022'
        if varSheetname_GS == 'DayDoseOfHouse':
            varRI_to_write = rowValues['Radio ISRC'].loc[rowValues.index[0]]
            varRE_to_write = rowValues['Radio/Extended'].loc[rowValues.index[0]]
            if varIndxValueToCompare < 449 and varIndxValueToCompare > 273:
                varRDF_to_write = varRD_to_write + ',2022'
                varRDF_to_write = pd.to_datetime(varRDF_to_write).strftime('%d.%m.%Y')
                varRD_to_write = varRD_to_write + ', 2022'
                return [varRD_to_write,varRDF_to_write,varRI_to_write,varRE_to_write]
            elif varIndxValueToCompare > 1 and varIndxValueToCompare < 273:
                varRDF_to_write = varRD_to_write + ',2021'
                varRDF_to_write = pd.to_datetime(varRDF_to_write).strftime('%d.%m.%Y')
                varRD_to_write = varRD_to_write + ', 2021'
                return [varRD_to_write, varRDF_to_write, varRI_to_write, varRE_to_write]
            elif  varIndxValueToCompare > 449:
                varRDF_to_write = varRD_to_write + ',2023'
                varRDF_to_write = pd.to_datetime(varRDF_to_write).strftime('%d.%m.%Y')
                varRD_to_write = varRD_to_write + ', 2023'
                return [varRD_to_write, varRDF_to_write, varRI_to_write, varRE_to_write]
        elif varSheetname_GS == 'FloatingBlueRecords':
            varRI_to_write = rowValues['ISRC'].loc[rowValues.index[0]]
            varRE_to_write = rowValues['COVER?'].loc[rowValues.index[0]]
            if varIndxValueToCompare > 4 and varIndxValueToCompare < 178:
                varRDF_to_write = varRD_to_write + ',2022'
                varRDF_to_write = pd.to_datetime(varRDF_to_write).strftime('%d.%m.%Y')
                varRD_to_write = varRD_to_write + ', 2022'
                return [varRD_to_write, varRDF_to_write, varRI_to_write, varRE_to_write]
            elif varIndxValueToCompare > 178 :
                varRDF_to_write = varRD_to_write + ',2023'
                varRDF_to_write = pd.to_datetime(varRDF_to_write).strftime('%d.%m.%Y')
                varRD_to_write = varRD_to_write + ', 2023'
                return [varRD_to_write, varRDF_to_write, varRI_to_write, varRE_to_write]
            elif varIndxValueToCompare <4:
                varRDF_to_write = varRD_to_write + ',2021'
                varRDF_to_write = pd.to_datetime(varRDF_to_write).strftime('%d.%m.%Y')
                varRD_to_write = varRD_to_write + ', 2021'
                return [varRD_to_write, varRDF_to_write, varRI_to_write, varRE_to_write]
        elif varSheetname_GS == 'DeepCloudMusic':
            varRI_to_write = rowValues['ISRC'].loc[rowValues.index[0]]
            varRE_to_write = rowValues['COVER?'].loc[rowValues.index[0]]
            if varIndxValueToCompare > 4 and varIndxValueToCompare <14:
                varRDF_to_write = varRD_to_write + ',2022'
                varRDF_to_write = pd.to_datetime(varRDF_to_write).strftime('%d.%m.%Y')
                varRD_to_write = varRD_to_write + ', 2022'
                return [varRD_to_write, varRDF_to_write, varRI_to_write, varRE_to_write]
            elif varIndxValueToCompare < 4:
                varRDF_to_write = varRD_to_write + ',2021'
                varRDF_to_write = pd.to_datetime(varRDF_to_write).strftime('%d.%m.%Y')
                varRD_to_write = varRD_to_write + ', 2021'
                return [varRD_to_write, varRDF_to_write, varRI_to_write, varRE_to_write]
            elif varIndxValueToCompare >14:
                varRDF_to_write = varRD_to_write + ',2023'
                varRDF_to_write = pd.to_datetime(varRDF_to_write).strftime('%d.%m.%Y')
                varRD_to_write = varRD_to_write + ', 2023'
                return [varRD_to_write, varRDF_to_write, varRI_to_write, varRE_to_write]