# Flask
mkdir webenv
python3 -m venv webenv
source webenv/bin/activate
pip3 install Flask Flask-JWT

# mongodb
wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -
sudo apt-get install gnupg
echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list
sudo apt-get update
sudo apt-get install -y mongodb-org

# WSLでservice mongodを実行する為の処理
mkdir tmp
cd /tmp
wget https://raw.githubusercontent.com/mongodb/mongo/master/debian/init.d -O mongod
chmod +x ./mongod
sudo mv mongod /etc/init.d/
sudo service mongod start
cd ..
rm -r tmp

# mongodb　ユーザー作成
mongo
use admin
db.createUser(
    {
            user:yoraba,
            pwd:12345678,
            roles:[
                {
                    "role" : "root",
                    "db" : "admin"
                }
            ]
    }
)

# DB作成
use fx_rnn

# TALib
# Download ta-lib-0.4.0-src.tar.gz and:
# 
# $ untar and cd
# $ ./configure --prefix=/usr
# $ make
# $ sudo make install

sudo apt-get install build-essential python3-dev
pip3 install wheel
pip3 install TA-Lib

# pip
pip3 install pandas numpy matplotlib
pip3 install tensorflow keras
pip3 install mongoengine
