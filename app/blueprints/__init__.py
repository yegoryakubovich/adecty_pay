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


from app.blueprints.account import blueprint_account
from app.blueprints.main import blueprint_main
from app.blueprints.errors import blueprint_errors
from app.blueprints.wallet import blueprint_wallet


blueprints = (
    blueprint_errors,
    blueprint_main,
    blueprint_account,
    blueprint_wallet,
)
