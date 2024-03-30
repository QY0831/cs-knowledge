"""
API:
发布feed: 
POST v1/me/feed
Args:
    content
    auth_token

获取feed:
GET /v1/me/feed

feed发布：
用户call 发布API -> 负载均衡器 -> Web服务器 -> Worker服务器(帖子服务、广播服务、通知服务)

Web服务器：
- 与客户端通信
- 身份验证、流量控制

帖子服务：
保存帖子到缓存、数据库。

广播服务：
可分为写模型和读模型：
写广播：直接推送，新帖子发布后，立刻传递到好友的news feeds缓存中。
读广播：不直接推送，当其他用户加载主页时，才拉取最新动态。
为防止热点问题，大部分用户使用写广播，对于有大量好友、粉丝的用户，使用读广播。
工作流程：
1. 从图数据库（适合管理好友）获取好友id
2. 从好友缓存或数据库中获取好友信息
3. 发送好友列表和新动态到消息队列
4. 广播worker从队列获取数据，将<post_id, user_id>放到news feed缓存红

通知服务：
告知好友有新的推送。

获取feed:
用户call 获取API -> 负载均衡器 -> Web服务器 -> news feed服务（Worker）

news feed服务从news feed缓存获取帖子id列表，再从帖子缓存（数据库）中获取详情，整合成json传给客户端。

"""
from django.urls import path
from . import views

urlpatterns = [
    # 其他URL模式
    path('v1/me/feed/', views.FeedView.as_view(), name='feed'),
]

from rest_framework import generics
from rest_framework.response import Response

class FeedView(generics.ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        content = request.data.get('content')
        auth_token = request.data.get('auth_token')

        # 执行必要的验证或处理
        # ...

        # 将feed保存到数据库或执行其他操作
        # ...

        # 返回成功的响应
        return Response({'message': '成功创建Feed'})

    def get(self, request, *args, **kwargs):
        # 执行必要的身份验证或授权检查
        # ...

        # 从数据库或其他资源获取feed
        # ...

        # 返回feed数据作为JSON响应
        feed_data = {
            # 根据需要填充feed数据
            'articles': [
                {
                    'title': '文章1',
                    'content': '文章1的内容'
                },
                {
                    'title': '文章2',
                    'content': '文章2的内容'
                }
            ]
        }
        return Response(feed_data)