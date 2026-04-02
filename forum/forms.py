from django import forms
from django.contrib.auth.models import User
from .models import Post, Reply, Category, UserProfile


class PostForm(forms.ModelForm):
    """发帖表单"""
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入帖子标题（5-200 字符）',
                'maxlength': 200,
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '请输入帖子内容（支持 Markdown 语法）',
                'rows': 10,
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),
        }
    
    def clean_title(self):
        """验证标题"""
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError('标题长度不能少于 5 个字符')
        if len(title) > 200:
            raise forms.ValidationError('标题长度不能超过 200 个字符')
        return title
    
    def clean_content(self):
        """验证内容"""
        content = self.cleaned_data.get('content')
        if len(content.strip()) == 0:
            raise forms.ValidationError('帖子内容不能为空')
        return content


class ReplyForm(forms.ModelForm):
    """回复表单"""
    
    class Meta:
        model = Reply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '请输入回复内容...',
                'rows': 4,
            }),
        }
    
    def clean_content(self):
        """验证内容"""
        content = self.cleaned_data.get('content')
        if len(content.strip()) == 0:
            raise forms.ValidationError('回复内容不能为空')
        return content


class UserProfileForm(forms.ModelForm):
    """用户资料编辑表单"""
    
    class Meta:
        model = UserProfile
        fields = ['signature', 'bio']
        widgets = {
            'signature': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '个人签名（255 字符以内）',
                'maxlength': 255,
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '个人简介',
                'rows': 5,
            }),
        }