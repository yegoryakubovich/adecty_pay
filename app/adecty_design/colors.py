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


from adecty_design.properties.colors import Colors
from config import IS_FEXPS


colors = Colors(
    background='#fff',
    background_secondary='#d1d1d1',
    negative='#ed7474',
    positive='#a9ffa3',
    primary='#000',
    primary_secondary='#9c9c9c',
    selected='#777',
    text='#363636',
    unselected='#fff',
) if not IS_FEXPS else Colors(
    background='#181818',
    background_secondary='#383838',
    negative='#ed7474',
    positive='#57a752',
    primary='#fffc5a',
    primary_secondary='#d3d766',
    selected='#777',
    text='#fff',
    unselected='#fff',
)
