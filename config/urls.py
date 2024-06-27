"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include
from sharecloth import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    
    path('sharecloth/', include('sharecloth.urls')), 
    # config/urls.py 디렉터리는 프로젝트 성격의 파일
    # sharecloth/로 시작하는 페이지 요청 -> sharecloth/urls.py 파일의 매핑 정보를 읽어서 처리
    # sharecloth/로 시작하는 URL 추가 시 sharecloth/urls.py 파일만 수정하면 된다

    path('accounts/', include('account_test.urls')), # 계정 테스트용 URL

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
