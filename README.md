
Тестовое задание для компании MirGovorit.  
Выполнено в соответствии с ТЗ https://clck.ru/38Fwcb

## Начало работы:

1. Запустите миграции
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
2. Запустите проект

```bash
python manage.py runserver
```
## Администрирование проекта:
Доступ к админке сайта:

```bash
username: admin
password: admin
```
В случае проблем введите в директории /test_case_mirgovorot:
```bash
python manage.py createsuperuser
```
И следуйте инструкции в терминале.

## Документация API:
### Эндпоинт:  add_product/<recipe_id>/<product_id>/<weight>/
GET add_product/recipe_id>/product_id/weight>/
Обновляет/добавляет в существующий рецепт новый ингредиент или обновлеяет его количество.

### Эндпоинт:  cook_recipe/<recipe_id>/.
GET cook_recipe/<recipe_id>/

Пользователь готовит по выбранному рецепту. Поля продуктов обновляют свой счетчик.

### Эндпоинт:  show_recipes_without_product/<product_id>/
GET show_recipes_without_product/<product_id>/
Получить список всех рецептов, в которых нет этого продукта или его меньше, чем 10 г.  
