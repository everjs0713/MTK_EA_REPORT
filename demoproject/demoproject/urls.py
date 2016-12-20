"""demoproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views, chartdemo, pivotdemo, chartraw

sort_order = {
    'Report': 0,
    'Charts': 1,
    'Pivot Charts': 2,
    'Charts w/ RawQuerySet': 3,
}
sidebar_items = []

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^upload/$', views.upload_file,name='upload'),
    url(r'^upload/$', views.upload_file,
        {
            'title': 'Upload File',
            'sidebar_section': 'Report',
        },
        name='file_upload',
        ),

    url(r'^record/$', views.file_list,
        {
            'title': 'File Manage',
            'sidebar_section': 'Report',
        },
        name='file_manage',
        ),
    url(r'^report-details/$', views.report_details, 
        {
            'title': 'Report Analyzer',
            'sidebar_section': 'Report',
        },  name='query_report'), 
        
]

# build sidebar_items first
seen_sections = []
for u in urlpatterns:
    if u.default_args:
        section = u.default_args['sidebar_section']
        title = u.default_args['title']

        # check if we've seen this section already
        if section not in seen_sections:
            item = {
                'sort_order': sort_order[section],
                'section': section,
                'links': [],
            }
            sidebar_items.append(item)
            seen_sections.append(section)

        # now add the new link to the sidebar section
        for item in sidebar_items:
            if item['section'] == section:
                item['links'].append((title, u.name))
                break

        del u.default_args['sidebar_section']

# now assign sidebar_items to urls
for u in urlpatterns:
    if u.default_args:
        u.default_args['sidebar_items'] = sidebar_items
