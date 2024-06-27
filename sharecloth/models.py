from django.contrib.auth.models import User

from django.db import models

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


'''
모델 신규 생성 및 변경시 makemigrations -> migrate
'''

''' 사용 안함
class user_info(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.IntegerField()
    user_location = models.DecimalField(max_digits=10, decimal_places=5)
    land_item_info = models.IntegerField() #post의 item_num과 동일 번호 -> 대여중인 아이템 표시에 사용
    email = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=100)


'''

class Project(models.Model):
    logo =  models.ImageField(upload_to='images/')


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_num = models.IntegerField()# 게시물 식별을 위한 고유 번호 (대여 중인 아이템 확인용)
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=200)
    content = models.TextField()
    can_land = models.BooleanField() # 현재 아이템 상태가 빌릴 수 있나, 없나 확인
    price = models.IntegerField()
    thumbnail = models.ImageField(upload_to='thumbnails/')
    publisher_name = models.CharField(max_length=100) # 게시물 올린 사람 (user_info의 id 값)
    create_date = models.DateField(auto_now_add=True)
    address = models.CharField(max_length=255, default="Unknown")
    
    #카테고리 필터 / choices[('column명', '출력텍스트')] ->상품 등록 페이지에서 카테고리 선택 시 집적 입력 대신 선택 가능
    gender = models.CharField(max_length=10, choices=[('men', '남자'), ('women', '여자')], null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    tpo = models.CharField(max_length=20, choices=[('campus', '캠퍼스'), ('date', '데이트'), ('wedding', '하객룩(웨딩룩)'), ('daily', '데일리')], null=True, blank=True)
    season = models.CharField(max_length=20, choices=[('spring', '봄'), ('summer', '여름'), ('autumn', '가을'), ('winter', '겨울')], null=True, blank=True)
    mood = models.CharField(max_length=20, choices=[('street', '스트릿'), ('casual', '캐주얼'), ('minimal', '미니멀'), ('amekaji', '아메카지'), ('feminine', '페미닌'), ('business', '비즈니스')], null=True, blank=True)

    def __str__(self):
        return self.title
    


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.TextField() # mypage에서 위치 검색 후 위치정보 저장
    donation = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # 기부한 금액
    mileage = models.DecimalField(max_digits=10, decimal_places=2,default=0.00) # 마일리지 (기부금 10,000원 당 1,000원)


    def __str__(self):
        return self.user.username
    

# 결제 완료 후 Rental 인스턴스 생성 및 저장
class Rental(models.Model):   # 대여 정보
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rent_date = models.DateField()
    return_date = models.DateField()

    def __str__(self):
        return f'{self.post.title} rented by {self.userprofile.user.username}'



# User 모델의 인스턴스가 생성될 때, 자동으로 UserProfile 인스턴스도 생성되도록 신호를 설정
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()






'''
CharField : 길이 제한 텍스트
TextField : 길이 제한 없는 텍스트
DateTimeField : 날짜와 시간 관계 속성

Django Model Field 
https://velog.io/@qlgks1/Django-Model-%ED%95%84%EB%93%9Cfiled-%EB%AA%A8%EC%9D%8C%EC%A7%91

Django DB 조회/수정 (use shell)
https://velog.io/@devzunky/TIL-no.66-Django-Basic-19-%EB%8D%B0%EC%9D%B4%ED%84%B0-%EC%A1%B0%ED%9A%8C%ED%95%98%EA%B8%B0

https://velog.io/@celeste/Django-C.R.U.D

'''   