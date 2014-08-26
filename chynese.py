#!/usr/bin/env python
# encoding: utf-8


# TODO: documentation
# description


# imports
import json
from urllib2 import unquote


# functions
def load_data(file_name='data.json'):
    # TODO: documentation
    '''
    '''

    data_file = open(file_name).read()
    data = json.loads(data_file)

    return data


def main():
    # TODO: documentation
    '''
    '''

    data = load_data()

    # encode the character to be displayed
    bytesquoted = data['characters'][0]['character'].encode('utf8')
    unquoted = unquote(bytesquoted)
    print unquoted.decode('utf8')


# run the main function
if __name__ == '__main__':
    main()
