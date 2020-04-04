import json
import logging
from collections import defaultdict
from os.path import join

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Experiment, DataFolder, RawData
from .plotting import plot_pxmy_to_bytes, plot_pxmy_and_neighbours, plot_pxmy_without_neighbours

logger = logging.getLogger(__name__)
# rows_in_exp = Experiment.objects.using('retina').all()
# rows_in_data = DataFolder.objects.using('retina').all()
datadict = defaultdict(list)


# for row in rows_in_data:
#     datadict[row.exp.pk].append(row.dataxxx)

@api_view(['POST'])
def SendDataOutside(local_trace):
    print(" local to: ", local_trace)
    print("typ to: ", type(local_trace))
    test_response = [{"long": "19.944", "lat": "50.047"}, {"long": "19.946", "lat": "50.044"},
            {"long": "19.941", "lat": "50.043"}]
    try:
        height = json.loads(local_trace.body)
        print(" local to: ", height)
        print("typ to: ", type(height))

        return JsonResponse(test_response, safe=False)
    except ValueError as e:
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)


@login_required
def home(request, pk=None):
    # if pk:
    #     exp = Experiment.objects.using('retina').get(pk=pk)
    #
    # expname = [row.experimentname.split('/')[-1] for row in rows_in_exp]
    # expdict = {Experiment.objects.using('retina')[0]: 'exp_with_pk'}
    # expdict.update({Experiment.objects.using('retina')[1]: 'exp_with_pk'})
    # expdict.update({Experiment.objects.using('retina')[2]: 'exp_with_pk'})
    with open(r'C:\HackYEAH_2020\HackYEAH-2020-COVID19\db.json', 'r') as file:
        parsed_json = json.load(file)

    return render(request, 'retina/home_button.html', {'json': parsed_json})


def about(request):
    return render(request, 'retina/about.html', {'title': 'about'})


@login_required
def create_exp_view(request, pk):
    return render(request, 'retina/rawdata_form.html', {'pk': pk})


@login_required
def load_px_my(request):
    data_id = request.GET.get('data_id')
    if data_id is not None and data_id.isdigit():
        pxmy = RawData.objects.using('retina').filter(data_id=data_id).all()
        print('jestem w load_px_my', pxmy)
        return render(request, 'retina/pxmy_dropdown_list_options.html', {'pxmy': pxmy})
    else:
        return HttpResponse('')


@login_required
def load_pattern_number(request):
    data_id = request.GET.get('data_id')
    if data_id is not None and data_id.isdigit():
        pat_num = RawData.objects.using('retina').filter(data_id=data_id).values_list('pattern_number',
                                                                                      flat=True).order_by(
            'pattern_number')
        pat_num = set(pat_num)
        return render(request, 'retina/pattern_number_dropdown_list_options.html', {'pat_num': pat_num})
    else:
        return HttpResponse('')


@login_required
def load_dataxxx(request):
    exp_id = request.GET.get('exp_id')
    dataxxx = DataFolder.objects.using('retina').filter(exp_id=exp_id).all()
    return render(request, 'retina/dataxxx_dropdown_list_options.html', {'dataxxx': dataxxx})


@login_required
def load_pattern_file(request):
    pxmy_id = request.GET.get('pxmy_id')
    pattern = RawData.objects.using('retina').get(id=pxmy_id).pattern_file
    return HttpResponse(pattern)


@login_required
def movie_numbers(request):
    data_id = request.GET.get('data_id')
    if data_id is not None and data_id.isdigit():
        movies = RawData.objects.using('retina').filter(data_id=data_id).values_list('movie_number',
                                                                                     flat=True).distinct().order_by(
            'movie_number')
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n\n')
        print(movies)
        return render(request, 'retina/movies_dropdown_list_options.html', {'movies': movies})
    else:
        return HttpResponse('')


@login_required
def movie_for_pattern(request):
    pattern_number = request.GET.get('pat_num')
    data_id = request.GET.get('data_id')
    if pattern_number is not None and pattern_number.isdigit():
        movies = RawData.objects.using('retina').filter(pattern_number=pattern_number, data_id=data_id).values_list(
            'movie_number',
            flat=True).distinct().order_by(
            'movie_number')
        return render(request, 'retina/movies_dropdown_list_options.html', {'movies': movies})
    else:
        return HttpResponse('')


@login_required
def get_plot(request):
    response = HttpResponse(content_type='application/png')
    response['Content-Disposition'] = 'attachment; filename="plot.png"'

    electrode_from = int(request.GET.get('electrode_from'))
    electrode_to = int(request.GET.get('electrode_to'))
    movie_number = request.GET.get('movie_number')
    rawdata_id = request.GET.get('rawdata_id')
    data_id = request.GET.get('data_id')

    paths = []

    if movie_number is not None:
        rawdatas = RawData.objects.using('retina').filter(movie_number=int(movie_number), data_id=int(data_id)).all()
        logger.info(f'rawdatas={rawdatas}')
        print(movie_number)
        print(data_id)

        for rawdata in rawdatas:
            dataxxx = DataFolder.objects.using('retina').get(id=rawdata.data_id)
            experim = Experiment.objects.using('retina').get(id=dataxxx.exp_id)
            path = join(experim.experimentname, dataxxx.dataxxx, rawdata.px_my)
            paths.append(path)

    if rawdata_id is not None:
        rawdata = RawData.objects.using('retina').get(id=rawdata_id)
        dataxxx = DataFolder.objects.using('retina').get(id=rawdata.data_id)
        experim = Experiment.objects.using('retina').get(id=dataxxx.exp_id)
        path = join(experim.experimentname, dataxxx.dataxxx, rawdata.px_my)
        paths.append(path)

    print("\n\n\npaths= " + str(paths) + '\n\n\n')
    # TODO marge path via join()
    plot = plot_pxmy_to_bytes(paths, electrode_from, electrode_to)
    response.write(plot)
    return response


@login_required
def get_pattern_plot(request):
    response = HttpResponse(content_type='application/png')
    response['Content-Disposition'] = 'attachment; filename="plot.png"'

    pat_number = request.GET.get('pat_num')
    electrode_to_plot = int(request.GET.get('ele_to_plot'))
    movie_number = int(request.GET.get('movie_number'))
    data_id = request.GET.get('data_id')
    neighbours = request.GET.get('neighbours')

    if not request.GET.get('y_axis_min').strip():
        y_axis_min = None
    else:
        y_axis_min = int(request.GET.get('y_axis_min'))

    if not request.GET.get('y_axis_max').strip():
        y_axis_max = None
    else:
        y_axis_max = int(request.GET.get('y_axis_max'))

    if not request.GET.get('x_axis_min').strip():
        x_axis_min = None
    else:
        x_axis_min = int(request.GET.get('x_axis_min'))

    if not request.GET.get('x_axis_max').strip():
        x_axis_max = None
    else:
        x_axis_max = int(request.GET.get('x_axis_max'))

    selected_path = None

    rawdatas = RawData.objects.using('retina').filter(pattern_number=int(pat_number),
                                                      data_id=int(data_id)).all().order_by(
        'movie_number')

    for rawdata in rawdatas:
        dataxxx = DataFolder.objects.using('retina').get(id=rawdata.data_id)
        experim = Experiment.objects.using('retina').get(id=dataxxx.exp_id)
        if rawdata.movie_number == movie_number:
            selected_path = join(experim.experimentname, dataxxx.dataxxx, rawdata.px_my)

    print(type(neighbours))
    print("print 1 %%%%%%%%%%%%%%%%%%%%%%%", neighbours)
    print('selected path: {selected_path}')
    if neighbours != "false":
        print("print 2 %%%%%%%%%%%%%%%%%%%%%%%", neighbours)
        print('selected path: {selected_path}')
        plot = plot_pxmy_and_neighbours([selected_path], electrode_to_plot, movie_number, y_axis_min=y_axis_min,
                                        y_axis_max=y_axis_max,
                                        x_axis_min=x_axis_min, x_axis_max=x_axis_max)
        response.write(plot)
        return response

    else:
        print("print 3 %%%%%%%%%%%%%%%%%%%%%%%", neighbours)
        print('selected path: {selected_path}')
        plot = plot_pxmy_without_neighbours([selected_path], electrode_to_plot, movie_number, y_axis_min=y_axis_min,
                                            y_axis_max=y_axis_max,
                                            x_axis_min=x_axis_min, x_axis_max=x_axis_max)
        response.write(plot)
        return response
