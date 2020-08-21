import requests
import os
import json
import traceback

dir_path = os.path.join('up_100')


def get_http_session(pool_connections=2, pool_maxsize=10, max_retries=3):
    session = requests.session()
    adapter = requests.adapters.HTTPAdapter(
        pool_connections=pool_connections, pool_maxsize=pool_maxsize, max_retries=max_retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def save_file(filepath, content):
    with open(filepath, 'a') as f:
        f.write(content)


def make_dir(name):
    up_dir = os.path.join(dir_path, name)
    if not os.path.exists(up_dir):
        os.makedirs(up_dir)
    return up_dir


def log(content, level, filepath):
    print(content)
    if level == 'error':
        with open(filepath, 'a') as f:
            f.write(content)
    elif level == 'fail':
        with open(filepath, 'a') as f:
            f.write(content)


def read_json(filepath):
    with open(filepath, 'r') as f:
        res = f.read()
    return json.loads(res)


def get_up_base_info(name, uid):
    try:
        url = f'https://api.bilibili.com/x/space/arc/search?mid={uid}&pn=1&ps=25&order=click&jsonp=jsonp'

        r = get_http_session().get(url, timeout=100)
        if r.status_code == 200:
            up_dir = make_dir(name)
            filepath = os.path.join(up_dir, f'{uid}_base_info.json')
            content = json.dumps(r.json(), indent=4, ensure_ascii=False)
            save_file(filepath, content)
            print(f'{name} upOwner info saved success')
        else:
            fail_str = f'name: {name},uid: {uid}, url: {url}'
            log(fail_str, 'fail', 'base_info_error.log')
    except Exception as e:
        log(traceback.format_exc(), 'error', 'base_info_error.log')
        error_str = f'name: {name}, uid: {uid}'
        log(error_str, 'error', 'base_info_error.log')


def base_info_task(power_json):
    for d in power_json:
        uid = d['uid']
        name = d['name']
        get_up_base_info(name, uid)


def get_up_video_info(name, uid, filepath):
    res = read_json(filepath)
    vlist = res['data']['list']['vlist']
    for v in vlist:
        aid = v['aid']
        url = f'https://api.bilibili.com/x/player/pagelist?aid={aid}&jsonp=jsonp'
        player = get_http_session().get(url, timeout=10)
        player = player.json()
        data = player['data']
        if not data:
            return
        for d in data:
            try:
                cid = d['cid']
                barrage_url = f'https://api.bilibili.com/x/v1/dm/list.so?oid={cid}'
                r = get_http_session().get(barrage_url, timeout=10)
                uid_dir_path = os.path.join(dir_path, uid)
                if not os.path.exists(uid_dir_path):
                    os.makedirs(uid_dir_path)
                barrage_path = os.path.join(uid_dir_path, f'barrage_{aid}.xml')
                r.encoding = 'utf-8'
                content = r.text
                save_file(barrage_path, content)
                print(f'video id: {aid} barrage save success')
            except Exception as e:
                log(traceback.format_exc(), 'error', 'get_up_video_info.log')
                error_str = f'name: {name}, uid: {uid}'
                log(error_str, 'error', 'get_up_video_info.log')


def main():
    # power_up = read_json('power_up_100.json')
    # base_info_task(power_up)
    get_up_video_info('8366990','-欣小萌-','up_100/-欣小萌-/8366990_base_info.json')

if __name__ == '__main__':
    main()
