import os
from chartit import DataPool, Chart
from .models import MonthlyWeatherByCity
from .decorators import add_source_code_and_doc
from django.shortcuts import render_to_response

from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView

from .models import Document
from .forms import DocumentForm
from .forms import UploadFileForm
from .models import modelwithfilefield
def homepage(_):
    ds = DataPool(
        series=[{
            'options': {
                'source': MonthlyWeatherByCity.objects.all()
            },
            'terms': [
                'month',
                'houston_temp',
                'boston_temp',
                'san_francisco_temp'
            ]
        }]
    )

    def monthname(month_num):
        names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
        return names[month_num]

    cht = Chart(
        datasource=ds,
        series_options=[{
            'options': {
                'type': 'line',
                'stacking': False
            },
            'terms': {
                'month': [
                    'boston_temp',
                    'houston_temp']
            }
        }],
        chart_options={
            'title': {
                'text': 'Weather by Month'},
            'xAxis': {
                'title': {
                    'text': 'Month'}},
            'yAxis': {
                'title': {
                    'text': 'Temperature'}},
            'legend': {
                'enabled': False},
            'credits': {
                'enabled': False}},
        x_sortf_mapf_mts=(None, monthname, False))
    return render_to_response('index.html', {'chart_list': cht})


@add_source_code_and_doc
def demohome(_, title, code, doc, sidebar_items):
    """
    Welcome to the Django-Chartit Demo. This demo has a lot of sample charts
    along with the code to help you get familiarized with the Chartit API.

    The examples start with simple ones and get more and  more complicated.
    The latter examples use concepts explained in the examples earlier. So if
    the source code of a particular chart looks confusing, check to see if any
    details have already been explained in a previous example.

    The models that the examples are based on are explained in Model Details.

    Thank you and have fun exploring!
    """
    code = None
    return render_to_response('demohome.html',
                              {'chart_list': None,
                               'code': code,
                               'title': title,
                               'doc': doc,
                               'sidebar_items': sidebar_items})


@add_source_code_and_doc
def model_details(_, title, code, doc, sidebar_items):


    code='hello'
    return render_to_response('model_details.html',
                              {'code': code,
                               'title': title,
                               'doc': doc,
                               'sidebar_items': sidebar_items})

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('list'))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render(
        request,
        'list.html',
        {'documents': documents, 'form': form}
    )

def upload_file(request):
    if request.method == 'POST':
        files = request.FILES.getlist('file')        
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            for f in files:
                newdoc = modelwithfilefield(upload_to=f)
                newdoc.save()
            return HttpResponseRedirect('/demo/model-details/')    
    else:
        form = UploadFileForm()   
    # Load documents for the list page
    documents = modelwithfilefield.objects.all()        
    return render(request, 'upload.html', {'documents': documents, 'form': form})
    
