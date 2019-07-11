# 自定义中间件
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse

class MD1(MiddlewareMixin):

    def process_request(self,request):  # process_request：多中间件情况下，按照settings文件配置顺序执行
        print('MD1 的 ',request)
    
    # process_view：按照 MIDDLEWARE 中的注册顺序从前到后顺序执行的
    def process_view(self,request,view_func,view_args,view_kwargs):

        print("MD1 中的process_view")
        # print(view_func, view_func.__name__)  # view_func：是使用的函数名称
        # print(view_kwargs)  # view_kwargs:是将传递给视图的关键字参数的字典，view_args:是元祖
        return None

    def process_response(self,request,response):  # process_response：是按照MIDDLEWARE中的注册顺序倒序执行的
        print('MD1 的 ',response)
           
        return response

    def process_exception(self,request,exception):
        print(exception)
        print("MD1 中的process_exception")

   



class MD2(MiddlewareMixin):

    def process_request(self,request):
        print('MD2 的 ',request)
    
    
    def process_view(self,request,view_func,view_args,view_kwargs):  

        print("MD2 中的process_view")
        # print(view_func, view_func.__name__)
        # print(view_kwargs)     

    def process_response(self,request,response):
        print('MD2 的 ',response)

        return response

    def process_exception(self,request,exception):  # 在报错时才执行
        print(exception)
        print("MD2 中的process_exception")

    


