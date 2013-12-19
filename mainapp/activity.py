# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialToken, SocialAccount
from twython import Twython
import json
from classes.TweetFeed import TweetFeed
from classes.Search import Search
from search import search_general
from streaming import MyStreamer
from models import MaxTweetId


consumer_key = 'seqGJEiDVNPxde7jmrk6dQ'
consumer_secret = 'sI2BsZHPk86SYB7nRtKy0nQpZX3NP5j5dLfcNiP14'
access_token = ''
access_token_secret =''

admin_access_token = '2248425234-EgPSi3nDAZ1VXjzRpPGMChkQab5P0V4ZeG1d7KN'
admin_access_token_secret = 'ST8W9TWqqHpyskMADDSpZ5r9hl7ND6sEfaLvhcqNfk1v4'

from math import radians, cos, sin, asin, sqrt
def distance(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km


from django.template import RequestContext


from mainapp.classes.AjaxHandle import AjaxHandle


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def home(request):
    keyword = request.GET.get('q',"")
    my_lon = float(request.GET.get('lon',85.33333330000005))
    my_lat = float(request.GET.get('lat',27.7))
    location = request.GET.get('location',"")
    if my_lon == "" or my_lat=="":
        my_lon = 85.33333330000005
        my_lat = 27.7



    # tweet_doc = {
    #     'tweet_id':543654,
    #     'parent_tweet_id':0,
    #     'status':" Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur bibendum ornare dolor, quis ullamcorper ligula sodales.",    
    #     'location':{"type": "Point", "coordinates": [float(my_lon), float(my_lat)]},
    #     'user':{
    #     'username':"david",
    #     'name': "David Villa",
    #     'profile_img':"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
    #     'Description':"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod",
    #     'place':"78 Example Street, Test Town"
    #     }
    # }

    tweets_list = [
    {
      "status":"The word in the sense of an agricult",
      "tweet_id":598725,
      "user":{
         "username":"sujit",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sujit maharjan",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            81.10714880445049,
            4.275171682599845
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to f",
      "tweet_id":924951,
      "user":{
         "username":"sujit",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sujit maharjan",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -66.99422611484249,
            -69.68745636382164
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue source, whether taxes, customs, rent",
      "tweet_id":123100,
      "user":{
         "username":"roshan",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"roshan bhandari",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -43.81967166556324,
            -41.71057018336109
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue",
      "tweet_id":516604,
      "user":{
         "username":"roshan",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"roshan bhandari",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            25.80906578078619,
            78.91650887928645
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the v",
      "tweet_id":596039,
      "user":{
         "username":"sujit",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sujit maharjan",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -72.07900592326766,
            47.30230085428895
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives ",
      "tweet_id":401044,
      "user":{
         "username":"subit",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"subit raj",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -60.39120527800033,
            41.89293555867078
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue source, whether taxes,",
      "tweet_id":656966,
      "user":{
         "username":"sarvagya",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sarvagya pant",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -85.1570762974721,
            6.145832765605663
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from",
      "tweet_id":420365,
      "user":{
         "username":"santosh",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"santosh ghimire",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            27.07234373750024,
            -86.48202539262182
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue s",
      "tweet_id":139702,
      "user":{
         "username":"roshan",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"roshan bhandari",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -48.72392107362604,
            -0.4428872647164561
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue source, whether",
      "tweet_id":147423,
      "user":{
         "username":"subit",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"subit raj",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            64.16634900458388,
            -84.05963049820464
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue source, whether taxes",
      "tweet_id":558221,
      "user":{
         "username":"rasana",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"rasana manandhar",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -80.38239080285811,
            79.36214543470521
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue source, whethe",
      "tweet_id":895254,
      "user":{
         "username":"astha",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"astha pant",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            49.61568035989914,
            -24.63643433298804
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of a",
      "tweet_id":308071,
      "user":{
         "username":"subit",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"subit raj",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -3.9138288723927372,
            -57.591136664513435
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue source, whether taxes, customs, rents of",
      "tweet_id":38128,
      "user":{
         "username":"sujit",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sujit maharjan",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -33.20071409688176,
            -19.11923712638418
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a reven",
      "tweet_id":450004,
      "user":{
         "username":"sudip",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sudip kafle",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            40.23427340579957,
            -77.11400088065336
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue source, whether taxes, customs, ",
      "tweet_id":704184,
      "user":{
         "username":"sarvagya",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sarvagya pant",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -89.5823736607534,
            33.88826065085844
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultura",
      "tweet_id":503862,
      "user":{
         "username":"rasana",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"rasana manandhar",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -43.76806732422184,
            25.243770441946886
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue source, whether taxes, cus",
      "tweet_id":256503,
      "user":{
         "username":"rasana",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"rasana manandhar",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -5.898330555022524,
            -33.924246204590055
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The ",
      "tweet_id":362895,
      "user":{
         "username":"subit",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"subit raj",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            86.87591698611058,
            27.096558318329823
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultura",
      "tweet_id":58804,
      "user":{
         "username":"santosh",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"santosh ghimire",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -69.19749261771715,
            -86.0664325265599
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The ",
      "tweet_id":794441,
      "user":{
         "username":"rasana",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"rasana manandhar",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -53.9573933783709,
            49.868415781103124
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue so",
      "tweet_id":17830,
      "user":{
         "username":"sujit",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sujit maharjan",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -63.37917299611937,
            6.024116492530758
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue source",
      "tweet_id":708775,
      "user":{
         "username":"sijan",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sijan bhandari",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            25.71122609922937,
            -73.97807579141553
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives f",
      "tweet_id":705865,
      "user":{
         "username":"sudip",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sudip kafle",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -10.930899650870103,
            -14.852876710636885
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"Th",
      "tweet_id":655135,
      "user":{
         "username":"umanga",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"umanga bista",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            54.49666423554439,
            49.076341587696874
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The",
      "tweet_id":711857,
      "user":{
         "username":"astha",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"astha pant",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -1.6660318414207231,
            -14.034845295319673
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense",
      "tweet_id":717773,
      "user":{
         "username":"astha",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"astha pant",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -55.431867114270574,
            32.64327060458302
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural ",
      "tweet_id":80300,
      "user":{
         "username":"ange",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"ange acharya",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            38.03446440202035,
            22.8336772641082
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sen",
      "tweet_id":466390,
      "user":{
         "username":"sijan",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sijan bhandari",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            71.84765156696857,
            1.510268565797921
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue source, whether taxes, customs, rents ",
      "tweet_id":915753,
      "user":{
         "username":"ange",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"ange acharya",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            61.27215847642511,
            -34.36012850508869
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sen",
      "tweet_id":647750,
      "user":{
         "username":"umanga",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"umanga bista",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -27.84470814620463,
            -8.439841558651775
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in th",
      "tweet_id":536783,
      "user":{
         "username":"sijan",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sijan bhandari",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            8.968165535789094,
            -73.66353447902348
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue source, whether tax",
      "tweet_id":885482,
      "user":{
         "username":"sudip",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sudip kafle",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -35.28205433618864,
            8.407930272975552
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the ver",
      "tweet_id":315867,
      "user":{
         "username":"sudip",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sudip kafle",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            82.33759649449817,
            40.31932902216136
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue source, whether taxes, custom",
      "tweet_id":191614,
      "user":{
         "username":"sarvagya",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sarvagya pant",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            14.105383991783189,
            -82.53709369451694
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The w",
      "tweet_id":623377,
      "user":{
         "username":"umanga",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"umanga bista",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -35.69479329052188,
            24.080794621565527
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding deriv",
      "tweet_id":332537,
      "user":{
         "username":"sujit",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sujit maharjan",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            81.65269040626727,
            50.41751344793145
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue source, whe",
      "tweet_id":145703,
      "user":{
         "username":"roshan",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"roshan bhandari",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            26.03990603934627,
            73.178179671251
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives",
      "tweet_id":505206,
      "user":{
         "username":"subit",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"subit raj",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -12.782081752986725,
            -24.20653597165534
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to",
      "tweet_id":260408,
      "user":{
         "username":"umanga",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"umanga bista",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -32.436287109504775,
            12.906631259806584
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives f",
      "tweet_id":14979,
      "user":{
         "username":"roshan",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"roshan bhandari",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -11.88838033103399,
            -34.106418723874945
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue ",
      "tweet_id":242922,
      "user":{
         "username":"rasana",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"rasana manandhar",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -65.98676426851773,
            47.33026615372885
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue source, whether taxes, customs, rents of a g",
      "tweet_id":782463,
      "user":{
         "username":"roshan",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"roshan bhandari",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            31.69982429396312,
            20.45874140679389
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue source, whether taxes, cust",
      "tweet_id":30317,
      "user":{
         "username":"santosh",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"santosh ghimire",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            46.04467600986637,
            77.46805572377525
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding de",
      "tweet_id":992889,
      "user":{
         "username":"sudip",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sudip kafle",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -58.88729088760983,
            28.073984487780116
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricult",
      "tweet_id":763217,
      "user":{
         "username":"sudip",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sudip kafle",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -69.09510240842346,
            -48.767475866284755
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue",
      "tweet_id":670304,
      "user":{
         "username":"sarvagya",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sarvagya pant",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            14.135618127852618,
            -77.04808499586477
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricu",
      "tweet_id":971752,
      "user":{
         "username":"rasana",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"rasana manandhar",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            88.76506698304424,
            89.69694657497251
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue source, whether t",
      "tweet_id":220841,
      "user":{
         "username":"ange",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"ange acharya",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -83.84672948508499,
            -8.855476830896185
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue source, whether taxes, customs, re",
      "tweet_id":958703,
      "user":{
         "username":"sujit",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sujit maharjan",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -68.29885988074308,
            17.565398179416043
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue source, whether taxes, customs, rents of ",
      "tweet_id":223390,
      "user":{
         "username":"rasana",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"rasana manandhar",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -65.1579524323257,
            -21.797297646664685
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a reve",
      "tweet_id":304915,
      "user":{
         "username":"santosh",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"santosh ghimire",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -6.095535568104246,
            -9.568406702488598
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue sour",
      "tweet_id":999583,
      "user":{
         "username":"umanga",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"umanga bista",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -25.209073914719188,
            88.25091041330398
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue source, ",
      "tweet_id":703794,
      "user":{
         "username":"santosh",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"santosh ghimire",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            55.74785224715681,
            18.472305825096157
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense ",
      "tweet_id":993255,
      "user":{
         "username":"subit",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"subit raj",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -27.776944018944427,
            -35.49877299636244
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the ve",
      "tweet_id":747108,
      "user":{
         "username":"sijan",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sijan bhandari",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -70.49349389743503,
            30.731000246401965
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue sour",
      "tweet_id":444825,
      "user":{
         "username":"subit",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"subit raj",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            35.40691125995323,
            -7.764986402638474
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue source, whether taxes, customs, ",
      "tweet_id":719306,
      "user":{
         "username":"subit",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"subit raj",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            75.66048128736524,
            -12.89826947706099
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding ",
      "tweet_id":415974,
      "user":{
         "username":"sijan",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sijan bhandari",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -69.85209649781474,
            86.32822644764123
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense ",
      "tweet_id":968602,
      "user":{
         "username":"santosh",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"santosh ghimire",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            59.099927842331546,
            -2.8208042801232502
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural la",
      "tweet_id":861943,
      "user":{
         "username":"sarvagya",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sarvagya pant",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            12.9991723167463,
            88.98269117089178
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The wor",
      "tweet_id":664005,
      "user":{
         "username":"rasana",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"rasana manandhar",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            86.91090138718612,
            -62.4428338681375
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to f",
      "tweet_id":86414,
      "user":{
         "username":"subit",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"subit raj",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -77.43304863404519,
            -44.49956792029205
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue source, whether taxes, customs",
      "tweet_id":493298,
      "user":{
         "username":"subit",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"subit raj",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            43.55969870627391,
            -57.693532583170686
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue source, whether ",
      "tweet_id":31468,
      "user":{
         "username":"rasana",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"rasana manandhar",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            87.24942684030296,
            56.98204684313667
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb",
      "tweet_id":651802,
      "user":{
         "username":"sujit",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sujit maharjan",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            70.03367857149274,
            85.69349815141386
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"",
      "tweet_id":113761,
      "user":{
         "username":"ange",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"ange acharya",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -64.52018256650749,
            -79.851299655854
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agric",
      "tweet_id":148919,
      "user":{
         "username":"sarvagya",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sarvagya pant",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            7.7010878859402565,
            24.018524920119763
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue source, whether",
      "tweet_id":354667,
      "user":{
         "username":"umanga",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"umanga bista",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            73.04062072130468,
            13.993915951680126
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to",
      "tweet_id":183555,
      "user":{
         "username":"umanga",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"umanga bista",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            25.376120306932194,
            -25.25355066449569
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an ag",
      "tweet_id":803829,
      "user":{
         "username":"sarvagya",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sarvagya pant",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            72.55993741157621,
            -59.61030451156132
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of",
      "tweet_id":334081,
      "user":{
         "username":"ange",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"ange acharya",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -68.74869121462622,
            24.65500263968386
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the se",
      "tweet_id":658575,
      "user":{
         "username":"umanga",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"umanga bista",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            52.869146647686705,
            50.61402450971349
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"Th",
      "tweet_id":164863,
      "user":{
         "username":"roshan",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"roshan bhandari",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            75.97080757720897,
            36.3624018320435
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the ve",
      "tweet_id":416237,
      "user":{
         "username":"astha",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"astha pant",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            6.7186140823015155,
            -29.34928535399322
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agri",
      "tweet_id":207118,
      "user":{
         "username":"ange",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"ange acharya",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            29.73592877784273,
            -39.268407721276276
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"Th",
      "tweet_id":812867,
      "user":{
         "username":"roshan",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"roshan bhandari",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -20.211500364308538,
            -50.86088894687278
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricu",
      "tweet_id":401108,
      "user":{
         "username":"ange",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"ange acharya",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            46.20445725809462,
            51.9227649559583
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an a",
      "tweet_id":385277,
      "user":{
         "username":"umanga",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"umanga bista",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            4.21376822905801,
            45.3082266840599
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue source, whether taxes, customs, rents of a ",
      "tweet_id":412926,
      "user":{
         "username":"sujit",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sujit maharjan",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            88.30315620020956,
            61.488463692044746
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land",
      "tweet_id":25960,
      "user":{
         "username":"sudip",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sudip kafle",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -30.552733493470136,
            14.403942576175284
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land",
      "tweet_id":267572,
      "user":{
         "username":"sijan",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sijan bhandari",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -52.429033942995446,
            -13.082892175259282
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural lan",
      "tweet_id":164115,
      "user":{
         "username":"ange",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"ange acharya",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -47.614670100186615,
            -73.90794996750648
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm ",
      "tweet_id":272025,
      "user":{
         "username":"umanga",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"umanga bista",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            87.27407612125126,
            1.1881174128855432
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue source, whether ta",
      "tweet_id":724597,
      "user":{
         "username":"umanga",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"umanga bista",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            62.809214307504206,
            -23.908272515640764
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb t",
      "tweet_id":214838,
      "user":{
         "username":"sujit",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sujit maharjan",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -80.12574676105895,
            77.21620617485233
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue source, whether taxes, ",
      "tweet_id":146009,
      "user":{
         "username":"roshan",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"roshan bhandari",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            34.792826548490005,
            -54.53041853185048
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-",
      "tweet_id":198678,
      "user":{
         "username":"roshan",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"roshan bhandari",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -35.35233346853353,
            35.12071506341464
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue sour",
      "tweet_id":889284,
      "user":{
         "username":"subit",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"subit raj",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            15.850003826008589,
            73.4230120886691
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue source, whether ta",
      "tweet_id":46156,
      "user":{
         "username":"sarvagya",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sarvagya pant",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            49.70695727334149,
            -77.17823723767133
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an ag",
      "tweet_id":732553,
      "user":{
         "username":"astha",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"astha pant",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            38.20687790017795,
            68.22952730965604
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding d",
      "tweet_id":76849,
      "user":{
         "username":"rasana",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"rasana manandhar",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            3.8320738059917425,
            56.40886410708058
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue source, whether taxes, custom",
      "tweet_id":293720,
      "user":{
         "username":"umanga",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"umanga bista",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            41.25136636494516,
            -57.34765423866182
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue source, whether taxes, ",
      "tweet_id":335096,
      "user":{
         "username":"santosh",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"santosh ghimire",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -26.725772748869055,
            23.64921168791947
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in t",
      "tweet_id":437506,
      "user":{
         "username":"sarvagya",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sarvagya pant",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -6.876621620329733,
            28.116248563909256
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derive",
      "tweet_id":27503,
      "user":{
         "username":"sijan",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sijan bhandari",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            30.244233502641496,
            67.80683334126512
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a revenue source, whether taxes, ",
      "tweet_id":987450,
      "user":{
         "username":"sujit",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sujit maharjan",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            81.19523041447115,
            -5.757803789349865
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives fr",
      "tweet_id":677941,
      "user":{
         "username":"sujit",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sujit maharjan",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -3.7758830461616832,
            70.96402848198807
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derives from the verb to farm a r",
      "tweet_id":415038,
      "user":{
         "username":"sudip",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sudip kafle",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            -8.593437573436585,
            -10.264946008407186
         ]
      },
      "parent_tweet_id":0
   },
   {
      "status":"The word in the sense of an agricultural land-holding derive",
      "tweet_id":934761,
      "user":{
         "username":"sujit",
         "place":"78 Example Street, Test Town",
         "profile_img":"https://pbs.twimg.com/profile_images/378800000141996074/6a363e3c4f2a84a956c3cb27c50b2ca0_normal.png",
         "name":"sujit maharjan",
         "Description":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod"
      },
      "location":{
         "type":"Point",
         "coordinates":[
            73.79114836162385,
            -61.221514126025724
         ]
      },
      "parent_tweet_id":0
   }
]



    print len(tweets_list)
    # from pymongo import Connection
    # c = Connection()
    # c.drop_database('foodtrade')
    # tweet_handler = TweetFeed() 
    # for tweet_doc in tweets_list:
    #     tweet_handler.insert_tweet(tweet_doc)

    search_handle = Search(keyword, my_lon, my_lat, "nepal")
    results = search_handle.search()
    print results

    for i in range(len(results)):
        
        distance_text = ""
        # try:
        lonlat_distance = distance(my_lon, my_lat, results[i]['location']['coordinates'][0],results[i]['location']['coordinates'][1])
        if lonlat_distance>1:
            distance_text = str(lonlat_distance) +" Km"
        else:
            distance_text = str(lonlat_distance*1000) + " m"
        # except:
            pass

        results[i]['distance_text'] = distance_text


    parameters = {}
    parameters['results'] = results
    parameters['json_data'] = json.dumps(results)
    parameters['search'] = {'query':keyword, 'place':location, 'lon':my_lon, 'lat':my_lat}





    return render_to_response('activity.html',parameters ,context_instance=RequestContext(request))

