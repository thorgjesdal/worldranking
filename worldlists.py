import requests
from bs4 import BeautifulSoup
def reduce_world_list(event, clas, target_number):
   #url = 'https://www.iaaf.org/world-rankings/overall-ranking/men?regionType=countries&region=nor&page=1'
   url = 'https://www.iaaf.org/records/toplists/jumps/pole-vault/outdoor/men/senior/2019?regionType=area&region=europe&page=1&bestResultsOnly=true'
   #url = 'https://www.iaaf.org/world-rankings/'+event+'/'+clas+'?regionType=area&region=europe&page=1'
   headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'}

   max_participants_per_country = 3
   suspended_countries = ['RUS']
   
   r = requests.get(url, headers=headers)
   #print(r.text)
   soup = BeautifulSoup(r.text, 'html.parser')
   trows = soup.find_all('tr')
   full_ranking =[]
   for row in trows:
#     print(row)
      i = row.find(attrs={"data-th" : "Rank"})
      if i is not None:
         n = row.find(attrs={"data-th" : "Competitor"})
         name = n.text
         c = row.find(attrs={"data-th" : "Nat"})
         country = c.text
         m = row.find(attrs={"data-th" : "Mark"})
         mark = m.string
         full_ranking.append( ( (name.strip(), country.strip(), mark.strip()) ) )
   
   participants_per_country = {}
   reduced_ranking=[]  
   surplus_ranking=[]  

#  print (full_ranking)
   for i in full_ranking:
      c = i[1]
#     print(c)
      if c not in participants_per_country.keys():
         participants_per_country[c] = 0

      if c not in suspended_countries:
         if participants_per_country[c] < max_participants_per_country:
            reduced_ranking.append(i)
            participants_per_country[c] += 1
         else:
            surplus_ranking.append(i)

   cutoff = reduced_ranking[target_number-1][2]
      
   print('Standard = ', cutoff)
   print('Reduced ranking')
   l = 0
   for i in reduced_ranking:
      l +=1
      print(l,i)

   print('Surplus ranking')
   for i in surplus_ranking:
      print(i)
         
   return cutoff, reduced_ranking, surplus_ranking

    
c,r,s = reduce_world_list('pole-vault','men',26)
print (c)

"""
classes = ['men', 'women']
events = {}
events['men'] =   ['100m', '200m', '400m', '800m', '1500m', '5000m', '10000m', '110mh', '400mh', '3000msc', 'high-jump', 'pole-vault', 'long-jump', 'triple-jump', 'shot-put', 'discus-throw', 'hammer-throw', 'javelin-throw', 'decathlon']
events['women'] =   ['100m', '200m', '400m', '800m', '1500m', '5000m', '10000m', '100mh', '400mh', '3000msc', 'high-jump', 'pole-vault', 'long-jump', 'triple-jump', 'shot-put', 'discus-throw', 'hammer-throw', 'javelin-throw', 'heptathlon']
ea_targetnumbers = {}
ea_targetnumbers['men'] = {'100m' : 32, '200m' : 32, '400m' : 32, '800m' : 32, '1500m' : 24, '5000m' : 20, '10000m' : 24, '110mh' : 32, '400mh' : 32, '3000msc' : 32, 'high-jump' : 26, 'pole-vault' : 26, 'long-jump' : 26, 'triple-jump' : 26, 'shot-put' : 26, 'discus-throw' : 26, 'hammer-throw' : 26, 'javelin-throw' : 26, 'decathlon' : 24}
ea_targetnumbers['women'] = {'100m' : 32, '200m' : 32, '400m' : 32, '800m' : 32, '1500m' : 24, '5000m' : 20, '10000m' : 24, '100mh' : 32, '400mh' : 32, '3000msc' : 32, 'high-jump' : 26, 'pole-vault' : 26, 'long-jump' : 26, 'triple-jump' : 26, 'shot-put' : 26, 'discus-throw' : 26, 'hammer-throw' : 26, 'javelin-throw' : 26, 'heptathlon' : 24}
iaaf_targetnumbers = {}
iaaf_targetnumbers['men'] = {'100m' : 56, '200m' : 56, '400m' : 48, '800m' : 48, '1500m' : 45, '5000m' : 42, '10000m' : 27, '110mh' : 40, '400mh' : 40, '3000msc' : 45, 'high-jump' : 32, 'pole-vault' : 32, 'long-jump' : 32, 'triple-jump' : 32, 'shot-put' : 32, 'discus-throw' : 32, 'hammer-throw' : 32, 'javelin-throw' : 32, 'decathlon' : 24}
iaaf_targetnumbers['women'] = {'100m' : 56, '200m' : 56, '400m' : 48, '800m' : 48, '1500m' : 45, '5000m' : 42, '10000m' : 27, '100mh' : 40, '400mh' : 40, '3000msc' : 32, 'high-jump' : 32, 'pole-vault' : 32, 'long-jump' : 32, 'triple-jump' : 32, 'shot-put' : 32, 'discus-throw' : 32, 'hammer-throw' : 32, 'javelin-throw' : 32, 'heptathlon' : 24}

targetnumbers = iaaf_targetnumbers
for c in classes:
   for e in events[c]:
      cut,reduced,surplus = reduce_world_ranking(e,c,targetnumbers[c][e])
      print(e,c,cut)
"""
