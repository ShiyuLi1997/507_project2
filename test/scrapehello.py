#scrapehello.py

from bs4 import BeautifulSoup

f = open("helloFinal.html")
html_text = f.read()
#print(type(html_text))
#
#print(html_text)
#print("                  ")
#print("                  ")
soup = BeautifulSoup(html_text, 'html.parser')
#print("soup: ",soup)

# searching by tag
all_list_items = soup.find_all('li')
all_divs = soup.find_all('div')

# searching by tag AND class
all_european_list_items = soup.find_all('li', class_='european')

# searching by id
all_hello_elements = soup.find_all(id='hello-list')

print(all_hello_elements)
print()
print(all_hello_elements[0])
print()
print(all_hello_elements[0].contents[1])
print()
print(all_hello_elements[0].contents[1].contents)
print()


print("iterating with contents")
for item in all_hello_elements[0].contents[1].contents:
    print(item)

print("============================================================")
print("ITERATING THROUGH ITEMS IN A LIST")
hello_list_items = all_hello_elements[0].find_all('li')
for item in hello_list_items:
    print(item.text.strip())
