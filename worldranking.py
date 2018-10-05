import requests
from bs4 import BeautifulSoup
#url = 'https://worldrankings-staging.aws.iaaf.org/world-rankings/pole-vault/men?regionType=world&page=1'
url = 'https://worldrankings-staging.aws.iaaf.org/world-rankings/pole-vault/men?regionType=area&region=europe&page=1'
target_number = 32
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

print('Standard = ', reduced_ranking[target_number-1][2])
print('Reduced ranking')
for i in reduced_ranking:
   print(i)

print('Surplus ranking')
for i in surplus_ranking:
   print(i)

