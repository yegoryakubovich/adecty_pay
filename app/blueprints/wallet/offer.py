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


from flask import Blueprint, redirect, request

from adecty_api_client.adecty_api_client_error import AdectyApiClientError
from adecty_design.properties import Font, Margin, Padding, Align, AlignType
from adecty_design.widgets import Text, Button, View, ViewType, ButtonType, Card, Dictionary, Form, InputSelect, \
    InputButton, InputFile, InputText
from adecty_design.widgets.icon import Icon
from app.adecty_api_client import adecty_api_client
from app.adecty_design import colors, interface
from app.adecty_design.navigation import navigation_none
from app.functions.data_input import data_input


blueprint_wallet_offer = Blueprint('blueprint_wallet_offer', __name__, url_prefix='/offer')


@blueprint_wallet_offer.route(rule='/create', endpoint='wallet_offer_create', methods=('GET', 'POST'))
@data_input({'account_session_token': True, 'wallet': True})
def wallet_offer_create(account_session_token, wallet):
    form_widgets = []

    offer_type = request.form.get('offer_type')
    offer_currency = request.form.get('offer_currency')
    offer_system_description = request.form.get('offer_system_description')
    offer_value_from = request.form.get('offer_value_from')
    offer_value_to = request.form.get('offer_value_to')
    offer_rate = request.form.get('offer_rate')

    form_widgets += [
        Text(
            text='1. Тип предложения',
            font=Font(
                size=22,
                weight=500,
            ),
            margin=Margin(top=12),
        ),
        InputSelect(
            id='offer_type',
            options=[
                'INPUT', 'OUTPUT',
            ],
            margin=Margin(horizontal=12),
            is_disabled=True if offer_type else False,
            selected=offer_type,
        ),
    ]
    if offer_type:
        form_widgets += [
            Text(
                text='2. Валюта, которую хотите {}'.format('продать' if offer_type == 'INPUT' else 'купить'),
                font=Font(
                    size=22,
                    weight=500,
                ),
                margin=Margin(top=12),
            ),
            InputSelect(
                id='offer_currency',
                options=[
                    'RUB', 'USD',
                ],
                margin=Margin(horizontal=12),
                is_disabled=True if offer_currency else False,
                selected=offer_currency,
            ),
        ]

    if offer_currency:
        systems = adecty_api_client.pay.systems.get(currency_name=offer_currency)['systems']

        form_widgets += [
            Text(
                text='3. Способ получения {}'.format(offer_currency),
                font=Font(
                    size=22,
                    weight=500,
                ),
                margin=Margin(top=12),
            ),
            InputSelect(
                id='offer_system_description',
                options=[system['description'] for system in systems],
                margin=Margin(horizontal=12),
                is_disabled=True if offer_system_description else False,
                selected=offer_system_description,
            ),
        ]

    if offer_system_description:
        form_widgets += [
            Text(
                text='4. Сколько вы готовы {} (указывается в USD)'
                .format('продать' if offer_type == 'INPUT' else 'купить'),
                font=Font(
                    size=22,
                    weight=500,
                ),
                margin=Margin(top=12),
            ),
            Text(
                text='От',
                font=Font(
                    size=16,
                    weight=400,
                ),
                margin=Margin(down=4),
            ),
            InputText(
                id='offer_value_from',
                value=offer_value_from,
                margin=Margin(down=12),
                is_disabled=True if offer_value_from else False,
            ),
            Text(
                text='До',
                font=Font(
                    size=16,
                    weight=400,
                ),
                margin=Margin(down=4),
            ),
            InputText(
                id='offer_value_to',
                value=offer_value_to,
                margin=Margin(down=12),
                is_disabled=True if offer_value_to else False,
            ),
        ]

    if offer_value_from and offer_value_to:
        form_widgets += [
            Text(
                text='6. Количество {currency} за 1 USD (курс)'.format(currency=offer_currency),
                font=Font(
                    size=22,
                    weight=500,
                ),
                margin=Margin(top=12),
            ),
            InputText(
                id='offer_rate',
                value=offer_rate,
                margin=Margin(horizontal=12),
                is_disabled=True if offer_rate else False,
            ),
        ]

    form_widgets.append(
        InputButton(text='Продолжить'),
    )

    widgets = [
        View(type=ViewType.horizontal, widgets=[
            Button(type=ButtonType.chip, url='/wallet/offers/get',
                   color_background=colors.background,
                   icon=Icon(path='app/icons/back.svg', color=colors.text)),
            Text(
                text='Новое предложение',
                font=Font(
                    size=32,
                    weight=700,
                ),
            ),
        ]),
        Form(widgets=form_widgets),
    ]

    interface_html = interface.html_get(widgets=widgets, active='wallet_offers')
    return interface_html
