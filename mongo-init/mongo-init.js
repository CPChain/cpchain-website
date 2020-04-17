
db.auth('admin', 'password')

db = db.getSiblingDB('cpchain')
db.createUser({user: 'uname', pwd: 'password', roles: [{role: "readWrite" , db:"cpchain"}]})

db = db.getSiblingDB('wallet')
db.createUser({user: 'wallet', pwd: 'password', roles: [{role: "readWrite" , db:"wallet"}]})
