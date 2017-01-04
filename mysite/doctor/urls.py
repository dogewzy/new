from django.conf.urls import url
from . import views

app_name = 'doctor'
urlpatterns = [
    # 统一前缀为doctor
    # 这部分是诊断页面的，要修改index
    url(r'^entry', views.entry_index, name='entry'),
    url(r'^medicine_information/$', views.medicine_information, name='medicine_information'),
    url(r'^main_information/$', views.main_information, name='main_information'),
    url(r'^result/$', views.result, name='result'),
    url(r'^display/$', views.display, name='display'),
    url(r'^diagnose/$', views.diagnose, name='diagnose'),
    url(r'^diag_record/([0-9]+)/$', views.diag_record, name='diag_record'),
    # 这部分是病人资料的
    url(r'^$', views.index, name='index'),
    url(r'^patient/$', views.patient, name='patient'),
    url(r'^patient_log/$', views.patient_log, name='patient_log'),
    url(r'^patient_edit/$', views.patient_edit, name='patient_edit'),
    url(r'^patient_search/$', views.patient_search, name='patient_search'),
    url(r'^patient_search_day/$', views.patient_search_day, name='patient_search_day'),
    url(r'^patient_num/$', views.patient_num, name='patient_num'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    # 这部分挂号
    url(r'^registration/$', views.register, name='registration'),
    url(r'^r_search/$', views.r_search, name='r_search'),
    url(r'^r_display/$', views.r_display, name='r_display'),
    url(r'^r_index/$', views.r_index, name='r_index'),
    #
    url(r'^price/$', views.price, name='price'),
    # 这部分药品管理的
    url(r'^medicine/$', views.medicine, name='medicine'),
    url(r'^medicine_add/$', views.medicine_add, name='medicine_add'),
    url(r'^medicine_num/$', views.medicine_num, name='medicine_num'),
]
