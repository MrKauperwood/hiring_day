import pytest
import requests


BASE_URL = r"https://jsonplaceholder.typicode.com/posts/"

# POSITIVE PARAMETERS
TEST_DATA_KEYS = ["userId", "id", "title", "body"]
TEST_TITLE = "qui est esse"
UNIQUE_IDS = [1, 10, 100]
POST_IDS = [1, 10, 100]
USER_IDS = [1, 10]
TEST_BODY = "eveniet quo quis\nlaborum totam consequatur non dolor\nut et est repudiandae\nest voluptatem vel debitis et magnam"

# NEGATIVE PARAMETERS
NEGATIVE_USER_IDS = [-1, 0, 11, 0.1]
NEGATIVE_UNIQUE_IDS = [0, -1, 101, 100.1]
NEGATIVE_TEST_TITLE = ["", TEST_TITLE*50]
NEGATIVE_TEST_BODY = ["", TEST_BODY*50]
COMMON_NEGATIVE_PARAMETERS = ["!", "@", "*", "(", "-", "=", "+", "\\", "//", '`', "&", "№", ";", "^"]
NEGATIVE_FAIL_PARAMETERS = ["%"]

# API
API_USER_ID_POSTS = "?userId="
API_ID_POST = "?id="
API_ID_POST2 = ""
API_TITLE_PREFIX = "?title="
API_TITLE = API_TITLE_PREFIX + TEST_TITLE
API_BODY_PREFIX = "?body="
API_BODY = API_BODY_PREFIX + TEST_BODY
API_JOIN = "/comments"

# MISC
STATUS_CODES = {"NOT FOUND": 404,
                "OK": 200,
                "Internal Server Error": 500}

# Headers Functions
def check_status_code(response, expected_status):
    assert response.status_code == STATUS_CODES[expected_status], f"Status Code != {STATUS_CODES[expected_status]}"


def check_content_type(response):
    assert response.headers['Content-Type'] == "application/json; charset=utf-8"


def check_headers(response, expected_status):
    check_status_code(response, expected_status)
    check_content_type(response)


# Body Functions


def check_count_of_all_elements(response_json, expected_count):
    actual_count = len(response_json)
    assert actual_count == int(expected_count), \
        f"Body should be contains {expected_count} elements, but contains {actual_count}"


def check_count_of_elements_by_user_id(response_text, user_id, expected_count):
    actual_count = response_text.count(f"\"userId\": {user_id},")
    assert actual_count == int(expected_count), \
        f"Body should be contains {expected_count} elements with user_id={user_id}, but contains {actual_count}"


def check_count_of_elements_by_post_id(response_text, postId, expected_count):
    actual_count = response_text.count(f"\"postId\": {postId},")
    assert actual_count == int(expected_count), \
        f"Body should be contains {expected_count} elements with postId={postId}, but contains {actual_count}"


def check_all_keys_are_present_in_resources(dict_resource):
    for key in TEST_DATA_KEYS:
        assert key in dict_resource, \
            f"Required key {key} is missing in {dict_resource}"


def check_value_in_dict(dict_resource, key, expected_value):
    assert dict_resource[key] == expected_value, \
        f"Value '{dict_resource[key]}' is not valid! Value should be '{expected_value}'"


# POSITIVE TESTS
def test_getting_list_of_all_resources():
    response = requests.get(BASE_URL)
    check_headers(response, "OK")
    check_count_of_all_elements(response.json(), 100)
    for user_id in range(1, 11):
        check_count_of_elements_by_user_id(response.text, user_id, 10)
    for dict_resource in response.json():
        check_all_keys_are_present_in_resources(dict_resource)


@pytest.mark.parametrize("user_id", USER_IDS)
def test_getting_list_of_resources_by_user_id(user_id):
    response = requests.get(BASE_URL + API_USER_ID_POSTS + str(user_id))
    check_headers(response, "OK")
    check_count_of_all_elements(response.json(), 10)
    check_count_of_elements_by_user_id(response.text, user_id, 10)
    for dict_resource in response.json():
        check_all_keys_are_present_in_resources(dict_resource)
        check_value_in_dict(dict_resource, "userId", user_id)


@pytest.mark.parametrize("api_unique_id", [API_ID_POST, API_ID_POST2])
@pytest.mark.parametrize("unique_id", UNIQUE_IDS)
def test_getting_resource_by_unique_id(api_unique_id, unique_id):
    response = requests.get(BASE_URL + api_unique_id + str(unique_id))
    check_headers(response, "OK")
    response_json = response.json()
    if type(response_json) == type({}):
        response_json = [response_json]
    check_count_of_all_elements(response_json, 1)
    for dict_resource in response_json:
        check_all_keys_are_present_in_resources(dict_resource)
        check_value_in_dict(dict_resource, "id", unique_id)


def test_getting_resource_by_title():
    response = requests.get(BASE_URL + API_TITLE)
    check_headers(response, "OK")
    check_count_of_all_elements(response.json(), 1)
    for dict_resource in response.json():
        check_all_keys_are_present_in_resources(dict_resource)
        check_value_in_dict(dict_resource, "title", TEST_TITLE)

def test_getting_resource_by_body():
    api_body_for_url = API_BODY.replace(r'\n', "%0a")
    response = requests.get(BASE_URL + api_body_for_url)
    check_headers(response, "OK")
    check_count_of_all_elements(response.json(), 1)
    for dict_resource in response.json():
        check_all_keys_are_present_in_resources(dict_resource)
        check_value_in_dict(dict_resource, "body", TEST_BODY)


@pytest.mark.parametrize("postId", POST_IDS)
def test_join_with_comments_by_user_id(postId):
    response = requests.get(BASE_URL + str(postId) + API_JOIN)
    check_headers(response, "OK")
    check_count_of_all_elements(response.json(), 5)
    check_count_of_elements_by_post_id(response.text, postId, 5)
    for dict_resource in response.json():
        check_value_in_dict(dict_resource, "postId", postId)



# NEGATIVE TESTS
@pytest.mark.parametrize("user_id", NEGATIVE_USER_IDS + COMMON_NEGATIVE_PARAMETERS)
def test_negative_by_user_id(user_id):
    response = requests.get(BASE_URL + API_USER_ID_POSTS + str(user_id))
    check_headers(response, "OK")
    assert response.json() == []


@pytest.mark.parametrize("unique_id", NEGATIVE_UNIQUE_IDS + COMMON_NEGATIVE_PARAMETERS)
def test_negative_by_unique_id_1( unique_id):
    response = requests.get(BASE_URL + API_ID_POST + str(unique_id))
    check_headers(response, "OK")
    assert response.json() == []


@pytest.mark.parametrize("unique_id", NEGATIVE_UNIQUE_IDS + COMMON_NEGATIVE_PARAMETERS)
def test_negative_by_unique_id_2( unique_id):
    response = requests.get(BASE_URL + API_ID_POST2 + str(unique_id))
    check_headers(response, "NOT FOUND")
    assert response.json() == {}


@pytest.mark.parametrize("unique_id", NEGATIVE_FAIL_PARAMETERS)
def test_negative_by_unique_id_3( unique_id):
    response = requests.get(BASE_URL + API_ID_POST2 + str(unique_id))
    check_headers(response, "Internal Server Error")
    assert response.json() == {}, "Failed to decode param!!!"


@pytest.mark.parametrize("title", NEGATIVE_TEST_TITLE + COMMON_NEGATIVE_PARAMETERS)
def test_negative_by_title(title):
    response = requests.get(BASE_URL + API_TITLE_PREFIX + title)
    check_headers(response, "OK")
    assert response.json() == []


@pytest.mark.parametrize("body", NEGATIVE_TEST_BODY)
def test_negative_by_body(body):
    api_body_for_url = body.replace(r'\n', "%0a")
    response = requests.get(BASE_URL + API_BODY_PREFIX + api_body_for_url)
    check_headers(response, "OK")
    assert response.json() == []


# FAILS
# https://jsonplaceholder.typicode.com/posts?asdasdasdasdasdasdudasder_id=0.1
# https://jsonplaceholder.typicode.com/posts/%