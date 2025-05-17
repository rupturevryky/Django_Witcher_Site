from django.core.management.base import BaseCommand, CommandError
from witcher.models import Monster
import json


class Command(BaseCommand):
    help = 'Управление бестиарием монстров'

    def add_arguments(self, parser):
        parser.add_argument('action', type=str,
                            help='Действие (add/delete/search)')
        parser.add_argument('--name', type=str, help='Название монстра')
        parser.add_argument('--type', type=str, help='Тип монстра')
        parser.add_argument('--weaknesses', type=str,
                            help='Слабости монстра (через запятую)')
        parser.add_argument('--description', type=str, help='Описание монстра')
        parser.add_argument('--weakness', type=str, help='Слабость для поиска')

    def handle(self, *args, **options):
        action = options['action'].lower()

        if action == 'add':
            self.add_monster(options)
        elif action == 'delete':
            self.delete_monster(options)
        elif action == 'search':
            self.search_monsters(options)
        else:
            raise CommandError(
                'Неизвестное действие. Используйте add, delete или search.')

    def add_monster(self, options):
        if not all([options['name'], options['type'], options['weaknesses'], options['description']]):
            raise CommandError(
                'Для добавления монстра необходимы все параметры: --name, --type, --weaknesses, --description')

        try:
            weaknesses = [w.strip() for w in options['weaknesses'].split(',')]
            monster = Monster.objects.create(
                name=options['name'],
                type=options['type'],
                weaknesses=weaknesses,
                description=options['description']
            )
            self.stdout.write(self.style.SUCCESS(
                f'Монстр "{monster.name}" успешно добавлен'))
        except Exception as e:
            raise CommandError(f'Ошибка при добавлении монстра: {str(e)}')

    def delete_monster(self, options):
        if not options['name']:
            raise CommandError(
                'Для удаления монстра необходимо указать --name')

        try:
            monster = Monster.objects.get(name=options['name'])
            monster.delete()
            self.stdout.write(self.style.SUCCESS(
                f'Монстр "{options["name"]}" успешно удален'))
        except Monster.DoesNotExist:
            raise CommandError(f'Монстр "{options["name"]}" не найден')
        except Exception as e:
            raise CommandError(f'Ошибка при удалении монстра: {str(e)}')

    def search_monsters(self, options):
        if not options['weakness']:
            raise CommandError(
                'Для поиска монстров необходимо указать --weakness')

        try:
            monsters = Monster.objects.filter(
                weaknesses__contains=[options['weakness']])
            if monsters:
                self.stdout.write(self.style.SUCCESS(
                    f'Найдены монстры, уязвимые к {options["weakness"]}:'))
                for monster in monsters:
                    self.stdout.write(
                        f'\n{monster.name} ({monster.get_type_display()})')
                    self.stdout.write(
                        f'Слабости: {", ".join(monster.weaknesses)}')
                    self.stdout.write(f'Описание: {monster.description}')
            else:
                self.stdout.write(self.style.WARNING(
                    f'Монстры, уязвимые к {options["weakness"]}, не найдены'))
        except Exception as e:
            raise CommandError(f'Ошибка при поиске монстров: {str(e)}')
