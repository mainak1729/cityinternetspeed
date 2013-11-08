import csv
import datetime
import jinja2
import json
import operator
import os
import webapp2

from CommonData import cityList

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

minDate = '2008-01-01'
maxDate = '2013-10-19'

firstForm = jinja_env.get_template('form.html').render(cityList=cityList,
    cityName='Ahmedabad',
    startDate='2013-01-01',
    endDate='2013-10-19',
    minDate=minDate,
    maxDate=maxDate)

class Isp(object):
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
    def dateStringToDate(self, dateString): #for YYYY-MM-DD
        return datetime.date(*map(lambda x: int(x), dateString.split('-')))

    def dateRangeToDates(self, dateRange): #for 'YYYY-MM-DD to YYYY-MM-DD'
        return map(self.dateStringToDate, dateRange.split(' to '))

    def generateDataRows(self, ispList, attribute):
        return [[ isp.ispName,
            getattr(isp, attribute),
            isp.ispName.upper()
                + '\nAverage download speed: '
                + '{0:.3f}'.format(isp.downloadKbps)
                + ' kbps\nAverage upload speed: '
                + '{0:.3f}'.format(isp.uploadKbps)
                + ' kbps\nNumber of tests analysed: '
                + str(isp.totalTests)
                + '\nAverage distance between the client and the server across all tests: '
                + '{0:.3f}'.format(isp.distanceKms)
                + ' km'] for isp in ispList]

    def get(self):
        self.response.out.write(firstForm)

    def post(self):
        cityName = self.request.get('city')
        '''
        cityDataFile is a csv file containing ISP name, test date, average download speed (kbps), average upload speed (kbps), number of tests analysed, average distance (miles) between the client and the server across all tests. For example,

        ahmedabadData.py:
        "NIB (National Internet Backbone)","2008-01-01",1549.52,237.856,272,283.735
        '''
        cityDataFile = cityName.lower() + 'Data.csv'
        cityData = open(cityDataFile, 'r')

        startDate, endDate = self.dateRangeToDates(self.request.get('dateRange'))

        self.render('form.html',
            cityList=cityList,
            cityName=cityName,
            startDate=startDate,
            endDate=endDate,
            minDate=minDate,
            maxDate=maxDate)

        ispList = []
        ispNameList = []

        dataIterator = csv.reader(cityData, skipinitialspace=True)
        currentData = dataIterator.next()

        while self.dateStringToDate(currentData[1]) < startDate:
            currentData = dataIterator.next()

        while self.dateStringToDate(currentData[1]) <= endDate:
            try:
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
                currentData = dataIterator.next()
            except StopIteration:
                break

        cityData.close()

        for isp in ispList:
            isp.downloadKbps /= isp.count
            isp.uploadKbps /= isp.count
            isp.distanceKms /= isp.count

        ispListSortedByDownloadKbps = sorted(ispList, key=operator.attrgetter('downloadKbps'), reverse=True)
        ispListSortedByUploadKbps = sorted(ispList, key=operator.attrgetter('uploadKbps'), reverse=True)
        dataRowsForDownloadSpeed = self.generateDataRows(ispListSortedByDownloadKbps, 'downloadKbps')
        dataRowsForUploadSpeed = self.generateDataRows(ispListSortedByUploadKbps, 'uploadKbps')

        self.render('chart.html',
            cityName=cityName,
            startDate=str(startDate),
            endDate=str(endDate),
            dataRowsForDownloadSpeed=json.dumps(dataRowsForDownloadSpeed),
            dataRowsForUploadSpeed=json.dumps(dataRowsForUploadSpeed),
            ispCount=len(ispList),
            maxDate=maxDate)

app = webapp2.WSGIApplication([('/', MainPage)])
