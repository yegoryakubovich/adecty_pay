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

from flask import Blueprint

from adecty_design.properties import Font, Margin, Padding
from adecty_design.widgets import Text, Card, View, Button, ViewType, ButtonType
from app.adecty_design import colors, interface
from app.blueprints.wallet.create import blueprint_wallet_create
from app.functions.data_input import data_input


blueprint_wallet = Blueprint('blueprint_wallet', __name__, url_prefix='/wallet')
blueprint_wallet.register_blueprint(blueprint=blueprint_wallet_create)


@blueprint_wallet.route('/<deals_type>', endpoint='wallet_get', methods=('GET',))
@data_input({'account_session_token': True, 'wallet': True})
def wallet_get(account_session_token, wallet, deals_type):
    balance = wallet['balance']

    widgets = [
        Text(
            text='Мой кошелек',
            font=Font(
                size=32,
                weight=700,
            ),
            margin=Margin(down=8),
        ),
        Card(widgets=[
            Text(
                text='$ {balance}'.format(balance=balance),
                font=Font(
                    size=32,
                    weight=700,
                    color=colors.background,
                ),
            ),
            View(widgets=[
                Button(url='123', text='Полполнить', margin=Margin(horizontal=8)),
                Button(url='123', text='Вывести', margin=Margin(horizontal=8, left=12)),
            ], type=ViewType.horizontal),
        ], padding=Padding(horizontal=32, vertical=24), color_background=colors.primary),
        Text(
            text='Последние операции',
            margin=Margin(top=24, down=8),
            font=Font(
                size=32,
                weight=700,
            ),
        ),
        View(widgets=[
            Button(type=ButtonType.chip, url='input', margin=Margin(right=8), text=Text(
                text='Пополнения',
                font=Font(color=colors.background if deals_type == 'input' else colors.text),
            ), color_background=colors.primary if deals_type == 'input' else colors.background_secondary),
            Button(type=ButtonType.chip, url='output', margin=Margin(right=8), text=Text(
                text='Выводы',
                font=Font(color=colors.background if deals_type == 'output' else colors.text),
            ), color_background=colors.primary if deals_type == 'output' else colors.background_secondary),
            Button(type=ButtonType.chip, url='all', text=Text(
                text='Все',
                font=Font(color=colors.background if deals_type == 'all' else colors.text),
            ), color_background=colors.primary if deals_type == 'all' else colors.background_secondary),
        ], type=ViewType.horizontal),
    ]

    interface_html = interface.html_get(widgets=widgets, active='wallet')
    return interface_html
