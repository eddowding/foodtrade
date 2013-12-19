import json
import random
import sys

status_text = "The word in the sense of an agricultural land-holding derives from the verb to farm a revenue source, whether taxes, customs, rents of a group of manors or simply to hold an individual manor by the feudal land tenure of fee farm. The word is from the medieval Latin noun firma, also the source of the French word ferme, meaning a fixed agreement, contract,[4] from the classical Latin adjective firmus meaning strong, stout, firm.[5][6] As in the medieval age virtually all manors were engaged in the business of agriculture, which was their principal revenue source, so to hold a manor by the tenure of fee farm became synonymous with the practice of agriculture itself."
name_text = ["roshan bhandari", "sujit maharjan", "sijan bhandari", "subit raj", "santosh ghimire", "sudip kafle", "umanga bista", "sarvagya pant", "astha pant", "rasana manandhar", "ange acharya"]


def loadsampledata():
    saved = sys.stdout
    f = file('initial.json', 'wb')
    sys.stdout = f
    mydict = []
    for i in range(0, 100):
        user_rand = random.randrange(0, 11)
        mydict.append({'tweet_id': random.randrange(10000, 1000000),
                       'parent_tweet_id': 0,
                       'status': status_text[0: random.randrange(0, 140)],
                       'location': {'type': "Point",
                                    'coordinates': [random.uniform(-1, 1) * 90, random.uniform(-1, 1) * 90]
                                    },
                       'user': {'username': name_text[user_rand].split(" ")[0],
                                'name': name_text[user_rand],
                                'profile_img': "https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
                                'Description': "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod",
                                'place': "78 Example Street, Test Town"
                                },
                       }
                      )
    print json.dumps(mydict)

    sys.stdout = saved
    f.close()

loadsampledata()
