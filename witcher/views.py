from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from datetime import datetime, timedelta
import csv

from .models import SchoolUser, Monster, Contract, Equipment, Quest
from .forms import UserRegistrationForm, SchoolLoginForm
from .decorators import school_required, rank_required

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            school = form.cleaned_data.get('school')
            SchoolUser.objects.create(user=user, school=school)
            messages.success(
                request, 'Регистрация успешна! Теперь вы можете войти.')
            return redirect('witcher:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'witcher/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = SchoolLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            school = form.cleaned_data.get('school')
            user = authenticate(username=username, password=password)

            if user is not None:
                try:
                    school_user = user.schooluser
                    if school_user.school == school:
                        login(request, user)
                        messages.success(
                            request, f'Добро пожаловать в {school_user.get_school_display()}!')
                        return redirect('witcher:profile')
                    else:
                        messages.error(request, 'Неверная школа')
                except SchoolUser.DoesNotExist:
                    messages.error(
                        request, 'Вы не принадлежите ни к одной школе')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль')
    else:
        form = SchoolLoginForm()
    return render(request, 'witcher/login.html', {'form': form})


@login_required
def witcher_profile(request):
    try:
        school_user = request.user.schooluser
        witcher = {
            'name': request.user.username,
            'school': school_user.get_school_display(),
            'signs': ['Игни', 'Аард', 'Квен', 'Ирден', 'Аксий'],
            'toxicity': 45,
            'vitality': 85,
            'stamina': 90
        }
        return render(request, 'witcher/profile.html', {'witcher': witcher})
    except SchoolUser.DoesNotExist:
        messages.error(request, "Вы не принадлежите ни к одной школе")
        return redirect('witcher:login')


@school_required(['wolf'])
def kaermorhen(request):
    return render(request, 'witcher/kaermorhen.html', {
        'title': 'Кэр Морхен',
        'description': 'Древняя крепость Школы Волка, расположенная в горах Каэдвен. Здесь ведьмаки Школы Волка проходят обучение и тренировки.'
    })


@school_required(['viper'])
def gorthur_gvaed(request):
    return render(request, 'witcher/kaermorhen.html', {
        'title': 'Гортхур Гваэд',
        'description': 'Секретная база Школы Гадюки, расположенная в Нильфгаарде. Здесь обучаются элитные убийцы и шпионы.'
    })


@school_required(['griffin'])
def erlenwald(request):
    return render(request, 'witcher/kaermorhen.html', {
        'title': 'Эрленвальд',
        'description': 'Древняя крепость Школы Грифона, расположенная в горах Каэдвен. Известна своей обширной библиотекой и исследованиями в области магии.'
    })


def alchemy_items(request):
    # Тестовые данные для алхимии
    potions = [
        {
            'name': 'Чёрная кровь',
            'toxicity': 35,
            'description': 'Увеличивает урон по вампирам и делает вашу кровь ядовитой для них.'
        },
        {
            'name': 'Кот',
            'toxicity': 25,
            'description': 'Улучшает ночное зрение.'
        },
        {
            'name': 'Гром',
            'toxicity': 15,
            'description': 'Увеличивает урон от знаков.'
        }
    ]

    # Фильтрация по токсичности
    toxicity_threshold = request.GET.get('toxicity', 0)
    try:
        toxicity_threshold = int(toxicity_threshold)
    except ValueError:
        toxicity_threshold = 0

    filtered_potions = [
        p for p in potions if p['toxicity'] > toxicity_threshold]

    return render(request, 'witcher/alchemy.html', {
        'potions': filtered_potions,
        'toxicity_threshold': toxicity_threshold
    })


@rank_required('master')
def contracts(request):
    # Создаем тестовые данные, если их нет
    if not Contract.objects.exists():
        monsters = Monster.objects.all()
        if not monsters.exists():
            # Создаем тестового монстра, если нет ни одного
            monster = Monster.objects.create(
                name="Стрыга",
                type="vampire",
                weaknesses=["silver", "igni"],
                description="Опасный вампир, питающийся человеческой кровью"
            )
            monsters = [monster]

        # Создаем тестовые контракты
        for i, monster in enumerate(monsters):
            status = 'completed' if i % 2 == 0 else 'active'
            completed_by = request.user if status == 'completed' else None
            completed_at = datetime.now() - timedelta(days=i) if status == 'completed' else None

            Contract.objects.create(
                monster=monster,
                reward=1000 + (i * 100),
                status=status,
                completed_by=completed_by,
                completed_at=completed_at
            )

    contracts = Contract.objects.all().order_by('-created_at')
    return render(request, 'witcher/contracts.html', {
        'contracts': contracts
    })


@rank_required('master')
def generate_report(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contracts_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Монстр', 'Награда', 'Статус', 'Дата выполнения'])

    contracts = Contract.objects.filter(status='completed')
    for contract in contracts:
        writer.writerow([
            contract.monster.name,
            contract.reward,
            contract.get_status_display(),
            contract.completed_at.strftime(
                '%Y-%m-%d %H:%M:%S') if contract.completed_at else ''
        ])

    return response


def calculate_total_gold(contracts):
    return contracts.filter(status='completed').aggregate(total=Sum('reward'))['total'] or 0


@login_required
def witcher_stats(request):
    # Получаем текущее снаряжение из сессии или создаем тестовые данные
    equipment = request.session.get('equipment', {
        'sword': 'Серебряный меч',
        'armor': 'Броня Грифона',
        'boots': 'Сапоги ведьмака'
    })

    # Получаем уровень токсичности
    toxicity = request.session.get('toxicity', 45)

    # Получаем активные квесты
    active_quests = Quest.objects.filter(status='active')

    # Если нет активных квестов, создаем тестовые
    if not active_quests.exists():
        Quest.objects.create(
            name="Охота на стрыгу",
            description="Уничтожить стрыгу, терроризирующую деревню",
            status="active",
            reward=1000
        )
        Quest.objects.create(
            name="Проклятие леса",
            description="Снять проклятие с древнего леса",
            status="active",
            reward=1500
        )
        active_quests = Quest.objects.filter(status='active')

    # Получаем общее количество золота
    total_gold = calculate_total_gold(Contract.objects.all())

    return render(request, 'witcher/stats.html', {
        'equipment': equipment,
        'toxicity': toxicity,
        'active_quests': active_quests,
        'total_gold': total_gold
    })
