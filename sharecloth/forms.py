from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['user', 'address']
        fields = ['item_num', 'image', 'title', 'content', 'can_land', 'price', 'thumbnail', 'publisher_name',
                  'gender', 'height', 'tpo', 'season', 'mood']
        widgets = {
            'gender': forms.Select(choices=Post.gender, attrs={'class': 'form-control'}),
            'tpo': forms.Select(choices=Post.tpo, attrs={'class': 'form-control'}),
            'season': forms.Select(choices=Post.season, attrs={'class': 'form-control'}),
            'mood': forms.Select(choices=Post.mood, attrs={'class': 'form-control'}),
        } # post_detail.html 에서  {{ form.as_p }} 로 값을 입력받기 위한 폼

        labels = { # 상품 등록시 한글로 표시하기 위한 레이블 지정
            'item_num': '상품번호',
            'image': '사진 선택',
            'title': '게시물 제목',
            'content': '게시할 상품의 정보를 입력해 주세요',
            'can_land': '대여 가능 여부 (항상 체크헤주세요)',
            'price': '가격을 입력해주세요',
            'thumbnail': '썸네일로 사용될 사진을 선택해 주세요',
            'publisher_name': '이름을 입력해 주세요',
            'gender': '성별 입력',
            'height': '키 입력',
            'tpo': 'TPO',
            'season': '계절',
            'mood': 'MOOD',
        }

class PostFilterForm(forms.Form):
    gender = forms.ChoiceField(choices=[('male', '남자'), ('female', '여자')], required=False)
    height = forms.IntegerField(required=False)
    tpo = forms.CharField(max_length=50, required=False)
    season = forms.CharField(max_length=50, required=False)
    mood = forms.CharField(max_length=50, required=False)
