import requests
from bs4 import BeautifulSoup
def reduce_world_ranking(event, clas, target_number):
   #url = 'https://worldrankings-staging.aws.iaaf.org/world-rankings/pole-vault/men?regionType=world&page=1'
   url = 'https://worldrankings-staging.aws.iaaf.org/world-rankings/'+event+'/'+clas+'?regionType=area&region=europe&page=1'
   max_participants_per_country = 3
   suspended_countries = ['RUS']
   r = requests.get(url)
   soup = BeautifulSoup(r.text, 'html.parser')
   trows = soup.find_all('tr')
   full_ranking =[]
   for row in trows:
      i = row.find(attrs={"data-th" : "Place"})
      if i is not None:
         n = row.find(attrs={"data-th" : "Competitor"})
         name = n.string
         c = row.find(attrs={"data-th" : "Nat"})
         country = c.text
         s = row.find(attrs={"data-th" : "Score"})
         score = s.string
         full_ranking.append( ( (name.strip(), country.strip(), score.strip()) ) )
   
   participants_per_country = {}
   reduced_ranking=[]  
   surplus_ranking=[]  

   for i in full_ranking:
      c = i[1]
#  print(c)
      if c not in participants_per_country.keys():
         participants_per_country[c] = 0

      if c not in suspended_countries:
         if participants_per_country[c] < max_participants_per_country:
            reduced_ranking.append(i)
            participants_per_country[c] += 1
         else:
            surplus_ranking.append(i)

   cutoff = reduced_ranking[target_number-1][2]
   """
   print('Standard = ', reduced_ranking[target_number-1][2])
   print('Reduced ranking')
   for i in reduced_ranking:
      print(i)

   print('Surplus ranking')
   for i in surplus_ranking:
      print(i)
   """
   return cutoff, reduced_ranking, surplus_ranking

#c,r,s = reduce_world_ranking('pole-vault','men',26)
#print (c)
classes = ['men', 'women']
events = {}
events['men'] =   ['100m', '200m', '400m', '800m', '1500m', '5000m', '10000m', '110mh', '400mh', '3000msc', 'high-jump', 'pole-vault', 'long-jump', 'triple-jump', 'shot-put', 'discus-throw', 'hammer-throw', 'javelin-throw', 'decathlon']
events['women'] =   ['100m', '200m', '400m', '800m', '1500m', '5000m', '10000m', '100mh', '400mh', '3000msc', 'high-jump', 'pole-vault', 'long-jump', 'triple-jump', 'shot-put', 'discus-throw', 'hammer-throw', 'javelin-throw', 'heptathlon']
targetnumbers = {}
targetnumbers['men'] = {'100m' : 32, '200m' : 32, '400m' : 32, '800m' : 32, '1500m' : 24, '5000m' : 20, '10000m' : 24, '110mh' : 32, '400mh' : 32, '3000msc' : 32, 'high-jump' : 26, 'pole-vault' : 26, 'long-jump' : 26, 'triple-jump' : 26, 'shot-put' : 26, 'discus-throw' : 26, 'hammer-throw' : 26, 'javelin-throw' : 26, 'decathlon' : 24}
targetnumbers['women'] = {'100m' : 32, '200m' : 32, '400m' : 32, '800m' : 32, '1500m' : 24, '5000m' : 20, '10000m' : 24, '100mh' : 32, '400mh' : 32, '3000msc' : 32, 'high-jump' : 26, 'pole-vault' : 26, 'long-jump' : 26, 'triple-jump' : 26, 'shot-put' : 26, 'discus-throw' : 26, 'hammer-throw' : 26, 'javelin-throw' : 26, 'heptathlon' : 24}

for c in classes:
   for e in events[c]:
      cut,reduced,surplus = reduce_world_ranking(e,c,targetnumbers[c][e])
      print(e,c,cut)
