import csv
import datetime
import jinja2
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
        self.render('form.html', cityList=cityList)

class SpeedBar(Handler):
    def dateString_to_date(self, dateString): #for YYYY-MM-DD
        dateList = map(lambda x: int(x), dateString.split('-'))
        return datetime.date(dateList[0], dateList[1], dateList[2])

    def post(self):
        cityData = open('ahmedabadData.csv', 'rb')
        firstDate = datetime.date(2008, 1, 1)
        lastDate = datetime.date(2013, 10, 19)
        noData = False
        negativeRange = False
        invalidDate = False
        cityName = self.request.get('city')

        if cityName == 'Amritsar':
            cityData = open('amritsarData.csv', 'rb')
        if cityName == 'Aurangabad':
            cityData = open('aurangabadData.csv', 'rb')
        if cityName == 'Bangalore':
            cityData = open('bangaloreData.csv', 'rb')
        if cityName == 'Bhopal':
            cityData = open('bhopalData.csv', 'rb')
        if cityName == 'Bhubaneswar':
            cityData = open('bhubaneswarData.csv', 'rb')
        if cityName == 'Calicut':
            cityData = open('calicutData.csv', 'rb')
        if cityName == 'Chandigarh':
            cityData = open('chandigarhData.csv', 'rb')
        if cityName == 'Chennai':
            cityData = open('chennaiData.csv', 'rb')
        if cityName == 'Cochin':
            cityData = open('cochinData.csv', 'rb')
        if cityName == 'Coimbatore':
            cityData = open('coimbatoreData.csv', 'rb')
        if cityName == 'Delhi':
            cityData = open('delhiData.csv', 'rb')
        if cityName == 'Ernakulam':
            cityData = open('ernakulamData.csv', 'rb')
        if cityName == 'Faridabad':
            cityData = open('faridabadData.csv', 'rb')
        if cityName == 'Ghaziabad':
            cityData = open('ghaziabadData.csv', 'rb')
        if cityName == 'Gurgaon':
            cityData = open('gurgaonData.csv', 'rb')
        if cityName == 'Guwahati':
            cityData = open('guwahatiData.csv', 'rb')
        if cityName == 'Hyderabad':
            cityData = open('hyderabadData.csv', 'rb')
        if cityName == 'Indore':
            cityData = open('indoreData.csv', 'rb')
        if cityName == 'Jaipur':
            cityData = open('jaipurData.csv', 'rb')
        if cityName == 'Jalandhar':
            cityData = open('jalandharData.csv', 'rb')
        if cityName == 'Jodhpur':
            cityData = open('jodhpurData.csv', 'rb')
        if cityName == 'Kannur':
            cityData = open('kannurData.csv', 'rb')
        if cityName == 'Kanpur':
            cityData = open('kanpurData.csv', 'rb')
        if cityName == 'Kolkata':
            cityData = open('kolkataData.csv', 'rb')
        if cityName == 'Kottayam':
            cityData = open('kottayamData.csv', 'rb')
        if cityName == 'Lucknow':
            cityData = open('lucknowData.csv', 'rb')
        if cityName == 'Ludhiana':
            cityData = open('ludhianaData.csv', 'rb')
        if cityName == 'Madurai':
            cityData = open('maduraiData.csv', 'rb')
        if cityName == 'Meerut':
            cityData = open('meerutData.csv', 'rb')
        if cityName == 'Mumbai':
            cityData = open('mumbaiData.csv', 'rb')
        if cityName == 'Nagari':
            cityData = open('nagariData.csv', 'rb')
        if cityName == 'Nagpur':
            cityData = open('nagpurData.csv', 'rb')
        if cityName == 'Nasik':
            cityData = open('nasikData.csv', 'rb')
        if cityName == 'Patiala':
            cityData = open('patialaData.csv', 'rb')
        if cityName == 'Patna':
            cityData = open('patnaData.csv', 'rb')
        if cityName == 'Pondicherry':
            cityData = open('pondicherryData.csv', 'rb')
        if cityName == 'Pune':
            cityData = open('puneData.csv', 'rb')
        if cityName == 'Rajkot':
            cityData = open('rajkotData.csv', 'rb')
        if cityName == 'Surat':
            cityData = open('suratData.csv', 'rb')
        if cityName == 'Suri':
            cityData = open('suriData.csv', 'rb')
        if cityName == 'Thane':
            cityData = open('thaneData.csv', 'rb')
        if cityName == 'Thrissur':
            cityData = open('thrissurData.csv', 'rb')
        if cityName == 'Trivandrum':
            cityData = open('trivandrumData.csv', 'rb')
        if cityName == 'Vadodara':
            cityData = open('vadodaraData.csv', 'rb')
        if cityName == 'Vijayawada':
            cityData = open('vijayawadaData.csv', 'rb')

        try:
            startDate = self.dateString_to_date(self.request.get('startDate'))
            endDate = self.dateString_to_date(self.request.get('endDate'))
            if endDate < startDate:
                negativeRange = True
            else:
                if startDate > lastDate or endDate < firstDate:
                    noData = True
                else:
                    if startDate < firstDate:
                        startDate = firstDate
                    if endDate > lastDate:
                        endDate = lastDate
        except:
            invalidDate = True

        if invalidDate:
            self.response.out.write("""<html>
                <head>
                    <script type="text/javascript">
                        function goBack() {
                            window.history.back()
                        }
                    </script>
                </head>
                <body>
                    Invalid date! Please go back and try again.<br><br>
                    <input type="button" value="Back" onclick="goBack()">
                </body></html>""")
        elif negativeRange:
            self.response.out.write("""<html>
                <head>
                    <script type="text/javascript">
                        function goBack() {
                            window.history.back()
                        }
                    </script>
                </head>
                <body>
                    End date can't be earlier than start date. Please go back and try again.<br><br>
                    <input type="button" value="Back" onclick="goBack()">
                </body></html>""")
        elif noData:
            self.response.out.write("""<html>
                <head>
                    <script type="text/javascript">
                        function goBack() {
                            window.history.back()
                        }
                    </script>
                </head>
                <body>
                    Data are not available for the date range. Please go back and choose a range within 2008-01-01 and 2013-10-19.<br><br>
                    <input type="button" value="Back" onclick="goBack()">
                </body></html>""")
        else:
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
            self.response.out.write("""<html>
                <head>
                    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
                    <script type="text/javascript">
                        google.load('visualization', '1.0', {'packages':['corechart']});
                        google.setOnLoadCallback(drawDownloadChart);
                        google.setOnLoadCallback(drawUploadChart);
                        function drawDownloadChart() {
                            var data = new google.visualization.DataTable();
                            data.addColumn('string', 'ISP name');
                            data.addColumn('number', 'Average download speed (kbps)');
                            data.addColumn({type: 'string', role: 'tooltip'});
                            data.addRows(""" + repr([[isp.ispName, isp.downloadKbps,
                                isp.ispName.upper() + '\nAverage download speed: ' + '{0:.3f}'.format(isp.downloadKbps)
                                + ' kbps\nAverage upload speed: ' + '{0:.3f}'.format(isp.uploadKbps)
                                + ' kbps\nNumber of tests analysed: ' + str(isp.totalTests)
                                + '\nAverage distance between the client and the server across all tests: '
                                + '{0:.3f}'.format(isp.distanceKms) + ' km'] for isp in ispListSortedByDownloadKbps]) + """);
                            var options = {'title':'Average download speed (kbps) of ISPs in """
                                                             + cityName
                                                             + """ from """
                                                             + str(startDate)
                                                             + """ to """
                                                             + str(endDate)
                                                             + """',
                                                         'titleTextStyle':{'fontSize':14, 'bold':true},
                                                         'width':800,
                                                         'height':1700,
                                                         'legend':'none',
                                                         'chartArea':{'left':200, 'top':150},
                                                         'bar':{'groupWidth':5},
                                                         'hAxis':{'textStyle':{'fontSize':10}},
                                                         'vAxis':{'textStyle':{'fontSize':10}},
                                                         'tooltip':{'textStyle':{'fontSize':12}}};
                            var chart = new google.visualization.BarChart(document.getElementById('download_div'));
                            chart.draw(data, options);
                        }
                        function drawUploadChart() {
                            var data = new google.visualization.DataTable();
                            data.addColumn('string', 'ISP name');
                            data.addColumn('number', 'Average upload speed (kbps)');
                            data.addColumn({type: 'string', role: 'tooltip'});
                            data.addRows(""" + repr([[isp.ispName, isp.uploadKbps,
                                isp.ispName.upper() + '\nAverage download speed: ' + '{0:.3f}'.format(isp.downloadKbps)
                                + ' kbps\nAverage upload speed: ' + '{0:.3f}'.format(isp.uploadKbps)
                                + ' kbps\nNumber of tests analysed: ' + str(isp.totalTests)
                                + '\nAverage distance between the client and the server across all tests: '
                                + '{0:.3f}'.format(isp.distanceKms) + ' km'] for isp in ispListSortedByUploadKbps]) + """);
                            var options = {'title':'Average upload speed (kbps) of ISPs in """
                                                             + cityName
                                                             + """ from """
                                                             + str(startDate)
                                                             + """ to """
                                                             + str(endDate)
                                                             + """',
                                                         'titleTextStyle':{'fontSize':14, 'bold':true},
                                                         'width':800,
                                                         'height':1700,
                                                         'legend':'none',
                                                         'colors':['red'],
                                                         'chartArea':{'left':200, 'top':150},
                                                         'bar':{'groupWidth':5},
                                                         'hAxis':{'textStyle':{'fontSize':10}},
                                                         'vAxis':{'textStyle':{'fontSize':10}},
                                                         'tooltip':{'textStyle':{'fontSize':12}}};
                            var chart = new google.visualization.BarChart(document.getElementById('upload_div'));
                            chart.draw(data, options);
                        }
                        function goBack() {
                            window.history.back()
                        }
                    </script>
                    <title>ISPs' speed chart for Indian cities</title>
                </head>
                <body>
                    <div><input type="button" value="Back" onclick="goBack()"></div><br>
                    Please note that results include some private ISPs.<br>
                    Also actual speed vary over different parts of a city over different time of a day.
                    <div id="download_div"></div>
                    <div id="upload_div"></div>
                    Data from <a href="http://www.netindex.com/source-data/" target="_blank">http://www.netindex.com/source-data/</a><br>
                    <a href="https://drive.google.com/file/d/0B6GVDqnESJVseEdsclM4YzNoOEU/edit?usp=sharing" target="_blank">FAQ</a> from source<br>
                    Last updated: 2013-10-19<br>
                    <a href="mailto:mainak1729@gmail.com?subject=Feedback%20for%20cityinternetspeed" target="_blank">Feedback</a><br><br>
                    <div><input type="button" value="Back" onclick="goBack()"></div>
                </body></html>""")

app = webapp2.WSGIApplication([('/', MainPage),
                                                             ('/submit', SpeedBar)],
                                                             debug=True)
