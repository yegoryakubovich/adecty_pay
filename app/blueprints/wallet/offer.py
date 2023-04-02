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


from flask import Blueprint, request

from adecty_design.properties import Font, Margin
from adecty_design.widgets import Text, Button, View, ViewType, ButtonType, Form, InputSelect, \
    InputButton, InputText
from adecty_design.widgets.icon import Icon
from app.adecty_api_client import adecty_api_client
from app.adecty_design import colors, interface
from app.functions.data_input import data_input
from app.functions.to_amount import to_amount, AmountType


blueprint_wallet_offer = Blueprint('blueprint_wallet_offer', __name__, url_prefix='/offer')


@blueprint_wallet_offer.route(rule='/create', endpoint='wallet_offer_create', methods=('GET', 'POST'))
@data_input({'account_session_token': True, 'wallet': True})
def wallet_offer_create(account_session_token, wallet):
    types = {'input': 'Пополнение кошелька', 'output': 'Вывод с кошелька'}
    currencies = adecty_api_client.pay.currencies.get()['currencies']
    currencies_descriptions = [currency['description'] for currency in currencies]
    systems = []
    sysyems_descriptions = []

    # Form data
    offer_type_str = request.form.get('offer_type')
    offer_type = None
    offer_currency_name_str = request.form.get('offer_currency')
    offer_currency_name = None
    offer_currency_places_decimal = None
    offer_value_from_str = request.form.get('offer_value_from')
    offer_value_from = None
    offer_value_to_str = request.form.get('offer_value_to')
    offer_value_to = None
    offer_rate_str = request.form.get('offer_rate')
    offer_rate = None
    offer_system_str = request.form.get('offer_system_description')
    offer_system = None

    if offer_type_str:
        offer_type = [name for name, value in types.items() if value == offer_type_str][0]
    if offer_currency_name_str:
        offer_currency_name, offer_currency_places_decimal = [(currency['name'], currency['places_decimal'])
                                                              for currency in currencies
                                                              if currency['description'] == offer_currency_name_str][0]
        systems = adecty_api_client.pay.systems.get(currency_name=offer_currency_name)['systems']
        sysyems_descriptions = [system['description'] for system in systems]
    if offer_value_from_str:
        offer_value_from = to_amount(
            amount=offer_value_from_str,
            places_decimal=offer_currency_places_decimal,
            amount_type=AmountType.integer,
        )
        offer_value_from_str = to_amount(
            amount=offer_value_from_str,
            places_decimal=offer_currency_places_decimal,
            amount_type=AmountType.string,
        )
    if offer_value_to_str:
        offer_value_to = to_amount(
            amount=offer_value_to_str,
            places_decimal=offer_currency_places_decimal,
            amount_type=AmountType.integer,
        )
        offer_value_to_str = to_amount(
            amount=offer_value_to_str,
            places_decimal=offer_currency_places_decimal,
            amount_type=AmountType.string,
        )
    if offer_rate_str:
        offer_rate = to_amount(
            amount=offer_rate_str,
            places_decimal=offer_currency_places_decimal,
            amount_type=AmountType.integer,
        )
        offer_rate_str = to_amount(
            amount=offer_rate_str,
            places_decimal=offer_currency_places_decimal,
            amount_type=AmountType.string,
        )
    if offer_system_str:
        offer_system = [
            system
            for system in systems
            if system['description'] == offer_system_str
        ][0]

    form_widgets = [
        Text(
            text='1. Формат предложения',
            font=Font(
                size=22,
                weight=500,
            ),
            margin=Margin(top=12),
        ),
        InputSelect(
            id='offer_type',
            options=[t for t in types.values()],
            margin=Margin(horizontal=12),
            is_disabled=True if offer_type else False,
            selected=offer_type_str,
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
                options=currencies_descriptions,
                margin=Margin(horizontal=12),
                is_disabled=True if offer_currency_name_str else False,
                selected=offer_currency_name_str,
            ),
        ]

    if offer_currency_name_str:
        form_widgets += [
            Text(
                text='3. Способ получения {}'.format(offer_currency_name_str),
                font=Font(
                    size=22,
                    weight=500,
                ),
                margin=Margin(top=12),
            ),
            InputSelect(
                id='offer_system_description',
                options=sysyems_descriptions,
                margin=Margin(horizontal=12),
                is_disabled=True if offer_system_str else False,
                selected=offer_system_str,
            ),
        ]

    if offer_system_str:
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
                margin=Margin(top=12, down=4),
            ),
            InputText(
                id='offer_value_from',
                value=offer_value_from_str,
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
                value=offer_value_to_str,
                margin=Margin(down=12),
                is_disabled=True if offer_value_to else False,
            ),
        ]

    if offer_value_from and offer_value_to:
        form_widgets += [
            Text(
                text='6. Количество {currency} за 1 USD (курс)'.format(currency=offer_currency_name_str),
                font=Font(
                    size=22,
                    weight=500,
                ),
                margin=Margin(top=12),
            ),
            InputText(
                id='offer_rate',
                value=offer_rate_str,
                margin=Margin(horizontal=12),
                is_disabled=True if offer_rate else False,
            ),
        ]

    if offer_rate:
        system_data = offer_system['data']
        form_widgets += [
            Text(
                text='7. Реквизиты',
                font=Font(
                    size=22,
                    weight=500,
                ),
                margin=Margin(top=12, down=8),
            ),
        ]
        for field in system_data:
            form_widgets += [
                Text(
                    text=field['description'],
                    font=Font(
                        size=16,
                        weight=400,
                    ),
                    margin=Margin(down=4),
                ),
                InputText(
                    id=field['name'],
                    value=offer_value_to_str,
                    margin=Margin(down=12),
                    is_disabled=True if offer_value_to else False,
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
