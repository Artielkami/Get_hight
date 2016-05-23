# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Path
from django.db.models import F
from main import Main
import django_excel as excel
import pyexcel_xlsx
from .forms import UploadForm, SearchWay


# Create your views here.

def new(request):
    # paths = Path.objects.exclude(old_stop__exact=F('new_top'))
    paths = Path.objects.all()
    paginator = Paginator(paths, 50)

    page = request.GET.get('page')
    try:
        path = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        path = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        path = paginator.page(paginator.num_pages)
    return render(request,
                  'show/index.html',
                  {
                      'new': True,
                      'list_arcana': path,
                      'text_header': 'Welcome to the International'
                  }
                  )


def update(request, rs_path_id):
    search_form = SearchWay()
    Main.update_a_record(rs_path_id)
    return render(request,
                  'show/index.html',
                  {
                      'form': search_form,
                      'text_header': u'Quá trình kiếm kiếm đã diễn ra thuận lợi',
                      'rs_path': Path.objects.get(pk=rs_path_id),
                      'text_4_test': u'Kết quả đã tìm được: '
                  }
                  )
    # return HttpResponseRedirect('/show')


def index(request):
    if request.method == 'POST':
        if 'search_all' in request.POST:
            sql = Main()
            # form = SearchWay(request.POST)
            sql.update_all()
            return HttpResponseRedirect('/show/new')
        elif 'search' in request.POST:
            search_form = SearchWay(request.POST)
            if search_form.is_valid():
                cleaned_data = search_form.cleaned_data
                sql = Main.search(dep=cleaned_data['departure'],
                                  arr=cleaned_data['destination'])
                request.session['is_search'] = True
                if sql:
                    request.session['search_result'] = sql
            else:
                request.session['is_false_search'] = True
            return HttpResponseRedirect('/show')
        else:
            sql = Main()
            search_way_form = SearchWay(request.POST,
                                        request.POST['departure'],
                                        request.POST['destination'])
            if search_way_form.is_valid():
                cleaned_data = search_way_form.cleaned_data
                rs = sql.get_flight(cleaned_data['departure'],
                                    cleaned_data['destination'])
                request.session['is_search'] = True
                if rs:
                    request.session['search_result'] = rs
            else:
                request.session['is_false_search'] = True
            return HttpResponseRedirect('/show')
    else:
        search_form = SearchWay()
        if request.session.get('search_result'):
            rs = request.session.get('search_result')
            del request.session['search_result']
            del request.session['is_search']
            return render(request,
                          'show/index.html',
                          {
                              'form': search_form,
                              'text_header': u'Quá trình kiếm kiếm đã diễn ra thuận lợi',
                              'rs_path': Path.objects.get(pk=rs),
                              'text_4_test': u'Kết quả đã tìm được: '
                          }
                          )
        elif request.session.get('is_search'):
            del request.session['is_search']
            return render(request,
                          'show/index.html',
                          {
                              'form': search_form,
                              'text_header': u'Quá trình kiếm kiếm đã diễn ra không thành công',
                              'rs_path': None,
                              'text_4_test': u'Không có kết quả cần tìm'
                          }
                          )
        elif request.session.get('is_false_search'):
            del request.session['is_false_search']
            return render(request,
                          'show/index.html',
                          {
                              'form': search_form,
                              'text_header': u'Quá trình kiếm kiếm có sự cố',
                              'rs_path': None,
                              'text_4_test': u'Có lỗi đã diễn ra'
                          }
                          )
        else:
            # form = SearchWay()
            paths = Path.objects.all()
            paginator = Paginator(paths, 50)

            page = request.GET.get('page')
            try:
                path = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                path = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                path = paginator.page(paginator.num_pages)
            return render(request,
                          'show/index.html',
                          {
                              'form': search_form,
                              'list_arcana': path,
                              'text_header': 'Welcome to the International'
                          }
                          )


def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            filehandle = request.FILES['file']
            # paginator = Paginator(filehandle..get_records(), 30)
            # text_2_render = u'Đã xử lý xong'
            filehandle.save_to_database(
                model=Path,
                mapdict=['departure_port',
                         'destination_port',
                         'search_flag',
                         'transfer_flag',
                         'direct_flag',
                         'lcc_flag',
                         'old_stop', ]
            )
            return HttpResponseRedirect('/show')
        else:
            form2 = UploadForm()
            text_2_render1 = 'sai sai sai sai sai'
            return render_to_response(
                'show/import.html',
                {
                    'form': form2,
                    'text_header': text_2_render1
                },
                context_instance=RequestContext(request)
            )
    else:
        form = UploadForm()
        # template = loader.get_template('show/import.html')
        return render(request,
                      'show/import.html',
                      {
                          'form': form,
                          'text_header': 'All hail EE-sama, chọn file excel.xlsx để nạp dữ liệu '
                                         'vào database'
                      },
                      context_instance=RequestContext(request)
                      )
