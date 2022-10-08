
import random
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

domain_dict = {'Clear Pool and Mountain Cavern': ['Noblesse Oblige', 'Bloodstained Chivalry', 'Scholar', 'Gambler'],
               'Domain of Guyun': ['Retracing Bolide', 'Archaic Petra', 'Brave Heart', 'Lucky Dog'],
               'Hidden Palace of Zhou Formula': ['Crimson Witch of Flames', 'Lavawalker', 'Martial Artist', "Defender's Will"],
               'Midsummer Courtyard': ['Thundersoother', 'Thundering Fury', 'Adventurer', 'Resolution of Sojourner'],
               'Momiji-Dyed Court': ['Emblem of Severed Fate', "Shimenawa's Reminiscence", 'Tiny Miracle', 'Resolution of Sojourner'],
               'Peak of Vindagnyr': ['Heart of Depths', 'Blizzard Strayer', 'Gambler', "Defender's Will"],
               'Ridge Watch': ['Pale Flame', 'Tenacity of the Millileth', 'Martial Artist', 'Brave Heart'],
               'Slumbering Court': ['Ocean-Hued Clam', 'Husk of Opulent Dreams', 'Brave Heart', "Defender's Will"],
               'Spire of Solitary Enlightenment': ['Gilded Dreams', 'Deepwood Memories', 'Gambler', 'Tiny Miracle'],
               'The Lost Valley': ['Echoes of an Offering', 'Vermillion Hereafter', 'Gambler', 'Martial Artist'],
               'Valley of Remembrance': ['Maiden Beloved', 'Viridescent Venerer', 'Traveling Doctor', 'Tiny Miracle']}

sands_stats = ['HP%', 'ATK%', 'DEF%', 'Energy Recharge%', 'Elemental Mastery']
goblet_stats = ['HP%', 'ATK%', 'DEF%', 'Pyro DMG%', 'Electro DMG%', 'Cryo DMG%', 'Hydro DMG%', 'Dendro DMG%', 'Anemo DMG%', 'Geo DMG%', 'Physical DMG%', 'Elemental Mastery']
circlet_stats = ['HP%', 'ATK%', 'DEF%', 'CRIT Rate%', 'CRIT DMG%', 'Healing%', 'Elemental Mastery']

piece_dict = {1:'Flower', 2:'Plume', 3:'Sands', 4:'Goblet', 5:'Circlet'}
mstat_dict = {'Flower':[['HP'],[100]],
              'Plume':[['ATK'],[100]],
              'Sands':[sands_stats,[26.68, 26.66, 26.66, 10, 10]],
              'Goblet':[goblet_stats,[19.175, 19.175, 19.150, 5, 5, 5, 5, 5, 5, 5, 5, 2.5]],
              'Circlet':[circlet_stats,[22, 22, 22, 10, 10, 10, 4]]}
flatrates = [15.79, 15.79, 10.53, 10.53, 10.53, 10.53, 10.53, 7.89, 7.89]
pctrates = [15, 15, 15, 10, 10, 10, 10, 7.5, 7.5]
elementalrates = [13.64, 13.64, 13.64, 9.09, 9.09, 9.09, 9.09, 9.09, 6.82, 6.82]
critrates = [14.63, 14.63, 14.63, 9.76, 9.76, 9.76, 9.76, 9.76, 7.32]
substats = ['HP', 'ATK', 'DEF', 'HP%', 'ATK%', 'DEF%', 'Energy Recharge%', 'Elemental Mastery', 'CRIT Rate%', 'CRIT DMG%']
sstat_dict = {'HP': [substats.copy(), flatrates],
              'ATK': [substats.copy(), flatrates],
              'HP%': [substats.copy(), pctrates],
              'ATK%': [substats.copy(), pctrates],
              'DEF%': [substats.copy(), pctrates],
              'Energy Recharge%': [substats.copy(), pctrates],
              'Elemental Mastery': [substats.copy(), pctrates],
              'CRIT Rate%': [substats.copy(), critrates],
              'CRIT DMG%': [substats.copy(), critrates],}

for key in ['HP', 'ATK', 'HP%', 'ATK%', 'DEF%', 'Energy Recharge%', 'Elemental Mastery', 'CRIT Rate%', 'CRIT DMG%']:
  sstat_dict[key][0].remove(key)

for elemental in ['Pyro DMG%', 'Electro DMG%', 'Cryo DMG%', 'Hydro DMG%', 'Dendro DMG%', 'Anemo DMG%', 'Geo DMG%', 'Physical DMG%', 'Healing%']:
  sstat_dict[elemental] = [substats.copy(), elementalrates]


class Artifact:
  def __init__(self, stars, aset):
    self.aset = aset
    self.stars = stars
    self.piece = piece_dict[random.randint(1, 5)]
    self.mstat = random.choices(population = mstat_dict[self.piece][0], weights = mstat_dict[self.piece][1], k = 1)[0]
    self.sstat = []
    while len(self.sstat) < stars - 1:
      roll = random.choices(population = sstat_dict[self.mstat][0], weights = sstat_dict[self.mstat][1], k = 1)[0]
      if roll not in self.sstat:
        self.sstat.append(roll)
    
class Domain:
  def __init__(self, sets):
    self.sets = sets
    self.output = {3:[],
                   4:[],
                   5:[]}
    self.exp = 0
    self.match = False
  
  def create_match(self,  stars = [], asets = [], pieces = [], mstats = [], sstats = []):
    self.match = {'stars': stars,
                  'asets': asets,
                  'pieces': pieces,
                  'mstats': mstats,
                  'sstats': sstats}
  
  def check_match(self, a, verbose = False):
    if len(self.match['stars']) > 0 and a.stars not in self.match['stars']:
      return False
    if len(self.match['asets']) > 0 and a.aset not in self.match['asets']:
      return False
    if len(self.match['pieces']) > 0 and a.piece not in self.match['pieces']:
      return False
    if len(self.match['mstats']) > 0 and a.mstat not in self.match['mstats']:
      return False
    if len(self.match['sstats']) > 0:
      checklist = self.match['sstats'].copy()
      for stat in a.sstat:
        if stat in checklist:
          checklist.remove(stat)
      if len(checklist) > 0:
        return False
    if verbose:
      st.write(f'{a.stars}* {a.aset} {a.piece}')
      st.write(f'Main stat: {a.mstat}')
      st.write(f'Substats: {a.sstat}')
    return True

      

    


  def run(self, n = 1, verbose = False):
    fives = random.choices(population = [1,2], weights = [93, 7], k = 1)[0]
    fours = random.choices(population = [2,3], weights = [52, 48], k = 1)[0]
    threes = random.choices(population = [3,4], weights = [45, 55], k = 1)[0]
    match_found = False
    for j in range(n):
      for i in range(fives):
        a = Artifact(stars = 5, aset = random.choice(self.sets[:2]))
        if self.check_match(a, verbose):
          match_found = True
        self.output[5].append(a)
        self.exp += 3780
      for i in range(fours):
        a = Artifact(stars = 4, aset = random.choice(self.sets))
        if self.check_match(a, verbose):
          match_found = True
        self.output[4].append(a)
        self.exp += 2520
      for i in range(threes):
        a = Artifact(stars = 3, aset = random.choice(self.sets[2:]))
        if self.check_match(a, verbose):
          match_found = True
        self.output[3].append(a)
        self.exp += 1260
      
    return match_found
def lowercase(s):
  return s.lower()
  

st.title('Genshin Artifact Simulator')
condensed = st.sidebar.checkbox(label = 'Use Condensed Resin', value = False)
#verbose = st.sidebar.checkbox(label = 'Print results', value = False)
verbose = False
user_domain = st.sidebar.selectbox(label = 'Select a domain:', options =  domain_dict.keys())
user_sets = st.sidebar.multiselect('Select sets:', domain_dict[user_domain])
user_stars = []
if len(user_sets) > 0:
  fives, threes = False, False
  for uset in user_sets:
    if uset in domain_dict[user_domain][:2]:
      fives = True
    if uset in domain_dict[user_domain][2:]:
      threes = True
    if fives:
      user_stars.append(5)
    user_stars.append(4)
    if threes:
      user_stars.append(3)
  user_stars = st.sidebar.multiselect('Select stars:', user_stars) 
user_pieces = st.sidebar.multiselect('Select pieces:', ['Flower', 'Plume', 'Sands', 'Goblet', 'Circlet'])
soi = set()
if 'Sands' in user_pieces:
  for stat in sands_stats:
    soi.add(stat)
if 'Goblet' in user_pieces:
  for stat in goblet_stats:
    soi.add(stat)
if 'Circlet' in user_pieces:
  for stat in circlet_stats:
    soi.add(stat)
if len(soi) > 0:
  user_mstats = st.sidebar.multiselect('Select main stats:', soi)
else:
  user_mstats = []
if 'Flower' in user_pieces:
  user_mstats.append('hp')
if 'Plume' in user_pieces:
  user_mstats.append('atk')       
user_sstats = st.sidebar.multiselect('Select substats:', substats)


iterations = 100
attempts = []
if st.sidebar.button('Run simulation!'):
    for i in range(iterations):
        d = Domain(domain_dict[user_domain])
        d.create_match(asets = user_sets, stars = user_stars, pieces = user_pieces, mstats = user_mstats, sstats = user_sstats)
        run_count = 0
        while run_count < 1000:
            run_count += 1
            if d.run(verbose = verbose):
                break
            if condensed and d.run(verbose = verbose):
                break
        attempts.append(run_count)
    attempts.sort()
    st.write(f'Mean (average) number of runs: {sum(attempts)/iterations}')
    st.write(f'Median number of runs: {(attempts[iterations//2] + attempts[(iterations - 1)//2])/2}')
    
    fig = plt.figure(figsize = (12,6))
    
    sns.set_theme('notebook')
    plt.plot(range(1, iterations + 1), attempts)
    plt.title('Simulation distribution')
    plt.ylabel('Number of runs')
    plt.xlabel('Speed percentile')
    plt.xlim(1, iterations)
    plt.ylim(0, max(attempts))
    plt.fill_between(range(1, iterations + 1), attempts)
    st.pyplot(fig)
