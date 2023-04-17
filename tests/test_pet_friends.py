from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

#1
def test_get_api_key_for_valid_email_and_empty_password(email=valid_email, password=''):
    """Проверяем запрос с пустым паролем и с валидным емейлом. Проверяем нет ли ключа в ответe """

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result


#2
def test_get_api_key_for_valid_email_and_invalid_password(email= valid_email, password='InVaLid_PaSSworD1'):
    """ Проверяем запрос с валидным емейлом и невалидным паролем. Смотрим нет ли ключа в ответе """

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result


#3
def test_add_new_pet_negative_age(name='Кот', animal_type='кот', age='-10'):
    '''Проверка добавления нового питомца без фото с отрицательынм возрастом.'''

    #Запрашиваем ключ API и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    #Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    #Сверяем ожидаемый и фактический результат
    assert status == 200
    assert result['name'] == name
    assert result['age'] !=0
    #Баг - животное не должно добавляться нереального возраста.


#4
def test_add_new_pet_without_name(name='', animal_type='пес', age='3'):
    """Проверяем что можно добавить питомца c пустым полем Имя"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом. Ожидаем, что питомца без обязательного поля создать невозможно
    assert status == 200
    assert result['name'] == ''
    #Баг - животное не должно добавляться ,без обязательного поля

#5
def test_add_new_empty_pet(name='', animal_type='', age=''):
    '''Проверка добавления нового питомца без данных.'''

    # Запрашиваем ключ API и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем ожидаемый и фактический результат
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age
    #Баг - животное не должно добавляться без обязательных полей для заполнения

#6
def test_add_new_pet_with_long_name(name='Очень длинное имяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяяя',
                                    animal_type='хомяк',
                                    age='1'):
    """Проверка, что нельзя добавить питомца с именем длиннее 50 символов"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert len(result['name']) > 50
    #Баг - сайт позволяет добавить питомца с именем длиннее 50 символов


#7
def test_delete_api_pets_invalid_pet_id():
    '''Проверяем, что можно удалить питомца с невалидным id'''

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Берём невалидный id питомца и отправляем запрос на удаление
    pet_id = 'привет'
    status, _ = pf.delete_pet(auth_key, pet_id)

    assert status == 200
    #Баг, тк питомца с таким id нет

#8
def test_create_pet_with_photo(name='Вася', animal_type="котик", age='3', photo='images/cat.jpg'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, photo)

    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age
    assert result['id'] is not None
    assert result['pet_photo'] is not None
    assert 'jpeg' in result['pet_photo']
    #Проверка добавления питомца с фото

#9
def test_create_pet_only_with_photo(name=' ', animal_type=" ", age=' ', photo='images/dog.jpg'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, photo)

    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age
    assert result['id'] is not None
    assert result['pet_photo'] is not None
    assert 'jpeg' in result['pet_photo']
    #Баг, тк нельзя добавлять питомца только с фото, заполнены не все обязательные поля

#10
def test_update_unfo_about_pet_without_id(pet_id= ' '):

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.update_pet_info(auth_key, pet_id, name='Кеша', animal_type='папугай', age=2)

    assert status == 400
    #Проверка, что нельзя изменить данные питомца без pet_id