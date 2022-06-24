"""
A library of python functions for extracting the Andra metadata, data and images
"""

def excell2csv(filelocs):
    """
    function to go through the directories of calcimetry spread
    :param filelocs: location of the files/directories
    :return:
    """
    directories = []
    for name in os.listdir(filelocs):
        if os.path.isdir(filelocs + name):
            directories.append(filelocs + name)

    excell_files = []
    for directory in directories:
        for fname in os.listdir(directory):
            if os.path.isfile(f'{directory}/{fname}'):
                # different file names of course
                if 'Calcimétrie' in fname and 'Zone.Identifier' not in fname:
                    excell_files.append(f'{directory}/{fname}')
                elif 'CALCIMETRIE' in fname and 'Zone.Identifier' not in fname:
                    excell_files.append(f'{directory}/{fname}')
                elif 'Calcimètre' in fname and 'Zone.Identifier' not in fname:
                    excell_files.append(f'{directory}/{fname}')
                elif 'Calci' in fname and 'Zone.Identifier' not in fname:
                    excell_files.append(f'{directory}/{fname}')
                elif 'calcimétrie' in fname and 'Zone.Identifier' not in fname:
                    excell_files.append(f'{directory}/{fname}')

    dfcolms = []
    for file in excell_files:
        df = pd.read_excel(file)
        sf = df.iloc[:, 0]
        if 'Cote' in list(sf):
            dfcolms.append(len(df.columns))

            if len(df.columns) < 5:
                print(file)
                break

            if len(df.columns) > 7:
                for i in range(7, len(df.columns)):
                    colname = f'Unnamed: {i}'
                    df = df.drop([colname], axis=1)

            dfe = df.dropna().copy()
            dfe.columns = ['Cote', 'à 1 minute', 'à 4 minutes', 'à 19 minutes', '% CaCO3', '% Dolomie', '% insolubles']

        if 'Cote toit' in list(sf):
            dfcolms.append(len(df.columns))

            if len(df.columns) < 5:
                print(file)
                break

            if len(df.columns) > 7:
                for i in range(7, len(df.columns)):
                    colname = f'Unnamed: {i}'
                    df = df.drop([colname], axis=1)

            dfe = df.dropna().copy()
            df.drop(df.columns[1], axis=1)
            dfe.columns = ['Cote', 'à 1 minute', 'à 3 minutes', 'à 15 minutes', '% CaCO3', '% Dolomie', '% insolubles']

        csv_file = file.split('.xls')[0] + '.csv'
        print(csv_file)
        dfe.to_csv(csv_file)