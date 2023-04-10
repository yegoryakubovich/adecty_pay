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
from json import loads, dumps

from flask import Blueprint, request, redirect

from adecty_api_client.adecty_api_client_error import AdectyApiClientError
from adecty_design.properties import Font, Margin
from adecty_design.widgets import Text, Button, View, ViewType, ButtonType, Form, InputSelect, \
    InputButton, InputText
from adecty_design.widgets.icon import Icon
from app.adecty_api_client import adecty_api_client
from app.adecty_design import colors, interface
from app.adecty_design.functions import message_get
from app.functions.data_input import data_input
from app.functions.to_amount import to_amount, AmountType


blueprint_wallet_offer = Blueprint('blueprint_wallet_offer', __name__, url_prefix='/offer')


@blueprint_wallet_offer.route(rule='/create', endpoint='wallet_offer_create', methods=('GET', 'POST'))
@data_input({'account_session_token': True, 'wallet': True})
def wallet_offer_create(account_session_token, wallet):
    message = ''

    types = {'input': 'Пополнение кошелька', 'output': 'Вывод с кошелька'}
    currencies = adecty_api_client.pay.currencies.get()['currencies']
    currencies_descriptions = [currency['description'] for currency in currencies]
    systems = []
    sysyems_descriptions = []

    # Form data
    offer_type_str = request.form.get('offer_type')
    offer_type = None
    offer_currency_name_str = request.form.get('offer_currency')
    offer_currency_places_decimal = None
    offer_value_from_str = request.form.get('offer_value_from')
    offer_value_from = None
    offer_value_to_str = request.form.get('offer_value_to')
    offer_value_to = None
    offer_rate_str = request.form.get('offer_rate')
    offer_rate = None
    offer_system_str = request.form.get('offer_system_description')
    offer_system = None
    offer_system_data = {}

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
            offer_system_data[field['name']] = request.form.get(field['name'])
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
                    value=offer_system_data.get(field['name']),
                    margin=Margin(down=12),
                    is_disabled=True if offer_system_data.get(field['name']) else False,
                ),
            ]

        if not (None in offer_system_data.values()):
            try:
                adecty_api_client.pay.wallet.offer.create(
                    account_session_token=account_session_token,
                    type=offer_type,
                    system_name=offer_system['name'],
                    system_data=dumps(offer_system_data),
                    value_from=offer_value_from,
                    value_to=offer_value_to,
                    rate=offer_rate,
                )
                return redirect(location='/wallet/offers/get')
            except AdectyApiClientError as e:
                message = message_get(text=e.txt)

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

    widgets.insert(0, message)

    interface_html = interface.html_get(widgets=widgets, active='wallet_offers')
    return interface_html


@blueprint_wallet_offer.route(
    rule='/<offer_id>/update/active',
    endpoint='wallet_offer_update_active',
    methods=('GET', 'POST'),
)
@data_input({'account_session_token': True, 'wallet': True})
def wallet_offer_update_active(account_session_token, wallet, offer_id):
    try:
        adecty_api_client.pay.wallet.offer.update(
            account_session_token=account_session_token,
            id=offer_id,
        )
    except AdectyApiClientError:
        pass
    return redirect(location='/wallet/offers/get')


@blueprint_wallet_offer.route(rule='/<offer_id>/update', endpoint='wallet_offer_update', methods=('GET', 'POST'))
@data_input({'account_session_token': True, 'wallet': True})
def wallet_offer_update(account_session_token, wallet, offer_id):
    try:
        offer = adecty_api_client.pay.wallet.offer.get(
            account_session_token=account_session_token,
            id=offer_id,
        )['offer']
    except AdectyApiClientError:
        return redirect(location='/wallet/offers/get')

    offer_rate = to_amount(
        amount=offer['rate']/100,
        places_decimal=2,
        amount_type=AmountType.string,
    )
    offer_currency_name = offer['system']['currency']['description']
    offer_system_data = loads(offer['system']['data'])
    systems = adecty_api_client.pay.systems.get(currency_name=offer_currency_name)['systems']
    offer_system = [
            system
            for system in systems
            if system['name'] == offer['system']['name']
    ][0]
    system_data_required = offer_system['data']

    form_widgets = [
        Text(
            text='1. Количество {currency} за 1 USD (курс)'.format(currency=offer_currency_name),
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
        ),
    ]

    form_widgets += [
        Text(
            text='2. Реквизиты',
            font=Font(
                size=22,
                weight=500,
            ),
            margin=Margin(top=12, down=8),
        ),
    ]

    for field in system_data_required:
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
                value=offer_system_data[field['name']],
                margin=Margin(down=12),
            ),
        ]

    form_widgets.append(
        InputButton(text='Сохранить изменения'),
    )
    form_widgets.append(
        Button(
            url='/wallet/offer/{}/delete',
            text='Удалить предложение',
        ),
    )

    widgets = [
        View(type=ViewType.horizontal, widgets=[
            Button(type=ButtonType.chip, url='/wallet/offers/get',
                   color_background=colors.background,
                   icon=Icon(path='app/icons/back.svg', color=colors.text)),
            Text(
                text='Редактировать предложение',
                font=Font(
                    size=32,
                    weight=700,
                ),
            ),
        ]),
        Form(widgets=form_widgets),
    ]

    try:
        adecty_api_client.pay.wallet.offer.update(
            account_session_token=account_session_token,
            id=offer_id,
        )
    except AdectyApiClientError:
        pass

    interface_html = interface.html_get(widgets=widgets, active='wallet_offers')

    if request.method == 'POST':
        offer_system_data_new = {}
        offer_rate_new = request.form.get('offer_rate')
        offer_rate_new_int = to_amount(
            amount=offer_rate_new,
            places_decimal=2,
            amount_type=AmountType.integer,
        )

        for field in system_data_required:
            offer_system_data_new[field['name']] = request.form.get(field['name'])

        offer_system_data_new = dumps(offer_system_data_new)

        if not (None in offer_system_data.values()) and offer_rate_new_int:
            adecty_api_client.pay.wallet.offer.update(
                account_session_token=account_session_token,
                id=offer_id,
                system_data=offer_system_data_new,
                rate=offer_rate_new_int,
            )
            return redirect('/wallet/offers/get')

    return interface_html
