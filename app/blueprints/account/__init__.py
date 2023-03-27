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


from flask import Blueprint, request, redirect


blueprint_account = Blueprint('blueprint_account', __name__, url_prefix='/account')


@blueprint_account.route('/session/token/save', endpoint='account_session_token_save', methods=('GET', ))
def account_session_token_save():
    account_session_token = request.args.get('account_session_token')

    response = redirect(location='/wallet/all')
    response.set_cookie(key='account_session_token', value=account_session_token, max_age=60*60*7)

    return response