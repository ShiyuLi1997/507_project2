#################################
##### Name:Wenxuan Zhang
##### Uniqname:wenxuan
#################################

from bs4 import BeautifulSoup
import requests
import json
import secrets # file that contains your API key


class NationalSite:
    '''a national site

    Instance Attributes
    -------------------
    category: string
        the category of a national site (e.g. 'National Park', '')
        some sites have blank category.
    
    name: string
        the name of a national site (e.g. 'Isle Royale')

    address: string
        the city and state of a national site (e.g. 'Houghton, MI')

    zipcode: string
        the zip-code of a national site (e.g. '49931', '82190-0168')

    phone: string
        the phone of a national site (e.g. '(616) 319-7906', '307-344-7381')
    '''
    def __init__(self, category, name, address, zipcode, phone):
        self.category = category
        self.name = name
        self.address = address
        self.zipcode = zipcode
        self.phone = phone

    def info(self):
        
        return "{} ({}): {} {}".format(self.name,self.category,self.address,self.zipcode)
    
    

def build_state_url_dict():
    ''' Make a dictionary that maps state name to state page url from "https://www.nps.gov"

    Parameters
    ----------
    None

    Returns
    -------
    dict
        key is a state name and value is the url
        e.g. {'michigan':'https://www.nps.gov/state/mi/index.htm', ...}
    '''
    dic = dict()

    html = requests.get('https://www.nps.gov/index.htm').text
    soup = BeautifulSoup(html, 'html.parser')
    search_div = soup.find(class_='dropdown-menu SearchBar-keywordSearch')

    hello_list_items_link = search_div.find_all('a')     

    for item in hello_list_items_link:
        link = item.get('href')
        # print(link)
        # print(item.text.lower())
        dic[item.text.lower()] = "https://www.nps.gov" + link
    return dic

       

def get_site_instance(site_url):
    '''Make an instances from a national site URL.
    
    Parameters
    ----------
    site_url: string
        The URL for a national site page in nps.gov
    
    Returns
    -------
    instance
        a national site instance
    '''
    html = requests.get(site_url).text
    soup = BeautifulSoup(html, 'html.parser')
    name_div = soup.find(class_='col-sm-12')
    name_link = name_div.find_all('a') 
    name1 = name_link[0].text.strip()

    type_link = name_div.find_all("span")
    type1 = type_link[0].text.strip()

    add_div = soup.find(class_='mailing-address')
    add_link = add_div.find_all('span')
    add1 = add_link[-3].text
    zip1 = add_link[-1].text.strip()

    abb1 = add_link[-2].text
    add1 = add1 +", " +abb1

    pho_div = soup.find(class_='vcard')
    pho_link = pho_div.find_all('span')
    pho1 = pho_link[-1].text.strip()

    res = NationalSite(type1, name1, add1, zip1, pho1)
    return res


def get_cache(fn):
    try :   
        with open(fn,"r") as f:
            data = json.load(f)
        f.close()
        return data
    except FileNotFoundError:
        return {}

def dump_cache(fn,data):
    with open(fn,"w") as f:
        json.dump(data, f)
    f.close()

def get_sites_for_state(state_url):
    '''Make a list of national site instances from a state URL.
    
    Parameters
    ----------
    state_url: string
        The URL for a state page in nps.gov
    
    Returns
    -------
    list
        a list of national site instances
    '''
    # read cache if exists open cache function(create new caching dictionary) and save function(save dictionary to cache file) request with cache function(fetching(if statement))
    data = get_cache ("cache.json")
    # user input
    comm = input("User input: ")
    # check if input is in data key
    if comm in data.keys():
        # if comm in key
        print("Using Cache")
        # ......
    else:
        # if comm not in key
        print("Fetching")
        #


    


def get_nearby_places(site_object):
    '''Obtain API data from MapQuest API.
    
    Parameters
    ----------
    site_object: object
        an instance of a national site
    
    Returns
    -------
    dict
        a converted API return from MapQuest API
    '''
    # check if need to modify p1 and p2
    pass
    

if __name__ == "__main__":
    wy_list = get_sites_for_state('https://www.nps.gov/state/wy/index.htm')