import requests, json

class DBService:
    def __init__(self):
        self.url_domain = 'https://trek.nasa.gov/moon/DSBservice/'

    def get_domain(self):
        return self.url_domain

    def query_by_bbox(self, ul_lon, ul_lat, lr_lon, lr_lat):
        param_str = str(ul_lon) + "," + str(ul_lat) + ","  + str(lr_lon) + "," + str(lr_lat)
        endpoint = self.url_domain + "webapi/lroc/CUMINDEX/labels/ptif?bbbox=" + param_str
        print(endpoint)
        response = requests.get(endpoint)
        return json.loads(response.content)

    
def main():
    db_service = DBService()
    json = db_service.query_by_bbox(-147.23657,40.34749,-147.11735,40.40706)
    for record in json:
        print(record['product_id'] + " : " + record['url'])


if __name__ == '__main__':
    main()