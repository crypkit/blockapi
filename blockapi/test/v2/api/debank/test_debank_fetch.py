import pytest

from blockapi.v2.models import FetchResult

OPTION_SAVE_DATA = True


@pytest.mark.integration
def test_fetch_balances(real_debank_api):
    response = real_debank_api.fetch_balances(
        '0x7a16ff8270133f063aab6c9977183d9e72835428'
    )
    _save('fetch-result-balances', response)


@pytest.mark.integration
def test_fetch_portfolio(real_debank_api):
    response = real_debank_api.fetch_portfolio(
        '0x7a16ff8270133f063aab6c9977183d9e72835428'
    )
    _save('fetch-result-portfolio', response)


@pytest.mark.integration
def test_fetch_protocols(real_debank_api):
    response = real_debank_api.fetch_protocols()
    _save('fetch-result-protocols', response)


@pytest.mark.integration
def test_fetch_chains(real_debank_api):
    response = real_debank_api.fetch_chains()
    _save('fetch-result-chains', response)


@pytest.mark.integration
def test_fetch_usage():
    assert False


def _save(name: str, data: FetchResult):
    if not OPTION_SAVE_DATA:
        return

    with open(f'data/{name}.json', "w") as file:
        file.write(data.json())
