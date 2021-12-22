import requests,json,time,sys
from py_zipkin import Encoding
from py_zipkin.zipkin import zipkin_span

#APMのエンドポイント
def http_transport(encoded_span):
    requests.post(
        'https://<APMのエンドポイント>/20200101/observations/public-span?dataFormat=zipkin&dataFormatVersion=2&dataKey=<Publid Key>',
        data=encoded_span,
        headers={'Content-Type': 'application/json'},
    )    
    
def weather(code):
   with zipkin_span(
      service_name="Weather SampleAPM",
      span_name="Get Weather Data from Meteorological Agency",
      transport_handler=http_transport,
      encoding = Encoding.V2_JSON,
      sample_rate=100
  ):     
    
    #Span表示用のダミー処理1
    @zipkin_span(service_name='Weather SampleAPM', span_name='Span Sleep1')
    def some_function1():
        time.sleep(5/1000)
    some_function1()
    
    #気象庁のAPIにアクセス
    @zipkin_span(service_name='Weather SampleAPM', span_name='Access Weathere API')
    def Access_API():
        api = "https://www.jma.go.jp/bosai/forecast/data/forecast/{areacode}.json"       
        url = api.format(areacode = code)
        response = requests.get(url)
        data = response.json()
        wday=data[0]["timeSeries"][0]["timeDefines"][0]
        name=data[0]["timeSeries"][0]["areas"][0]["area"]["name"]
        weather=data[0]["timeSeries"][0]["areas"][0]["weathers"][0]
        print(wday + " " + name + " " + weather)  
    Access_API()
    
    #Span表示用のダミー処理2
    @zipkin_span(service_name='Weather SampleAPM', span_name='Span Sleep2')
    def some_function2():
        time.sleep(5/1000)
    some_function2()
                    
weather(sys.argv[1])
