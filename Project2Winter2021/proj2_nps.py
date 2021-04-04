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
    print("in p1")

    data = loads_cache("data.json")
    if "P1" in data.keys():
      print("caching")
      dic = data["P1"]
      return dic
    
    else:
      print("fetching")
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

      save_cache(dic,"P1")
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

    print("in p2")
    data = loads_cache("data.json")
    if "P2" in data.keys() and site_url in data["P2"].keys():
      # found what i need
      print("caching")
      NS = data["P2"][site_url]
      res = NationalSite(data["P2"][site_url]["type"],data["P2"][site_url]["name"],data["P2"][site_url]["add"],data["P2"][site_url]["zip"],data["P2"][site_url]["pho"])
      # no need to save to cache
      return res
      
    else:
      print("fetching")
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

      # Not found what I need
      NS = {"type":type1, "name":name1, "add":add1, "zip":zip1, "pho":pho1}
      if "P2" in data.keys():
          data["P2"][site_url] = NS
      else:
          data["P2"] = {site_url:NS}
      # save to cache      
      save_cache(data["P2"],"P2")

      res = NationalSite(type1, name1, add1, zip1, pho1)
      return res

# helper function
def save_cache(data,key):
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
      
  if key == "P1":
      cache["P1"] = data
  elif key == "P2":
      cache["P2"] = data
  elif key == "P3":
      cache["P3"] = data
  # dump to cache file
  dump_cache("data.json",cache)

# helper function
def loads_cache(fn):
    try :   
        with open(fn,"r") as f:
            data = json.load(f)
            f.close()
            return data
    except FileNotFoundError:
        return {}
# helper function
def dump_cache(fn,data):
    '''
    cache format:
      {
        P1 : {michigan:"url",alabama:"url",etc.},

        P2 : {
                site_url1: {NS},    # NS as dict
                site_url2: {NS}
              }

        P3 : {michigan:[url1,url2,etc.],
              alabama:[url1,url2,etc.],
             },
      }
    '''
    with open(fn,"w") as f:
        json.dump(data, f)
    f.close()

# helper func for part 3
def get_all_urls_for_a_state(all_state_dic,state):
    """
    This is a helper function for part 3
    
    This func takes a state name, and search for 
        all the superlinks of its National Parks

    Param:  state: string
    Return: dict()

    """
    data = loads_cache("data.json")
    if "P3" in data.keys() and state in data["P3"].keys():
        print("caching")
        dic = data["P3"]
        return dic
    
    else:
        result_parks_url = all_state_dic[state]
        html = requests.get(result_parks_url).text
        soup = BeautifulSoup(html, 'html.parser')
        search_div = soup.find(id = 'parkListResultsArea')
        add_link = search_div.find_all('a')
        res_dic = {state:[]}
        for item in add_link:
            link = item.get('href')
            if link.startswith('/'):
              res_dic[state].append("https://www.nps.gov" + link + "index.htm")
        # store in cache
        if "P3" in data.keys():
            data["P3"][state] = res_dic
            save_cache(data["P3"],"P3")
        else:
            

        data["P3"][state] = res_dic
        save_cache(data["P3"],"P3")
        
    return res_dic

def print_part_three_format(data):
    print(data)

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
    # use part 1
    all_state_dic = build_state_url_dict()
    # user input
    state = input("State Name: ").lower()
    # get all the sites urls of a state
    d = get_all_urls_for_a_state(all_state_dic,state)
    print_part_three_format(d)



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
    # check if need to modify p1 and p2
    pass
    

if __name__ == "__main__":
    wy_list = get_sites_for_state('https://www.nps.gov/state/wy/index.htm')