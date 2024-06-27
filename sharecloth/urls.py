from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.decorators import login_required

app_name = 'sharecloth'


# clothshare > index.html에서 href='{% url 'sharecloth:login_page' %}'부분에서
# app_name 없으면  is not a registered namespace 에러 발생
# 에러 해결 참고 글 : https://velog.io/@keybomb/Django-%ED%8A%9C%ED%86%A0%EB%A6%AC%EC%96%BC-namespace-%EC%97%90%EB%9F%AC

urlpatterns = [
    path('1/', views.index, name='main'), #views.py의 index()
    # config/urls.py의 sharecloth/ + sharecloth/urls.py의  '' => sharecloth/
    path('1/<int:pk>/', views.post_detail, name='post_detail'),


    path('mypage/', login_required(views.my_page), name='mypage'),
    path('payment/<int:post_id>/', views.payment, name='payment'),
    path('return_item/<int:rental_id>/', views.return_items, name="return_item"),
    

    path('create/', views.post_create, name='post_create'), 
    # 게시물 등록 페이지로 이동

    path('1/<int:pk>/', views.post_detail, name='post_detail'),
    # 선택한 게시물 상세 페이지로 이동

    path('update_address/', views.update_address, name='update_address'),
    # mypage에서 위치 검색 후 DB에 저장

    path('donation/', views.donation_page, name='donation_page'),
    path('convert_donation_to_mileage/', views.convert_donation_to_mileage, name='convert_donation_to_mileage'),
    # 도네이션 페이지 이동 / 기부금액을 마일리지로 전환

    path('search/', views.search_results, name='search_results'),
    # 게시물 검색 후 해당하는 포스트만 표시하는 페이지

    path('post_list', views.post_list, name='post_list'),
    # 필터가 적용된 포스트만 표시하는 페이지
    
    path('payment_page/<int:post_id>/', views.payment_page, name='payment_page'),
    # 결제 페이지


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # 미디어 파일 서빙을 위한 설정 / 개발 환경에서 미디어 파일 제공 / 실제 배포 환경에서는 다른 방식 사용해야 함

    


# 사용자는 create URL을 통해 게시물 등록 페이지에 접근, 입력한 정보가 폼을 통해 DB에 저장. 
# MEDIA_URL, MEDIA_ROOT 설정 : 업로드된 이미지 파일이 지정된 폴더에 저장된다.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)