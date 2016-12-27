from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout


login_url = "http://localhost:8000/doctor/login/"
name_dic = {
    'doctor': '孟医生',
    'dogewzy': '管理员',
    'guahao': '挂号员小李',
    'yaofang': '药房小刘',
}

# 这个还没用到
@permission_required(perm='doctor.add_price',
                     login_url=login_url)
def entry_index(request):
    # 提供查询入口
    return render(request, 'doctor/index.html')


def main_information(request):
    # 在医生填写完基本信息之后转到这个url
    # 接收基本划价信息
    # 通过hidden input传递了划价编号
    if request.method == 'POST':
        form = DiagnoseForm(request.POST)
        if form.is_valid():
            new = Diagnose()
            new.register_num = form.cleaned_data['挂号编号']
            new.p_number = form.cleaned_data['病人编号']
            new.man = form.cleaned_data['操作人']
            new.time = form.cleaned_data['诊断时间']
            new.result = form.cleaned_data['诊断结果']
            new.prescription = ''
            new.save()
            addform = AddForm()
            return render(request, 'doctor/medicine.html', {'number': new.register_num, 'addform': addform})


def medicine_information(request):
    # 显示药品划价信息表单,以及已经添加的药品
    # 这里有一个hidden input
    # 把所有
    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            number = request.POST['number']
            the_diagnose = Diagnose.objects.get(register_num=number)
            the_diagnose.prescription += form.cleaned_data['药品名称'] + '!' + str(form.cleaned_data['数量']) + '#'
            the_diagnose.save()
            # 提取药品信息
            all_m = the_diagnose.get_medicine_list()
            addform = AddForm()
            # 提供药品余量信息
            m = Medicine.objects.all()
            info = {}
            for i in m:
                info[i.name] = i.amount
            return render(request, 'doctor/medicine.html', {'info': info, 'all_m': all_m,
                                                            'number': number, 'addform': addform})


def result(request):
    return render(request, 'doctor/result.html')


@permission_required(perm='doctor.add_price',
                     login_url=login_url)
def display(request):

    '''药房根据挂号编号开药'''

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            num = form.cleaned_data['划价编号']
            price = Diagnose.objects.get(register_num=num)
            # 需要处理的一个额外逻辑是余量管理
            process_li = price.get_all_name_num()
            for i in process_li:
                target = Medicine.objects.get(name=i[0])
                target.amount -= int(i[1])
                target.save()
            # 展示context中需要num，p_num，total_cost,man,一个药品信息的list
            p_num = price.p_number
            man = price.man
            li = price.get_medicine_list()
            total_cost = price.get_total_price()
            return render(request, 'doctor/display.html', {
                'num': num,
                'p_num': p_num,
                'man': man,
                'li': li,
                'total_cost': total_cost,
            })

    else:
        form = SearchForm()
        return render(request, 'doctor/search.html', {'form': form})


@permission_required(perm='doctor.add_diagnose',
                     login_url=login_url)
def diagnose(request):
    form = DiagnoseForm()
    name = name_dic[request.user.username]
    return render(request, 'doctor/diagnose.html', {'form': form, 'name': name})


def diag_record(request, p_num):
    d = Diagnose.objects.filter(p_number=p_num)
    r = []
    for each_diagnose in d:
        r.append((each_diagnose.result, each_diagnose.prescription, each_diagnose.time))
    return render(request, 'doctor/diag_record.html', {'record': r})


def index(request):
    return render(request, 'polls/index.html')


def patient(request):
    all_patients = Patient.objects.order_by('id')
    return render(request, 'polls/patient.html', {'all_patients': all_patients})


def patient_log(request):
    is_ok = False
    print(1)
    if request.method == 'POST':
        print(2)
        form = TesPForm(request.POST)
        if form.is_valid():
            print(3)
            new_p = Patient()
            new_p.p_name = form.cleaned_data['p_name']
            new_p.p_sex = form.cleaned_data['p_sex']
            new_p.p_age = form.cleaned_data['p_age']
            new_p.p_number = form.cleaned_data['p_number']
            new_p.p_tel_number = form.cleaned_data['p_tel_number']
            new_p.p_address = form.cleaned_data['p_address']
            new_p.p_marriage = form.cleaned_data['p_marriage']
            new_p.p_id_num = form.cleaned_data['p_id_num']
            new_p.save()
            is_ok = True
            return render(request, 'polls/patient_log.html', {'form': form, 'isok': is_ok})
    else:
        form = TesPForm()
    return render(request, 'polls/patient_log.html', {'form': form, 'isok': is_ok})


def patient_num(request):
    if request.method == 'POST':
        form = EditToBeSaveForm(request.POST)
        if form.is_valid():
            num = form.cleaned_data['病人编号']
            new_p = Patient.objects.get(p_number=num)
            if new_p:
                new_p.p_name = form.cleaned_data['姓名']
                new_p.p_sex = form.cleaned_data['性别']
                new_p.p_age = form.cleaned_data['年龄']
                new_p.p_tel_number = form.cleaned_data['电话号码']
                new_p.save()
                return render(request, 'polls/patient_edit.html')
    else:
        form = EditToBeSaveForm()
        return render(request, 'polls/patient_num.html', {'form': form})


def patient_edit(request):
    return render(request, 'polls/patient_edit.html')


def patient_search(request):
    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            number = form.cleaned_data['病人编号']
            patient_s = Patient.objects.filter(p_number=number)[0]
            return render(request, 'polls/patient_display.html', {'patient': patient_s})
    else:
        form = EditForm()
        return render(request, 'polls/patient_search.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['账号']
            password = form.cleaned_data['密码']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                print(user.user_permissions)
                return render(request, 'polls/patient_edit.html')
            else:
                pass
    else:
        form = LoginForm()
        return render(request, 'polls/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    message = '您已经登出'
    return render(request, 'polls/index.html', {'message': message})


def patient_record(request, p_num):
    pass


def price(request):
    pass


@permission_required(perm='doctor.add_medicine',
                     login_url=login_url)
def medicine(request):
    all_medicine = Medicine.objects.order_by('id')
    return render(request, 'medicine/index.html', {'all_medicine': all_medicine})


def medicine_add(request):
    if request.method == 'POST':
        form = MedForm(request.POST)
        if form.is_valid():
            m = Medicine()
            m.name = form.cleaned_data['name']
            m.amount = form.cleaned_data['amount']
            m.number = form.cleaned_data['number']
            m.price = form.cleaned_data['price']
            m.sort = form.cleaned_data['sort']
            m.unit = form.cleaned_data['unit']
            m.save()
            all_medicine = Medicine.objects.order_by('id')
            return render(request, 'medicine/index.html', {'all_medicine': all_medicine})
    form = MedForm()
    return render(request, 'medicine/add.html', {'form': form})


def medicine_num(request):
    if request.method == 'POST':
        form = MAddForm(request.POST)
        if form.is_valid():
            m = Medicine.objects.get(number=form.cleaned_data['药品编号'])
            m.amount += form.cleaned_data['增加的量']
            m.save()
            all_medicine = Medicine.objects.order_by('id')
            return render(request, 'medicine/index.html', {'all_medicine': all_medicine})
    else:
        form = MAddForm()
        return render(request, 'medicine/num.html', {'form': form})


# 下面这部分是挂号的views
@permission_required(perm='doctor.add_register',
                     login_url=login_url)
def register(request):
    obs = Register.objects.all()[0:5]
    return render(request, 'registration/register.html', {'obs': obs})


def r_search(request):
    if request.method == 'POST':
        form = ReSearchForm(request.POST)
        if form.is_valid():
            num = form.cleaned_data['挂号编号']
            ob = Register.objects.get(register_num=num)
            return render(request, 'registration/display.html', {'ob': ob})
    else:
        form = ReSearchForm
    return render(request, 'registration/search.html', {'form': form})


def r_index(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_d = Register()
            new_d.cost = form.cleaned_data['费用']
            new_d.name = form.cleaned_data['姓名']
            new_d.operator = form.cleaned_data['操作人']
            new_d.section = form.cleaned_data['科室']
            new_d.register_num = form.cleaned_data['挂号编号']
            new_d.save()
            obs = Register.objects.all()[0:5]
            return render(request, 'registration/register.html', {'obs': obs})
    else:
        form = RegisterForm()
        name = name_dic[request.user.username]
        return render(request, 'registration/index.html', {'form': form, 'name':name})


def r_display(request):
    return render(request, 'registration/display.html')
