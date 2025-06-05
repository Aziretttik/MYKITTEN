from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test
from .forms import CatCreateForm, AdoptionRequestForm, CatForm
from .models import Cat, AdoptionRequest
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required

#Главная страница
def index_view(request):
    return render(request, 'main/index.html')


def is_staff(user):
    return user.is_staff


def is_admin(user):
    return user.is_superuser

# создание объекта кошки
@login_required
@user_passes_test(is_admin)
def create_cat(request):
    if request.method == 'POST':
        form = CatCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CatCreateForm()
    return render(request, 'main/create_cat.html', {'form': form})


def cat_catalog(request):
    search_query = request.GET.get('q', '')
    age_filter = request.GET.get('age', '')
    cats = Cat.objects.filter(is_adopted=False)

    if search_query:
        cats = cats.filter(
            Q(name__icontains=search_query) |  # поиск по имени
            Q(color__icontains=search_query) |  # поиск по окрасу
            Q(age__icontains=str(search_query))  # поиск по возрасту (преобразуем в строку)
        ).distinct()

    if age_filter:
        if age_filter == 'young':
            cats = cats.filter(age__lte=3)
        elif age_filter == 'adult':
            cats = cats.filter(age__gt=3, age__lte=6)
        elif age_filter == 'senior':
            cats = cats.filter(age__gt=6)


    paginator = Paginator(cats, 6)  # По 6 котиков на странице
    page_number = request.GET.get('page', 1)
    cats_page = paginator.get_page(page_number)

    return render(request,
                  'main/cat_catalog.html',
                  {
                      'cats': cats_page,
                      'search_query': search_query,
                      'age_filter': age_filter,
                  })


def cat_detail(request, cat_id):
    cat = get_object_or_404(Cat, id=cat_id)
    return render(request, 'main/cat_detail.html', {'cat': cat})


@login_required
def adopt_cat(request, cat_id):
    cat = get_object_or_404(Cat, id=cat_id)

    # Проверяем, не подавал ли пользователь уже заявку на этого кота
    existing_request = AdoptionRequest.objects.filter(
        user=request.user,
        cat=cat,
        status='pending'
    ).exists()

    if existing_request:
        messages.warning(request, 'Вы уже подали заявку на этого котика')
        return redirect('cat_detail', cat_id=cat_id)

    # Проверяем, не усыновлен ли уже кот
    if cat.is_adopted:
        messages.error(request, 'Извините, этот котик уже нашел свой дом')
        return redirect('cat_catalog')

    if request.method == 'POST':
        form = AdoptionRequestForm(request.POST)
        if form.is_valid():
            adoption = form.save(commit=False)
            adoption.user = request.user
            adoption.cat = cat
            adoption.status = 'pending'
            adoption.save()

            messages.success(request, 'Ваша заявка успешно отправлена! Мы свяжемся с вами после рассмотрения.')
            return redirect('cat_detail', cat_id=cat_id)
    else:
        form = AdoptionRequestForm()

    return render(request, 'main/adopt_cat.html', {'form': form, 'cat': cat})


@user_passes_test(is_staff)
def add_cat(request):
    if request.method == 'POST':
        form = CatForm(request.POST, request.FILES)
        if form.is_valid():
            cat = form.save()
            return redirect('cat_detail', cat.id)
    else:
        form = CatForm()
    return render(request, 'main/cat_form.html', {'form': form})


@user_passes_test(is_staff)
def edit_cat(request, cat_id):
    cat = get_object_or_404(Cat, id=cat_id)
    if request.method == 'POST':
        form = CatForm(request.POST, request.FILES, instance=cat)
        if form.is_valid():
            cat = form.save()
            return redirect('cat_detail', cat.id)
    else:
        form = CatForm(instance=cat)
    return render(request, 'main/cat_form.html', {'form': form, 'cat': cat})


@user_passes_test(is_staff)
def delete_cat(request, cat_id):
    cat = get_object_or_404(Cat, id=cat_id)
    cat.delete()
    return redirect('cat_catalog')


@user_passes_test(is_staff)
def toggle_adoption(request, cat_id):
    cat = get_object_or_404(Cat, id=cat_id)
    cat.is_adopted = not cat.is_adopted
    cat.save()
    return redirect('cat_detail', cat_id)

@staff_member_required
def adoption_requests(request):
    requests = AdoptionRequest.objects.all().order_by('-created_at')

    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        new_status = request.POST.get('status')

        if request_id and new_status:
            try:
                adoption_request = AdoptionRequest.objects.get(id=request_id)
                adoption_request.status = new_status

                # Если заявка одобрена
                if new_status == 'approved':
                    cat = adoption_request.cat
                    # Меняем статус кошки на "усыновлен"
                    cat.is_adopted = True
                    cat.save()

                    # Отклоняем все остальные заявки на эту кошку
                    AdoptionRequest.objects.filter(
                        cat=cat,
                        status='pending'
                    ).exclude(
                        id=adoption_request.id
                    ).update(
                        status='rejected'
                    )

                    messages.success(
                        request,
                        f'Заявка одобрена! Кошка {cat.name} помечена как усыновленная.'
                    )
                else:
                    messages.success(request, 'Статус заявки успешно обновлен')

                adoption_request.save()

            except AdoptionRequest.DoesNotExist:
                messages.error(request, 'Заявка не найдена')

        return redirect('adoption_requests')

    return render(request, 'main/adoption_requests.html', {'requests': requests})


@login_required
def my_adoption_requests(request):
    # Получаем только заявки текущего пользователя
    requests = AdoptionRequest.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'main/my_adoption_requests.html', {'requests': requests})

