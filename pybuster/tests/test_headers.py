import pytest

from pybuster.src import constants
from pybuster.src.headers import Headers


@pytest.fixture(scope="session", autouse=True)
def setup():
    headers_object = Headers()
    return headers_object


def test_should_generate_random_user_agent(setup):
    fail_message = "FAIL: there is at least one duplicate user agent."
    headers_object = setup
    user_agents = [
        headers_object.generate_random_user_agent(),
        headers_object.generate_random_user_agent(),
        headers_object.generate_random_user_agent(),
    ]
    unique_user_agents = set(user_agents)
    is_unique_user_agents = (len(unique_user_agents) == 3)
    assert is_unique_user_agents, fail_message


def test_should_generate_internet_explorer_user_agent(setup):
    fail_message = "FAIL: the user agent is not windows explorer."
    headers_object = setup
    user_agent = headers_object.generate_user_agent_for_internet_explorer()
    is_internet_explorer = constants.BROWSER_NAME_INTERNET_EXPLORER in user_agent
    assert is_internet_explorer, fail_message


def test_should_generate_firefox_user_agent(setup):
    fail_message = "FAIL: the user agent is not firefox explorer."
    headers_object = setup
    user_agent = headers_object.generate_user_agent_for_firefox()
    is_firefox = constants.BROWSER_NAME_FIREFOX in user_agent
    assert is_firefox, fail_message


def test_should_generate_chrome_user_agent(setup):
    fail_message = "FAIL: the user agent is not chrome."
    headers_object = setup
    user_agent = headers_object.generate_user_agent_for_chrome()
    is_chrome = constants.BROWSER_NAME_CHROME in user_agent
    assert is_chrome, fail_message


def test_should_generate_safari_user_agent(setup):
    fail_message = "FAIL: the user agent is not safari."
    headers_object = setup
    user_agent = headers_object.generate_user_agent_for_safari()
    is_safari = constants.BROWSER_NAME_SAFARI in user_agent
    assert is_safari, fail_message
