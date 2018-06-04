import re
import os
import getpass #for username
# import sys

# if 'lin' in sys.platform:
def_dir = os.path.join(os.sep,'home',getpass.getuser(), 'Desktop',
            'mass_fetch')

if not os.path.exists(def_dir):
    os.makedirs(def_dir)


class Values:
    language = ('en', 'cs', 'da', 'de', 'es', 'fr', 'id','it', 'hu', 'nl', 'no', 'pl', 'pt', 'ro', 'sk', 'fi', 'sv', 'tr', 'vi', 'th', 'bg', 'ru', 'el', 'ja', 'ko', 'zh')
    image_type=("photo","illustration", "vector", 'all')
    orientation=('all', 'horizontal', 'vertical')
    category=("any","fashion","nature","backgrounds","science","education","people","feelings","religion","health","places","animals","industry","food","computer","sports","transportation","travel","buildings","business","music")
    colors =("default","grayscale", "transparent", "red", "orange", "yellow", "green", "turquoise", "blue", "lilac", "pink", "white", "gray", "black", "brown" )
    order=("popular", "latest")
    video_type=("all", "film", "animation")
    quality=("high", "medium", "large")

    #SOME DEFAULT VALUES OF QUERIES
    quantity= '100'
    search_term=''
    list_search=''
    def_path=def_dir


    #ALLOWED REGEXES FOR QUERIES
    #1)number
    #2)word
    #3)word list
    #4)path

    numeric_value=re.compile(r'^[0-9]+$')
    fetch_values=re.compile(r'^[a-zA-Z\ ]+$')
    multi_search=re.compile(r'^[a-zA-Z][a-zA-Z, ]*$')
    #here only linux path file
    output_path=re.compile(r'^[a-zA-Z/_0-9]*$')
