import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from textwrap import wrap
from os import listdir


def add(self, key, value):
    # used to add to dictionaries
    self[key] = value

def readEpisodeForCharacters(episode):
    df = pd.read_csv('scripts/'+episode, names=["Number", "Character", "Line"])
    #print(df.head(5))
    rslf_len= len(df.index)
    #print df.columns

    #rslt_df = df.loc[(df['Character'] == "Kate Spivack")]
    #print(rslt_df.head)

    rslf = df.groupby('Character')
    rslf_char = {}
    rslf_char = rslf.groups.keys()

    #print rslf.groups
    rslf_tally=rslf.size()
    print rslf_tally
    rslf_tally.to_csv('tally/'+episode, header=False)
    rslf_num=[]
    rslf_num_per=[]
    print rslf_char
    for char in rslf_char:
        rslf_num.append(rslf_tally.loc[char])
        rslf_num_per.append(float((rslf_tally.loc[char]*100)/rslf_len))

    print "Total Lines: ", rslf_len
    episodeCharGraph(rslf_char, rslf_num, rslf_num_per, episode)
    

def episodeCharGraph(rslf_char, rslf_num, rslf_num_per,episode):
    rslf_char = ['\n'.join(wrap(c, 7, replace_whitespace=False)) for c in rslf_char]

    plt.subplot(2, 1, 1)
    plt.bar(rslf_char, rslf_num, width=0.3, color='green')
    plt.xticks(rotation=45, fontsize=5)
    plt.xlabel('Characters')
    plt.ylabel('# of lines')
    plt.title('Episode Line Tallies')
    plt.yticks(np.arange(0, max(rslf_num) + 5, 25))
    plt.grid(linestyle=':', linewidth=1, color='#B5E772')

    plt.subplot(2, 1, 2)
    plt.ylabel("Percentage")
    plt.xticks(rotation=45, fontsize=7)
    plt.bar(rslf_char, rslf_num_per, width=0.3, color='blue')
    plt.yticks(np.arange(0, max(rslf_num_per) + 5, 5))
    plt.grid(linestyle=':', linewidth=1, color='#72C4E7')

    episode=episode.split(".")[0]
    plt.savefig('img/'+episode+'.png')


def episodeCharLineOnly(rslf_char, rslf_num, rslf_len):
    print(rslf_len)
    rslf_char = ['\n'.join(wrap(c, 7, replace_whitespace=False)) for c in rslf_char]
    fig, ax = plt.subplots()
    ax.bar(rslf_char, rslf_num, width=0.3, color='green')
    ax.yaxis.grid(linestyle=':', linewidth=1, color='#B5E772')

    plt.xticks(rotation=45)

    plt.xlabel('Characters')
    plt.ylabel('# of lines')
    plt.title('Episode Line Tallies')
    plt.yticks(np.arange(0, max(rslf_num) + 5, 25))
    #plt.show()

def readSeason(season, bool):
    path='scripts/'
    extension='csv'
    filenames = listdir(path)
    filenames = [filename for filename in filenames if filename.endswith(extension) and filename.startswith(season)]
    print filenames
    if (bool == 1):
        readSeasonForCharacters(filenames)

def readSeasonForCharacters(filenames):
    characters={}
    num=0
    #Episode analysis
    for filename in filenames:
        readEpisodeForCharacters(filename)

        #Season analysis:get line numbers
        tally=pd.read_csv('tally/'+filename, names=['Char','Line Tally'])
        num+=tally['Line Tally'].sum()
        print num
        #print tally.nlargest(3, 'Line Tally')

        #save character line numbers
        for index, row in tally.iterrows():
            #print(row['Char'], row['Line Tally'])
            if row['Char'] not in characters:
                add(characters, row['Char'], row['Line Tally'])
            else:
                characters[row['Char']]+=row['Line Tally']



    print characters

    #Season analysis: more? top 5? graph? save characters as a dataframe?


def main():
    print("PANDAS")
    episode = "s1e02.csv"
    season = 's2'


    readSeason(season, 1)
    #readEpisodeForCharacters(episode)


if __name__ == '__main__':
    main()


