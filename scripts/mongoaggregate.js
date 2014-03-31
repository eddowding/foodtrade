db.userprofile.aggregate([{ "$group": {"_id": "$useruid","count": { "$sum": 1 }}},{ "$match": {"count": { "$gt": 1 }}}])['result'].forEach(function(myDoc){
            id = myDoc._id;
            change_users = db.userprofile.find({'useruid':id});
            count = myDoc.count;
            for (var i=0; i<count; i++){
                    minid = db.userprofile.aggregate([ { '$group': { '_id':0, 'minId': { '$min': "$useruid"} } } ]);
                    doc = change_users[i];
                    new_id = minid['result'][0]['minId'] -1;
                    db.userprofile.update({'username':doc['username']}, {'$set':{'useruid':new_id}});
            }
})