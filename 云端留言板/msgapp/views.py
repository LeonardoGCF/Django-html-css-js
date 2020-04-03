from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse,JsonResponse,FileResponse
import os
from django.template import Template,Context
# Create your views here.
def msgproc (request):
    datalist = []
    if request.method == "POST":
        userA = request.POST.get("userA", None)
        userB = request.POST.get("userB", None)
        msg = request.POST.get("msg",None)
        time = datetime.now()
        with open('msggate.txt','a+') as f:
            f.write("{}--{}--{}--{}\n".format(userA,userB,msg,time.strftime("%Y-%m-%d %H:%M:%S")))

    if request.method == "GET":
        userC = request.GET.get("userC", None)
        if userC != None:
            with open ("msggate.txt",'r') as f:
                cnt = 0
                for line in f:
                    linedata = line.split('--')
                    if linedata[0]==userC:
                        cnt += 1
                        d = {'userA':linedata[1],'msg':linedata[2],'time':linedata[3]}
                        datalist.append(d)

                    if cnt >= 10:
                        break
    return render(request,'msgSingleWeb.html',{"data":datalist})

def homeproc (request):
    #方法1
    #return HttpResponse("<h1>欢迎来到关朝峰的留言板，如需留言请访问<a href= '/msggate/'>该页面</a></h1>")

    #方法二 定义response类
    response =HttpResponse()
    response.write("<h1>欢迎来到关朝峰的留言板，如需留言请访问<a href= '/msggate/'>该页面</a></h1>")
    response.write("<h1> Don't miss me, I will come back</h1>")
    response.write( "<h1>这是我的<a href= '/photo/'>照片</a></h1>" )
    response.write( "<h1>这是我的<a href= '/secret/'>联系方式</a></h1>" )
    return response

def homeproc2 (request):
    response =JsonResponse({'tel':'3318012479'})
    return response

def homeproc3 (request):
    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    response = FileResponse(open(cwd + '/msgapp/IMG_2283的副本.JPG','rb'))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment:filename = "photo.jpg"'
    return response

def pgproc (request):
    template = Template('<h1> The name of the document is{{name}}</h1>')
    context = Context({'name':"测试渲染功能"})
    return HttpResponse(template.render(context))