from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django import forms
from .models import BlogPost

# 表单类直接写在视图文件中，无需单独forms.py
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'text']
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}

# 主页：展示所有博文
def index(request):
    posts = BlogPost.objects.order_by('-date_added')
    return render(request, 'index.html', {'posts': posts})

# 新增/编辑博文：复用一个视图处理
@login_required
def post_edit(request, post_id=None):
    # 编辑模式：获取博文并校验权限；新增模式：新建空对象
    post = get_object_or_404(BlogPost, id=post_id) if post_id else None
    if post and post.owner != request.user:
        return redirect('index')

    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user  # 关联用户
            new_post.save()
            return redirect('index')
    else:
        form = BlogPostForm(instance=post)

    return render(request, 'post_form.html', {'form': form, 'post': post})
