#
# (c) 2023, Yegor Yakubovich
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from flask import request, redirect

from adecty_api_client.adecty_api_client_error import AdectyApiClientError
from app.adecty_api_client import adecty_api_client


ACCOUNT_SESSION_TOKEN_GET_URL = 'https://account.adecty.com/account/session/token/get?redirect_url=192.168.100.230:5000'


def data_input(schema: dict):
    def wrapper(function):
        def validator(*args, **kwargs):
            data = {} | kwargs
            if 'account_session_token' in schema.keys():
                account_session_token = request.cookies.get('account_session_token')
                if not account_session_token:
                    return redirect(location=ACCOUNT_SESSION_TOKEN_GET_URL)
                try:
                    adecty_api_client.account.get(account_session_token=account_session_token)
                except AdectyApiClientError:
                    return redirect(location=ACCOUNT_SESSION_TOKEN_GET_URL)
                data['account_session_token'] = account_session_token
            if 'wallet' in schema.keys():
                try:
                    wallet = adecty_api_client.pay.wallet.get(account_session_token=data['account_session_token'])
                except AdectyApiClientError:
                    return redirect(location='/wallet/create/terms')
                data['wallet'] = wallet

            return function(*args, **data)

        return validator

    return wrapper
