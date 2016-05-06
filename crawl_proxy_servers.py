'''
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU Affero General Public License as
* published by the Free Software Foundation, either version 3 of the
* License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU Affero General Public License for more details.
*
* You should have received a copy of the GNU Affero General Public
* License
* along with this program. If not, see
* <http://www.gnu.org/licenses/>.
'''
import requests
import multiprocessing
from bs4 import BeautifulSoup

proxy_list = []

test_url = 'http://ipservice.163.com/isFromMainland'
crawl_url = 'http://cn-proxy.com'

def crawl_proxy_servers():
  page = requests.get(crawl_url)
  if page.status_code == requests.codes.ok:
    bsobj = BeautifulSoup(page.text, 'html.parser')
    
    try:
      proxy_table = bsobj.find('div',
          {'class':'table-container'}).find('table').find('tbody')
      for tr in proxy_table.findAll('tr'):
        proxy_info = tr.findAll('td')
        ip = proxy_info[0]
        port = proxy_info[1]
        print(ip.get_text())
        print(port.get_text())
        proxy = ip.get_text()+':'+port.get_text()
        if test_proxy_server(proxy):
          proxy_list.append(proxy)
    except AttributeError as e:
      print('Tag not found')
    
  else:
    print("wrong url")


def test_proxy_server(proxy):
  proxies = {
        'http':proxy
      }

  try:
    response = requests.get(test_url, proxies=proxies, timeout=10)
    if response.status_code == requests.codes.ok:
      print(response.text)
      if response.text == 'true':
        return True
      else:
        return False
    else:
      print('[163 test]: return error code')
      return False
  except (requests.exceptions.Timeout, requests.exceptions.RequestException,
      requests.exceptions.ConnectionError) as e:
    print('[163 test]: some bad happened')
    return False

if __name__ == '__main__':
  crawl_proxy_servers()
  print("final list:")
  print(proxy_list)


