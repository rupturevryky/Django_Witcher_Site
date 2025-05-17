from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Witcher(models.Model):
    SCHOOL_CHOICES = [
        ('wolf', 'Школа Волка'),
        ('cat', 'Школа Кота'),
        ('bear', 'Школа Медведя'),
        ('griffin', 'Школа Грифона'),
        ('viper', 'Школа Гадюки'),
    ]

    name = models.CharField(max_length=100, verbose_name="Имя")
    school = models.CharField(
        max_length=20, choices=SCHOOL_CHOICES, verbose_name="Школа")
    signs = models.JSONField(default=list, verbose_name="Знаки")
    toxicity = models.IntegerField(default=0, verbose_name="Токсичность")
    vitality = models.IntegerField(default=100, verbose_name="Жизненная сила")
    stamina = models.IntegerField(default=100, verbose_name="Выносливость")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ведьмак"
        verbose_name_plural = "Ведьмаки"


class AlchemyItem(models.Model):
    TYPE_CHOICES = [
        ('potion', 'Зелье'),
        ('bomb', 'Бомба'),
        ('oil', 'Масло'),
        ('decoction', 'Отвар'),
    ]

    name = models.CharField(max_length=100, verbose_name="Название")
    type = models.CharField(
        max_length=20, choices=TYPE_CHOICES, verbose_name="Тип")
    toxicity = models.IntegerField(default=0, verbose_name="Токсичность")
    description = models.TextField(verbose_name="Описание")
    ingredients = models.JSONField(default=list, verbose_name="Ингредиенты")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Алхимический предмет"
        verbose_name_plural = "Алхимические предметы"


class SchoolUser(models.Model):
    SCHOOL_CHOICES = [
        ('wolf', 'Школа Волка'),
        ('viper', 'Школа Гадюки'),
        ('griffin', 'Школа Грифона'),
    ]

    RANK_CHOICES = [
        ('novice', 'Новичок'),
        ('master', 'Мастер'),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Пользователь")
    school = models.CharField(
        max_length=20, choices=SCHOOL_CHOICES, verbose_name="Школа")
    rank = models.CharField(
        max_length=20, choices=RANK_CHOICES, default='novice', verbose_name="Ранг")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_school_display()}"

    class Meta:
        verbose_name = "Пользователь школы"
        verbose_name_plural = "Пользователи школ"


class Monster(models.Model):
    TYPE_CHOICES = [
        ('necrophage', 'Некрофаг'),
        ('specter', 'Призрак'),
        ('vampire', 'Вампир'),
        ('elemental', 'Элементаль'),
        ('hybrid', 'Гибрид'),
        ('draconid', 'Драконид'),
        ('insectoid', 'Насекомое'),
        ('cursed', 'Проклятый'),
        ('relict', 'Реликт'),
    ]

    WEAKNESS_CHOICES = [
        ('silver', 'Серебро'),
        ('igni', 'Игни'),
        ('aard', 'Аард'),
        ('quen', 'Квен'),
        ('yrden', 'Ирден'),
        ('axii', 'Аксий'),
        ('dimeritium', 'Диммерит'),
        ('moon_dust', 'Лунная пыль'),
        ('devil_puffball', 'Чертова поганка'),
    ]

    name = models.CharField(max_length=100, verbose_name="Название")
    type = models.CharField(
        max_length=20, choices=TYPE_CHOICES, verbose_name="Тип")
    weaknesses = models.JSONField(default=list, verbose_name="Слабости")
    description = models.TextField(verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Монстр"
        verbose_name_plural = "Монстры"


class Contract(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активный'),
        ('completed', 'Выполнен'),
        ('failed', 'Провален'),
    ]

    monster = models.ForeignKey(
        Monster, on_delete=models.CASCADE, verbose_name="Монстр")
    reward = models.IntegerField(verbose_name="Вознаграждение")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="Статус")
    completed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Выполнил")
    completed_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Дата выполнения")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Контракт на {self.monster.name} - {self.get_status_display()}"

    class Meta:
        verbose_name = "Контракт"
        verbose_name_plural = "Контракты"


class Equipment(models.Model):
    SLOT_CHOICES = [
        ('sword', 'Меч'),
        ('armor', 'Броня'),
        ('boots', 'Ботинки'),
        ('gloves', 'Перчатки'),
        ('pants', 'Штаны'),
    ]

    name = models.CharField(max_length=100, verbose_name="Название")
    slot = models.CharField(
        max_length=20, choices=SLOT_CHOICES, verbose_name="Слот")
    description = models.TextField(verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_slot_display()})"

    class Meta:
        verbose_name = "Снаряжение"
        verbose_name_plural = "Снаряжение"


class Quest(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активный'),
        ('completed', 'Завершен'),
        ('failed', 'Провален'),
    ]

    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="Статус")
    reward = models.IntegerField(verbose_name="Вознаграждение")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

    class Meta:
        verbose_name = "Квест"
        verbose_name_plural = "Квесты"
