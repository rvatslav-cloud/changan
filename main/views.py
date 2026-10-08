
from django.shortcuts import render, get_object_or_404, redirect
from django.http import  HttpResponse, JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.contrib import messages
from django.urls import reverse_lazy, reverse


from django.views.generic import TemplateView, ListView, DetailView

from .forms import ReviewForm, AppForm, RegisterForm
from .models import App, Review, Category
# Create your views here.

SORTS = {
    'new' : '-created_at',
    'name' : 'name',
    'price' : 'price',
    'expensive' : '-price',
}

class IndexView(ListView):
    model = App
    template_name = 'main/index.html'
    context_object_name = 'apps'
    paginate_by = 3

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        sort = self.request.GET.get('sort', '')

        if not sort:
            sort = 'name' if q else 'new'

        if q:
            apps = App.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))
        else:
            apps = App.objects.all()

        return apps.select_related('author').order_by(SORTS.get(sort, '-сreated_at'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        context['sort'] = self.request.GET.get('sort', '')
        context['featured'] = App.objects.order_by('-price').first()
        return context


class AboutView(TemplateView):
    template_name = 'main/about.html'


@require_GET
def reviews(request):
    all_reviews = Review.objects.order_by('-created_at').all()
    return render(request, 'main/reviews.html',{
        'reviews' : all_reviews,
    })


class AppDetailView(DetailView):
    model = App
    template_name = 'main/app_detail.html'
    context_object_name = 'app'
    pk_url_kwarg = 'app_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app = self.object
        context['similar_by_price'] = App.objects.filter(
            price__gte = app.price - 30,
            price__lte=app.price + 30,
        ).exclude(id=app.id)[:3]
        form = ReviewForm()
        if self.request.user.is_authenticated and 'username' in form.fields:
            form.fields.pop('username')
        context['form'] = form
        context['reviews'] = app.reviews.all()
        context['is_favorite'] = (
                self.request.user.is_authenticated
                and app.favorited_by.filter(pk=self.request.user.pk).exists()
        )
        return context


@require_GET
def category_detail(request,category_id):
    category = get_object_or_404(Category, id =category_id)
    q = request.GET.get('q', '')
    apps = App.objects.filter(category=category)
    if q:
        apps = apps.filter(Q(name__icontains=q) | Q(description__icontains=q)).order_by('name')
    else:
        apps = apps.order_by('-created_at')

    paginator = Paginator(apps,4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    most_expensive = apps.order_by('-price').first()
    return render(request, 'main/category.html', {
        'category' : category,
        'page_obj' : page_obj,
        'most_expensive': most_expensive,
        'q' : q,
    })


@require_GET
def free_apps(request):
    apps = App.objects.filter(price=0).order_by('-created_at')
    return render(request, 'main/free.html',{'apps' : apps,})


@require_GET
def new(request):
    apps =App.objects.order_by('-created_at').all()

    paginator = Paginator(apps,3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main/new.html',{'page_obj' : page_obj})


@require_GET
def top_paid(request):
    apps = App.objects.filter(price__gt=0).order_by('-price')[:10]
    return render(request,'main/top.html',{'apps' : apps})

@require_GET
def no_category(request):
    apps = App.objects.filter(category=None)
    return render(request,'main/no_category.html',{'apps' : apps})

@require_GET
def free_in_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    apps = App.objects.filter(category=category, price=0)
    return render(request, 'main/free_in_category.html', {
        'category': category,
        'apps': apps,
    })

@require_GET
def cheap_apps(request):
    apps = App.objects.filter(price__lt = 100,price__gt = 0).order_by('price')
    return render(request,'main/cheap.html',{'apps' : apps})

@require_GET
def app_detail_with_app_name(request, app_id, app_name):
    print(f"Название из Url: {app_name}")
    app = get_object_or_404(App, id=app_id)

    if app_name != app.name:
        return redirect('main:app_detail_with_app_name', app_id=app.id, app_name=app.name)

    similar_by_price = App.objects.filter(
        price__gte=app.price - 30,
        price__lte=app.price + 30,
    ).exclude(id=app.id)[:3]
    return render(request, 'main/app_detail.html', {
        'app': app,
        'similar_by_price': similar_by_price,
    })
@require_GET
def apps_list(request, is_free):
    if is_free:
        apps = App.objects.filter(price=0)
        title = 'Бесплатные приложения'
    else:
        apps = App.objects.filter(price__gt=0)
        title = 'Платные приложения'

    return render(request, 'main/apps_list.html', {
        'apps': apps,
        'title': title,
    })


@require_GET
def app_json(request, app_id):
    app = get_object_or_404(App, id=app_id)
    data = {
        'id': app.id,
        'name' : app.name,
        'description' : app.description,
        'price' : float(app.price),
        'downloads' : app.downloads,
        'category': app.category.name if app.category else None,
        'created_at' : app.created_at.strftime('%Y-%m-%d %H:%M:%S'),
    }
    return JsonResponse(data)


@require_POST
def add_review(request, app_id):
    app = get_object_or_404(App, id=app_id)
    data = request.POST.copy()
    if request.user.is_authenticated:
        data['username'] = request.user.username
    form = ReviewForm(data)

    if form.is_valid():
        review = form.save(commit=False)
        review.app = app
        review.save()
        messages.success(request, 'Отзыв сохранён.')
        return redirect('main:app_detail', app_id=app.id)

    if request.user.is_authenticated and 'username' in form.fields:
        form.fields.pop('username')
    reviews = app.reviews.all()
    similar_by_price = App.objects.filter(
        price__gte=app.price - 30,
        price__lte=app.price + 30,
    ).exclude(id=app.id)[:3]
    return render(request, 'main/app_detail.html', {
        'app': app,
        'form': form,
        'reviews': reviews,
        'similar_by_price': similar_by_price,
        'is_favorite':(
            request.user.is_authenticated
            and app.favorited_by.filter(pk=request.user.pk).exists()
        ),
    })


@login_required
def add_app(request):
    if request.method == 'POST':
        form = AppForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.author = request.user
            app.save()
            messages.success(request, f'Приложение {app.name} опубликовано.')
            return redirect('main:app_detail', app_id=app.id)
    else:
        form = AppForm()
    return render(request,'main/add_app.html', {'form' : form})


def register(request):
    if request.user.is_authenticated:
        return redirect('main:index')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request,f"Добро пожаловать, { user.username }. Ваш аккаунт создан!")
            return redirect('main:index')
    else:
        form = RegisterForm()
    return render(request, 'main/register.html',{'form' : form})

class StoreLoginView(LoginView):
    template_name = 'main/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"С возвращением,{ self.request.user.username }!")
        return response


class StoreLogoutView(LogoutView):
    next_page = reverse_lazy('main:index')


@login_required
def my_apps(request):
    apps = App.objects.filter(author=request.user).order_by('-created_at')
    return render(request,'main/my_apps.html', {'apps' : apps})


@login_required
def edit_app(request, app_id):
    app = get_object_or_404(App, id=app_id)
    if not (
            request.user.has_perm('main.change_app')
            or request.user.is_staff
            or app.author_id == request.user.id
    ):
        messages.error(request, 'Редактировать карточку может только её автор.')
        return redirect('main:app_detail', app_id=app.id)

    if request.method =='POST':
        form = AppForm(request.POST,request.FILES, instance=app)
        if form.is_valid():
            form.save()
            messages.success(request, f'Карточка {app.name} обновлена.')
            return redirect('main:app_detail', app_id=app.id)
    else:
        form = AppForm(instance=app)
    return render(request, 'main/edit_app.html', {'form' : form, 'app' : app})


class StorePasswordResetView(PasswordResetView):
    template_name = 'main/password_reset_form.html'
    email_template_name = 'main/password_reset_email.html'
    subject_template_name = 'main/password_reset_subject.txt'
    success_url = reverse_lazy('main:password_reset_done')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['email'].label = 'Электронная почта'
        return form

class StorePasswordResetDoneView(PasswordResetDoneView):
    template_name = 'main/password_reset_done.html'

class StorePasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'main/password_reset_confirm.html'
    success_url = reverse_lazy('main:password_reset_complete')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if form is not None and 'new_password1' in form.fields:
            form.fields['new_password1'].label = 'Новый пароль'
            form.fields['new_password2'].label = 'Повтор пароля'
        return form

class StorePasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'main/password_reset_complete.html'

@login_required
def favorites(request):
    apps = (
        request.user.favorite_apps
        .select_related('category','author')
        .order_by('name')
    )
    return render(request, 'main/favorites.html', {'apps' : apps})

@require_POST
def toggle_favorite(request, app_id):
    app = get_object_or_404(App, id=app_id)
    if not request.user.is_authenticated:
        login_url = reverse('main:login')
        next_url = reverse('main:app_detail', args=[app.id])
        return redirect(f'{login_url}?next={next_url}')
    if app.favorited_by.filter(pk=request.user.pk).exists():
        app.favorited_by.remove(request.user)
        messages.success(request, f'{app.name} убрано из Избранного.')
    else:
        app.favorited_by.add(request.user)
        messages.success(request, f'{app.name} в Избранном.')
    return redirect('main:app_detail', app_id=app.id)

