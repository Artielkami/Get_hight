# -*- coding: utf-8 -*-
from area import Geojp
from .models import Path
import requests

# Done this one


class Main(object):
    """testing"""
    _lst = {}
    # for row in sheet1.iter_rows():
    #     if row[5].value == 1:
    #         if row[1].value in _lst:
    #             _lst[row[1].value].append(row[2].value)
    #         else:
    #             _lst[row[1].value] = [row[2].value]

    # Global variable for mapping
    _map = Geojp()

    def make_lst(self):
        self._lst = {}
        tmp = Path.objects.filter(direct_flag=True)
        for item in tmp:
            if item.departure_port in self._lst:
                self._lst[item.departure_port].append(item.destination_port)
            else:
                self._lst[item.departure_port] = [item.destination_port]

    @staticmethod
    def texty(dep, des):
        tmp = Path.objects.filter(departure_port=dep).filter(direct_flag=True)
        # rs = Path.objects.filter(destination_port__in=tmp.values_list(self.))
        lst = []
        append_list = lst.append
        for item in tmp:
            q = Path.objects.filter(destination_port=des, departure_port=item.destination_port, direct_flag=True)
            if q:
                append_list(q[0].departure_port)

        return lst

    @staticmethod
    def getprice(departure, arrival, day='20160620'):
        """Get the lowest cost of treval between 2 port"""
        url = 'http://10.10.20.132/best_price/tabicapi_api'
        dp = departure
        ar = arrival
        dp_time = day
        info = {'departure_port': dp, 'arrival_port': ar, 'departure_date': dp_time}
        r = ''
        try:
            r = requests.get(url, params=info)
        except requests.exceptions.ConnectionError:
            print 'Quỳ, ca này khó, bác sĩ bó tay !'
        else:
            while r.status_code != 200:
                r = requests.get(url, params=info)
        try:
            k = r.json()['f_price']
        except KeyError:
            return 666666
        else:
            return k

    def get_total_price(self, dep1, arr1, mid):
        """Get price for all travel path"""
        f1 = self.getprice(departure=dep1, arrival=mid)
        f2 = self.getprice(departure=mid, arrival=arr1)
        if f1 and f2:
            return f1 + f2
        else:
            return 0

    @staticmethod
    def get_key(lst):
        if len(lst) <= 3:
            rs = [item[1] for item in lst]
        else:
            rs = [lst[i][1] for i in xrange(0, 3)]
        return rs

    def sort_and_filter(self, start, end, listitem):
        rs = []
        for item in listitem:
            k = self.get_total_price(dep1=start, arr1=end, mid=item)
            if k:
                rs.append([k, item])
        rs.sort(key=lambda x: x[0])
        return self.get_key(rs)

    def get_way(self, depart, desti, dictaw, cdt=0):
        """Function for calculate continous airport"""
        out = []  # mảng chứ giá trị kết quả
        con = []  # mảng tạm chứa giá trị trung chuyển
        if cdt:
            con = dictaw
        else:
            if depart in dictaw:
                con = dictaw[depart]
        des_area, des_id = self._map.get_area(desti)
        dep_area, dep_id = self._map.get_area(depart)
        if dep_id < des_id:
            for item in con:
                if dep_id <= self._map.get_area_id(item) <= des_id:
                    out.append(item)
                else:
                    pass
        elif dep_id > des_id:
            for item in con:
                if dep_id >= self._map.get_area_id(item) >= des_id:
                    out.append(item)
                else:
                    pass
        else:
            for item in con:
                if (des_id - 1) <= self._map.get_area_id(item) <= (des_id + 1):
                    out.append(item)
                else:
                    pass
        return out

    def get_way_by_dict(self, depart, desti, dictaw):
        """Function for calculate continous airport"""
        out = []  # mảng chứ giá trị kết quả
        con = []  # mảng tạm chứa giá trị trung chuyển
        if depart in dictaw:
            con = dictaw[depart]
        des_area, des_id = self._map.get_area(desti)
        dep_area, dep_id = self._map.get_area(depart)
        if dep_id < des_id:
            for item in con:
                if (dep_id <= self._map.get_area_id(item) <= des_id) and (desti in dictaw[item]):
                    out.append(item)

        elif dep_id > des_id:
            for item in con:
                if (dep_id >= self._map.get_area_id(item) >= des_id) and (desti in dictaw[item]):
                    out.append(item)
                else:
                    pass
        else:
            for item in con:
                if ((des_id - 1) <= self._map.get_area_id(item) <= (des_id + 1)) and (desti in dictaw[item]):
                    out.append(item)
                else:
                    pass
        return out

    def get_flight(self, dep, des):
        lst = self.texty(dep, des)
        print 'lst', lst
        if not lst:
            return None
        mlst = self.get_way(dep, des, lst, 1)
        # print 'mlst', mlst
        flst = self.sort_and_filter(dep, des, mlst)
        # print 'flst', flst
        connecting_route = Path.objects.get_connecting_route(des, dep)
        rs = Path.objects.get(pk=connecting_route.id)
        rs.new_top = ','.join(flst)
        # print rs.new_top
        rs.save()
        return rs.id

    def get_fly_by_dict(self, dep, des):
        connecting_route = Path.objects.get_connecting_route(des, dep)
        if connecting_route:
            mlst = self.get_way_by_dict(dep, des, self._lst)
            # print 'mlst', mlst
            flst = self.sort_and_filter(dep, des, mlst)
            # print 'flst', flst
            rs = Path.objects.get(pk=connecting_route.id)
            rs.new_top = ','.join(flst)
            # print rs.new_top
            rs.save()

    def update_all(self):
        self.make_lst()
        q = Path.objects.all()
        for obj in q:
            self.get_fly_by_dict(obj.departure_port, obj.destination_port)

    # new function after 22/05/2016
    @staticmethod
    def update_a_record(rid):
        q = Path.objects.get(pk=rid)
        tmp = q.old_stop
        q.old_stop = q.new_top
        q.new_top = tmp
        q.save()
        return True

    @staticmethod
    def search(dep, arr):
        note = Path.objects.get(departure_port=dep, destination_port=arr)
        if note:
            return note.id
        else:
            return None
