from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv, time

row = ['Фамилия',
                   'ФИО',
                   'Номер',]
start_time = time.time()
with open('PI.csv', 'w', newline='', encoding='utf-8') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(row)
    for Npage in range(1, 138):
        html = ('https://grls.rosminzdrav.ru/ciexperts.aspx?F=&N=&P=&D=&ExpertID=&All=0&PageSize=&order=fio&orderType=desc&pagenum='
                +str(Npage)
                +'&moduleId=2&isApproved=1')
        # Получим значения ID всех ссылок
        print(html)
        html_doc = urlopen(html).read()
        soup = BeautifulSoup(html_doc, 'html.parser')
        onclickalls = soup.find_all('tr', {'align': 'left'})
        for onclickall in onclickalls:
            if 'onclick' not in onclickall.attrs:
                continue
            value = onclickall['onclick']
            print(value)
            if not value.startswith('go('):
                continue
            position = value.index('expGUID')
            #print(position)
            value = value[position:-2]
            #print('ID: %s' % value)
            html2 = ('https://grls.rosminzdrav.ru/CIExpert.aspx?moduleId=2&' + value)
            print(html2)
            html2_doc = urlopen(html2).read()
            soup2 = BeautifulSoup(html2_doc, 'html.parser')
            FIO = soup2.find('span', {'id': 'ctl00_plate_lblFIO'})
            Experience = soup2.find('span', {'id': 'ctl00_plate_lblExperience'})
            headdiv = soup2.find('td', {'id': 'ctl00_plate_headdiv'})

            row = ['%s' % FIO.text,
                   ' %s' % Experience.text,
                   ' %s' % headdiv.text[57:len(headdiv.text)-1],]
            print(row)
            writer.writerow(row)
        print('Done page: %s' % str(Npage))
        #time.sleep(5)
csvFile.close()
print("--- %s seconds ---" % (time.time() - start_time))
