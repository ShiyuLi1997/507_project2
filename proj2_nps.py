#################################
##### Name:Wenxuan Zhang
##### Uniqname:wenxuan
#################################

from bs4 import BeautifulSoup
import requests
import json
import secrets  # file that contains your API key


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

        return "{} ({}): {} {}".format(self.name, self.category, self.address,
                                       self.zipcode)


# part 1
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
    data = loads_cache("data.json")
    if "P1" in data.keys() and len(data["P1"]):
        print("Using cache")
        dic = data["P1"]
        return dic

    else:
        print("Fetching")
        dic = {}
        html = requests.get('https://www.nps.gov/index.htm').text
        soup = BeautifulSoup(html, 'html.parser')
        search_div = soup.find(class_='dropdown-menu SearchBar-keywordSearch')

        hello_list_items_link = search_div.find_all('a')

        for item in hello_list_items_link:
            link = item.get('href')
            # print(link)
            # print(item.text.lower())
            dic[item.text.lower()] = "https://www.nps.gov" + link

        save_cache(dic, "P1")
        return dic


# part 2
def get_site_instance(site_url):
    '''
    Make an instances from a national site URL.
    
    Parameters
    ----------
    site_url: string
        The URL for a national site page in nps.gov
    
    Returns
    -------
    instance
        a national site instance
    '''

    data = loads_cache("data.json")
    if "P2" in data.keys() and site_url in data["P2"].keys():
        # found what i need
        print("Using cache")
        NS = data["P2"][site_url]
        res = NationalSite(data["P2"][site_url]["type"],
                           data["P2"][site_url]["name"],
                           data["P2"][site_url]["add"],
                           data["P2"][site_url]["zip"],
                           data["P2"][site_url]["pho"])
        # no need to save to cache
        return res

    else:
        print("Fetching")
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
        add1 = add1 + ", " + abb1

        pho_div = soup.find(class_='vcard')
        pho_link = pho_div.find_all('span')
        pho1 = pho_link[-1].text.strip()

        # Not found what I need and be ready to store the data
        NS = {
            "type": type1,
            "name": name1,
            "add": add1,
            "zip": zip1,
            "pho": pho1
        }
        if "P2" in data.keys():
            data["P2"][site_url] = NS
        else:
            data["P2"] = {site_url: NS}
        # save to cache
        save_cache(data["P2"], "P2")

        res = NationalSite(type1, name1, add1, zip1, pho1)
        return res


# helper function
def save_cache(data, key):
    ''' To save the current state of data into cache
    Parameters
    ----------
    data: dict
        The dictionary to save
    key: string
        The key where to save
    Returns
    -------
    None
    '''
    cache = loads_cache("data.json")
    if "P1" not in cache.keys():
        cache["P1"] = {}
    if "P2" not in cache.keys():
        cache["P2"] = {}
    if "P3" not in cache.keys():
        cache["P3"] = {}
    if "P4" not in cache.keys():
        cache["P4"] = {}

    if key == "P1":
        cache["P1"].update(data)
    elif key == "P2":
        cache["P2"].update(data)
    elif key == "P3":
        cache["P3"].update(data)
    elif key == "P4":
        cache["P4"].update(data)
    # dump to cache file
    dump_cache("data.json", cache)


# helper function
def loads_cache(fn):
    try:
        with open(fn, "r") as f:
            data = json.load(f)
            f.close()
            return data
    except:
        return {}


# helper function
def dump_cache(fn, data):
    '''
    cache format:
      {
        P1 : {michigan:"state_url",alabama:"state_url",etc.},

        P2 : {
                site_url1: NS ,    # NS as dict
                site_url2: NS
              },

        P3 : {state_url1:[site_url1,site_url2,etc.],
              state_url2:[site_url1,site_url2,etc.]
             },

        P4 : {
              NationalSite.name : {many data},
              NationalSite.name : {many data}
            }
      }
    '''
    with open(fn, "w") as f:
        json.dump(data, f)
    f.close()


# helper func for part 3
def get_all_urls_for_a_state(state_url):
    """
    This is a helper function for part 3
    
    This func takes a state name, and search for 
        all the superlinks of its National Parks

    Param:  state: string
    Return: dict()

    """
    data = loads_cache("data.json")
    if "P3" in data.keys() and state_url in data["P3"].keys():
        print("Using cache")
        dic = data["P3"]
        return dic

    else:
        print("Fetching")
        html = requests.get(state_url).text
        soup = BeautifulSoup(html, 'html.parser')
        search_div = soup.find(id='parkListResultsArea')
        add_link = search_div.find_all('a')
        res_dic = {state_url: []}
        for item in add_link:
            link = item.get('href')
            if link.startswith('/'):
                res_dic[state_url].append("https://www.nps.gov" + link +
                                          "index.htm")
        # store in cache
        save_cache(res_dic,"P3")

    return res_dic


# helper function for part 3
# print out part 3's dictionary
def print_part_three_format(data,state):
    print("----------------------------------")
    print("List of national sites in {}".format(state))
    print("----------------------------------")
    i = 1
    for item in data:
        print("[{}] {}".format(i,item.info()))
        i += 1


# part 3
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

    # use helper function to get a format like 
    # state_url1:[site_url1,site_url2,etc.]
    # a dictionary containing state url pointing to a list of site urls.
    d = get_all_urls_for_a_state(state_url)
    # iterate all the site_urls in the list
    # and using part 2 to get the NationalSite Object.
    res = []
    for site_url in d[state_url]:
        res.append(get_site_instance(site_url))
    # finally return the result which contains 
    # a list of NationalSite objects
    # print_part_three_format(res,state)
    return res


# part 4
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
    data = loads_cache("data.json")
    if "P4" in data.keys() and site_object.name in data["P4"].keys():
        # found what i need
        print("Using cache")
        res = data["P4"][site_object.name]
        # no need to save to cache
        return res

    else:
        print("Fetching")
        # check if need to modify p1 and p2
        nearby_url = "http://www.mapquestapi.com/search/v2/radius"
        fullurl=nearby_url + "?key={key}&origin={zip}&maxMatches=10&radius=10&ambiguities=ignore&outFormat=json".format(key=secrets.API_KEY,zip=site_object.zipcode)
        # request
        content = requests.get(fullurl).text
        nearby_data = json.loads(content)
        # store in json file
        d ={}
        d[site_object.name] = nearby_data
        save_cache(d,"P4")
        # return
        return nearby_data

def validate_state_name (state,all_state_name):
    if state == "exit": return 0  # exit
    elif state not in all_state_name.keys(): return 1 # invalid input
    else: return 2  # valid input

def validate_number(num,length):
    try:
        num = int(num)
        if num <= length and num >= 1: return True
        else: return False
    except: 
        return False

def print_part_four(nearby_data,NS):
    print("----------------------------------")
    print("Places near {}".format(NS.name))
    print("----------------------------------")
    for item in nearby_data["searchResults"]:
        name = item["name"]
        if "group_sic_code_name" in item.keys() and len(item["group_sic_code_name"])!=0:
          category = item["group_sic_code_name"]
        else:
          category = "no category"

        if "address" in item.keys() and len(item["address"])!=0:
          address = item["address"]
        else:
          address = "no address"

        if "city" in item.keys() and len(item["city"])!=0:
          city = item["city"]
        else:
          city = "no city"

        print("- {} ({}): {}, {}".format(name,category,address,city))

def begin():
    # use part 1 to get the dict of all the states and their urls.
    part_one = build_state_url_dict()
    # user input inside a while loop to check the validation
    while 1:
        comm = input("Enter a state name (e.g. Michigan, michigan) or \"exit\": ").lower()
        validate = validate_state_name(comm,part_one)
        if validate == 0: # quit
            break
        elif validate == 1: # invalid input
            print("[Error] Enter proper state name")
            print()
            continue
        else: # valid input
            part_three = get_sites_for_state(part_one[comm])
            print_part_three_format(part_three,comm)
            # processing choosing number part
            while 1:
                print()
                print("---------------------------------------")
                num = input("Choose the number for detail search or \"exit\" or \"back\": ")
                if num == "exit": return
                elif num == "back": break
                else:
                    validate = validate_number(num,len(part_three))
                    if not validate:
                        print("[Error] Invalid input")
                        
                        continue
                    else: 
                        num = int(num)
                        # find nearby places
                        NS = part_three[num-1]
                        part_four = get_nearby_places(NS)
                        print_part_four(part_four,NS)

                        

if __name__ == "__main__":
    # wy_list = get_sites_for_state('https://www.nps.gov/state/al/index.htm')

    # start this code    
    begin()

