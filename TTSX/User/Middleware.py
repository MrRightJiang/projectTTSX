# coding=utf-8
class MiddleWare:

    '''
        设立这个中间件作用：1.记录用户向服务器发送请求之前的路径

        http://www.itcast.cn/python/?a=100

        get_full_path 取的是：   /python/?a=100  包括所以的参数
        path 取的是：            /python/        不包含参数

    '''
    def process_view(self,request,view_name,view_args,view_kwargs):

        if request.path not in [
                        '/user/register/',
                        '/user/register_headle/',
                        '/user/login/',
                        '/user/login_headle/',
                        '/user/register/',
                        '/user/loginout/',
                                ]:
            request.session['url_path']=request.get_full_path()
