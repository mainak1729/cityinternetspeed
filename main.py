import csv
import datetime
import jinja2
import json
import logging
import operator
import os
import webapp2

from CommonData import cityList

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Isp:
    def __init__(self, isp_name, download_kbps, upload_kbps, total_tests, distance_kms):
        self.ispName = isp_name
        self.count = 1
        self.downloadKbps = download_kbps
        self.uploadKbps = upload_kbps
        self.totalTests = total_tests
        self.distanceKms = distance_kms

class Handler(webapp2.RequestHandler):
    def write(self, *args, **keywords):
        self.response.out.write(*args, **keywords)
    def render_str(self, template, **parameters):
        t = jinja_env.get_template(template)
        return t.render(parameters)
    def render(self, template, **keywords):
        self.write(self.render_str(template, **keywords))

class MainPage(Handler):
    def get(self):
        self.render('form.html',
                    cityList=cityList,
                    defaultStartDate='2013-01-01',
                    defaultEndDate='2013-10-19',
                    dataStartDate='2008, 1 - 1, 1',
                    dataEndDate='2013, 10 - 1, 19')

class SpeedBar(Handler):
    def dateString_to_date(self, dateString): #for YYYY-MM-DD
        dateList = map(lambda x: int(x), dateString.split('-'))
        return datetime.date(dateList[0], dateList[1], dateList[2])

    def post(self):
        cityData = open('ahmedabadData.csv', 'rb')
        firstDate = datetime.date(2008, 1, 1)
        lastDate = datetime.date(2013, 10, 19)
        noData = False
        cityName = self.request.get('city')
        cityDataFile = cityName.lower() + 'Data.csv'
        cityData = open(cityDataFile, 'rb')

        startDate = self.dateString_to_date(self.request.get('startDate'))
        endDate = self.dateString_to_date(self.request.get('endDate'))
        ispList = []
        ispNameList = []

        for currentData in csv.reader(cityData, skipinitialspace=True):
            currentDate = self.dateString_to_date(currentData[1])
            if (currentDate >= startDate) and (currentDate <= endDate):
                currentIspName = currentData[0]
                if currentIspName not in ispNameList:
                    ispList.append(Isp(currentIspName, float(currentData[2]), float(currentData[3]), int(currentData[4]), float(currentData[5])*1.60934))
                    ispNameList.append(currentIspName)
                else:
                    currentIndex = ispNameList.index(currentIspName)
                    ispList[currentIndex].count += 1
                    ispList[currentIndex].downloadKbps += float(currentData[2])
                    ispList[currentIndex].uploadKbps += float(currentData[3])
                    ispList[currentIndex].totalTests += int(currentData[4])
                    ispList[currentIndex].distanceKms += float(currentData[5])*1.60934

        cityData.close()

        for isp in ispList:
            isp.downloadKbps /= isp.count
            isp.uploadKbps /= isp.count
            isp.distanceKms /= isp.count

        ispListSortedByDownloadKbps = sorted(ispList, key=operator.attrgetter('downloadKbps'), reverse=True)
        ispListSortedByUploadKbps = sorted(ispList, key=operator.attrgetter('uploadKbps'), reverse=True)
        dataRowsForDownloadSpeed = [[isp.ispName, isp.downloadKbps,
            isp.ispName.upper() + '\nAverage download speed: ' + '{0:.3f}'.format(isp.downloadKbps)
            + ' kbps\nAverage upload speed: ' + '{0:.3f}'.format(isp.uploadKbps)
            + ' kbps\nNumber of tests analysed: ' + str(isp.totalTests)
            + '\nAverage distance between the client and the server across all tests: '
            + '{0:.3f}'.format(isp.distanceKms) + ' km'] for isp in ispListSortedByDownloadKbps]
        dataRowsForUploadSpeed = [[isp.ispName, isp.uploadKbps,
            isp.ispName.upper() + '\nAverage download speed: ' + '{0:.3f}'.format(isp.downloadKbps)
            + ' kbps\nAverage upload speed: ' + '{0:.3f}'.format(isp.uploadKbps)
            + ' kbps\nNumber of tests analysed: ' + str(isp.totalTests)
            + '\nAverage distance between the client and the server across all tests: '
            + '{0:.3f}'.format(isp.distanceKms) + ' km'] for isp in ispListSortedByUploadKbps]
        self.render('chart.html',
                    cityName=cityName,
                    startDate=str(startDate),
                    endDate=str(endDate),
                    dataRowsForDownloadSpeed=json.dumps(dataRowsForDownloadSpeed),
                    dataRowsForUploadSpeed=json.dumps(dataRowsForUploadSpeed),
                    lastUpdatedDate='2013-10-19')

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/submit', SpeedBar)],
                               debug=True)
