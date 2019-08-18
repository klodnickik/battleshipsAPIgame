import requests
import random
import time

#bs_server_url="https://bs.123craft.eu"
bs_server_url="http://127.0.0.1:5000"
game_id = "dmdhbvoe"
player_id = "p1"
player_key = "gdvhbpazva"

def shoot():

    ## randomly select shot location
    row = random.randint(0,9)
    col = random.randint(0,9)

    ## generate URL for API call
    shoot_url = bs_server_url + "/api/v0/shoot/"+game_id+"/"+player_key+"/"+player_id+"/"+str(col)+"/"+str(row)
    r = requests.get(shoot_url)
    print ("Shot: col: {}, row: {}".format(col,row))

    _status_code = r.status_code
    _response = r.text
    print ("Status code: {}, response : {}".format(_status_code, _response))

def main():
    print ("Start of simple bot")

    status_url = bs_server_url+"/api/v0/status/"+game_id+"/"+player_id

    _end_loop = False

    while _end_loop == False:
        # check status
        r = requests.get(status_url)

        _status_code = r.status_code
        _response = r.text

        print ("Status code: {}, response : {}".format(_status_code, _response))

        if _status_code == 200 and _response[0:4] == "[ok]": 
            print ("Ready for shot")
            shoot()

        if _status_code == 200 and _response[0:5] == "[end]": 
            print ("game over")
            _end_loop = True

        # error status code handling 
        if (_status_code == 404) or (_status_code == 403) :
            print ("Error, please check bot configuration")
            _end_loop = True

        # error status code handling 
        if (_status_code == 500) :
            print ("Server error")
            _end_loop = True

        # wait 5 secs
        time.sleep(1)

if __name__ == "__main__":
    main()