#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
World Bank:
----------

Gets data for each country on a specific indicator.

"""
import logging
import os

import ckanapi
import requests
import wbdata
import config
from ckanapi import NotAuthorized, CKANAPIError, ServerIncompatibleError
import csv

logger = logging.getLogger(__name__)


def get_indicator_data(indicator=None):

    indicator_data = wbdata.get_data(indicator=indicator,
                                     country=config.COUNTRIES)
    data = []
    indicator_name = ''
    for i in indicator_data:
        try:
            y = {'year': i.get('date'),
                 'country': i['country'].get('value'),
                 'indicator': i['indicator'].get('value'),
                 'value': i.get('value')}
            data.append(y)
        except AttributeError:
            pass

    file_name = data[0].get('indicator', indicator)
    file_name = file_name.replace(' ', '_') + '.csv'
    outputFile = open('scraped_data/' + file_name, 'w')
    output = csv.writer(outputFile)
    output.writerow(data[0].keys())
    for row in data:
        output.writerow(row.values())  # values row


def upload_datasets_to_ckan(ckan, package_name, package_title):
    try:
        print 'Creating "{package_title}" package'.format(**locals())
        package = ckan.action.package_create(name=package_name,
                                             title=package_title)
    except ckanapi.ValidationError, e:
        if (e.error_dict['__type'] == 'Validation Error' and
                    e.error_dict['name'] == ['That URL is already in use.']):
            print '"{package_title}" package already exists'.format(**locals())
            package = ckan.action.package_show(id=package_name)
        else:
            raise

    for filename in os.listdir('scraped_data'):
        path = os.path.join('scraped_data', filename)
        extension = os.path.splitext(filename)[1][1:].upper()
        resource_name = 'Example {extension} file'.format(extension=extension)
        print 'Creating "{resource_name}" resource'.format(**locals())
        r = requests.post(config.openAFRICA_URL + '/api/action/resource_create',
                          data={'package_id': package['id'],
                                'name': resource_name,
                                'format': extension,
                                'url': 'upload',  # Needed to pass validation
                                },
                          headers={'Authorization': config.openAFRICA_API_KEY},
                          files=[('upload', file(path))])

        if r.status_code != 200:
            print 'Error while creating resource: {0}'.format(r.content)
            break




