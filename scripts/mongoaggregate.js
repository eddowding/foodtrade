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


db.userprofile.find().forEach( function(myDoc) {
   if (myDoc['sign_up_as'] == 'unclaimed'){
       u_conn = db.tradeconnection.find({'b_userid':myDoc['useruid']});
       u_c_conn = db.tradeconnection.find({'c_userid':myDoc['useruid']});
       mem_
       if(u_conn.length()==0 && u_c_conn.length() ==0){
            db.userprofile.remove({'username':myDoc['username']});
       }}
    });