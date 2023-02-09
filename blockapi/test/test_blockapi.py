from decimal import Decimal

from blockapi import (
    check_address_valid,
    get_all_supported_coins,
    get_api_classes_for_coin,
)
from blockapi.test_data import get_test_api_key, test_addresses


class TestBlockApiProviders:
    def __init__(self, data=None, methods=None):
        """State what currencies should be tested on which addresses
        with which expected values

        Args:
            data (list): list of dicts with structure
            {
                "currency": (str),  # Should be valid symbol
                "address": (str),
                "value": (Decimal)
            }
            methods (list): what methods should be tested, if None
                get_balance is tested
        """

        self.currencies = get_all_supported_coins()
        self.data = data if data is not None else []
        self.methods = methods if methods else ['get_balance']
        self.results = {m: [] for m in self.methods}
        self.diagnostic = None
        self.error_api = []

    def run_all(self):
        """Auto run of all APIs using test data"""
        data = []

        # Create test sample
        for currency in self.currencies:
            if not test_addresses.get(currency):
                continue

            data.append(
                {
                    'currency': currency,
                    'address': test_addresses[currency][0],
                    'value': '0',
                }
            )

        self.data = data
        self.run()

    def run(self):
        """Runs tests for given data"""

        for currency in self.data:
            classes = get_api_classes_for_coin(symbol=currency['currency'])

            for class_ in classes:
                # try to load api_key
                api_key = get_test_api_key(class_.__name__)
                try:
                    class_instance = class_(
                        address=currency['address'], api_key=api_key
                    )
                except Exception as e:
                    self.error_api.append(
                        {'api': class_.__name__, 'error': 'Init error', 'message': e}
                    )
                    continue

                for method in self.methods:
                    try:
                        self.results[method].append(
                            {
                                'result': getattr(class_instance, method)(),
                                'api': class_.__name__,
                                'currency': currency['currency'],
                                'success': True,
                            }
                        )
                    except Exception as e:
                        self.error_api.append(
                            {
                                'api': class_.__name__,
                                'error': f'{method} error',
                                'message': e,
                            }
                        )

    def get_diagnostic(self, method=None):
        """Returns info about results"""

        if method is None:
            method = 'get_balance'

        if not self.results:
            return 'Run "run" or "run_all" first.'

        if method not in self.methods:
            return 'Choose valid method.'

        return {
            'api_with_error': [a['api'] for a in self.error_api],
            'api_with_result_none': [
                r['api'] for r in self.results[method] if r['result'] is None
            ],
            'api_with_structure_error': [
                r['api']
                for r in self.results[method]
                if not isinstance(r['result'], list)
            ],
            'api_with_results': {
                c: {
                    'results': [
                        r
                        for r in self.results[method]
                        if r['result'] is not None
                        and r['currency'] == c
                        and isinstance(r['result'], list)
                    ],
                    'mean': self._mean(method=method, currency=c),
                }
                for c in self.currencies
            },
        }

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, _data):
        valid_data = []
        not_valid_data = []
        for d in _data:
            if d['currency'] not in self.currencies:
                not_valid_data.append({'message': 'Symbol not valid', 'data': d})
                continue

            if not check_address_valid(d['currency'], d['address']):
                not_valid_data.append(
                    {'message': 'Check address not successful', 'data': d}
                )
                continue

            try:
                d['value'] = Decimal(d['value'])
            except ValueError:
                not_valid_data.append({'message': 'Value is not a number', 'data': d})
                continue

            valid_data.append(d)

        self._data = valid_data

    def _mean(self, method, currency):
        records = [
            r['result']
            for r in self.results[method]
            if r['result'] is not None
            and r['currency'] == currency
            and isinstance(r['result'], list)
        ]

        sum_ = sum(
            [
                next((i['amount'] for i in r if i['symbol'] == currency), 0)
                for r in records
            ]
        )
        return sum_ / len(records) if records else 0
