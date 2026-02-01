db = db.getSiblingDB('admin');
db.auth(process.env.MONGO_INITDB_ROOT_USERNAME, process.env.MONGO_INITDB_ROOT_PASSWORD);

db = db.getSiblingDB('notifications_db');
db.createUser({
  user: 'notification_svc',
  pwd: process.env.NOTIF_MONGO_PASS || 'notif_pass',
  roles: [{ role: 'readWrite', db: 'notifications_db' }]
});

db = db.getSiblingDB('configs_db');
db.createUser({
  user: 'config_svc',
  pwd: process.env.CONFIG_MONGO_PASS || 'config_pass',
  roles: [{ role: 'readWrite', db: 'configs_db' }]
});

print('✅ MongoDB users and databases initialized');
