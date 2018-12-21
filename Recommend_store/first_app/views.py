# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys

import unicodedata
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render
from models import Customer, Store, NumericUserSearch, StoreProduct, AllShoppingFromTaleqaniToFatemi
from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from django.http import HttpResponse
import numpy as np
import pandas as pd
from scipy.spatial import distance
from urllib2 import Request as url_request
from urllib2 import urlopen
import json
import math
import time
from operator import itemgetter
import re



reload(sys)
sys.setdefaultencoding('utf-8')

# Create your views here.





class AboutView(TemplateView):
    template_name = 'about.html'


class BaseView(TemplateView):
    template_name = 'base.html'


def distance_geographic_between_store_and_user(get_store_coordinates, user_coordinate, start_id_store_id_with_first_category, end_id_store_id_with_first_category):
    headers = {
        'Accept': 'application/json; charset=utf-8'
    }

    str_url = str()
    user_coordinates = user_coordinate
    for i in range(start_id_store_id_with_first_category, end_id_store_id_with_first_category):
        long = str(get_store_coordinates[i][1])
        comma = ','
        lat = str(get_store_coordinates[i][2])
        append_sign_each_point = '%7C'
        str_url += long + comma + lat + append_sign_each_point
    request_distance = url_request('https://api.openrouteservice.org/matrix?api_key=5b3ce3597851110001cf624855704328a35746098c6f6f287a22cd66&profile=driving-car&locations='
                                   + user_coordinates + '%7C' + str_url + '&metrics=distance', headers=headers)
    response_body = json.loads(urlopen(request_distance).read())
    distance_result_with_0 = list(response_body['distances'][0])
    distance_result_remove_dist_between_user_and_user = distance_result_with_0[1:]
    return distance_result_remove_dist_between_user_and_user


def calculate_distance_between_store_and_user_for_all_stores(get_store_coordinates, user_coordinates, store_id_with_first_category):
    get_store_coordinates = get_store_coordinates
    get_store_id_based_first_category = store_id_with_first_category
    if 0 < len(get_store_id_based_first_category) <= 40:
        dist_between_user_and_stores = distance_geographic_between_store_and_user(get_store_coordinates=get_store_coordinates, user_coordinate=user_coordinates,
                                                                                  start_id_store_id_with_first_category=0, end_id_store_id_with_first_category=len(get_store_id_based_first_category))

    if 40 < len(get_store_id_based_first_category) < 80:
        dist_between_user_and_stores_part_1 = distance_geographic_between_store_and_user(user_coordinate=user_coordinates, get_store_coordinates=get_store_coordinates,
                                                                                         start_id_store_id_with_first_category=0, end_id_store_id_with_first_category=40)
        dist_between_user_and_stores_part_2 = distance_geographic_between_store_and_user(user_coordinate=user_coordinates, get_store_coordinates=get_store_coordinates,
                                                                                         start_id_store_id_with_first_category=40, end_id_store_id_with_first_category=len(get_store_id_based_first_category))
        dist_between_user_and_stores = dist_between_user_and_stores_part_1 + \
            dist_between_user_and_stores_part_2

    if 80 < len(get_store_id_based_first_category) < 120:
        dist_between_user_and_stores_part_1 = distance_geographic_between_store_and_user(user_coordinate=user_coordinates, get_store_coordinates=get_store_coordinates,
                                                                                         start_id_store_id_with_first_category=0, end_id_store_id_with_first_category=40)
        dist_between_user_and_stores_part_2 = distance_geographic_between_store_and_user(user_coordinate=user_coordinates, get_store_coordinates=get_store_coordinates,
                                                                                         start_id_store_id_with_first_category=40, end_id_store_id_with_first_category=80)
        dist_between_user_and_stores_part_3 = distance_geographic_between_store_and_user(user_coordinate=user_coordinates, get_store_coordinates=get_store_coordinates,
                                                                                         start_id_store_id_with_first_category=80, end_id_store_id_with_first_category=len(get_store_id_based_first_category))
        dist_between_user_and_stores = dist_between_user_and_stores_part_1 + \
            dist_between_user_and_stores_part_2 + dist_between_user_and_stores_part_3

    if 120 < len(get_store_id_based_first_category) < 160:
        dist_between_user_and_stores_part_1 = distance_geographic_between_store_and_user(user_coordinate=user_coordinates, get_store_coordinates=get_store_coordinates,
                                                                                         start_id_store_id_with_first_category=0, end_id_store_id_with_first_category=40)
        dist_between_user_and_stores_part_2 = distance_geographic_between_store_and_user(user_coordinate=user_coordinates, get_store_coordinates=get_store_coordinates,
                                                                                         start_id_store_id_with_first_category=40, end_id_store_id_with_first_category=80)
        dist_between_user_and_stores_part_3 = distance_geographic_between_store_and_user(user_coordinate=user_coordinates, get_store_coordinates=get_store_coordinates,
                                                                                         start_id_store_id_with_first_category=80, end_id_store_id_with_first_category=120)
        dist_between_user_and_stores_part_4 = distance_geographic_between_store_and_user(user_coordinate=user_coordinates, get_store_coordinates=get_store_coordinates,
                                                                                         start_id_store_id_with_first_category=120, end_id_store_id_with_first_category=len(get_store_id_based_first_category))
        dist_between_user_and_stores = dist_between_user_and_stores_part_1 + dist_between_user_and_stores_part_2 + \
            dist_between_user_and_stores_part_3 + dist_between_user_and_stores_part_4

    if 160 < len(get_store_id_based_first_category) < 200:
        dist_between_user_and_stores_part_1 = distance_geographic_between_store_and_user(user_coordinate=user_coordinates, get_store_coordinates=get_store_coordinates,
                                                                                         start_id_store_id_with_first_category=0, end_id_store_id_with_first_category=40)
        dist_between_user_and_stores_part_2 = distance_geographic_between_store_and_user(user_coordinate=user_coordinates, get_store_coordinates=get_store_coordinates,
                                                                                         start_id_store_id_with_first_category=40, end_id_store_id_with_first_category=80)
        dist_between_user_and_stores_part_3 = distance_geographic_between_store_and_user(user_coordinate=user_coordinates, get_store_coordinates=get_store_coordinates,
                                                                                         start_id_store_id_with_first_category=80, end_id_store_id_with_first_category=120)
        dist_between_user_and_stores_part_4 = distance_geographic_between_store_and_user(user_coordinate=user_coordinates, get_store_coordinates=get_store_coordinates,
                                                                                         start_id_store_id_with_first_category=120, end_id_store_id_with_first_category=160)
        dist_between_user_and_stores_part_5 = distance_geographic_between_store_and_user(user_coordinate=user_coordinates, get_store_coordinates=get_store_coordinates,
                                                                                         start_id_store_id_with_first_category=160, end_id_store_id_with_first_category=len(get_store_id_based_first_category))
        dist_between_user_and_stores = dist_between_user_and_stores_part_1 + dist_between_user_and_stores_part_2 + \
            dist_between_user_and_stores_part_3 + \
            dist_between_user_and_stores_part_4 + dist_between_user_and_stores_part_5

    return dist_between_user_and_stores


def calcullate_euc_distance_between_user_store_based_first_category(first_category, first_category_size_based_second_category, normalize_user, get_store_id_based_first_category):
    create_first_category_zero_for_list = first_category_size_based_second_category
    df_0 = pd.DataFrame()
    for stores in get_store_id_based_first_category:
        lst_store_feaure = [0] * create_first_category_zero_for_list
        df_0.loc[stores[0], 0] = stores[0]
        for second_cat in range(1, (create_first_category_zero_for_list + 1)):

            count_second_category_type_for_each_store_based_first_category = StoreProduct.objects.filter(
                store_id=stores[0], first_category=first_category, second_category=second_cat).values_list('second_category').count()

            df_0.loc[stores[0], second_cat] = count_second_category_type_for_each_store_based_first_category

    df_store_id_and_euc_dist_user_store = pd.DataFrame(columns=['a', 'b'])
    for store_i, i in zip(get_store_id_based_first_category, range(0, len(get_store_id_based_first_category))):

        lst_store_feature = []
        df_store_id_and_euc_dist_user_store.loc[store_i[0], 'a'] = store_i[0]
        for j in range(1, (create_first_category_zero_for_list + 1)):
            lst_store_feature.append(df_0.iat[i, j])
        lst_norm = np.linalg.norm(lst_store_feature)
        normalize_store_feature = lst_store_feature / lst_norm

        euc_distance_user_and_store = distance.euclidean(
            normalize_store_feature, normalize_user)
        #
        euc_distance_user_and_store= (math.sqrt(create_first_category_zero_for_list))-(euc_distance_user_and_store)
        euc_distance_user_and_store = euc_distance_user_and_store/math.sqrt(create_first_category_zero_for_list)
        euc_distance_user_and_store = euc_distance_user_and_store*100
        euc_distance_user_and_store= round(euc_distance_user_and_store,ndigits=2)
        df_store_id_and_euc_dist_user_store.loc[store_i[0],
                                                'b'] = euc_distance_user_and_store
        sorted_dataframe = df_store_id_and_euc_dist_user_store.sort_values([
                                                                           'b'],ascending=False)
    df_list=list()
    df_tuple=tuple()
    for i , j in zip(sorted_dataframe.ix[:,'a'],sorted_dataframe.ix[:,'b']):
        df_list.append(i)
        df_list.append(j)
    it = iter(df_list)
    df_tuple = zip(it, it)
    # df_list = sorted_dataframe.ix[:, 'a']
    return df_tuple


def normalized_user_feature_space(first_category, user_id, create_first_category_zero_for_list, distinct_second_category_for_user_base_first_category):

    lst_user = [0] * create_first_category_zero_for_list
    for second_cat in distinct_second_category_for_user_base_first_category:
        count_each_second_category_for_each_first_category_based_user = NumericUserSearch.objects.filter(
            user_id=user_id, numeric_first_category=first_category, numeric_second_category=second_cat[0]).values_list('numeric_second_category').count()

        lst_user[second_cat[0] -
                 1] = count_each_second_category_for_each_first_category_based_user
    lst_norm_user = np.linalg.norm(lst_user)
    normalized_user = lst_user / lst_norm_user
    return normalized_user

longtitude=0

def lat_ajax(request):
        global longitude

        return HttpResponse(longitude)

@login_required
def qet_queryset(request, num):
    user_id = request.user.id
    first_category = int(num)

    longitude = request.GET.get('longitude')





    # this query: count second category for each first categroy finding feature space list size
    create_first_category_zero_for_list = NumericUserSearch.objects.filter(
        numeric_first_category=first_category).distinct('numeric_second_category').count()

    # this query: count second category that user search from these products' type
    distinct_second_category_for_user_base_first_category = list(NumericUserSearch.objects.filter(user_id=user_id, numeric_first_category=first_category).values_list(
        'numeric_second_category').distinct('numeric_second_category').order_by('numeric_second_category'))

    # this func: normalized user feature space for example: user_feature_space=[1,0,2,0] => all item between 0,1 => [0.2***,0,.5***,0]
    normalized_user = normalized_user_feature_space(first_category=first_category, user_id=user_id, create_first_category_zero_for_list=create_first_category_zero_for_list,
                                                    distinct_second_category_for_user_base_first_category=distinct_second_category_for_user_base_first_category)

    """
    create store feature space
    """
    # this query: extract stores id that they have this first category
    get_store_id_based_first_category = list(StoreProduct.objects.filter(
        first_category=first_category).distinct('store_id').values_list('store_id'))

    # this func: calculate euclidean distances between normalized user feature space and all noramlized store(with this first category) feature space
    df_list = calcullate_euc_distance_between_user_store_based_first_category(
        first_category=first_category, first_category_size_based_second_category=create_first_category_zero_for_list, normalize_user=normalized_user, get_store_id_based_first_category=get_store_id_based_first_category)

    shopping = AllShoppingFromTaleqaniToFatemi

    # this query: extract stores coordinates that stores have this first category type
    get_store_coordinates = shopping.objects.filter(
        first_category=num).values_list('gid', 'long', 'lat').order_by('gid')

    user_coordinates = "51.4042800000" + ',' + "35.7014014000"

    # this func: calculate distance( data has been extracted from open route services api (OSM)) between user long, lat and stores locations
    dist_between_user_and_stores = calculate_distance_between_store_and_user_for_all_stores(
        get_store_coordinates=get_store_coordinates, user_coordinates=user_coordinates, store_id_with_first_category=get_store_id_based_first_category)

    # this query:  extract store gid that ordered by gid( order for matching gid and distance)
    query_order_by_gid = list(shopping.objects.filter(
        first_category=first_category).values_list('gid').order_by('gid'))


    get_store_name_order_by_gid= shopping.objects.raw('SELECT  gid,name FROM public.all_shopping_from_taleqani_to__fatemi where first_category=%s order by gid;' %first_category)
    list_with_gid_and_dist=list()
    for i, j,k in zip(dist_between_user_and_stores, query_order_by_gid,get_store_coordinates):




        list_with_gid_and_dist.append(j[0])
        list_with_gid_and_dist.append(i)
        list_with_gid_and_dist.append(k[1])
        list_with_gid_and_dist.append(k[2])



    it = iter(list_with_gid_and_dist)
    tuple_with_gid_and_dist = zip(it, it,it,it)

    sort_geographic_distance = tuple(sorted(tuple_with_gid_and_dist, key=itemgetter(1)))
    store_code= [x[0] for x in sort_geographic_distance]
    store_distance=[x[1] for x in sort_geographic_distance]
    store_coordinates_longtitude=[x[2] for x in sort_geographic_distance]
    store_coordinates_latitude=[x[3] for x in sort_geographic_distance]
    store_code_and_distance = zip(store_code, store_distance)
    store_coordinates=zip(store_coordinates_latitude,store_coordinates_longtitude)
    return render(request, 'test.html', context={'store_code_distance':store_code_and_distance,'store_coordinates': store_coordinates,'similarity_dist':df_list})


# @login_required
# def get_queryset(request):
#     user_id = request.user.id
#     first=request.get_full_path()
#     dict_list={}
#     distinct_first_category_for_user = list(NumericUserSearch.objects.filter(user_id=user_id).values_list(
#         'numeric_first_category').distinct('numeric_first_category').order_by('numeric_first_category'))
#     for item in distinct_first_category_for_user:
    # first_category = int(item[0])
    # create_first_category_zero_for_list= NumericUserSearch.objects.filter(numeric_first_category=first_category).distinct('numeric_second_category').count()
    # distinct_second_category_for_user_base_first_category = list(NumericUserSearch.objects.filter(user_id=user_id, numeric_first_category=first_category).values_list(
    #     'numeric_second_category').distinct('numeric_second_category').order_by('numeric_second_category'))
    # lst = [0]*create_first_category_zero_for_list
    # for second_cat in distinct_second_category_for_user_base_first_category:
    #
    #     count_each_second_category_for_each_first_category_based_user= NumericUserSearch.objects.filter(user_id=user_id,numeric_first_category=first_category,numeric_second_category=second_cat[0]).values_list('numeric_second_category').count()
    #
    #     lst[second_cat[0]-1]= count_each_second_category_for_each_first_category_based_user
#
#
#
#         if first_category==1:
#             dict_list['cat_1']=lst
#         if first_category==2:
#             dict_list['cat_2']=lst
#         if first_category==3:
#             dict_list['cat_3']=lst
#         if first_category==4:
#             dict_list['cat_4']=lst
#         if first_category==5:
#             dict_list['cat_5']=lst
#         if first_category==6:
#             dict_list['cat_6']=lst
#         if first_category==7:
#             dict_list['cat_7']=lst
#         if first_category==8:
#             dict_list['cat_8']=lst
#         if first_category==9:
#             dict_list['cat_9']=lst
#         if first_category==10:
#             dict_list['cat_10']=lst
#         if first_category==11:
#             dict_list['cat_11']=lst
#         if first_category==12:
#             dict_list['cat_12']=lst
#     return render(request, 'test.html', context=dict_list)


def my_custom_sql(self):
    user_id = 2
    category_type = 2
    with connection.cursor() as cursor:
        cursor.execute("SELECT  numeric_second_category,count (numeric_second_category) FROM public.numeric_user_search where user_id=1 and numeric_first_category=12 group by numeric_second_category")

        row = cursor.fetchone()

    return row
