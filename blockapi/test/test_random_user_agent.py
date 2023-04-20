from blockapi.utils.user_agent import get_random_user_agent


def test_get_random_user_agent():
    assert get_random_user_agent()
