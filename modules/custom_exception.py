#!/usr/bin/env python
# coding: utf-8

class InvalidUrl(Exception):
    def __init__(self, MESSAGE='Your URL is not valid'):
        self.message = MESSAGE
        super().__init__(self.message)
        
class FailedToFetch(Exception):
    def __init__(self, MESSAGE='Could not fetch data from your url'):
        self.message = MESSAGE
        super().__init__(self.message)
        
class FileNotFound(Exception):
    def __init__(self, FILE='file', MESSAGE='unable to be found'):
        self.file = FILE
        self.message = MESSAGE
        super().__init__(self.file + ' ' + self.message)
        
class EmptyList(Exception):
    def __init__(self, LIST='List', MESSAGE='is empty'):
        self.list = LIST
        self.message = MESSAGE
        super().__init__(self.list + ' ' + self.message)
