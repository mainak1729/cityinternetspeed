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

class Isp(object):
    def __init__(self, isp_name, download_kbps, upload_kbps, total_tests, distance_kms):
        self.ispName = isp_name
        self.count = 1
        self.downloadKbps = download_kbps
        self.uploadKbps = upload_kbps
        self.totalTests = total_tests
        self.distanceKms = distance_kms

minDate = '2008-01-01'
maxDate = '2013-10-19'

def dateStringToDate(dateString): #for YYYY-MM-DD
    return datetime.date(*map(lambda x: int(x), dateString.split('-')))

def dateRangeToDates(dateRange): #for 'YYYY-MM-DD to YYYY-MM-DD'
    return map(dateStringToDate, dateRange.split(' to '))

def generateDataRows(ispList, attribute):
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

def generateChartData(cityName, startDate, endDate):
    #cityDataFile is a csv file containing ISP name, test date, average download speed (kbps), average upload speed (kbps), number of tests analysed, average distance (miles) between the client and the server across all tests. For example,

    #ahmedabadData.py:
    #"NIB (National Internet Backbone)","2008-01-01",1549.52,237.856,272,283.735

    cityDataFile = cityName.lower() + 'Data.csv'
    cityData = open(cityDataFile, 'r')

    ispList = []
    ispNameList = []

    dataIterator = csv.reader(cityData, skipinitialspace=True)
    currentData = dataIterator.next()

    while dateStringToDate(currentData[1]) < startDate:
        currentData = dataIterator.next()

    while dateStringToDate(currentData[1]) <= endDate:
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
    dataRowsForDownloadSpeed = generateDataRows(ispListSortedByDownloadKbps, 'downloadKbps')
    dataRowsForUploadSpeed = generateDataRows(ispListSortedByUploadKbps, 'uploadKbps')

    return dataRowsForDownloadSpeed, dataRowsForUploadSpeed

firstCityName = 'Ahmedabad'
firstStartDate = '2013-01-01'
firstEndDate = '2013-10-19'
firstDataRowsForDownloadSpeed, firstDataRowsForUploadSpeed = generateChartData(firstCityName, dateStringToDate(firstStartDate), dateStringToDate(firstEndDate))

firstForm = jinja_env.get_template('form.html').render(cityList=cityList,
    cityName=firstCityName,
    startDate=firstStartDate,
    endDate=firstEndDate,
    minDate=minDate,
    maxDate=maxDate)

firstChart = jinja_env.get_template('chart.html').render(cityName=firstCityName,
    startDate=firstStartDate,
    endDate=firstEndDate,
    dataRowsForDownloadSpeed=json.dumps(firstDataRowsForDownloadSpeed),
    dataRowsForUploadSpeed=json.dumps(firstDataRowsForUploadSpeed),
    ispCount=len(firstDataRowsForDownloadSpeed),
    maxDate=maxDate)

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
        self.response.out.write(firstForm)
        self.response.out.write(firstChart)

    def post(self):
        cityName = self.request.get('city')

        startDate, endDate = dateRangeToDates(self.request.get('dateRange'))

        self.render('form.html',
            cityList=cityList,
            cityName=cityName,
            startDate=startDate,
            endDate=endDate,
            minDate=minDate,
            maxDate=maxDate)

        dataRowsForDownloadSpeed, dataRowsForUploadSpeed = generateChartData(cityName, startDate, endDate)

        self.render('chart.html',
            cityName=cityName,
            startDate=str(startDate),
            endDate=str(endDate),
            dataRowsForDownloadSpeed=json.dumps(dataRowsForDownloadSpeed),
            dataRowsForUploadSpeed=json.dumps(dataRowsForUploadSpeed),
            ispCount=len(dataRowsForDownloadSpeed),
            maxDate=maxDate)

app = webapp2.WSGIApplication([('/', MainPage)])
