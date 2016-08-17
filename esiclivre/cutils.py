#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals  # unicode by default
import json

from flask.ext.restplus import Api


def paginate(query, page, per_page_num):
    '''Paginate a query, returning also the total before pagination.'''
    total = query.count()
    return (query.offset(page*per_page_num).limit(per_page_num).all(), total)


class ExtraApi(Api):

    def __init__(self, *args, **kwargs):
        super(ExtraApi, self).__init__(*args, **kwargs)
        self.parser_arguments = {
            'token': {
                'location': 'json',
                'help': 'The authentication token.',
            },
            'page': {
                'type': int,
                'default': 0,
                'help': 'Page doc!!',
            },
            'per_page_num': {
                'type': int,
                'default': 20,
                'help': 'PPN doc!!',
            },
        }
        self.update_general_parser()

    def update_general_parser(self):
        '''Create a new general parser with current parser_arguments.'''
        self.general_parser = self.create_parser(*self.parser_arguments)

    def update_parser_arguments(self, arguments):
        '''Updates the parser_arguments and recreates the general_parser.'''
        self.parser_arguments.update(arguments)
        self.update_general_parser()

    def create_parser(self, *args):
        '''Create a parser for the passed arguments.'''
        parser = self.parser()
        for arg in args:
            parser.add_argument(arg, **self.parser_arguments[arg])
        return parser

    def general_parse(self):
        '''Parse arguments using any arguments from parser_argumentsar.'''
        return self.general_parser.parse_args()

    def abort_with_msg(self, error_code, msg, fields):
        '''Aborts sending information about the error.'''
        self.abort(error_code, json.dumps({
            'message': msg,
            'fields': fields
        }))
