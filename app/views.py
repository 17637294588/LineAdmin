from django.shortcuts import render
from Online_education.settings import *
from app.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from app.serializer import *
import json
from django.http import HttpResponse

# Create your views here.


from django.conf import settings
from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client     

# 重写存储引擎方法
class FastDfsStroage(Storage):

    def __init__(self, base_url = None, client_conf = None):
        """
            初始化对象
            :param base_url:
            :param client_conf:
        """
        if base_url is None:
            base_url = FDAS_URL
            # 'http://39.106.64.101:8888/'
        self.base_url = base_url

        if client_conf is None:
            client_conf = FDFS_CLIENT_CONF
            # FDFS_CLIENT_CONF = os.path.join(BASE_DIR, 'client.conf')
        self.client_conf = client_conf


    def _open(self, name, mode = 'rb'):
    
        """
            打开文件
            :param name:
            :param mode:
            :return:
        """
        pass

    def _save(self, name, content):
        """
            保存文件
            :param name: 传入文件名
            :param content: 文件内容
            :return:保存到数据库中的FastDFSDE文件名
        """
        client = Fdfs_client(self.client_conf)
        ret = client.upload_by_buffer(content.read())

        if ret.get("Status") != "Upload successed.":
            raise Exception("upload file failed")
        file_name = ret.get("Remote file_id")

        return file_name


    def exists(self, name):
        """
            检查文件是否重复, FastDFS自动区分重复文件
            :param name:
            :return:
        """
        return False

    def url(self, name):
        """
            获取name文件的完整url
            :param name:
            :return:
        """
        return self.base_url + name



# 获取分类
class Get_cate_mes(APIView):

    def get(self,request):

        cates = CourseType.objects.all()
        if cates:
            cate_list = CateSerializer(instance=cates,many=True)
            return Response({'code':200,'mes':cate_list.data})
        else:
            return Response({'code':201,'mes':'没有数据'})



# 改变分类数据
class Change_cate(APIView):

    def get(self,request,cid):
        courses = Course.objects.filter(coursetype=cid).all()
        course_list = CourseSerializer(instance=courses,many=True)
        return Response({'code':200,'mes':course_list.data})


# 展示所有课程
class Get_course_mes(APIView):

    def get(self,request):

        courses = Course.objects.all()
        if courses:
            course_list = CourseSerializer(instance=courses,many=True)
            return Response({'code':200,'mes':course_list.data})

        else:
            return Response({'code':201,'mes':'没有数据'})


# 课程详情页数据
class Get_course_detail(APIView):

    def get(self,request,id):

        courses = Course.objects.filter(id=id).first()
        if courses:

            chapter_list = courses.chapter_set.all()

            data = []
            for i in chapter_list:
                dict1 = {}
                dict1['xiaojie'] = i.coursecell_set.all().values('name','id','order_id','choices')
                dict1['name'] = i.name
                dict1['id'] = i.id 
                data.append(dict1)  

     
            course = CourseSerializer(instance=courses)
            return Response({'code':200,'mes':course.data,'chapter_list':data})
        else:
            return Response({'code':201,'mes':'没有数据'})


# 查看课程小节类型
class Chack_type(APIView):

    def get(self,request,id):
        
        coursecell = CourseCell.objects.filter(id=id).first()
        coursecelles = CourseCellSerializer(instance=coursecell)

       
        return Response(coursecelles.data)





import oss2
import time
from urllib import parse

# 路径上传
def upload_oss_file(key):
    endpoint = 'oss-cn-beijing.aliyuncs.com'
    
    auth = oss2.Auth('LTAIhkOHwqyDMkZa', 'UtjzEEVdjgto334c4lVM0uRb8urORA')
    bucket = oss2.Bucket(auth, endpoint, 'sujiankang')
    current_fold = time.strftime('%Y-%m-%d',time.localtime())
    current_file_path = key
    file_path = 'C:/Users/sujiankang/Desktop/'+ key
    # 上传
    bucket.put_object_from_file(current_file_path, file_path)
  
    url = 'https://sujiankang.oss-cn-beijing.aliyuncs.com/'+parse.quote(current_file_path)
    return url


# key = '哈哈.mp4'
# url = upload_oss_file(key)



'''
os 模块下有个 bs..什么的可以拿到整个路径后的文件名
os.path.basename()

from urllib.parse import unquote
print(unquote('%E5%93%88%E5%93%88'))

x = parse.quote(‘武动乾坤‘)
print(x)

https://sujiankang.oss-cn-beijing.aliyuncs.com/%E5%93%88%E5%93%88.mp4
https://sujiankang.oss-cn-beijing.aliyuncs.com/%E5%93%88%E5%93%88.mp4
'''







class Upload_file(APIView):

    def post(self,request):
        file = request.data['file']

        print(file)
        sub_file(file)

        # print(type(str(file)))
        return Response({'code':200})





def sub_file(file):
    auth = oss2.Auth('LTAIhkOHwqyDMkZa', 'UtjzEEVdjgto334c4lVM0uRb8urORA')

    bucket = oss2.Bucket(auth, 'oss-cn-beijing.aliyuncs.com', 'sujiankang')
    
 
  
    # print(dir(file))
    bucket.put_object_from_file(file.name,file.name)

    # with open(file.read(), 'wb') as fileobj:
    #     # Seek方法用于指定从第1000个字节位置开始读写。上传时会从您指定的第1000个字节位置开始上传，直到文件结束。
    #     fileobj.seek(1000,os.SEEK_SET)
    #     # Tell方法用于返回当前位置。
    #     current = fileobj.tell()
    
    #     bucket.put_object(file.name,fileobj)


    #  f = open(os.path.join(settings.STATICS_IMG,'',file.name),'wb')
    #     #写文件 遍历文件流
    #     for chunk in file.chunks():
    #         f.write(chunk)





# 富文本编辑器上传图片
class Upload_img(APIView):

    '''
        InMemoryUploadedFile
        request.data: <QueryDict: {'ckCsrfToken': ['gg9b266v1QIREU6rmi9x1Q86SoanA50Dbm9SMnm7'], 'upload': [<InMemoryUploadedFile: djando.jpg (image/jpeg)>]}>
        {'Group name': 'group1', 'Remote file_id': 'group1\\M00/00/00/rBHmx10Z0fyAL47uAAA4r8qepmk6717777', 'Status': 'Upload successed.', 'Localfile name': '', 'Uploaded size': '14.00KB', 'Storage IP': '39.106.64.101'}
    '''
    def post(self,request):
        print('===============')
        file = request.data['upload']     # djando.jpg
        file_url = upload_fastdfs(file)
        print(file_url)

        return Response({"uploaded":"true", "url":'http://39.106.64.101:8888/'+file_url})



def upload_fastdfs(files):
    client = Fdfs_client(FDFS_CLIENT_CONF)
    ret = client.upload_by_buffer(files.read())

    if ret.get("Status") != "Upload successed.":
        raise Exception("upload file failed")
    file_id = ret.get("Remote file_id")

    return file_id







# # 接受前端信息
# @accept_websocket
# def test_socket(request):

#     if request.is_websocket():
#     # request.websocket:<dwebsocket.backends.default.websocket.DefaultWebSocket object at 0x0000014177655DA0>
#         for message in request.websocket:
#             c = str(message,encoding='utf-8')
#             print(c)

#             request.websocket.send(message)

#导入websocket装饰器
from dwebsocket.decorators import accept_websocket,require_websocket
# 主动推送消息
@accept_websocket
def test_websocket(request):

    if request.is_websocket:

        data = {
            'DateNow':time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))
        }
        request.websocket.send(json.dumps(data))





import paramiko
import threading
import time



host = '39.106.64.101'
username = 'root'
password = 'Su123456'


# 第一种实现方法
# @accept_websocket
# def terminals(request):
#     '''
#         创建两个管道 ws  channle
#         ws:是前端和 django 交互的管道，用于前端和 django 数据交互
#         channle：是django和linux交互的管道，用于 django和 linux 数据交互
#     '''

#     if request.is_websocket:
#         sh = paramiko.SSHClient()
#         sh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         sh.connect(host,username=username,password=password)
#         channle = sh.invoke_shell(term='xterm')   # channle：django和 linux管道
#         ws = request.websocket                    # ws: vue 和 django 管道

#         t = threading.Thread(target=recv_ssh_mes,args=(channle,ws))
#         t.setDaemon(True)       # 会随着主进程的消亡而消亡
#         t.start()

#         while not channle.exit_status_ready():
#             '''
#                 ws.recv() ws.read() ws.wait() 接受前端发来的数据
#                 ws.send()  发送给浏览器数据
#             '''
#             cmd = ws.wait()
#             if cmd:
#                 # 如果有命令则将命令发送给 linux
#                 channle.send(cmd)

#             else:
#                 break

#         ws.close()          # 关闭连接
#         channle.close()



'''
    写一个线程专门用来接收 linux 返回的数据返回给前端，因为有时一条命令会返回很多条数据，
    并不是一唱一和，需要一个线程任务专门来读取返回数据返回前端
'''
# def recv_ssh_mes(channle,ws):
#     '''
#         需要将两个管道接收过来，channle用于读取 linux返回的数据
#         ws 用于将返回的数据发送给前端
#     '''
#     while not channle.exit_status_ready():
#         try:
#             data = channle.recv(1024)
#             ws.send(data)

#         except:
#             break



'''
    WebSSH
    websocket我们在在线教育中用在了制作开发WebSSH领域
    将传统的SSH C/S服务端客户端处理方式升级成了B/S架构
    给学生提供的虚拟环境，以供在线使用真实Linux环境进行编程
        虚拟环境：docker搭建沙箱环境, K8S，运维工作人员来进行
            工单系统
        paramiko模块进行虚拟终端的连接建立
            exec_command: 命令传输
        invoke_shell: xterm == vue(xterm)
    线程：解决在服务端可能返回的命令并不是一次性或一次就返回完毕的
    websocket < tcp
        tcp会在长时间数据没有沟通的时候，自动断开
    心跳包：
        1：确认服务器是否存活
        2：维持了连接的活跃性
'''

# 第二种实现方法
'''
    定义一个函数专门用来创建 django和linux 管道
    定义一个函数专门用来向 linux 发送命令
    定义一个线程专门用来从 linux 接受数据返回前端
    定义主接口实现逻辑
'''

def create_channle(host,username,password):
    '''
        创建 channle 管道
    '''
    sh = paramiko.SSHClient()
    sh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sh.connect(host,username=username,password=password)
    channle = sh.invoke_shell(term='xterm')

    return channle


def send_ssh_mes(channle,cmd):
    '''
        发送命令给 linux 
    '''

    try:
        channle.send(cmd)

    except Exception as e:
        print(e)


def get_ssh_mes(channle,ws):
    '''
        定义接受 linux 线程,接受数据返回给前端
    '''
    while not channle.exit_status_ready():
        try:
            data = channle.recv(1024)
            ws.send(data)
        except:
            break


host = '39.106.64.101'
username = 'root'
password = 'Su123456'
@accept_websocket
def terminals(request):
    '''
        定义接口
    '''
    if request.is_websocket():

        ws = request.websocket      # 创建 前端和 django 通道
        channle = create_channle(host,username,password)  # 创建SSH连接通道    

        t = threading.Thread(target=get_ssh_mes,args=(channle,ws))
        t.setDaemon(True)          # 设定守护线程，主线程退出，子线程也跟着退出，需要先声明再启动线程
        t.start()                  # 启动线程
        
        while not channle.exit_status_ready():
            cmd = ws.wait()            # 读取前端发过来的命令数据
            if cmd:
                send_ssh_mes(channle,cmd)   # 调用发送命令函数

            else:
                break

        channle.close()
        ws.close()

print('=======================')