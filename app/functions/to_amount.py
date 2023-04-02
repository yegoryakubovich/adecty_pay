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


class AmountType:
    string = 'string'
    integer = 'integer'
    float = 'float'


def to_amount(
        amount: str | float | int,
        places_decimal: int,
        amount_type: str = AmountType.integer,
) -> str | float | int | None:
    if type(amount) is str:
        amount = amount.replace(',', '.')
        amount = amount.replace(' ', '')
        try:
            amount = float(amount)
        except ValueError:
            return None

    if amount_type == AmountType.string:
        return f'{amount:.{places_decimal}f}'
    elif amount_type == AmountType.float:
        return amount
    elif amount_type == AmountType.integer:
        return int(amount * pow(10, places_decimal))
