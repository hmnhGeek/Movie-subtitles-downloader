import requests
import bs4, os
import argparse as ap
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

p = ap.ArgumentParser()
p.add_argument("tag", type = str, help = "movie name")
p.add_argument("-s", type = str, dest = 's', help = "download location")
args = p.parse_args()

url = "http://www.yifysubtitles.com"
search_url = url+"/search?q="

def movie(tag, loc = None):

    cwd = os.getcwd()

    if not os.path.isdir(loc):
        os.mkdir(loc)
    os.chdir(loc)

    URL = search_url+tag
    r = requests.get(URL)

    soup = bs4.BeautifulSoup(r.text)
    found = {}

    for div in soup.findAll('div', attrs = {'class': 'media-body'}):
        a = div.findAll('a')
        
        for i in a:
            source = url+'/'+ i.attrs['href']
            title = i.find("h3").contents
            found.update({title[0]:source})

    print "Found", len(found), "movies."
    count = 1

    temp = found.keys()
    for i in temp:
        print count, i
        count+=1

    print "Press ctrl-c to exit."
    

    try:
        choice = input(">>> ")
        if choice <= len(temp):
            chosen = temp[choice-1]
            sublink = found[chosen]

            subs = []

            subsoup = bs4.BeautifulSoup(requests.get(sublink).text)

            for tr in subsoup.findAll('tr'):
                for td in tr.findAll('td'):
                    try:
                        if td.attrs['class'] == ['download-cell',]:
                            anch = td.findAll('a')
                            for j in anch:
                                subs.append(j.attrs['href'])
                    except:
                        pass


            print "Found", len(subs), "subtitles..."
            counter = 1
            for i in subs:
                print counter, i
                counter += 1

            print "Press ctrl-c to exit."
            try:
                x = input("Which subtitle? ")

                if x <= len(subs):
                    selected = subs[x-1]
                    sel = url + selected

                    itemsoup = bs4.BeautifulSoup(requests.get(sel).text)

                    for anchor_tag in itemsoup.findAll('a', attrs = {'class':'btn-icon download-subtitle'}):
                        File = anchor_tag.attrs['href']
                        print "Downloading ---->", File
                        with open(os.path.basename(File), 'wb') as f:
                            f.write(requests.get(File).content)
                        print "Downloaded: 200 (OK)"
            except KeyboardInterrupt:
                return

        os.chdir(cwd)
        return 1
    except KeyboardInterrupt:
        return 

if args.tag and args.s:
    movie(args.tag, args.s)

elif args.tag and not args.s:
    movie(args.tag, os.getcwd())
