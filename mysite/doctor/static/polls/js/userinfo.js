var nameDic = {
            'wzy':'超级管理员',
            'guahao':'挂号员',
            'yaofang':'药房人员',
            'yisheng':'医生',
            'huajia':'划价员',
            'guahao':'挂号员',
        }
var name = nameDic['{{ name|safe }}'];
var element=document.getElementById("login");
element.innerHTML =  "<a href='http://localhost:8000/用户权限'><span >"+name+"</span></a>";
