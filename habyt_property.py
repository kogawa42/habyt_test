import requests
import pandas as pd
import os

class ParseAPI:
    def __init__(self, url):
        self.url = url
        self.data = None
        self.sellable_unit_df = None
        self.address_df = None
        self.image_df = None
        self.fee_df = None
        self.monthly_price_df = None

    def get_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            self.data = response.json()
        else:
            print(response.status_code)

    def make_sellable_unit_df(self):
        self.sellable_unit_df = pd.DataFrame([
            {
                'id': prop.get('id'), 
                'propertyId': prop.get('propertyId'),
                'fullAddress': prop.get('address', {}).get('fullAddress'),
                'roomNumber': prop.get('address', {}).get('roomNumber'),     
                'occupancyType': prop.get('occupancyType'),
                'bedrooms': prop.get('bedrooms'),
                'listingSqft': prop.get('listingSqft'),
                'unitSqft': prop.get('unitSqft'),
                'availableDate': prop.get('availableDate'),
                'minimumStay': prop.get('pricing', {}).get('minimumStay'),
                'minimumPrice': prop.get('pricing', {}).get('minimumPrice'),
                'maximumPrice': prop.get('pricing', {}).get('maximumPrice')
            } 
            for prop in self.data
        ])
        self.sellable_unit_df = self.sellable_unit_df.drop_duplicates(subset='id')
             
    def make_address_df(self):
        self.address_df = pd.DataFrame([
            {
                'propertyId': prop.get('propertyId'),
                'streetAddress': prop.get('address', {}).get('streetAddress'),
                'city': prop.get('address', {}).get('city'),
                'stateCode': prop.get('address', {}).get('stateCode'),
                'postalCode': prop.get('address', {}).get('postalCode'),
                'countryCode': prop.get('address', {}).get('countryCode'),
                'description': prop.get('description'),
                'propertyName': prop.get('propertyName'),
                'propertyDescription': prop.get('propertyDescription'),
                'marketingName': prop.get('marketingName'),
                'floorplanName': prop.get('floorplanName'),
                'neighborhood': prop.get('neighborhood'),
                'neighborhoodDescription': prop.get('neighborhoodDescription'),
                'latitude': prop.get('address', {}).get('latitude'),
                'longitude': prop.get('address', {}).get('longitude'),
                'belongedCity': prop.get('address', {}).get('belongedCity'),
                'currencyCode': prop.get('currencyCode')
            } 
            for prop in self.data
        ])
        self.address_df = self.address_df.drop_duplicates(subset='propertyId')

    def make_image_df(self):
        self.image_df = pd.DataFrame([
            {
                'id': prop.get('id'),
                'url': img.get('url'),
                'tag': img.get('tag')
            }
            for prop in self.data for img in prop.get('images', [])
        ])
        self.image_df = self.image_df.drop_duplicates(subset=['id', 'url'])
            
    def make_fee_df(self):
        self.fee_df = pd.DataFrame([
            {
                'id': prop.get('id'),
                'name': fee.get('name'),
                'description': fee.get('description'),
                'amount': fee.get('amount'),
                'isMandatory': fee.get('isMandatory'),
                'isRefundable': fee.get('isRefundable')
            } 
            for prop in self.data for fee in prop.get('fees', [])
        ])
        self.fee_df = self.fee_df.drop_duplicates(subset=['id', 'name'])

    def make_monthly_price_df(self):
        self.monthly_price_df = pd.DataFrame([
            {
                'id': prop.get('id'),
                'name': month.get('name'),
                'months': month.get('months'),
                'amount': month.get('amount'),
                'concessionsApplied': month.get('concessionsApplied')
            } 
            for prop in self.data for month in prop.get('pricing', {}).get('monthlyPricing', [])
        ])
        self.monthly_price_df = self.monthly_price_df.drop_duplicates(subset=['id', 'name'])

    def output_to_csv(self):
        dataframes = {
            'sellable_unit_df': getattr(self, 'sellable_unit_df', None),
            'address_df': getattr(self, 'address_df', None),
            'image_df': getattr(self, 'image_df', None),
            'fee_df': getattr(self, 'fee_df', None),
            'monthly_price_df': getattr(self, 'monthly_price_df', None)
        }
        
        if not os.path.exists('output'):
            os.makedirs('output')

        for name, df in dataframes.items():
            if df is not None:
                df.to_csv(f'output/{name}.csv', index=False)
            else:
                print(f"{name} does not exist")

if __name__ == "__main__":
    url = "https://www.common.com/cmn-api/listings/common"
    parser = ParseAPI(url)
    parser.get_data()
    parser.make_sellable_unit_df()
    parser.make_address_df()
    parser.make_image_df()
    parser.make_fee_df()
    parser.make_monthly_price_df()
    parser.output_to_csv()

