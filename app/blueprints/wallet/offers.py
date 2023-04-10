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

from adecty_design.properties import Font, Margin, Padding, Align, AlignType
from adecty_design.widgets import Text, Button, View, ViewType, ButtonType, Card, Dictionary
from adecty_design.widgets.icon import Icon
from app.adecty_api_client import adecty_api_client
from app.adecty_design import colors, interface
from app.functions.data_input import data_input


blueprint_wallet_offers = Blueprint('blueprint_wallet_offers', __name__, url_prefix='/offers')


@blueprint_wallet_offers.route(rule='/get', endpoint='wallet_offers_get', methods=('GET',))
@data_input({'account_session_token': True, 'wallet': True})
def wallet_offers_get(account_session_token, wallet):
    wallet_offers = adecty_api_client.pay.wallet.offers_get(
        account_session_token=account_session_token,
    )['wallet_offers']

    widgets = [
        View(
            type=ViewType.horizontal,
            widgets=[
                Text(
                    text='Мои предложения',
                    font=Font(
                        size=32,
                        weight=700,
                    ),
                ),
                Button(
                    type=ButtonType.chip,
                    text='Создать',
                    url='/wallet/offer/create',
                    icon=Icon(path='app/icons/add.svg'),
                ),
            ],
            properties_additional=[Align(type=AlignType.space_between)],
        )
    ]
    for offer in wallet_offers:
        widgets.append(Card(
            widgets=[
                Text(
                    text='{system_name}'.format(
                        system_name=offer['system']['description'],
                    ),
                    font=Font(
                        size=22,
                        weight=500,
                    ),
                ),
                Dictionary(
                    margin=Margin(horizontal=12),
                    keys=['Количество', 'Курс', 'Активно до'],
                    values=[
                        '{value_from} - {value_to} USD'.format(
                            value_from=offer['value_from'] / 100,
                            value_to=offer['value_to'] / 100,
                        ),
                        '{rate} {currency} за 1 USD'.format(
                            rate=offer['rate'] / 100,
                            currency=offer['system']['currency']['description'],
                        ),
                        '{updated_datetime}'.format(updated_datetime=offer['updated_datetime'])
                    ],

                ),
                View(
                    type=ViewType.horizontal,
                    widgets=[
                        Button(
                            type=ButtonType.chip,
                            text='Редактировать',
                            url='/wallet/offer/{offer_id}/update'.format(
                                offer_id=offer['id'],
                            ),
                            icon=Icon(path='app/icons/edit.svg', color=colors.text),
                            color_background=colors.background,
                        ),
                        Button(
                            type=ButtonType.chip,
                            text='Продлить',
                            url='/wallet/offer/{offer_id}/update/active'.format(
                                offer_id=offer['id'],
                            ),
                            icon=Icon(path='app/icons/update.svg', color=colors.background),
                            color_background=colors.positive,
                        ),
                    ],
                 ),
            ],
            margin=Margin(horizontal=12, ),
            padding=Padding(vertical=24, horizontal=18),
            color_background=colors.background_secondary,
        ))

    interface_html = interface.html_get(widgets=widgets, active='wallet_offers')
    return interface_html
