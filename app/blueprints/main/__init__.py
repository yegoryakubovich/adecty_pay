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


from flask import Blueprint, redirect

from app.functions.data_input import data_input


blueprint_main = Blueprint('blueprint_main', __name__, url_prefix='')


@blueprint_main.route('/', endpoint='main', methods=('GET',))
@data_input({'account_session_token': True})
def main(account_session_token):
    return redirect('/wallet/all')
