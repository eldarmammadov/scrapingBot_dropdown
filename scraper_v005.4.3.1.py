import functions as fnc
import re

import openpyxl
#from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
from openpyxl import load_workbook

import tkinter as tk
from tkinter import ttk

import os, sys,shutil

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

root = tk.Tk()
root.title("Track Scraping")
root.geometry('900x430')
canvas1 = tk.Canvas(root, width=800, height=730)
canvas1.pack(side='left',expand=True,fill=tk.X,padx=3,pady=3)
canvas2 = tk.Canvas(root, width=200, height=730)
canvas2.pack(side='right',padx=3,pady=3)

ListOfEntries=[]

fixed_entry = ttk.Entry(canvas1, width=100)
fixed_entry.pack(expand=True,fill=tk.X,padx=3,pady=3)
fixed_entry.focus()

text_entryNumbers=[]

def resource_path_output(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

df_csv_config = pd.read_json(resource_path_output('./ConfigurationFile/configFile.csv'))
lst_dropdown_keys=[]
#reading keys
def read_keys_dropdown():
    global lst_dropdown_keys
    lst_dropdown_keys=list(df_csv_config.to_dict().keys())
    lst_dropdown_keys.pop(0)
    lst_dropdown_keys.pop(-1)
    return lst_dropdown_keys

vOptions=read_keys_dropdown()
var_drp_list=tk.StringVar(canvas2)
tk.OptionMenu(canvas2,var_drp_list,*vOptions).pack()
print(var_drp_list.get())
#read json google url
def read_url():
    #df_csv_config = pd.read_json('cnfgFile.csv')
    pattern = re.compile(r"^(?:/.|[^//])*/((?:\\.|[^/\\])*)/")
    result = (re.match(pattern, df_csv_config.values[0][0]))
    return pattern.match(df_csv_config.values[0][0]).group(1)

#csv file read
def csv_file_read(sheet_name):
    # df_csv_config = pd.read_json('cnfgFile.csv')

    if sheet_name in df_csv_config.__iter__():
        v_ReleaseTitle = df_csv_config.to_dict('records')[0][sheet_name]
        v_ReleaseDate = df_csv_config.to_dict('records')[1][sheet_name]
        v_ReleaseUPC = df_csv_config.to_dict('records')[2][sheet_name]
        v_ReleaseISRC = df_csv_config.to_dict('records')[3][sheet_name]
        v_ReleaseGenre = df_csv_config.to_dict('records')[4][sheet_name]
        v_ReleasePriority = df_csv_config.to_dict('records')[5][sheet_name]
        v_ReleaseRadioExt = df_csv_config.to_dict('records')[6][sheet_name]
        v_ReleaseCountry = df_csv_config.to_dict('records')[7][sheet_name]
        return v_ReleaseTitle,v_ReleaseDate,v_ReleaseUPC,v_ReleaseISRC,v_ReleaseGenre,v_ReleasePriority,v_ReleaseRadioExt,v_ReleaseCountry

#number of urls-> added entry box
count_url=1
COUNT_ADD_URL_BOX=1

def addurlbox():
    global extraentryBoxValue
    global ListOfAddedEntryBoxes
    global  COUNT_ADD_URL_BOX
    ListOfAddedEntryBoxes=[]
    extraentryBox = tk.Entry(canvas1,width=100)
    extraentryBox.pack(expand=True,fill=tk.BOTH,padx=3,pady=3)
    text_entryNumbers.append(extraentryBox)
    extraentryBoxValue=extraentryBox
    ListOfAddedEntryBoxes.append(extraentryBox)
    COUNT_ADD_URL_BOX +=1
    print(len(ListOfAddedEntryBoxes),'LEN()',COUNT_ADD_URL_BOX)

def crawler():
    global  count_url
    inputs = []
    for widget in canvas1.winfo_children():
        if isinstance(widget, tk.Entry):
            inputs.append(widget.get())

    for i in range(len(inputs)):
        # taking url of SoundCloud platform
        # user inputs it, as string value
        varUrl_SC = inputs[i]

        # going to url(SC) via Selenium WebDriver
        chrome_options = Options()
        chrome_options.headless = True
        chrome_options.add_argument("start-maximized")
        # options.add_experimental_option("detach", True)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')

        def resource_path(relative_path):
            try:
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.dirname(__file__)
            return os.path.join(base_path, relative_path)

        #driver = webdriver.Chrome(resource_path('./driver/chromedriver.exe'))

        #webdriver_service = Service(resource_path('./driver/chromedriver.exe'))
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        driver.get(varUrl_SC)

        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()
            print('accepted cookies')
        except Exception as e:
            print('no cookie button!')

        # get text value of below items from opened SC website:
        # soundTitle_username, title, duration
        soundTitle_usernameTitleContainer = driver.find_element(By.CLASS_NAME, "soundTitle__title")
        varStrTitle = soundTitle_usernameTitleContainer.text
        soundTitle_usernameHeroContainer = driver.find_element(By.CLASS_NAME, "sc-link-secondary")
        varsoundTitle_usernameHeroContainer = soundTitle_usernameHeroContainer.text
        varLbl = varsoundTitle_usernameHeroContainer
        varsoundTitle_usernameHeroContainer = varsoundTitle_usernameHeroContainer.replace(' ', '')
        # playbackTimeline__duration
        ##playbackTimeline__duration =driver.find_element(By.CLASS_NAME,"playbackTimeline__duration")
        playbackTimeline__duration = driver.find_element(By.XPATH,
                                                         "*//div[contains(@class,'playbackTimeline__duration')]/span[2]")
        varplaybackTimeline_duration = playbackTimeline__duration.text
        varMin = varplaybackTimeline_duration.split(":")[0]
        varSec = varplaybackTimeline_duration.split(":")[1]
        lblGS = ttk.Label(canvas1).pack(expand=True,fill=tk.BOTH,padx=3,pady=3)
        ###lblGS = ttk.Label(canvas1).grid(column=1, row=11, sticky=('N'))#GRID
        canvas1.create_window(333,420,window=lblGS)#CREATE_WINDOW
        lbl_print_textSC=ttk.Label(canvas1, text="...gathered data from SoundCloud " + varStrTitle + " ...")
        lbl_print_textSC.pack(expand=True, fill=tk.BOTH, padx=3, pady=3)
        ###ttk.Label(canvas1, text="...gathered data from SoundCloud " + varStrTitle + " ...").grid(column=0, row=12, sticky='W')#GRID
        root.update()
        print('...gathered data from SoundCloud ' + varStrTitle + ' ...')

        varSheetname_GS = ''
        entry_var_temporary = tk.StringVar()
        entry_var_temporary.set(varsoundTitle_usernameHeroContainer)
        entry_shtname_temp=tk.Entry(canvas2,width=30,textvariable=entry_var_temporary)
        entry_shtname_temp.pack()
        entry_shtname_temp.bind('<Return>', lambda event: entry_shtname_temp.destroy())
        entry_shtname_temp.focus_set()
        root.after(7000,entry_shtname_temp.destroy)
        entry_shtname_temp.wait_window()

        if varsoundTitle_usernameHeroContainer!=entry_var_temporary.get():
            varSheetname_GS=entry_var_temporary.get()

        if varsoundTitle_usernameHeroContainer == 'FloatingBlueRecords' or varsoundTitle_usernameHeroContainer == 'DayDoseOfHouse':
            varSheetname_GS = varsoundTitle_usernameHeroContainer
        else:
            # look for sheetname as an input value entered by user
            entry_var=tk.StringVar()
            new_sheetname_entryBox=tk.Entry(canvas2,width=30,textvariable=entry_var)
            new_sheetname_entryBox.pack()
            new_sheetname_entryBox.bind('<Return>',lambda event: new_sheetname_entryBox.destroy())
            new_sheetname_entryBox.focus_set()

            new_sheetname_entryBox.wait_window()
            var_new_sheetName =entry_var.get()

            varSheetname_GS = var_new_sheetName  #input("Enter the sheetname in (GooSheets):")

        resCSVcolumnNames=csv_file_read(varSheetname_GS)
        vURL_GooShts = "https://docs.google.com/spreadsheets/d/1hpK3ziZq9QrdBi1FYnDy4SPKiciyo4UBwJBcHs0g2Rw/edit#gid=487846033"

        driver.quit()

        varSheetname_GS=var_drp_list.get()
        print(var_drp_list.get())
        sheetname = varSheetname_GS
        sheet_id = read_url()
        xls = pd.ExcelFile(f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx')
        df = pd.read_excel(xls, sheetname, header=0)

        print(varStrTitle.lower().replace(" ", ""),"+++")
        print(df[resCSVcolumnNames[0]].loc[lambda x: x.str.lower().replace(" ", "") == varStrTitle.lower().replace(" ", "")].index,'---')
        print(df.loc[df[resCSVcolumnNames[0]].str.lower().str.replace(' ', '') == varStrTitle.lower().replace(" ", ""), 'Release Title'])
        df[resCSVcolumnNames[0]].str.lower().str.replace(' ', '').eq(varStrTitle.lower().replace(" ", "")).any()

        rowValues = df.loc[df[resCSVcolumnNames[0]].str.lower().str.replace(' ', '') == varStrTitle.lower().replace(" ", "")]
        print(rowValues,'rV')
        varIndxValueToCompare = df[resCSVcolumnNames[0]].loc[lambda x: x.str.lower().str.replace(' ', '') == varStrTitle.lower().replace(" ", "")].index
        print(varIndxValueToCompare)
        varRT_to_write = rowValues[resCSVcolumnNames[0]].loc[rowValues.index[0]]
        print(varRT_to_write)

        numTire=varRT_to_write.count('-')
        if numTire >1:
            artistname_comma=varRT_to_write.split(",")
            if artistname_comma[-1].count('-')<=1:
                songTitle=artistname_comma[-1].split(" - ")[1]
                artNome0=",".join(artistname_comma[:-1])
                artNome=artNome0+','+artistname_comma[-1].split(" - ")[0]

                varArtistName = artNome
                varSongTitle = songTitle
            else:
                songTitle=artistname_comma[-1].split(" - ")[2]
                varSongTitle = songTitle
                artNome0='-'.join(artistname_comma[-1].split(" - ")[:-1])
                artNome=','.join(artistname_comma[:-1])+','+artNome0
                varArtistName=artNome
        else:
            varArtistName = varRT_to_write.split(" - ")[0]
            varSongTitle = varRT_to_write.split(" - ")[1]

        varG_to_write = rowValues[resCSVcolumnNames[4]].loc[rowValues.index[0]]
        varUPC_to_write = rowValues[resCSVcolumnNames[2]].loc[rowValues.index[0]]
        varPriority_to_write = rowValues[resCSVcolumnNames[5]].loc[rowValues.index[0]]
        varRD_to_write = rowValues[resCSVcolumnNames[1]].loc[rowValues.index[0]]
        if pd.isna(rowValues[resCSVcolumnNames[1]].loc[rowValues.index[0]]):
            a = varIndxValueToCompare[0]
            for i in range(10):
                a = a - 1
                varRD_to_write = df[resCSVcolumnNames[1]].loc[a]
                if pd.isna(varRD_to_write) == False:
                    break

        #function module import, returns list of variables
        varRD_to_write, varRDF_to_write, varRI_to_write, varRE_to_write=fnc.conditionals_year(varSheetname_GS,varIndxValueToCompare,rowValues,varRD_to_write,varRD_to_write,pd)

        varCntry_to_write = rowValues[resCSVcolumnNames[7]].loc[rowValues.index[0]]
        allData_ColumnList = ['Artist Name', 'Song Title', 'Country', 'Release Date', 'Release Date (Formatted)', 'UPC',
                              'ISRC', 'Genre', 'Minute', 'Seconds', 'URL Link', 'Label Name', 'Priority', 'Radio/Extended']
        allData_RowList = [varArtistName, varSongTitle, varCntry_to_write, varRD_to_write, varRDF_to_write, varUPC_to_write,
                           varRI_to_write, varG_to_write, varMin, varSec, varUrl_SC, varLbl, varPriority_to_write,
                           varRE_to_write]
        allData_readyfordf = dict(zip(allData_ColumnList, allData_RowList))

        AllDataOutput = pd.DataFrame(allData_readyfordf, index=[0])

        lblES = ttk.Label(canvas1).pack()
        ###lblES = ttk.Label(canvas1).grid(column=1, row=13, sticky=('N'))#GRID
        lbl_print_textGSH=ttk.Label(canvas1, text="...pulled out data also from googlesheets ...")
        lbl_print_textGSH.pack(expand=True,fill=tk.BOTH,padx=3,pady=3)
        ###ttk.Label(canvas1, text="...pulled out data also from googlesheets ...").grid(column=0, row=14, sticky='W')#GRID
        root.update()
        print('...pulled out data also from googlesheets ...')

        def resource_path_output(relative_path):
            """ Get absolute path to resource, works for dev and for PyInstaller """
            try:
                # PyInstaller creates a temp folder and stores path in _MEIPASS
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath(".")

            return os.path.join(base_path, relative_path)

        def resolve_path(path):
            if getattr(sys, "frozen", False):
                # If the 'frozen' flag is set, we are in bundled-app mode!
                resolved_path = os.path.abspath(os.path.join(sys._MEIPASS, path))
                print(resolved_path,'-+-')
            else:
                # Normal development mode. Use os.getcwd() or __file__ as appropriate in your case...
                resolved_path = os.path.abspath(os.path.join(os.getcwd(), path))
                print(resolved_path, '+-+')

            return resolved_path


        if getattr(sys,'frozen',False) and hasattr(sys,'_MEIPASS'):
            print('runs in PyIns bundle')
            print(os.path.abspath)
            print(os.getcwd())
        else:
            print('runs in normal python process')
        new_path=os.getcwd()
        new_path02 = new_path[:-4]
        new_path03xl = new_path02 + 'outputFile/outputData.xlsm'

        try:
            print(len(ListOfAddedEntryBoxes),'length')
            var_len=1
            if not ListOfAddedEntryBoxes:
                var_len
            else:
                var_len=len(ListOfAddedEntryBoxes)+1
        except NameError:
            var_len = 1

        with pd.ExcelWriter(new_path03xl, engine='openpyxl', mode='r+', if_sheet_exists='overlay',engine_kwargs={'keep_vba': True}) as writer:
            book = load_workbook(new_path03xl, keep_vba=True)

            print('read file')
            print(writer.engine)
            #writer.book = book
            #writer.sheets = {ws.title: ws for ws in book.worksheets}

            current_sheet = book['Sheet1']
            Column_A = current_sheet['A']
            maxrow = max(c.row for c in Column_A if c.value is not None)

            for sheetname in writer.sheets:
                AllDataOutput.to_excel(writer, sheet_name=sheetname, startrow=maxrow, index=False, header=False)

        ttk.Label(canvas2, text=f'{varSongTitle}...Done! {count_url}/{str(COUNT_ADD_URL_BOX)}').pack(side=tk.BOTTOM,fill=tk.Y,padx=3,pady=3)
        lbl_print_textSC.destroy()
        lbl_print_textGSH.destroy()
        root.update()
        count_url = count_url + 1

add_urlbox_button = tk.Button(canvas2, text="Add another URL-track from SoundCloud", font='Segoe 9', command=addurlbox)
add_urlbox_button.pack(padx=3,pady=3)

button1 = tk.Button(canvas2,text='scrape', command=crawler, bg='darkblue', fg='white',width=33)
button1.pack(padx=3,pady=3)

root.mainloop()
#pyinstaller -F --add-data "./outputFile/outputData.xlsm;./outputFile" --add-data "./ConfigurationFile/configFile.csv;./ConfigurationFile" scraper_v005.4.3.1.py --onefile --noconsole --clean --add-binary "./driver/chromedriver.exe;./driver"
#pyinstaller scraper_v005.4.3.1.py --onefile --add-binary "./driver/chromedriver.exe;./driver" --add-data "./outputFile/outputData.xlsm;./outputFile"