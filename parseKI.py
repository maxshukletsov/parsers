from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv, time

row = ['Номер РКИ',
                   ' Наименование ЛП',
                   ' Организация, проводящая КИ',
                   ' Страна разраб-ка',
                   ' Организация, привлеченная разработчиком ЛП',
                   ' Начало (дата)',
                   ' Окончание (дата)',
                   ' № протокола',
                   ' Протокол',
                   ' Фаза КИ',
                   ' Количество пациентов',
                   ' Области применения',]
start_time = time.time()
with open('KI.csv', 'w', newline='', encoding='utf-8') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(row)
    for Npage in range(1, 804):
        html = ('https://grls.rosminzdrav.ru/CiPermitionReg.aspx?PermYear=0&DateBeg=&DateEnd=&DateInc=&NumInc=&RegNm=&'
                +'Statement=&Protocol=&Qualifier=&ProtoNum=&idCIStatementCh=&CiPhase=&RangeOfApp=&Torg=&LFDos=&Producer'
                +'=&Recearcher=&sponsorCountry=&MedBaseCount=&CiType=&PatientCount=&OrgDocOut=2&Status=&NotInReg=0&'
                +'All=0&PageSize=8&order=date_perm&orderType=desc&pagenum='+str(Npage))
        # Получим значения ID всех ссылок
        #print(html)
        error = 0
        errorline =''
        html_doc = urlopen(html).read()
        soup = BeautifulSoup(html_doc, 'html.parser')
        onclickalls = soup.find_all('tr', {'class': 'hi_sys poi stat_reged'})
        for onclickall in onclickalls:
            if 'onclick' not in onclickall.attrs:
                continue
            number = onclickall.find('td').text
            #print(number)
            NRKI = onclickall.find('td', text = number).find_next('td').text
            #print(NRKI)
            DateCreate = onclickall.find('td', text=NRKI).find_next('td').text
            #print(DateCreate)
            Name = onclickall.find('td', text=DateCreate).find_next('td').text
            #print(Name)
            Organization = onclickall.find('td', text=Name).find_next('td').text
            #print(Organization)
            Country = onclickall.find('td', text=Organization).find_next('td').text
            #print(Country)
            OrgCreate = onclickall.find('td', text=Country).find_next('td').text
            #print(OrgCreate)
            StartDate = onclickall.find('td', text=OrgCreate).find_next('td').text
            #print(StartDate)
            EndDate = onclickall.find('td', text=OrgCreate).find_next('td').find_next('td').text
            #print(EndDate)
            ID = onclickall.find('td', text=EndDate).find_next('td').text
            #print(ID)
            FullName = onclickall.find('td', text=ID).find_next('td').text
            #print(FullName)
            Phase = onclickall.find('td', text=FullName).find_next('td').text
            #print(Phase)
            Vid = onclickall.find('td', text=Phase).find_next('td').text
            #print(Vid)
            ColMO = onclickall.find('td', text=Vid).find_next('td').text
            #print(ColMO)
            ValPatient = onclickall.find('td', text=Vid).find_next('td').find_next('td').text
            #print(ValPatient)
            Application = onclickall.find('td', text=Vid).find_next('td').find_next('td').find_next('td').text
            #print(Application)
            State = onclickall.find('td', text=Application).find_next('td').text
            #print(State)
            row = ['%s' % NRKI,
                   ' %s' % Name,
                   ' %s' % Organization,
                   ' %s' % Country,
                   ' %s' % OrgCreate,
                   ' %s' % StartDate,
                   ' %s' % EndDate,
                   ' %s' % ID,
                   ' %s' % FullName,
                   ' %s' % Phase,
                   ' %s' % ValPatient,
                   ' %s' % Application,]

            #print(row)
            try:
                writer.writerow(row)
            except UnicodeEncodeError:

                rowErr = u','.join(row)
                #rowErr = rowErr.replace('\u2265', '>=')
                #rowErr = rowErr.replace('\u2206', '/\\')
                #rowErr = rowErr.replace('\u2264', '=<')
                #rowErr = rowErr.replace('\u03b2', 'B')
                #rowErr = rowErr.replace('\u03b4', 'q')
                #rowErr = rowErr.replace('\u03b1', 'a')
                writer.writerow(rowErr)
                errorline = errorline + number +', '
                error = error+1
                print('errors: %s in line %s' % (str(error), errorline))
        print('Done page: %s ' % (str(Npage)))



        #time.sleep(0)
csvFile.close()
print("--- %s seconds ---" % (time.time() - start_time))
