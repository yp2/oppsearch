#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import urllib2

__author__ = 'daniel'

class Load(object):
    def __init__(self, f_rap):
        self.s_pattern = re.compile(r'.*(\d{8}).*(OPP-1|PIT-37|PIT-36|PIT36L|PIT-28).*(\d{4})\s+\w{1}\s+\d+\s+(\d{3}-\d{3}-\d{2}-\d{2}|P.\d{11}).*')
        self.opp = None
        self.pit = None
        self.f_rap = f_rap

    def run(self):
        self.opp, self.pit = self.__get_data(self.f_rap)

    def __get_data(self, file):
        """
        Function parse raport file in to separate list: with opp entries and pit
        entries. Eache entry in each list is a dictionary contaning: id, kod,
        rok, ident.
        :param file: opened input file
        :return: opp_list, pit_list
        """
        data_opp = []
        data_pit = []
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
                if data_ele.get('kod') == 'OPP-1':
                    data_opp.append(data_ele)
                else:
                    data_pit.append(data_ele)


        return data_opp, data_pit


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
            print "OppSearch\n"
            print "Nr\tKod\t\tNr dok\t\tIdentfikator\tRok"
            print 80*'-'
            x = 1
            for doc in self.search_result:
                print "%d.\t%s\t%s\t%s\t%s" % \
                (x, doc['kod'], doc['id'], doc['ident'], doc['rok'])
                x +=1
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

    try:
        fr = open('/home/daniel/git/python/oppsearch/rapviewall.htm', 'r')
    except IOError:
        print "Poda URL raportu:"
        url = raw_input(">>>> ")
        # print url
        req = urllib2.Request(url, None, {'User-agent': 'Mozilla/5.0'})
        page = urllib2.urlopen(req).read()
        fr = page.split('\n')

    loader = Load(fr)
    loader.run()
    search = SearchDoc(loader)
    search.run()