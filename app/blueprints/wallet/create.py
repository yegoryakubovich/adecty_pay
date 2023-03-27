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

from adecty_api_client.adecty_api_client_error import AdectyApiClientError
from adecty_design.properties import Font, Margin
from adecty_design.widgets import Text, Button
from app.adecty_api_client import adecty_api_client
from app.adecty_design import colors, interface
from app.adecty_design.navigation import navigation_none
from app.functions.data_input import data_input


blueprint_wallet_create = Blueprint('blueprint_wallet_create', __name__, url_prefix='/create')


@blueprint_wallet_create.route(rule='/terms', endpoint='wallet_create_terms', methods=('GET',))
@data_input({'account_session_token': True})
def wallet_create_terms(account_session_token):
    try:
        adecty_api_client.pay.wallet.get(account_session_token=account_session_token)
        return redirect(location='/wallet/all')
    except AdectyApiClientError:
        pass

    widgets = [
        Text(
            text='Создание кошелька',
            font=Font(
                size=32,
                weight=700,
            ),
            margin=Margin(down=8),
        ),
        Text(
            text='Ваш кошелек еще не создан. Для его создания Вам необходимо принять правила пользования сервисом:',
            font=Font(
                size=12,
                weight=600,
            ),
            margin=Margin(down=18),
        ),

        Text(
            text='1. Terms<br>'
                 'By accessing this Website, accessible from Finance Express.yegoryakubovich.com, you are agreeing to '
                 'be bound by these Website Terms and Conditions of Use and agree that you are responsible for the '
                 'agreement with any applicable local laws. If you disagree with any of these terms, you are '
                 'prohibited from accessing this site. The materials contained in this Website are protected '
                 'by copyright and trade mark law.<br>'
                 '<br>2. Use License<br>'
                 'Permission is granted to temporarily download one copy of the materials on Website for personal, '
                 'non-commercial transitory viewing only. This is the grant of a license, not a transfer of title, '
                 'and under this license you may not:<br>'
                 '- modify or copy the materials<br>'
                 '- use the materials for any commercial purpose or for any public display;<br>'
                 '- attempt to reverse engineer any software contained on Website;<br>'
                 '- remove any copyright or other proprietary notations from the materials;<br>'
                 '- transferring the materials to another person or "mirror" the materials on any other server.<br>'
                 '<br>3. Disclaimer<br>'
                 'All the materials on Finance Express’s Website are provided "as is". Finance Express makes no '
                 'warranties, may it be expressed or implied, therefore negates all other warranties. Furthermore, '
                 'Finance Express does not make any representations concerning the accuracy or reliability of the '
                 'use of the materials on its Website or otherwise relating to such materials or any sites linked to '
                 'this Website.<br>'
                 '<br>4. Limitations<br>'
                 'Finance Express or its suppliers will not be hold accountable for any damages that will arise with '
                 'the use or inability to use the materials on Finance Express’s Website, even if Finance Express or '
                 'an authorize representative of this Website has been notified, orally or written, of the possibility '
                 'of such damage. Some jurisdiction does not allow limitations on implied warranties or limitations '
                 'of liability for incidental damages, these limitations may not apply to you.<br>'
                 '<br>5. Revisions and Errata<br>'
                 'The materials appearing on Finance Express’s Website may include technical, typographical, or '
                 'photographic errors. Finance Express will not promise that any of the materials in this Website '
                 'are accurate, complete, or current. Finance Express may change the materials contained on its '
                 'Website at any time without notice. Finance Express does not make any commitment to update the '
                 'materials.<br>'
                 '<br>6. Links<br>'
                 'Finance Express has not reviewed all of the sites linked to its Website and is not responsible '
                 'for the contents of any such linked site. The presence of any link does not imply endorsement '
                 'by Finance Express of the site. The use of any linked website is at the user’s own risk.<br>'
                 '<br>7. Site Terms of Use Modifications<br>'
                 'Finance Express may revise these Terms of Use for its Website at any time without prior notice. '
                 'By using this Website, you are agreeing to be bound by the current version of these Terms and '
                 'Conditions of Use.<br>'
                 '<br>8. Governing Law<br>'
                 'Any claim related to Finance Express`s Website shall be governed by the laws of af without '
                 'regards to its conflict of law provisions.<br>',
            font=Font(
                size=12,
                weight=400,
            ),
            margin=Margin(down=8),
        ),
        Button(
            url='/wallet/create',
            text=Text(
                text='Принимаю правила, создать кошелек',
                font=Font(
                    weight=700,
                    color=colors.primary,
                ),
            ),
            margin=Margin(horizontal=18),
        ),
    ]

    interface_html = interface.html_get(widgets=widgets, active='wallet', navigation=navigation_none)
    return interface_html


@blueprint_wallet_create.route(rule='', endpoint='wallet_create', methods=('GET',))
@data_input({'account_session_token': True})
def wallet_create(account_session_token):
    try:
        adecty_api_client.pay.wallet.get(account_session_token=account_session_token)
        return redirect(location='/wallet/all')
    except AdectyApiClientError:
        pass

    try:
        adecty_api_client.pay.wallet.create(account_session_token=account_session_token)
        return redirect(location='/wallet/all')
    except AdectyApiClientError:
        return 500
