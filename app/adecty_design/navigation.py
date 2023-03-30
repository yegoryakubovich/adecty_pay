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


from adecty_design.widgets.icon import Icon
from adecty_design.widgets.required import Navigation, NavigationItem


navigation_main = Navigation(
    items=[
        NavigationItem(
            id='wallet',
            name='Wallet',
            url='/wallet/all',
            icon=Icon(path='app/icons/wallet.svg')
        ),
        NavigationItem(
            id='wallet_offers',
            name='My Offers',
            url='/wallet/offers/get',
            icon=Icon(path='app/icons/wallet_offers.svg')
        ),
        NavigationItem(
            id='deals',
            name='Deals',
            url='/deals',
            icon=Icon(path='app/icons/deals.svg')
        ),
    ]
)

navigation_none = Navigation(items=[])
