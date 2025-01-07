import requests, re
from bs4 import BeautifulSoup

ycpage = requests.get("http://www.yc.ac.kr/yonam/web/cop/bbs/selectBoardList.do?bbsId=BBSMSTR_000000000590")
soup = BeautifulSoup(ycpage.text, 'html.parser')
test_elements = soup.find_all('td')#, class_='td_subject')

def clener(text):
    result = re.sub(r"[*N\s]", "", text)
    return result

for a in test_elements:
    if 'td_datetime' in a.get('class', []) or 'td_subject' in a.get('class', []):
        print(a.text)




for a in test_elements:
    # if 'td_datetime' in a.get('class', []):
    #     print(clener(a.text))
    # if 'td_subject' in b.get('class', []):
    #     print(clener(a.text))
    print(a)
    print(b)