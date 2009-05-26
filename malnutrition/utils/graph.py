# this module contains methods that output
# data that is suitable for graphs
# without Django having a group by query its pretty 
# hard to get these things fast
# 
# this module has SQLITE SPECIFIC code that
# is very much tied to the modules to produce graphs for
# - number of messages
# - percentage by status
# - percentage by observation
# - average height/weight/muac over time
# 
# each assumes to be taking that statistic per month

from django.views.decorators.cache import cache_page
from django.db import connection
from django.core.cache import cache
from malnutrition.ui.views.graph import render

from datetime import datetime, timedelta
import time

class Data:
    pass

class Graphs:
    def __init__(self, classes=None, sql_setup=None, zones=None, zones_unfiltered=None, root=None, facilities=None, limit=None, length=365):
        """ Classes must be a dictionary of the key classes, so that we can find their tables in the graphing
            SQL so that if you have renamed them etc we can still find them. """
        assert "ReportMalnutrition" in classes.keys()
        self.classes = classes
        self.sql_setup = sql_setup
        self.zones = zones
        self.root = root
        self.limit = limit
        self.facilities = facilities
        self.length = length
        self.zones_unfiltered = zones_unfiltered

    def timeformat(self, tme):
        return time.mktime(datetime.strptime("%s/01" % tme, "%Y/%m/%d").timetuple()) * 1000
        
    def count(self, limit, *args):
        """ Just a simple count of all the reports per month """
        if not limit:
            limit = ""
        
        sql = "SELECT count(1) as count, strftime('%(sqlmonth)s', entered_at) as yearmonth  "\
            "FROM %(table)s "\
            "INNER JOIN %(case_table)s ON (%(case_table)s.id = %(table)s.case_id) "\
            "WHERE entered_at > %(length)s %(limit)s "\
            "GROUP BY yearmonth ORDER BY yearmonth;"
        # there are multiple levels of % in this, so this gets around that problem
        data = { "table": self.classes["ReportMalnutrition"]._meta.db_table, 
                 "case_table": self.classes["Case"]._meta.db_table,
                 "sqlmonth": "%%Y/%%m",
                 "limit": limit,
                 "length":  (datetime.now() - timedelta(days=self.length)).date() }


        cursor = connection.cursor()
        cursor.execute(sql % data)
        rows = cursor.fetchall()

        # convert into a datetime, then into time (sec) then * 1000 (flot uses miliseconds)
        res = [ [ self.timeformat(r[1]), r[0]  ] for r in rows ]
        return res

    def average(self, limit, *args):
        """ An average of one particular element """
        if not limit:
            limit = ""

        assert len(args) == 1 # has to be an column in there

        sql = "SELECT avg(%(column)s) as average, strftime('%(sqlmonth)s', entered_at) as yearmonth  "\
            "FROM %(table)s "\
            "INNER JOIN %(case_table)s ON (%(case_table)s.id = %(table)s.case_id) "\
            "WHERE entered_at > %(length)s %(limit)s "\
            "GROUP BY yearmonth ORDER BY yearmonth;"
            
        # there are multiple levels of % in this, so this gets around that problem
        data = { "table": self.classes["ReportMalnutrition"]._meta.db_table, 
                 "case_table": self.classes["Case"]._meta.db_table,
                 "sqlmonth": "%%Y/%%m",
                 "limit": limit,
                 "column": args[0],
                 "length":  (datetime.now() - timedelta(days=self.length)).date() }

        cursor = connection.cursor()
        cursor.execute(sql % data)
        rows = cursor.fetchall()
        # convert into a datetime, then into time (sec) then * 1000 (flot uses miliseconds)
        res = [ [ self.timeformat(r[1]), r[0]  ] for r in rows ]
        return res

    def percentage_status(self, limit, *statuses):
        # so limit can be anything eg 0, None
        if not limit:
            limit = ""
        cached = cache.get("percentage_status_by_zone: %s, %s" % (self.limit, statuses))
        if cached:
            # this can be cached
            res = cached
        else:
            sql = "SELECT count(1) as count, strftime('%(sqlmonth)s', entered_at) as yearmonth, status  "\
                "FROM %(table)s "\
                "INNER JOIN %(case_table)s ON (%(case_table)s.id = %(table)s.case_id) "\
                "WHERE entered_at > %(length)s %(limit)s "\
                "GROUP BY yearmonth, status ORDER BY yearmonth;"
            # there are multiple levels of % in this, so this gets around that problem
            data = { "table": self.classes["ReportMalnutrition"]._meta.db_table, 
                     "case_table": self.classes["Case"]._meta.db_table,
                     "sqlmonth": "%%Y/%%m",
                     "limit": limit,
                     "length":  (datetime.now() - timedelta(days=self.length)).date() }

            print sql % data
            cursor = connection.cursor()
            cursor.execute(sql % data)
            rows = cursor.fetchall()

            res = {}
            for r in rows:
                # convert into a datetime, then into time (sec) then * 1000 (flot uses miliseconds)
                tme = self.timeformat(r[1])
                if not res.has_key(tme):
                    res[tme] = {"total":0, "1":0, "2":0, "3":0, "4":0}
                res[tme]["total"] += int(r[0])
                if r[2]:
                    res[tme][str(r[2])] += int(r[0])
    
            cache.set("percentage_status_by_zone: %s, %s" % (self.limit, statuses), res, 60)

        # this bit should not be cached    
        nres = []
        keys = res.keys()
        keys.sort()
        for key in keys:
            count = 0

            for status in statuses:
                count += res[key][str(status)]

            percentage = (count / float(res[key]["total"])) * 100
            nres.append([ key, percentage ])
    
        return nres
        
    def percentage_stunting(self, limit, *args):
        # so limit can be anything eg 0, None
        if not limit:
            limit = ""

        cached = cache.get("percentage_stunting_by_zone: %s" % limit)
        if cached:
            # this can be cached
            res = cached
        else:
            sql = "SELECT count(1) as count, strftime('%(sqlmonth)s', entered_at) as yearmonth, stunted  "\
                "FROM %(table)s "\
                "INNER JOIN %(case_table)s ON (%(case_table)s.id = %(table)s.case_id) "\
                "WHERE entered_at > %(length)s %(limit)s "\
                "GROUP BY yearmonth, stunted ORDER BY yearmonth;"

            # there are multiple levels of % in this, so this gets around that problem
            data = { "table": self.classes["ReportMalnutrition"]._meta.db_table, 
                     "case_table": self.classes["Case"]._meta.db_table,
                     "sqlmonth": "%%Y/%%m",
                     "limit": limit,
                     "length":  (datetime.now() - timedelta(days=self.length)).date() }

            cursor = connection.cursor()
            cursor.execute(sql % data)
            rows = cursor.fetchall()

            res = {}
            for r in rows:
                # convert into a datetime, then into time (sec) then * 1000 (flot uses miliseconds)
                tme = self.timeformat(r[1])
                if not res.has_key(tme):
                    res[tme] = {"total":0, "stunted": 0}
                res[tme]["total"] += int(r[0])
                if r[2]:
                    res[tme]["stunted"] += int(r[0])
            
            cache.set("percentage_stunted_by_zone: %s" % limit, res, 60)

        # this bit should not be cached    
        nres = []
        keys = res.keys()
        keys.sort()
        for key in keys:
            percentage = (res[key]["stunted"] / float(res[key]["total"])) * 100
            nres.append([ key, percentage ])

        return nres

    def percentage_observation(self, limit, *args):
        # so limit can be anything eg 0, None
        if not limit:
            limit = ""

        cached = cache.get("percentage_observation_by_zone: %s and %s" % (limit, args))
        if cached:
            # this can be cached
            res = cached
        else:
            data = { 
                 "table": self.classes["ReportMalnutrition"]._meta.db_table, 
                 "observed_table": "%s_observed" % self.classes["ReportMalnutrition"]._meta.db_table,
                 "case_table": self.classes["Case"]._meta.db_table,
                 "sqlmonth": "%%Y/%%m",
                 "limit": limit,
                 "length":  (datetime.now() - timedelta(days=self.length)).date(),
                 "observed": args[0] }
             
            observed_sql = "SELECT count(1) as count, strftime('%(sqlmonth)s', entered_at) as yearmonth "\
                "FROM %(table)s "\
                "INNER JOIN %(observed_table)s ON (%(table)s.id = %(observed_table)s.reportmalnutrition_id) "\
                "INNER JOIN %(case_table)s ON (%(case_table)s.id = %(table)s.case_id) "\
                "WHERE entered_at > %(length)s %(limit)s "\
                "AND %(observed_table)s.observation_id = %(observed)s "\
                "GROUP BY yearmonth ORDER BY yearmonth;"
            
            cursor = connection.cursor()
            cursor.execute(observed_sql % data)
            observed_rows = cursor.fetchall()

            overall_sql = "SELECT count(1) as count, strftime('%(sqlmonth)s', entered_at) as yearmonth "\
                "FROM %(table)s "\
                "INNER JOIN %(case_table)s ON (%(case_table)s.id = %(table)s.case_id) "\
                "WHERE entered_at > %(length)s %(limit)s "\
                "GROUP BY yearmonth ORDER BY yearmonth;"

            cursor = connection.cursor()
            cursor.execute(overall_sql % data)
            overall_rows = cursor.fetchall()

            res = {}
            for r in overall_rows:
                # convert into a datetime, then into time (sec) then * 1000 (flot uses miliseconds)
                tme = self.timeformat(r[1])
                res[tme] = {"total": int(r[0]), "count": 0 }

            for r in observed_rows:
                # convert into a datetime, then into time (sec) then * 1000 (flot uses miliseconds)
                tme = self.timeformat(r[1])
                res[tme]["count"] = int(r[0])

            cache.set("percentage_observation_by_zone: %s and %s" % (limit, args), res, 60)

        # this bit should not be cached    
        nres = []
        keys = res.keys()
        keys.sort()
        for key in keys:
            percentage = (res[key]["count"] / float(res[key]["total"])) * 100
            nres.append([ key, percentage ])

        return nres
        
    def render(self, name, type, args=[]):
        """ Convenience method that produces output """
        sql = self.sql_setup(self)

        for line in sql:
            line["data"] = type(line["limit"], *args)

        result = Data()
        result.javascript = render(name, sql)
        result.data = sql
        result.name = name
        return result