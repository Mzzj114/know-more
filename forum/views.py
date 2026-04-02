from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db.models import Q, Count

# DRF imports
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

# Models and Forms
from django.contrib.auth.models import User
from .models import Category, Post, Reply, Like, Favorite, UserProfile
from .forms import PostForm, ReplyForm, UserProfileForm
from .services import PostService, ReplyService, InteractionService
from .serializers import (
    CategorySerializer, PostSerializer, PostDetailSerializer,
    ReplySerializer, LikeSerializer, FavoriteSerializer
)


# ==================== Template Views（页面渲染）====================

def forum_index(request):
    """论坛首页 - 显示所有分类和热门帖子"""
    # Category 模型已经有 post_count 字段，直接使用即可
    categories = Category.objects.filter(is_active=True).order_by('order')
    
    # 最新帖子
    latest_posts = Post.objects.select_related('author', 'category').filter(
        is_hidden=False
    ).order_by('-last_reply_at', '-created_at')[:10]
    
    context = {
        'categories': categories,
        'latest_posts': latest_posts,
    }
    return render(request, 'forum/index.html', context)


def category_detail(request, slug):
    """分类详情页 - 显示该分类下的所有帖子"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    
    # 获取帖子列表（带分页）
    posts = Post.objects.select_related('author', 'category').filter(
        category=category,
        is_hidden=False
    ).order_by('-is_pinned', '-last_reply_at', '-created_at')
    
    paginator = Paginator(posts, 20)  # 每页 20 个帖子
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'forum/category.html', context)


def post_detail(request, pk):
    """帖子详情页"""
    post = get_object_or_404(Post.objects.select_related('author__profile'), pk=pk)
    
    # 增加浏览量
    PostService.increment_view_count(post)
    
    # 获取回复列表
    replies = post.replies.select_related('author__profile').filter(
        is_hidden=False
    ).order_by('created_at')
    
    # 检查当前用户是否已点赞/收藏
    user_liked = False
    user_favorited = False
    
    if request.user.is_authenticated:
        from django.contrib.contenttypes.models import ContentType
        user_liked = Like.objects.filter(
            user=request.user,
            content_type=ContentType.objects.get_for_model(post),
            object_id=post.id
        ).exists()
        
        user_favorited = Favorite.objects.filter(
            user=request.user,
            post=post
        ).exists()
    
    context = {
        'post': post,
        'replies': replies,
        'user_liked': user_liked,
        'user_favorited': user_favorited,
    }
    return render(request, 'forum/post_detail.html', context)


@login_required
def create_post(request):
    """创建新帖子"""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            try:
                post = PostService.create_post(
                    author=request.user,
                    title=form.cleaned_data['title'],
                    content=form.cleaned_data['content'],
                    category_id=form.cleaned_data['category'].id
                )
                messages.success(request, '帖子发布成功！')
                return redirect('forum:post_detail', pk=post.id)
            except Exception as e:
                messages.error(request, f'发布失败：{str(e)}')
        else:
            messages.error(request, '请检查表单填写是否正确')
    else:
        form = PostForm()
    
    context = {
        'form': form,
        'categories': Category.objects.filter(is_active=True),
    }
    return render(request, 'forum/create_post.html', context)


@login_required
def edit_post(request, pk):
    """编辑帖子"""
    post = get_object_or_404(Post, pk=pk)
    
    # 权限检查：只有作者可以编辑
    if request.user != post.author and not request.user.is_staff:
        messages.error(request, '您没有权限编辑此帖子')
        return redirect('forum:post_detail', pk=pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            try:
                PostService.update_post(
                    post=post,
                    title=form.cleaned_data['title'],
                    content=form.cleaned_data['content'],
                    category=form.cleaned_data['category']
                )
                messages.success(request, '帖子更新成功！')
                return redirect('forum:post_detail', pk=post.id)
            except Exception as e:
                messages.error(request, f'更新失败：{str(e)}')
        else:
            messages.error(request, '请检查表单填写是否正确')
    else:
        form = PostForm(instance=post)
    
    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'forum/edit_post.html', context)


@login_required
@require_http_methods(["POST"])
def delete_post(request, pk):
    """删除帖子"""
    post = get_object_or_404(Post, pk=pk)
    
    # 权限检查
    if request.user != post.author and not request.user.is_staff:
        messages.error(request, '您没有权限删除此帖子')
        return redirect('forum:post_detail', pk=pk)
    
    try:
        PostService.delete_post(post)
        messages.success(request, '帖子已删除')
    except Exception as e:
        messages.error(request, f'删除失败：{str(e)}')
    
    return redirect('forum:forum_index')


@login_required
@require_http_methods(["POST"])
def create_reply(request, post_pk):
    """创建回复"""
    post = get_object_or_404(Post, pk=post_pk)
    
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            try:
                reply = ReplyService.create_reply(
                    author=request.user,
                    post=post,
                    content=form.cleaned_data['content'],
                )
                messages.success(request, '回复成功！')
                return redirect('forum:post_detail', pk=post.id)
            except Exception as e:
                messages.error(request, f'回复失败：{str(e)}')
        else:
            messages.error(request, '请检查回复内容')
    
    return redirect('forum:post_detail', pk=post.id)


@login_required
def user_profile(request, username):
    """用户个人主页"""
    user = get_object_or_404(User.objects.select_related('profile'), username=username)
    
    # 用户的帖子
    user_posts = Post.objects.filter(author=user, is_hidden=False).order_by('-created_at')[:10]
    
    # 用户的回复
    user_replies = Reply.objects.filter(author=user, is_hidden=False).order_by('-created_at')[:10]
    
    context = {
        'profile_user': user,
        'user_posts': user_posts,
        'user_replies': user_replies,
    }
    return render(request, 'forum/user_profile.html', context)


@login_required
def my_favorites(request):
    """我的收藏"""
    favorites = InteractionService.get_user_favorites(request.user)
    
    paginator = Paginator(favorites, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'forum/my_favorites.html', context)


@login_required
def edit_profile(request):
    """编辑个人资料"""
    profile = request.user.profile
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, '个人资料更新成功！')
            return redirect('forum:user_profile', username=request.user.username)
        else:
            messages.error(request, '请检查表单填写是否正确')
    else:
        form = UserProfileForm(instance=profile)
    
    context = {'form': form}
    return render(request, 'forum/edit_profile.html', context)


# ==================== API Views（DRF）====================

@api_view(['GET'])
@permission_classes([AllowAny])
def api_category_list(request):
    """获取所有分类列表"""
    categories = Category.objects.filter(is_active=True).order_by('order')
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def api_post_list(request):
    """获取帖子列表（支持筛选和分页）"""
    category_slug = request.query_params.get('category')
    search = request.query_params.get('search')
    
    posts = Post.objects.select_related('author', 'category').filter(is_hidden=False)
    
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    
    if search:
        posts = posts.filter(
            Q(title__icontains=search) | Q(content__icontains=search)
        )
    
    posts = posts.order_by('-is_pinned', '-last_reply_at', '-created_at')
    
    # 分页
    paginator = Paginator(posts, 20)
    page_number = request.query_params.get('page', 1)
    page_posts = paginator.get_page(page_number)
    
    serializer = PostSerializer(page_posts, many=True)
    return Response({
        'results': serializer.data,
        'count': paginator.count,
        'has_next': page_posts.has_next(),
        'has_previous': page_posts.has_previous(),
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def api_post_detail(request, pk):
    """获取帖子详情"""
    post = get_object_or_404(Post.objects.select_related('author', 'category'), pk=pk)
    serializer = PostDetailSerializer(post)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_like_toggle(request, content_type, object_id):
    """切换点赞状态"""
    from django.contrib.contenttypes.models import ContentType
    
    try:
        ct = ContentType.objects.get_by_natural_key(*content_type.split('.'))
        obj = ct.get_object_for_this_type(pk=object_id)
        
        liked, updated_obj = InteractionService.toggle_like(request.user, obj)
        
        return Response({
            'success': True,
            'liked': liked,
            'like_count': updated_obj.like_count,
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_favorite_toggle(request, post_id):
    """切换收藏状态"""
    post = get_object_or_404(Post, pk=post_id)
    
    try:
        favorited = InteractionService.toggle_favorite(request.user, post)
        
        return Response({
            'success': True,
            'favorited': favorited,
            'favorite_count': post.favorite_count,
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_create_reply(request, post_id):
    """创建回复（API 方式）"""
    post = get_object_or_404(Post, pk=post_id)
    
    content = request.data.get('content', '').strip()
    if not content:
        return Response({
            'success': False,
            'error': '回复内容不能为空'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        reply = ReplyService.create_reply(
            author=request.user,
            post=post,
            content=content,
        )
        
        serializer = ReplySerializer(reply)
        return Response({
            'success': True,
            'reply': serializer.data,
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)