#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import urllib2

__author__ = 'daniel'


class Load(object):
    def __init__(self, f_opp, f_pit):
        self.s_pattern = re.compile(r'.*(\d{8}).*(OPP-1|PIT-37|PIT-36|PIT36L|PIT-28).*(\d{4})\s+\w{1}\s+\d+\s+(\d{3}-\d{3}-\d{2}-\d{2}|P.\d{11}).*')
        self.opp = None
        self.pit = None
        self.f_opp = f_opp
        self.f_pit = f_pit

    def run(self):
        self.opp = self.__get_data(self.f_opp)
        self.pit = self.__get_data(self.f_pit)

    def __get_data(self, file):
        data = []
        try:
            lines = file.readlines()
        except AttributeError:
            lines = file

        for line in lines:
            result = self.s_pattern.search(line)
            if result:
                result = result.groups()
                data_ele = {'id': result[0],
                       'kod': result[1],
                       'rok': result[2],
                       'ident': result[3]
                }
                data.append(data_ele)

        return data


class SearchDoc(object):
    def __init__(self, loader):
        self.loader = loader
        self.search_result = []
        self.opp = self.loader.opp
        self.pit = self.loader.pit

    def run(self):
        # print len(self.opp)
        # print len(self.pit)

        if len(self.opp) > len(self.pit):
            # mamy więcej opp szukamy opp który nie ma pit'a
            self.__search_opp()
        else:
            self.__search_pit()

        self.__show()


    def __show(self):
        if self.search_result:
            print "Szukane dokumenty to:"
            for doc in self.search_result:
                print 80*'-'
                print "Kod: %s\nNr dokumentu: %s\nIdnetyfikator: %s\nRok: %s" % \
                      (doc['kod'], doc['id'], doc['ident'], doc['rok'])
                print 80*'-'
        else:
            print 'Nie znaleziono dokumentów....'


    def __search_opp(self):
        for opp in self.opp:
            hit = False
            for pit in self.pit:
                if opp['ident'] == pit['ident']:
                    hit = True
                    break

            if hit is False:
                self.search_result.append(opp)

    def __search_pit(self):
        for pit in self.pit:
            hit = False
            for opp in self.opp:
                if opp['ident'] == pit['ident']:
                    hit = True
                    break

            if hit is False:
                self.search_result.append(pit)


if __name__ == "__main__":

    arg = sys.argv[1:]
    if len(arg) == 2:
        # fo = urllib2.Request(arg[0])
        req = urllib2.Request(arg[0], None, {'User-agent': 'Mozilla/5.0'})
        page = urllib2.urlopen(req).read()
        fo = page.split('\n')
        req = urllib2.Request(arg[1], None, {'User-agent': 'Mozilla/5.0'})
        page = urllib2.urlopen(req).read()
        fp = page.split('\n')
    else:
        # pliki
        fo = open('', 'r')
        fp = open('', 'r')

    loader = Load(fo, fp)
    loader.run()
    search = SearchDoc(loader)
    search.run()