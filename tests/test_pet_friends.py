from api import PetFriends
from settings import valid_email, valid_password
import os


pf = PetFriends()

# Authorisation testing


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Check if api key request returns status 200 and result has 'key' word """
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_api_key_with_empty_email_and_password():
    """Check if api key request with empty email and password returns 403 error"""
    status, result = pf.get_api_key()
    print(result)
    assert status == 403
    assert "This user wasn't found in database" in result


def test_get_api_key_with_correct_email_and_empty_password(email=valid_email):
    """Check if api key request with correct email and empty password returns 403 error"""
    status, result = pf.get_api_key(email)
    print(result)
    assert status == 403
    assert "This user wasn't found in database" in result


def test_get_api_key_with_empty_email_correct_password(password=valid_password):
    """Check if api key request with empty email and correct password returns 403 error"""
    status, result = pf.get_api_key(password=password)
    print(result)
    assert status == 403
    assert "This user wasn't found in database" in result


# List of pets

def test_get_all_pets_with_valid_key(filter=""):
    """Check if pet_list request returns not an empty list. Available value for filter - 'my_pets' or '' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_pet_list(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_get_all_pets_with_invalid_key(filter=""):
    """Check if status of pet_list request with invalid authorisation key is 403 """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    auth_key['key'] = 'some_key'
    status, result = pf.get_pet_list(auth_key, filter)
    assert status == 403


def test_get_all_pets_with_valid_key_and_invalid_filter(filter="filter"):
    """Check if status of pet_list request with invalid filter is 500. Available value for filter - 'my_pets' or '' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_pet_list(auth_key, filter)
    assert status == 500


# Add new pet with photo

def test_add_new_pet_with_valid_data(name='Давай', animal_type='Работай', age='3', pet_photo='images/cat1.jpg'):
    """Check possibility to add new pet with correct data"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_invalid_key(name='Давай', animal_type='Работай', age='3', pet_photo='images/cat1.jpg'):
    """Check if add_new_pet request with invalid authorisation key returns status - 403 and result with
    the help message - "Please provide 'auth_key'" """
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    auth_key['key'] = 'invalid_key'

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 403
    assert "Please provide 'auth_key'" in result


def test_add_new_pet_with_valid_key_and_empty_info_fields(name='', animal_type='', age='',
                                                          pet_photo='images/cat1.jpg'):
    """Check if add_new_pet request with empty fields(name, animal_type, age) returns status code 400 """
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


def test_add_new_pet_with_valid_key_and_invalid_data_in_info_fields(name='Давай' * 1000, animal_type='??<>=!@#$%^&*()',
                                                                    age='-3.7', pet_photo='images/cat1.jpg'):
    """Check if add_new_pet requests with invalid data(too long name, special symbols in animal_type, negative and float
    number in age) returns status code 400 - data is incorrect"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


def test_add_new_pet_with_valid_key_and_invalid_age_field(name='Давай', animal_type='Работай', age='age',
                                                          pet_photo='images/cat1.jpg'):
    """Check if add_new_pet requests with invalid data(letters in age field instead of numbers)
    returns status code 400 - data is incorrect"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


def test_add_new_pet_with_unsupported_image_format(name='Давай', animal_type='Работай', age='3',
                                                   pet_photo='images/GIF.gif'):
    """Check if add_new_pet requests with unsupported image format returns status code 400 - data is incorrect"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


# Add new pet without photo

def test_add_new_pet_without_photo_with_valid_data(name='Имя', animal_type='Тип', age='4'):
    """Check possibility to add new pet without photo with correct data"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_without_photo_with_invalid_key(name='Имя', animal_type='Тип', age='4'):
    """Check if add_new_pet_without_photo request with invalid authorisation key returns status code 403"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    auth_key['key'] = 'invalid_key'

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 403


def test_add_new_pet_without_photo_with_invalid_data(name='', animal_type='type?<>!@#$' * 1000, age='-4age'):
    """Check if add_new_pet_without_photo requests with invalid data(empty name, too long animal_type with special
    symbols, negative age with letters) returns status code 400 - data is incorrect"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 400


# Add photo
def test_set_photo_of_pet_with_valid_data(pet_photo='images/cat1.jpg'):
    """Check possibility to add photo of existing pet"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_pet_list(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:  # if list of my_pets is not empty
        status, result = pf.set_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
    else:  # if my_pets is empty, add new pet without photo
        pf.add_new_pet_without_photo(auth_key, name='Имя', animal_type='Тип', age='4')
        _, my_pets = pf.get_pet_list(auth_key, "my_pets")

        status, result = pf.set_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

    assert status == 200
    assert result['pet_photo']


def test_set_photo_of_pet_with_invalid_key(pet_photo='images/cat1.jpg'):
    """Check if set_pet_photo request with invalid authorisation key returns status code 403"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    _, my_pets = pf.get_pet_list(auth_key, "my_pets")
    auth_key['key'] = "invalid_key"

    if len(my_pets['pets']) > 0:  # if list of my_pets is not empty
        status, result = pf.set_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
    else:  # if my_pets is empty, add new pet without photo
        pf.add_new_pet_without_photo(auth_key, name='Имя', animal_type='Тип', age='4')
        _, my_pets = pf.get_pet_list(auth_key, "my_pets")

        status, result = pf.set_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

    assert status == 403


def test_set_photo_of_pet_with_valid_key_and_invalid_pet_id(pet_photo='images/cat1.jpg'):
    """Check if set_pet_photo request with invalid pet_id returns status code 400 - provided data is incorrect"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_pet_list(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:  # if list of my_pets is not empty
        my_pets['pets'][0]['id'] = ""
        status, result = pf.set_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
    else:  # if my_pets is empty, add new pet without photo
        pf.add_new_pet_without_photo(auth_key, name='Имя', animal_type='Тип', age='4')
        _, my_pets = pf.get_pet_list(auth_key, "my_pets")
        my_pets['pets'][0]['id'] = ""

        status, result = pf.set_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

    assert status == 400


def test_set_photo_of_pet_with_valid_key_and_unsupported_image_format(pet_photo='images/GIF.gif'):
    """Check if set_pet_photo request with unsupported image format returns status code 400 - provided
    data is incorrect"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_pet_list(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:  # if list of my_pets is not empty
        status, result = pf.set_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
    else:  # if my_pets is empty, add new pet without photo
        pf.add_new_pet_without_photo(auth_key, name='Имя', animal_type='Тип', age='4')
        _, my_pets = pf.get_pet_list(auth_key, "my_pets")

        status, result = pf.set_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

    assert status == 400


# Delete pet
def test_delete_pet_with_valid_data():
    """Check possibility to delete pet with correct data"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_pet_list(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.delete_pet(auth_key, my_pets['pets'][0]['id'])
        assert status == 200
    else:
        raise Exception("There is not my pets")


def test_delete_pet_with_invalid_key():
    """Check if delete_pet request with invalid authorisation key and correct pet_id returns status code 403"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_pet_list(auth_key, "my_pets")
    auth_key['key'] = 'invalid_key'
    if len(my_pets['pets']) > 0:
        status, result = pf.delete_pet(auth_key, my_pets['pets'][0]['id'])
        assert status == 403
    else:
        raise Exception("There is not my pets")


def test_delete_pet_with_incorrect_pet_id():
    """Check if delete_pet request with invalid pet_id returns status code 400"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_pet_list(auth_key, "my_pets")
    my_pets['pets'][0]['id'] = "incorrect_id"
    if len(my_pets['pets']) > 0:
        status, result = pf.delete_pet(auth_key, my_pets['pets'][0]['id'])
        assert status == 400
    else:
        raise Exception("There is not my pets")


# Update_pet_info

def test_update_pet_info_with_valid_data(name='New name',
                                         animal_type='type8', age='5'):
    """Check if update_pet_info request changes pet data"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_pet_list(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_update_pet_info_with_invalid_key(name='New name', animal_type='type8', age='5'):
    """Check if update_pet_info request with incorrect authorisation key returns status code 403"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_pet_list(auth_key, "my_pets")
    auth_key['key'] = 'invalid_key'
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 403
    else:
        raise Exception("There is no my pets")


def test_update_pet_info_with_valid_key_and_invalid_data(name='><!@#$$%^&' * 1000, animal_type='', age='-5qwe'):
    """Check if update_pet_info request with incorrect data(too long name with special symbols, empty animal_type,
    negative age with letters) returns status code 400 - provided data is incorrect"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_pet_list(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 400
    else:
        raise Exception("There is no my pets")

