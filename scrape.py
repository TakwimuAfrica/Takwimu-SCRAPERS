from scrapers.worldbank_scrapper import *
from scrapers.config import openAFRICA_API_KEY, openAFRICA_URL, INDICATORS

if __name__ == '__main__':

    for i in INDICATORS.values():
        get_indicator_data(indicator=i)

    ckan = ckanapi.RemoteCKAN(openAFRICA_URL, apikey=openAFRICA_API_KEY)

    upload_datasets_to_ckan(ckan, package_name='World Bank Indicators',
                            package_title='World Bank Indicators')

