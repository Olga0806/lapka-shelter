from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages

from .models import Animal, AnimalPhoto, Application
from .forms import AnimalForm, ApplicationForm, KinologApplicationForm, RegisterForm


def is_kinolog(user):
    return user.is_authenticated and user.is_staff


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('animal_list')
        messages.error(request, 'Неверный логин или пароль')
    return render(request, 'animals/login.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('profile')
    else:
        form = RegisterForm()
    return render(request, 'animals/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# ---------- Публичные ----------

def animal_list(request):
    q = request.GET.get('q', '').strip()
    species = request.GET.get('species', '')
    sort = request.GET.get('sort', '-created_at')

    animals = Animal.objects.all()
    if q:
        animals = animals.filter(Q(name__icontains=q) | Q(breed__icontains=q))
    if species:
        animals = animals.filter(species=species)

    allowed = ['name', '-name', 'age', '-age', 'created_at', '-created_at']
    if sort in allowed:
        animals = animals.order_by(sort)

    return render(request, 'animals/animal_list.html', {
        'animals': animals, 'q': q, 'species': species, 'sort': sort,
        'species_choices': Animal.SPECIES_CHOICES,
    })


def animal_detail(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    return render(request, 'animals/animal_detail.html', {'animal': animal})


# ---------- Клиент ----------

@login_required
def profile_view(request):
    apps = Application.objects.filter(user=request.user).select_related('animal')
    return render(request, 'animals/profile.html', {'applications': apps})


@login_required
def application_create(request, animal_pk):
    animal = get_object_or_404(Animal, pk=animal_pk)

    existing = Application.objects.filter(
        user=request.user, animal=animal, status__in=['new', 'approved']
    ).first()
    if existing:
        messages.info(request, 'У вас уже есть активная заявка на это животное.')
        return redirect('profile')

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.animal = animal
            obj.save()
            messages.success(request, 'Заявка отправлена!')
            return redirect('profile')
    else:
        form = ApplicationForm(initial={
            'full_name': request.user.first_name or '',
            'phone': request.user.last_name or '',
        })
    return render(request, 'animals/application_create.html',
                  {'form': form, 'animal': animal})


# ---------- Кинолог ----------

@login_required
@user_passes_test(is_kinolog, login_url='animal_list')
def animal_create(request):
    if request.method == 'POST':
        form = AnimalForm(request.POST)
        if form.is_valid():
            animal = form.save()
            for f in request.FILES.getlist('photos'):
                AnimalPhoto.objects.create(animal=animal, image=f)
            messages.success(request, 'Животное добавлено')
            return redirect('animal_detail', pk=animal.pk)
    else:
        form = AnimalForm()
    return render(request, 'animals/animal_form.html',
                  {'form': form, 'title': 'Добавить животное'})


@login_required
@user_passes_test(is_kinolog, login_url='animal_list')
def animal_update(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    if request.method == 'POST':
        form = AnimalForm(request.POST, instance=animal)
        if form.is_valid():
            form.save()
            for f in request.FILES.getlist('photos'):
                AnimalPhoto.objects.create(animal=animal, image=f)
            messages.success(request, 'Данные обновлены')
            return redirect('animal_detail', pk=animal.pk)
    else:
        form = AnimalForm(instance=animal)
    return render(request, 'animals/animal_form.html',
                  {'form': form, 'title': 'Редактировать животное',
                   'animal': animal})


@login_required
@user_passes_test(is_kinolog, login_url='animal_list')
def animal_delete(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    if request.method == 'POST':
        animal.delete()
        messages.success(request, 'Животное удалено')
        return redirect('animal_list')
    return render(request, 'animals/animal_confirm_delete.html', {'animal': animal})


@login_required
@user_passes_test(is_kinolog, login_url='animal_list')
def photo_delete(request, pk):
    photo = get_object_or_404(AnimalPhoto, pk=pk)
    aid = photo.animal_id
    photo.delete()
    return redirect('animal_update', pk=aid)


@login_required
@user_passes_test(is_kinolog, login_url='animal_list')
def application_list(request):
    status = request.GET.get('status', '')
    apps = Application.objects.select_related('animal', 'user').all()
    if status:
        apps = apps.filter(status=status)
    return render(request, 'animals/application_list.html', {
        'applications': apps, 'status': status,
        'status_choices': Application.STATUS_CHOICES,
    })


@login_required
@user_passes_test(is_kinolog, login_url='animal_list')
def application_update(request, pk):
    obj = get_object_or_404(Application, pk=pk)
    if request.method == 'POST':
        form = KinologApplicationForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Заявка обновлена')
            return redirect('application_list')
    else:
        form = KinologApplicationForm(instance=obj)
    return render(request, 'animals/application_form.html',
                  {'form': form, 'app_obj': obj})


@login_required
@user_passes_test(is_kinolog, login_url='animal_list')
def application_delete(request, pk):
    obj = get_object_or_404(Application, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Заявка удалена')
        return redirect('application_list')
    return render(request, 'animals/animal_confirm_delete.html',
                  {'animal': obj.animal, 'app_obj': obj})