import requests
from base64 import b64encode
from random import choice
from flask import Flask, render_template, request, abort, jsonify

from database import Database
app = Flask(__name__)

db = Database()
db.create_database()
vk_token = "bd2ef70cf994d654dc85b37c8592c01b95ae49e68a7e3b992eee6d5d13e0c9e4a6b157692685ef2c0f84c"
with open("instagram_cookie.txt", "r", encoding="utf-8") as file:
    cookie = file.read()

@app.route('/vk', methods=["GET"])
def show_dialog():
    account_id = request.args.get('fid')
    url_id = request.args.get('url_id')
    dialog_variant = request.args.get('dn')
    owner_info = requests.get(f"https://api.vk.com/method/users.get?user_ids={account_id}&fields=photo_50&access_token={vk_token}&v=5.131").json()
    friend_info = requests.get(f"https://api.vk.com/method/friends.get?user_id={account_id}&count=50&fields=photo_50,sex&order=name&access_token={vk_token}&v=5.131").json()
    try:
        for friend_account in friend_info['response']['items']:
            if int(friend_account['sex']) == 2:
                companion_name = friend_account['first_name']
                ava_link_companion = friend_account['photo_50']
                break
    except KeyError:
        companion_name = "Петр"
        ava_link_companion = "https://sun1.beltelecom-by-minsk.userapi.com/s/v1/if1/grDxApKwEFVSNv2z-j3QbtGYu_BaeiVA4IRYLmj38ZVyP_8uAcqvEVrSAymbX-RHzFQ2ONoW.jpg?size=50x50&quality=96&crop=432,810,1099,1099&ava=1"
    if url_id is None:
        blur = True
    else:
        url_id_status = db.check_url_id(url_id)
        if url_id_status is not None:
            if url_id_status[0] == 0:
                db.use_link(url_id)
                blur = False
            else:
                return abort(500)
        else:
            return abort(500)
    return render_template(f'vk_dialog_variant_{dialog_variant}.html',
        owner_name=owner_info['response'][0]['first_name'],
        ava_link_owner=owner_info['response'][0]['photo_50'],
        companion_name=companion_name,
        ava_link_companion=ava_link_companion,
        blur=blur)  

@app.route('/instagram', methods=["GET"])
def show_dialog_inst():
    username = request.args.get('fid')
    url_id = request.args.get('url_id')
    dialog_variant = request.args.get('dn')
    headers = {
        'Host': 'www.instagram.com',
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0", 'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.instagram.com',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        "content-type": "application/json; charset=utf-8", }

    r = requests.get(f"https://www.instagram.com/{username}/?__a=1", headers=headers)
    if r.status_code == 200:
        try:
            data = r.json()
            ava_link_owner = data["graphql"]["user"]["profile_pic_url_hd"]
            print(ava_link_owner)
            r = requests.get(url=ava_link_owner)
            ava_link_owner = b64encode(r.content).decode("utf-8")
        except:
            ava_link_owner = "https://ih1.redbubble.net/image.1046392278.3346/mp,840x830,matte,f8f8f8,t-pad,1000x1000,f8f8f8.jpg"
    else:
        ava_link_owner = "https://ih1.redbubble.net/image.1046392278.3346/mp,840x830,matte,f8f8f8,t-pad,1000x1000,f8f8f8.jpg"
    ava_link_companion = "https://ih1.redbubble.net/image.1046392278.3346/mp,840x830,matte,f8f8f8,t-pad,1000x1000,f8f8f8.jpg"
    if url_id is None:
        blur = True
    else:
        url_id_status = db.check_url_id(url_id)
        if url_id_status is not None:
            if url_id_status[0] == 0:
                db.use_link(url_id)
                blur = False
            else:
                return abort(500)
        else:
            return abort(500)
    return render_template(f'inst_dialog_variant_{dialog_variant}.html',
        owner_name=username,
        ava_link_owner=ava_link_owner,
        companion_name="account deleted",
        ava_link_companion=ava_link_companion,
        blur=blur)


@app.route('/telegram', methods=["GET"])
def show_dialog_tg():
    phone = request.args.get('phone')
    url_id = request.args.get('url_id')
    dialog_variant = request.args.get('dn')
    if url_id is None:
        blur = True
    else:
        url_id_status = db.check_url_id(url_id)
        if url_id_status is not None:
            if url_id_status[0] == 0:
                db.use_link(url_id)
                blur = False
            else:
                return abort(500)
        else:
            return abort(500)
    random_name = ["Фатима Моисеева", "Дарья Никонова", "Александр Михайлов", "Руслан Пастухов", "Ева Черняева"]
    return render_template(f'tg_dialog_variant_{dialog_variant}.html',
        owner_name=f'+{phone.strip()}',
        ava_link_owner='data:image/jpeg;base64,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',
        companion_name=choice(random_name),
        ava_link_companion='data:image/jpeg;base64,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',
        blur=blur)

@app.route('/createUrlID', methods=["GET"])
def create_new_url_id():
    secret_key = request.args.get('key')
    api_secret_key = "Cqzsy9Bp3u3nifpjZ0Txoqt2aEi2E0RR"
    if secret_key == api_secret_key:
        urls_id = db.create_url()
        return jsonify(url_id=urls_id)

if __name__ == '__main__':
    app.run()
