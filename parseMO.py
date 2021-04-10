from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv, time

# параметры формирования запроса html страницы
numDoc = 'numDoc='
Name_Org = 'Name_Org='
region = 'region='
adr = 'adr='
OrgOut = 'OrgOut=2'  # 2
pageNum = 'pageNum='  # номера страницы
order = 'order=num_doc'
orderType = 'orderType=asc'
Npage=0
datedoc = 'datedoc='
CiAcrOrg = 'CiAcrOrg='
status = 'status=1'
Expert = 'expert=0'
all = 'all=0'
isOld = 'isOld=0'
num_doc_old = 'num_doc_old='
date_doc_old = 'date_doc_old='
name_org_old = 'name_org_old='
adr_old = 'adr_old='
moduleId = 'moduleId=2'
html = ('https://grls.rosminzdrav.ru/Ree_orgCI2.aspx' + '?' +
                numDoc + '&' +
                Name_Org + '&' +
                region + '&' +
                adr + '&' +
                OrgOut + '&' +
                pageNum + str(Npage) + '&' +
                order + '&' +
                orderType + '&' +
                datedoc + '&' +
                CiAcrOrg + '&' +
                status + '&' +
                Expert + '&' +
                all + '&' +
                isOld + '&' +
                num_doc_old + '&' +
                date_doc_old + '&' +
                name_org_old + '&' +
                adr_old + '&' +
                moduleId)
row = ['№',
                   'Наименование',
                   'Сокращенное наименование',
                   'Субъект РФ',
                   'Юридический адрес',
                   'Сроки аккредитации']
start_time = time.time()
with open('Clinics.csv', 'w', newline='', encoding='utf-8') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(row)
    for Npage in range(1, 86):
        html = ('https://grls.rosminzdrav.ru/Ree_orgCI2.aspx?numDoc=&Name_Org=&region=&adr=&OrgOut=2&pageNum='
                +str(Npage)
                +'&order=num_doc&orderType=asc&datedoc=&CiAcrOrg=&status=1&expert=0&all=0&isOld=0&num_doc_old=&date_doc_old=&name_org_old=&adr_old=&moduleId=2')
        # Получим значения ID всех ссылок
        print(html)
        html_doc = urlopen(html).read()
        soup = BeautifulSoup(html_doc, 'html.parser')
        onclickalls = soup.find_all('td', {'align': 'left'})
        for onclickall in onclickalls:
            if 'onclick' not in onclickall.attrs:
                continue
            value = onclickall['onclick']
            if not value.startswith('window.location.href='):
                continue
            position = value.index('.aspx?') + 6
            value = value[position:-13]
            #    print(value)
            html2 = ('https://grls.rosminzdrav.ru/CIAcrOrgTrial.aspx?' + value + '&moduleId=2')
            html2_doc = urlopen(html2).read()
            soup2 = BeautifulSoup(html2_doc, 'html.parser')
            headnumdoc = soup2.find('input', {'name': 'ctl00$plate$txtHeadNumDoc'}).get('value')
            name = soup2.find('textarea', {'name': 'ctl00$plate$txtDeveloper_Name_R'})
            namesh = soup2.find('textarea', {'name': 'ctl00$plate$txtDeveloper_Namesh_R'})
            regiontxt = soup2.find('input', {'name': 'ctl00$plate$txtRegion'}).get('value')
            adres = soup2.find('input', {'name': 'ctl00$plate$txtAdres'}).get('value')
            dates = soup2.find('input', {'name': 'ctl00$plate$txtDates'}).get('value')
            row = ['%s' % headnumdoc,
                   ' %s' % name.text.replace("\r\n", ""),
                   ' %s' % namesh.text.replace("\r\n", ""),
                   ' %s' % regiontxt,
                   ' %s' % adres,
                   ' %s' % dates]
            writer.writerow(row)
        print('Done page: %s' % str(Npage))
        time.sleep(5)
csvFile.close()
print("--- %s seconds ---" % (time.time() - start_time))
