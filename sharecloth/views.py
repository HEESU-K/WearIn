from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages

from .forms import PostForm
from .forms import PostFilterForm

# 모델 임포트
from .models import Post, UserProfile, Rental

from django.contrib.auth.decorators import login_required

from django.urls import reverse
from decimal import Decimal

import datetime


def index(request):  # 사이트 접속 시 바로 보이는 메인 페이지
    # templates/clothshare/base_view.html
    posts = Post.objects.all() # 모든 post 모델의 객체를 가져옴
    
    context = context = {
        'posts': posts,
    }

    return render(request, 'clothshare/base_view.html', context)



@login_required
def my_page(request):
    user = request.user
    UserInfo = UserProfile.objects.filter(user=user).first()  # UserProfile 인스턴스를 가져옴
    post = Post.objects.filter(user=request.user)
   
    address = UserInfo.address if UserInfo else '등록된 주소가 없습니다.'  # 주소 정보가 없는 경우 대비 

    user_profile = UserProfile.objects.get(user=request.user)
    
    # 현재 대여 중인 상품을 가져옴
    rented_items = Rental.objects.filter(userprofile=user_profile).order_by('-rent_date')

    # 반납까지 남은 날짜 계산을 위한 코드
    today = datetime.date.today()
    for item in rented_items:
        item.remaining_days = (item.return_date - today).days

    context = { 'post': post,
                'user':user,
                'user_address': address,
                'rented_items': rented_items
    }  # 템플릿으로 전달할 컨텍스트

    return render(request, 'my_page/my_page.html', context)
    # {'user': user} 처럼 특정 모델의 필드를 템플릿에서 출력하기 위해서는
    # 해당 정보를 context에 추가하여 템플릿으로 전달해야 함.


# 반납 시 해당 포스트 Rental DB에서 삭제
def return_items(request, rental_id):
    rental = Rental.objects.get(id=rental_id)
    rental.delete()

    return redirect(reverse('sharecloth:mypage'))
    

@login_required
def post_create(request): # 제품 등록 페이지
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user # 현재 로그인한 사용자를 게시물 작성자로 설정
            post.save()
            return redirect('sharecloth:main')  # 등록 후 리디렉션 될 페이지
    else:
        form = PostForm()
    return render(request, 'clothshare/post_create.html', {'form': form})


def post_detail(request, pk): # 메인 페이지에서 포스트를 누르면 상세 페이지로 이동
    posts = None
    # pk를 사용해서 특정 post 객체를 가져옴
    posts = get_object_or_404(Post, pk=pk)
    address = posts.address
    context = {
        'address': address,
        'posts': posts
    }
    return render(request, 'clothshare/post_detail.html', context)


@login_required
def update_address(request): # mypage 위치검색에서 위치 등록
    if request.method == 'POST':
        user = request.user
        address = request.POST.get('location')
        
        # Userinfo 인스턴스를 가져오거나 없으면 새로 생성
        userinfo, created = UserProfile.objects.get_or_create(user=user)
        # get_or_create 메서드는 객체와 생섯 여부를 나타내는 튜플 반환 -> 반환된 값에서 객체를 추출해야 함
        
        # address 필드 업데이트
        userinfo.address = address
        userinfo.save()
        
        return redirect('sharecloth:mypage')
    else:
        return render(request, 'error.html')
    

@login_required
def donation_page(request): # 도네이션 페이지 기부 진행바
    user = request.user
    user_profile = UserProfile.objects.get(user=request.user)
    
    donation = user_profile.donation
    mileage = user_profile.mileage
    
    # 사용자의 mileage 보다 price가 낮거나 같은 Post 객체들을 가져옴
    available_posts = Post.objects.filter(price__lte=user_profile.mileage)
    # 마일리지 전환까지 남은 기부금 (10,000-현재 donation)
    remaining_amount = 10000 - donation

    progress_percentage = (user_profile.donation / 10000) * 100
    context = {
        'user': user,
        'user_profile': user_profile,
        'progress_percentage': progress_percentage,
        'donation': donation,
        'mileage': mileage,
        'available_posts': available_posts,
        'remaining_amount': remaining_amount
    }
    
    return render(request, 'donation/donation.html', context)


@login_required
def convert_donation_to_mileage(request): # 기부 금액 마일리지로 전환
    user_profile = UserProfile.objects.get(user=request.user)
    donation_amount = user_profile.donation

    if donation_amount >= 10000:
        mileage_to_add = donation_amount * Decimal(str(0.05)) # 도네이션값이 10000이상일 때 기부금 5%를 마일리지로 누적
        user_profile.mileage += mileage_to_add
        user_profile.donation = 0 # 마일리지 누적 후 기부금 초기화
        user_profile.save()
        messages.success(request, "마일리지가 성공적으로 적립되었습니다.")
    else:
        messages.error(request, "기부금이 10,000원 이상이어야 마일리지 적립이 가능합니다.")
    
    return redirect('sharecloth:donation_page')


def search_results(request): # 헤더의 검색 기능
    query = request.GET.get('q')
    if query:
        results = Post.objects.filter(title__icontains=query) # title에 검색어가 포함된 포스트 검색
    else:
        results = Post.objects.none() # 빈 쿼리셋 반환
    
    return render(request, 'clothshare/search_results.html', {'results': results})


def post_list(request): # 필터 내용을 기반으로 포스트 필터링
    form = PostFilterForm(request.GET)
    posts = Post.objects.all()

    if form.is_valid():
        if form.cleaned_data['gender']:
            posts = posts.filter(gender=form.cleaned_data['gender'])
        if form.cleaned_data['height']:
            posts = posts.filter(height=form.cleaned_data['height'])
        if form.cleaned_data['tpo']:
            posts = posts.filter(tpo=form.cleaned_data['tpo'])
        if form.cleaned_data['season']:
            posts = posts.filter(season=form.cleaned_data['season'])
        if form.cleaned_data['mood']:
            posts = posts.filter(mood=form.cleaned_data['mood'])

    return render(request, 'clothshare/post_list.html', {'form': form, 'posts': posts})


def payment_page(request, post_id): # 결제 페이지
    user_profile = get_object_or_404(UserProfile, user=request.user)
    post = get_object_or_404(Post, id=post_id) # 결제화면에서 상품 정보 표시 용도
    if request.method == 'POST': # 상세 페이지에서 달력으로 직접 입력한 날짜를 payment_page로 전달
        rent_date = request.POST.get('rent_date')
        return_date = request.POST.get('return_date')

        rental = Rental(post=post, userprofile=user_profile, rent_date=rent_date, return_date=return_date)
        rental.save()

        return render(request, 'clothshare/payment_page.html', {
            'post': post,
            'rent_date': rent_date,
            'return_date': return_date
        })
    return redirect('clothshare:post_detail', post_id=post_id)


# 결제 버튼 누른 후
def payment(request, post_id):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':

        # 결제가 성공적으로 완료되었다고 가정하고 donation 필드 업데이트
        user_profile.donation += 1000
        user_profile.save()

        #결제 성공 후 Rental 인스턴스 생성
        user_profile = UserProfile.objects.get(user=request.user)
        post = Post.objects.get(id=post_id)

        return redirect('sharecloth:mypage') # 결제 후 이동
    return redirect('sharecloth:mypage') # 결제 후 이동