from django.db import models
from datetime import datetime


class Register(models.Model):
    register_num = models.IntegerField()
    name = models.CharField(max_length=100)
    section = models.CharField(max_length=100)
    cost = models.FloatField()
    operator = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class Price(models.Model):
    # 划价编号就是挂号编号
    register_num = models.IntegerField()
    p_number = models.IntegerField()
    man = models.CharField(max_length=100)
    # 药品信息存储格式为： '药品1编号！药品1数量# 药品2编号！药品2数量'
    prescription = models.CharField(max_length=500, null=True)

    def __str__(self):
        return '挂号编号' + ': ' + str(self.register_num)

    def get_medicine_list(self):
        # 返回一个药品信息的list
        total = []
        l1 = self.prescription.split('#')
        for item in l1[:-1]:
            l2 = item.split('!')
            m_name = l2[0]
            m_num = l2[1]
            m_price = Medicine.objects.get(name=m_name).price
            total.append([m_name, m_num, m_price])
        return total

    def get_total_price(self):
        # 返回该划价的总价
        total = 0
        l1 = self.prescription.split('#')
        for item in l1[:-1]:
            l2 = item.split('!')
            # 名称
            m_name = l2[0]
            # 数量
            m_num = l2[1]
            m_price = Medicine.objects.get(name=m_name).price
            total += float(m_num) * m_price
        return total


class Medicine(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    unit = models.CharField(max_length=100)
    sort = models.CharField(max_length=100)
    amount = models.IntegerField(default=100)

    def __str__(self):
        return str(self.name)


class Diagnose(models.Model):
    # 这里的register_num就是挂号编号，一个挂号对应一个诊断 p_number是病人编号
    # prescription是处方,就是price里面的药品信息，就是什么药开几盒什么药开几盒，做不做B超
    register_num = models.IntegerField(default=0)
    prescription = models.TextField(default='')
    result = models.TextField(default='')
    time = models.DateTimeField(default=datetime.today())
    man = models.CharField(default='temp', max_length=10)
    p_number = models.IntegerField(default=0)

    def __str__(self):
        return str(self.register_num)

    def get_medicine_list(self):
        # 返回一个药品信息的list
        total = []
        l1 = self.prescription.split('#')
        for item in l1[:-1]:
            l2 = item.split('!')
            m_name = l2[0]
            m_num = l2[1]
            m_price = Medicine.objects.get(name=m_name).price
            total.append([m_name, m_num, m_price])
        return total

    def get_total_price(self):
        # 返回该划价的总价
        total = 0
        l1 = self.prescription.split('#')
        for item in l1[:-1]:
            l2 = item.split('!')
            # 名称
            m_name = l2[0]
            # 数量
            m_num = l2[1]
            m_price = Medicine.objects.get(name=m_name).price
            total += float(m_num) * m_price
        return total

    def get_all_name_num(self):
        l1 = self.prescription.split('#')
        result = []
        for item in l1[:-1]:
            l2 = item.split('!')
            # 名称
            m_name = l2[0]
            # 数量
            m_num = l2[1]
            result.append([m_name, m_num])
        return result


class Patient(models.Model):
    # p_number是病人编号，p_id_num是身份证号码
    sex_choice = (
        ('男', '男'),
        ('女', '女'),
    )
    m_choice = (
        ('已婚', '已婚'),
        ('未婚', '未婚')
    )
    p_name = models.CharField(max_length=100, default=' ')
    p_age = models.IntegerField(default='')
    p_number = models.IntegerField(default='')
    p_tel_number = models.IntegerField(default='')
    p_sex = models.CharField(choices=sex_choice, max_length=2, default='男')
    p_marriage = models.CharField(choices=m_choice, max_length=2, default=' ')
    p_address = models.CharField(max_length=100, default=' ', null=True)
    p_id_num = models.CharField(max_length=100, default=' ', null=True)

    # def __str__(self):
    #     return str(self.p_name)


