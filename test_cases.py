"""Test for Quantori Scoring project site.

Backend testing.
"""

import random
import requests

SCORING_URL = 'https://dev.ddso-spot.quantori.com/'


def cookie_token():
    """Cookie extractor in list function

    Getting list of tokens from file 'Cookie'. This action is needed as a part of refreshing access token
    """
    with open('files/cookie.txt', 'r') as c_token:
        data = str(c_token.read()).split('; ')
    return data


def full_token():
    """Cookie extractor as a string function

    Getting full string of tokens from file 'Cookie'. This string is accepted by backend as access cookie
    """
    with open('files/cookie.txt', 'r') as c_token:
        data = str(c_token.read())
    return data


def open_csv_file_binary(file_name):
    """Open and reading in binary file content

    Getting full binary of CSV file content and save it in variable
    """
    with open('files/' + file_name, 'rb') as content:
        binary_content = content.read()
    return binary_content


def refresh_token():
    """Token refreshing function

    Refreshing token in accordance to API docs for Scoring
    """
    refresh_token_request = requests.post(SCORING_URL + 'api/authorization/refresh',
                                          headers={'Cookie': REFRESH_TOKEN_COOKIE,
                                                   'X-CSRF-REFRESH-TOKEN': CSRF_REFRESH_COOKIE})
    new_cookie = 'access_token_cookie=' + refresh_token_request.json()['access_token']
    return new_cookie


def random_string(length):
    """Creation of random valid name

    Creating username with variable length of valid symbols
    """
    symbols = 'QWERTYUIOPASDFGHJKLZXCVBNM qwertyuiopasdfghjklzxcvbnm_-.'
    name_for_user = ''
    while len(name_for_user) < length:
        name_for_user = name_for_user + random.choice(symbols)
    return name_for_user


def random_user_issue(length):
    """Creation random valid user issue for feedback

    Creating user issue for feedback with variable length of valid symbols
    """
    symbols = r'QWERTYUIOPASDFGHJKLZXCVBNM qwertyuiopasdfghjklzxcvbnm1234567890?!№%:,.;()@+=-_^$*\][}{~|/' + '"' + "'"
    name_for_user = ''
    while len(name_for_user) < length:
        name_for_user = name_for_user + random.choice(symbols)
    return name_for_user


def random_user_email(length):
    """Creating random valid user email for feedback

    Creating user email for feedback with variable length of valid symbols
    """
    symbols = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdghjklzxcvbnm1234567890_-'
    name_for_user = ''
    while len(name_for_user) < length - 6:
        name_for_user = name_for_user + random.choice(symbols)
    print(name_for_user)
    return name_for_user + '@f.net'


def change_user_name_func_happy(valid_user_name):
    """Username changing valid values

    Changing of username value to valid and return it to default value
    """
    change_name = requests.patch(SCORING_URL + 'api/authorization/name?name=' + valid_user_name,
                                 headers={'Cookie': FULL_TOKEN, 'X-CSRF-TOKEN': CSRF_ACCESS_TOKEN}, timeout=4)
    assert change_name.status_code == 200
    get_name = requests.get(SCORING_URL + 'api/authorization/me',
                            headers={'Cookie': NEW_COOKIE}, timeout=4)
    name_value = get_name.json()['name']
    assert get_name.status_code == 200
    assert name_value == valid_user_name
    change_name_back = requests.patch(SCORING_URL + 'api/authorization/name?name=New User',
                                      headers={'Cookie': FULL_TOKEN, 'X-CSRF-TOKEN': CSRF_ACCESS_TOKEN}, timeout=4)
    assert change_name_back.status_code == 200
    get_back_name = requests.get(SCORING_URL + 'api/authorization/me',
                                 headers={'Cookie': NEW_COOKIE}, timeout=4)
    change_name_value = get_back_name.json()['name']
    assert change_name_value == 'New User'


def change_user_name_negative(invalid_user_name):
    """Username changing invalid values

    Changing of username value to invalid and return it to default value
    """
    change_name = requests.patch(SCORING_URL + 'api/authorization/name?name=' + invalid_user_name,
                                 headers={'Cookie': FULL_TOKEN, 'X-CSRF-TOKEN': CSRF_ACCESS_TOKEN}, timeout=4)
    assert change_name.status_code == 400
    change_name_back = requests.patch(SCORING_URL + 'api/authorization/name?name=New User',
                                      headers={'Cookie': FULL_TOKEN, 'X-CSRF-TOKEN': CSRF_ACCESS_TOKEN}, timeout=4)

    assert change_name_back.status_code == 200
    get_back_name = requests.get(SCORING_URL + 'api/authorization/me',
                                 headers={'Cookie': NEW_COOKIE}, timeout=4)
    change_name_value = get_back_name.json()['name']
    assert change_name_value == 'New User'


def open_figure_file_binary(file_name):
    """Open image as binary content

    Function to open and read image file as binary content and save it in variable
    """
    with open(file_name, 'rb') as content:
        image_content = content.read()
        return image_content


def send_feedbacks_positive_testing(data_for_feedback, files):
    """Post acceptable feedback

    Posting feedback with valid values and images
    """
    post_feedback_request = requests.post(SCORING_URL + "api/feedback/user-feedback",
                                          headers={'Cookie': FULL_TOKEN, 'X-CSRF-TOKEN': CSRF_ACCESS_TOKEN},
                                          data=data_for_feedback, files=files)
    assert post_feedback_request.status_code == 201


def send_feedbacks_negative_testing(data_for_feedback, files):
    """Post unacceptable feedback

    Posting feedback with invalid values and images
    """
    post_feedback_request = requests.post(SCORING_URL + "api/feedback/user-feedback",
                                          headers={'Cookie': FULL_TOKEN, 'X-CSRF-TOKEN': CSRF_ACCESS_TOKEN},
                                          data=data_for_feedback, files=files)
    assert post_feedback_request.status_code == 422 or post_feedback_request.status_code == 400



def uploading_dataset(dataset_name):
    """Uploading dataset function

    This function contain 5 steps to upload selected CSV file. Picked file is opened by 'open_csv_file_binary' function
    """
    # 1 step. Open CSV file and get upload parameter for this file
    files = {'files': open_csv_file_binary(dataset_name)}
    upload_dataset = requests.get(SCORING_URL + 'api/upload/datasets/upload_params?filename=' + dataset_name,
                                  params={'filename': dataset_name},
                                  headers={'Cookie': FULL_TOKEN, 'X-CSRF-TOKEN': CSRF_ACCESS_TOKEN}, timeout=4)
    data_dict = upload_dataset.json()

    url_upload = data_dict['data']['url']
    upload_body_dict = data_dict['data']['fields']
    upload_body_dict['file'] = files
    assert upload_dataset.status_code == 200

    # 2 step. Post request to amazon server
    upload_dataset_post = requests.post(url_upload, data=upload_body_dict, files=files,
                                        headers={'Cookie': FULL_TOKEN, 'X-CSRF-TOKEN': CSRF_ACCESS_TOKEN})

    validate_path = data_dict['data']['fields']['key']
    validate_body = {"filepath": validate_path}
    assert upload_dataset_post.status_code == 204

    # 3 step. Validation of endpoint for selected dataset
    validate_dataset = requests.post(SCORING_URL + "api/upload/datasets/validate", json=validate_body,
                                     headers={'Cookie': FULL_TOKEN, 'X-CSRF-TOKEN': CSRF_ACCESS_TOKEN})

    validation_response = validate_dataset.json()
    uploaded_datatse_id = validation_response['id']
    assert validate_dataset.status_code == 200

    # 4 step. Check for result of uploading.
    """Here I use while loop because it is necessary to wait for SUCCESS status. But I faced to problem with uploading
    and I get everytime FAILURE status. That's why I added condition for FAILURE status."""
    logic = True
    while logic:
        check_of_validation = requests.get(SCORING_URL + 'api/task/' + uploaded_datatse_id + '/status',
                                           headers={'Cookie': FULL_TOKEN, 'X-CSRF-TOKEN': CSRF_ACCESS_TOKEN})
        result_of_validation_dict = check_of_validation.json()
        result_of_validation_status = result_of_validation_dict['status']

        if result_of_validation_status == "SUCCESS":
            logic = False
        elif result_of_validation_status == "FAILURE":
            break
        elif result_of_validation_status == "PENDING":
            counter_for_pending_status = 0
            while True:
                if counter_for_pending_status < 2:
                    counter_for_pending_status += 1
                else:
                    break
            logic = False

    # 5 step. Check for result of uploading
    result_of_validation = requests.get(SCORING_URL + 'api/task/' + uploaded_datatse_id + '/result',
                                        headers={'Cookie': FULL_TOKEN, 'X-CSRF-TOKEN': CSRF_ACCESS_TOKEN})
    result_of_validation_list = result_of_validation.json()
    response_of_validation_status = result_of_validation_list['status']
    assert result_of_validation.status_code == 200
    assert response_of_validation_status == 'SUCCESS'


def deleting_uploaded_files_and_restoring():
    """Function for deleting datasets

    This function delete first dataset in response. It contains two steps: get information about uploaded datasets
    and delete the first one in list
    """
    datasets_page = DATASET_LIST_URL_REQUEST

    list_of_datasets = datasets_page.json()
    id_dataset_for_deleting = list_of_datasets[0]['dataset_id']

    deleting_of_dataset = requests.delete(SCORING_URL + 'api/datasets/' + id_dataset_for_deleting,
                                          headers={'Cookie': FULL_TOKEN, 'X-CSRF-TOKEN': CSRF_ACCESS_TOKEN})
    assert deleting_of_dataset.status_code == 204

    restoring_dataset = requests.post(SCORING_URL+ 'api/datasets/'+ id_dataset_for_deleting+'/restore',
                                      headers={'Cookie': FULL_TOKEN, 'X-CSRF-TOKEN': CSRF_ACCESS_TOKEN})
    assert restoring_dataset.status_code == 200


def selecting_result_model_of_dataset_happy_path(url_parameters):
    """Function for selecting results of dataset

    This function get results from uploaded data set. Description is not clear, so I use setting from API specification.
    """
    datasets_page = DATASET_LIST_URL_REQUEST

    list_of_datasets = datasets_page.json()
    chosen_id_dataset = list_of_datasets[0]['dataset_id']

    filters_body = {'filter_indices': [0]}
    selected_result_model = requests.post(SCORING_URL + 'api/datasets/' + chosen_id_dataset + '/selected_result_model',
                                          headers={'Cookie': FULL_TOKEN, 'X-CSRF-TOKEN': CSRF_ACCESS_TOKEN},
                                          json=filters_body, params=url_parameters)
    assert selected_result_model.status_code == 200


def selecting_result_model_of_dataset_negative(url_parameters):
    """Function for selecting results of dataset

    This function get results from uploaded data set. Description is not clear so I use setting from API specification.
    """
    datasets_page = DATASET_LIST_URL_REQUEST

    list_of_datasets = datasets_page.json()
    chosen_id_dataset = list_of_datasets[0]['dataset_id']

    filters_body = {'filter_indices': [0]}
    selected_result_model = requests.post(SCORING_URL + 'api/datasets/' + chosen_id_dataset + '/selected_result_model',
                                          headers={'Cookie': FULL_TOKEN, 'X-CSRF-TOKEN': CSRF_ACCESS_TOKEN},
                                          json=filters_body, params=url_parameters)
    assert selected_result_model.status_code == 422 or selected_result_model.status_code == 404


def exporting_of_choosing_dataset_(exp_parameters):
    """Function for exporting results of dataset

    This function exporting chosen dataset to amazon. In API description some mistakes about query params.
    """
    datasets_page = DATASET_LIST_URL_REQUEST

    list_of_datasets = datasets_page.json()
    chosen_id_dataset = list_of_datasets[0]['dataset_id']

    export_dataset = requests.get(SCORING_URL + 'api/datasets/export/' + chosen_id_dataset,
                                  headers={'Cookie': FULL_TOKEN, 'X-CSRF-TOKEN': CSRF_ACCESS_TOKEN},
                                  params=exp_parameters)
    assert export_dataset.status_code == 200


def exporting_of_choosing_dataset_selecting_rows(exp_parameters, exp_json):
    """Function for exporting results of dataset selecting rows

    This function exporting chosen dataset to amazon. In API description some mistakes about query params.
    """
    datasets_page = DATASET_LIST_URL_REQUEST

    list_of_datasets = datasets_page.json()
    chosen_id_dataset = list_of_datasets[0]['dataset_id']

    export_dataset_selected_rows = requests.post(SCORING_URL + 'api/datasets/export_selected/' + chosen_id_dataset,
                                                 headers={'Cookie': FULL_TOKEN, 'X-CSRF-TOKEN': CSRF_ACCESS_TOKEN},
                                                 params=exp_parameters, json=exp_json)
    assert export_dataset_selected_rows.status_code == 200


def updating_of_chosen_dataset_name(random_dataset_name):
    """Function which change name for chosen dataset name

        This function change in Scoring for chosen dataset. In API description some mistakes: {{ID} in url and 'name'
        upload body has to have .csv extension}.
        """
    datasets_page = DATASET_LIST_URL_REQUEST

    list_of_datasets = datasets_page.json()
    chosen_id_dataset = list_of_datasets[0]['dataset_id']
    user_id = list_of_datasets[0]['user_id']

    update_selected_dataset = requests.patch(SCORING_URL + 'api/datasets/' + chosen_id_dataset,
                                             headers={'Cookie': FULL_TOKEN, 'X-CSRF-TOKEN': CSRF_ACCESS_TOKEN},
                                             params={'user_id': user_id, 'name': random_dataset_name + '.csv'})
    assert update_selected_dataset.status_code == 204


TOKEN_COOKIE = cookie_token()

ACCESS_TOKEN_COOKIE = TOKEN_COOKIE[-4]
CSRF_ACCESS_TOKEN = TOKEN_COOKIE[-3].replace('csrf_access_token=', '')
REFRESH_TOKEN_COOKIE = TOKEN_COOKIE[-2]
CSRF_REFRESH_COOKIE = TOKEN_COOKIE[-1].replace('csrf_refresh_token=', '')

NEW_COOKIE = refresh_token()

FULL_TOKEN = full_token()

IMAGES = {'snapshot': open_figure_file_binary('files/snapshot1.png'),
          'snapshot1': open_figure_file_binary('files/snapshot-bmp.bmp'),
          'snapshot2': open_figure_file_binary('files/snapshot-gif.gif'),
          'snapshot3': open_figure_file_binary('files/snapshot-jfif.jfif'),
          'snapshot4': open_figure_file_binary('files/snapshot-jpe.jpe'),
          'snapshot5': open_figure_file_binary('files/snapshot-jpeg.jpeg'),
          'snapshot6': open_figure_file_binary('files/snapshot-jpg.jpg'),
          'snapshot7': open_figure_file_binary('files/snapshot-tif.tif'),
          'snapshot8': open_figure_file_binary('files/snapshot-tiff.tiff'),
          }

USERNAME_LOWERCASE = 'vrznmpzayjhrelzancfbkwllxgrgtl'
USERNAME_UPPERCASE = 'LPGBNKJCIMCZIOIFRSZCGQNQQZLSPE'
NUMBERS = '1234567890'
PUNCTUATION = '. _-'

DATASET_LIST_URL_REQUEST = requests.get(SCORING_URL + 'api/datasets', headers={'Cookie': ACCESS_TOKEN_COOKIE})


def test_main_page():
    """TEST

    Main page availability
    """
    main_page = requests.get(SCORING_URL, timeout=1)
    assert main_page.status_code == 200
    assert main_page.headers['Connection'] == 'keep-alive'

    if main_page.status_code == 200:
        print('The status 200')


def test_autorization_access():
    """TEST

    Testing successfully authorization
    """
    login_page = requests.get(SCORING_URL + 'api/authorization/login')
    assert login_page.status_code == 200


def test_get_user_name():
    """TEST

    Testing username field has value is 'New user'
    """
    get_name = requests.get(SCORING_URL + 'api/authorization/me',
                            headers={'Cookie': NEW_COOKIE}, timeout=4)
    name_value = get_name.json()['name']
    assert get_name.status_code == 200
    assert name_value == 'New User'


# Happy path for username


def test_user_name_one_letter():
    """TEST

    Check acceptance of one-letter in username field
    """
    change_user_name_func_happy('F')


def test_user_name_one_number():
    """TEST

    Check acceptance of one-number in username field
    """
    change_user_name_func_happy('0')


def test_change_user_name_lowercase_letters():
    """TEST

    Check acceptance of lowercase letters in username field
    """
    change_user_name_func_happy(USERNAME_LOWERCASE)


def test_change_user_name_uppercase_letters():
    """TEST

    Check acceptance of uppercase letters in username field
    """
    change_user_name_func_happy(USERNAME_UPPERCASE)


def test_change_user_name_numbers():
    """TEST

    Check acceptance of numbers in username field
    """
    change_user_name_func_happy(NUMBERS)


def test_change_user_name_random_30():
    """TEST

    Check acceptance of 30 length valid symbols in username field
    """
    random_name_30 = random_string(30)
    change_user_name_func_happy(random_name_30)


# Negative tests for username


def test_user_name_blank():
    """TEST

    Check rejecting of empty username field
    """
    change_user_name_negative('')


def test_user_name_space():
    """TEST

    Check rejecting of space in username field
    """
    change_user_name_negative(' ')


def test_user_name_dot():
    """TEST

    Check rejecting of dot in username field
    """
    change_user_name_negative('.')


# These simbols are valid '#&+' !!!!
def test_user_name_inappropriate_symbol():
    """TEST

    Check rejecting of invalid symbols in username field
    """
    change_user_name_negative('Let ;er 1. I#U+')


def test_change_user_name_punctuation():
    """TEST

    Check rejecting of punctuation in username field
    """
    change_user_name_negative(PUNCTUATION)


def test_change_user_name_31_symbol():
    """TEST

    Check rejecting of 31 symbol in username field
    """
    random_name_31 = random_string(31)
    change_user_name_negative(random_name_31)


def test_user_cyrillic_letters():
    """TEST

    Check rejecting of cyrillic in username field
    """
    change_user_name_negative('ю')


def test_user_other_letters():
    """TEST

    Check rejecting of ß in username field
    """
    change_user_name_negative('ß')


def test_user_other_symbols():
    """TEST

    Check rejecting of special symbol in username field
    """
    change_user_name_negative('®')


# Happy path for feedback


def test_feedback_report_full_list_images_request_valid_values():
    """TEST

    Posting feedback with valid field values and list of all images
    """
    send_feedbacks_positive_testing(data_for_feedback={
        'user_issue': random_user_issue(7999),
        'type_of_request': 'Report an issue',
        'email': random_user_email(99)
    },
        files=IMAGES)


def test_feedback_suggest_full_list_images_request_valid_values_max():
    """TEST

    Posting feedback with maximum valid field values and image with almost max size
    """
    send_feedbacks_positive_testing(data_for_feedback={
        'user_issue': random_user_issue(8000),
        'type_of_request': 'Suggest an improvement',
        'email': random_user_email(100)
    },
        files={'snapshot': open_figure_file_binary('files/Large_image_9.5Mb.bmp')})


def test_feedback_other_max_image_small_valid_values():
    """TEST

    Posting feedback with minimum valid field values and image with max size
    """
    send_feedbacks_positive_testing(data_for_feedback={
        'user_issue': random_user_issue(1),
        'type_of_request': 'Other',
        'email': 'i@a.c'
    },
        files={'snapshot': open_figure_file_binary('files/Large_image_10Mb.bmp')})


def test_feedback_without_images_random_valid_values_list():
    """TEST

    Posting feedback with random valid field values (for type of request field we check acceptance of one million
    long string) and no image
    """
    send_feedbacks_positive_testing(data_for_feedback={
        'user_issue': random_user_issue(666),
        'type_of_request': random_user_issue(1000000),
        'email': random_user_email(16)
    },
        files={})


# Negative tests for feedback


def test_feedback_blank_user_issue_and_valid_values_list():
    """TEST

    Posting feedback with random valid field (user issue field is empty) values and list of valid images
    """
    send_feedbacks_negative_testing(data_for_feedback={
        'user_issue': '',
        'type_of_request': 'Other',
        'email': 'i@a.c'
    },
        files=IMAGES)


def test_feedback_blank_type_of_request_and_valid_values_list():
    """TEST

    Posting feedback with random valid field (type of request field is empty) values and list of valid images
    """
    send_feedbacks_negative_testing(data_for_feedback={
        'user_issue': random_user_issue(1234),
        'type_of_request': '',
        'email': random_user_email(35)
    },
        files=IMAGES)


def test_feedback_blank_email_and_valid_values_list():
    """TEST

    Posting feedback with random valid field (email filed is empty) values and list of valid images
    """
    send_feedbacks_negative_testing(data_for_feedback={
        'user_issue': random_user_issue(635),
        'type_of_request': random_user_issue(37),
        'email': ''
    },
        files=IMAGES)


def test_feedback_cyrillic_user_issue_valid_values_list():
    """TEST

    Posting feedback with random valid field (user issue field contain cyrillic letters)
    values and list of valid images
    """
    send_feedbacks_negative_testing(data_for_feedback={
        'user_issue': 'Пользователь',
        'type_of_request': random_user_issue(1),
        'email': random_user_email(98)
    },
        files=IMAGES)


def test_feedback_cyrillic_request_valid_values_list():
    """TEST

    Posting feedback with random valid field (type of request field contain cyrillic letters)
    values and list of valid images
    """
    send_feedbacks_negative_testing(data_for_feedback={
        'user_issue': random_user_issue(1),
        'type_of_request': 'Другое',
        'email': random_user_email(7)
    },
        files=IMAGES)


def test_feedback_cyrillic_email_valid_values_list():
    """TEST

    Posting feedback with random valid field (email field contain cyrillic letters)
    values and list of valid images
    """
    send_feedbacks_negative_testing(data_for_feedback={
        'user_issue': random_user_issue(1),
        'type_of_request': random_user_issue(23),
        'email': 'тест@маил.ру'
    },
        files=IMAGES)


def test_feedback_another_letter_in_issue_valid_values_list():
    """TEST

    Posting feedback with random valid field (user issue field contain ß letter)
    values and list of valid images
    """
    send_feedbacks_negative_testing(data_for_feedback={
        'user_issue': 'ß',
        'type_of_request': random_user_issue(123456),
        'email': random_user_email(25)
    },
        files=IMAGES)


def test_feedback_another_letter_in_request_valid_values_list():
    """TEST

    Posting feedback with random valid field (type of request field contain ß letter)
    values and list of valid images
    This test fail because no requirements for type of request.
    """
    send_feedbacks_negative_testing(data_for_feedback={
        'user_issue': random_user_issue(4000),
        'type_of_request': 'ß',
        'email': random_user_email(51)
    },
        files=IMAGES)


def test_feedback_another_letter_email_valid_values_list():
    """TEST

    Posting feedback with random valid field (email field contain ß letter)
    values and list of valid images
    """
    send_feedbacks_negative_testing(data_for_feedback={
        'user_issue': random_user_issue(1),
        'type_of_request': random_user_issue(23),
        'email': 'ß@mail.ru'
    },
        files=IMAGES)


def test_feedback_valid_values_oversize_image():
    """TEST

    Posting feedback with random valid field values and image with exceed size
    This test fail. I think backend can afford big images. No restrictions.
    """
    send_feedbacks_negative_testing(data_for_feedback={
        'user_issue': random_user_issue(2999),
        'type_of_request': 'Other',
        'email': random_user_email(99)
    },
        files={'snapshot': open_figure_file_binary('files/Large_image_12Mb.bmp')})


def test_feedback_valid_values_oversize_issue():
    """TEST

    Posting feedback with random valid field values (for user issue field exceed length of string) and valid image
    """
    send_feedbacks_negative_testing(data_for_feedback={
        'user_issue': random_user_issue(8001),
        'type_of_request': 'Other',
        'email': random_user_email(99)
    },
        files={'snapshot': open_figure_file_binary('files/Large_image_9.5Mb.bmp')})


def test_feedback_valid_values_oversize_request():
    """TEST

    Posting feedback with random valid field values (for type of request field I tried to
    exceed length of string. No chances) and valid images list
    """
    send_feedbacks_negative_testing(data_for_feedback={
        'user_issue': random_user_issue(799),
        'type_of_request': random_user_issue(10 ^ 9),
        'email': random_user_email(99)
    },
        files=IMAGES)


def test_feedback_valid_values_oversize_email():
    """TEST

    Posting feedback with random valid field values (for email field exceed length of string) and valid images list
    """
    send_feedbacks_negative_testing(data_for_feedback={
        'user_issue': random_user_issue(53),
        'type_of_request': 'Other',
        'email': random_user_email(101)
    },
        files=IMAGES)


def test_feedback_valid_values_wrong_file():
    """TEST

    Posting feedback with random valid field values and invalid file as image
    This test fail. It seems no control of extension on backend.
    """
    send_feedbacks_negative_testing(data_for_feedback={
        'user_issue': random_user_issue(5),
        'type_of_request': 'Other',
        'email': random_user_email(80)
    },
        files={'snapshot': open_figure_file_binary('files/Dataset_199_9.csv')})


def test_uploading_dataset():
    """TEST

    Procedure for uploading valid dataset
    Test fail. Cannot upload dataset, the uploading status stack in FAILURE or PENDING
    """
    uploading_dataset('Dataset_199_9.csv')


def test_datasets_page_availability():
    """TEST

    Check for availability of datasets list
    """
    datasets_page = DATASET_LIST_URL_REQUEST
    assert datasets_page.status_code == 200


def test_selecting_result_model_for_dataset_default_values():
    """TEST

    Selecting result model for uploaded dataset with default values. First in dataset list
    """
    selecting_result_model_of_dataset_happy_path(url_parameters={'page': '1',
                                                                 'per_page': '25',
                                                                 'sort': '',
                                                                 'order': '',
                                                                 })


def test_selecting_result_model_for_dataset_all_valid_values():
    """TEST

    Selecting result model for uploaded dataset with valid values for all fields. First in dataset list
    """
    selecting_result_model_of_dataset_happy_path(url_parameters={'page': 9999,
                                                                 'per_page': 100,
                                                                 'sort': 'col_1',
                                                                 'order': 'decr',
                                                                 })


def test_selecting_result_model_for_dataset_int_for_pages_str_for_per_page():
    """TEST

    Selecting result model for uploaded dataset with int for pages and str for per_page. First in dataset list
    """
    selecting_result_model_of_dataset_happy_path(url_parameters={'page': 0,
                                                                 'per_page': '50',
                                                                 'sort': 'col_3',
                                                                 'order': 'incr',
                                                                 })


# Negative tests for selecting result model


def test_selecting_result_model_for_dataset_blank_for_pages_str_for_per_page():
    """TEST

    Selecting result model for uploaded dataset with blank for pages and str for per_page. First in dataset list
    """
    selecting_result_model_of_dataset_negative(url_parameters={'page': '',
                                                               'per_page': '3',
                                                               'sort': '',
                                                               'order': '',
                                                               })


def test_selecting_result_model_for_dataset_int_for_pages_blank_for_per_page():
    """TEST

    Selecting result model for uploaded dataset with int for pages and blank for per_page. First in dataset list
    """
    selecting_result_model_of_dataset_negative(url_parameters={'page': 3,
                                                               'per_page': '',
                                                               'sort': '',
                                                               'order': '',
                                                               })


def test_selecting_result_model_for_dataset_int_for_pages_invalid_for_per_page():
    """TEST

    Selecting result model for uploaded dataset with int for pages and invalid for per_page. First in dataset list
    """
    selecting_result_model_of_dataset_negative(url_parameters={'page': 5,
                                                               'per_page': '31',
                                                               'sort': '',
                                                               'order': '',
                                                               })


def test_selecting_result_model_for_dataset_invalid_for_pages_valid_for_per_page():
    """TEST

    Selecting result model for uploaded dataset with letter for pages and valid for per_page. First in dataset list
    """
    selecting_result_model_of_dataset_negative(url_parameters={'page': 'd',
                                                               'per_page': '50',
                                                               'sort': '',
                                                               'order': '',
                                                               })


def test_selecting_result_model_for_dataset_valid_for_pages_letter_for_per_page():
    """TEST

    Selecting result model for uploaded dataset with valid for pages and letter for per_page. First in dataset list
    """
    selecting_result_model_of_dataset_negative(url_parameters={'page': '35',
                                                               'per_page': 'bla',
                                                               'sort': '',
                                                               'order': '',
                                                               })


def test_selecting_result_model_for_dataset_valid_for_pages_and_for_per_page_invalid_for_sort():
    """TEST

    Selecting result model for uploaded dataset with valid for pages and for per_page. Invalid for sort.
    First in dataset list
    """
    selecting_result_model_of_dataset_negative(url_parameters={'page': '1',
                                                               'per_page': '50',
                                                               'sort': 'column',
                                                               'order': '',
                                                               })


def test_selecting_result_model_for_dataset_valid_for_pages_for_per_page_sort_invalid_for_order():
    """TEST

    Selecting result model for uploaded dataset with valid for pages, per_page and sort. Invalid for order.
    First in dataset list
    """
    selecting_result_model_of_dataset_negative(url_parameters={'page': '1',
                                                               'per_page': '50',
                                                               'sort': '',
                                                               'order': 'abracadabra',
                                                               })


def test_exporting_chosen_dataset_with_valid_params():
    """TEST

    Export select dataset. Some misprints in API specification. Params selected for 5_5.csv file.
    """
    exporting_of_choosing_dataset_(exp_parameters={
        'page': '1',
        'per_page': '25',
        'only_visible': False,
        'sort': 'CID',
        'order': 'desc',
        'get_whole_dataset': True,
    })


def test_exporting_chosen_rows_of_dataset_valid_params():
    """TEST

        Export selected rows from dataset. Some misprints in API specification. Params selected for 5_5.csv file.
        """
    exporting_of_choosing_dataset_selecting_rows(exp_parameters={
        'page': '1',
        'per_page': '25',
        'only_visible': False,
        'sort': 'CID',
        'order': 'desc',
        'get_whole_dataset': False,
    }, exp_json={'filter_indices': [0, 2]})


def test_change_chosen_dataset_valid_name_max_size():
    """TEST

    Updating chosen dataset name with max valid length of name. In response length has to be 100 symbols, I found that
    dot before csv is counting
    """
    updating_of_chosen_dataset_name(random_string(99))


def test_deleting_uploaded_datasets():
    """TEST

    Deleting of uploaded datasets. It will give an exception if there is no uploaded sample lists
    """
    deleting_uploaded_files_and_restoring()