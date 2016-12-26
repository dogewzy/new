from django import forms
import datetime
from .models import Patient, Medicine

from django.utils.translation import ugettext_lazy as _


class MedForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = '__all__'
        labels = {
            'name': _('药品名称'),
            'price': _('价格'),
            'number': _('编号'),
            'amount': _('余量'),
            'sort': _('分类'),
            'unit': _('单位'),
        }


class MAddForm(forms.Form):
    药品编号 = forms.IntegerField()
    增加的量 = forms.IntegerField()


class TesPForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        labels = {
            'p_name': _('姓名'),
            'p_age': _('年龄'),
            'p_number': _('病人编号'),
            'p_tel_number': _('电话号码'),
            'p_sex': _('性别'),
            'p_marriage': _('婚姻状况'),
            'p_address': _('住址'),
            'p_id_num': _('身份证号码'),
        }


class EditForm(forms.Form):
    病人编号 = forms.IntegerField()


class EditToBeSaveForm(forms.Form):
    sex_choice = (
        ('男', '男'),
        ('女', '女'),
    )
    病人编号 = forms.IntegerField(label='你要修改的病人编号')
    姓名 = forms.CharField(max_length=100)
    年龄 = forms.IntegerField()
    电话号码 = forms.IntegerField()
    性别 = forms.ChoiceField(choices=sex_choice)


class LoginForm(forms.Form):
    账号 = forms.CharField(max_length=100)
    密码 = forms.CharField(max_length=100)


class AddForm(forms.Form):
    药品名称 = forms.CharField(max_length=100)
    数量 = forms.IntegerField()


class SearchForm(forms.Form):
    划价编号 = forms.IntegerField()


class DiagnoseForm(forms.Form):
    病人编号 = forms.IntegerField()
    挂号编号 = forms.IntegerField()
    诊断结果 = forms.CharField(widget=forms.Textarea)
    诊断时间 = forms.DateTimeField(initial=datetime.datetime.today())
    操作人 = forms.CharField(initial='孟医生')


class RegisterForm(forms.Form):
    挂号编号 = forms.IntegerField()
    姓名 = forms.CharField(max_length=100)
    section = (
        ('内科', '内科'),
        ('外科', '外科'),
        (None, '请选择科室')
    )
    科室 = forms.ChoiceField(
        choices=section,
    )
    费用 = forms.FloatField()
    操作人 = forms.CharField(max_length=100)


class ReSearchForm(forms.Form):
    挂号编号 = forms.IntegerField()


class MedicineAddForm(forms.Form):
    药品编号 = forms.IntegerField()
    添加数量 = forms.IntegerField()
