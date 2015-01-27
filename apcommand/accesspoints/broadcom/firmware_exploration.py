
# python standard library
import re

# third-party
from bs4 import BeautifulSoup

soup = BeautifulSoup(open('firmware_asp.html'))

# find_all returns a list, but since we specified the attrs, we know it has what we want
form = soup('form', attrs={'action': 'upgrade.cgi'})[0]

table = form('table')[0]

for table in form('table'):
    if any(['Version' in tag.next for tag in table('th')]):
        break
print(table)

data = table('td')
extractor = re.compile('\s*<[/]*td>')
for index in range(1,6,2):
    print(unicode(extractor.sub('', str(data[index])), errors='ignore'))