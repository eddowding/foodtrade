import mandrill 

md = mandrill.Mandrill('DS3yEW4HdOzqHGXOiXGPkg')
mes = mandrill.Messages(md)

message ={
	'to':[{'email':'brishi98@gmail.com', 'name':'Roshan Bhandari'}],
	'from_email':'no-reply@foodtrade.com', 
	'from_name':'FoodTrade', 
	'important':'true',
	'track_click':'true',
	'subject':'',
}
template_content = [{
      'name' : 'main',
      'content' : '''
      					<table>
	      					<tr>
      							<td>From</td><td>Activity</td><td>Action</td>
      						</tr>
      						<tr>
      							<td>@papworthfarms</td>
      							<td>@papworthfarms has accepted your invitation and joined FoodTrade</td>
      							<td><a href="http://foodtrade.com/inbox">[read] </a><a href="http://foodtrade.com/inbox"> [reply]</a></td>
      						</tr>
      						<tr>
      							<td>@papworthfarms</td>
      							<td>@papworthfarms joined FoodTrade</td>
      							<td><a href="http://foodtrade.com/inbox">[read] </a><a href="http://foodtrade.com/inbox"> [reply]</a></td>
      						</tr>
      					</table>
      				'''
   }, {'name':'inbox','content':'''<p>Please check your inbox for more details by clicking the following link</p><p><a href="http://foodtrade.com/inbox">My Foodtrade Inbox. </a></p>'''}]
mes.send_template('foodtrade-master', template_content, message)