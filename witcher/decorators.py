from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

from witcher.models import SchoolUser


def school_required(allowed_schools):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "Требуется авторизация")
                return redirect('witcher:login')

            try:
                school_user = request.user.schooluser
                if school_user.school not in allowed_schools:
                    messages.error(
                        request, "У вас нет доступа к этой странице")
                    return redirect('witcher:profile')
            except SchoolUser.DoesNotExist:
                messages.error(request, "Вы не принадлежите ни к одной школе")
                return redirect('witcher:login')

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def rank_required(required_rank):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Необходима авторизация')
                return redirect('witcher:login')

            try:
                if request.user.schooluser.rank != required_rank:
                    rank_display = dict(SchoolUser.RANK_CHOICES)[required_rank]
                    messages.error(
                        request, f'Для доступа к этой странице требуется ранг: {rank_display}')
                    return redirect('witcher:profile')
            except SchoolUser.DoesNotExist:
                messages.error(request, 'Вы не принадлежите ни к одной школе')
                return redirect('witcher:login')
            except Exception as e:
                messages.error(request, f'Ошибка доступа: {str(e)}')
                return redirect('witcher:profile')

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
