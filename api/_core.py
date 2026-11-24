"""S26X LEVEL CHECKER — login & level core (minister.py থেকে নেওয়া, UI/CLI ছাড়া)."""
import base64
import json
import time

import httpx
from Crypto.Cipher import AES
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import json_format
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
from google.protobuf.message import Message


# ========================================
#  FreeFire protobuf descriptor
# ========================================
_sym_db = _symbol_database.Default()

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0e\x46reeFire.proto"c\n\x08LoginReq\x12\x0f\n\x07open_id\x18\x16 \x01(\t'
    b'\x12\x14\n\x0copen_id_type\x18\x17 \x01(\t\x12\x13\n\x0blogin_token\x18\x1d '
    b'\x01(\t\x12\x1b\n\x13orign_platform_type\x18\x63 \x01(\t"]\n\x10\x42lacklist'
    b'InfoRes\x12\x1e\n\nban_reason\x18\x01 \x01(\x0e\x32\n.BanReason\x12\x17\n'
    b'\x0f\x65xpire_duration\x18\x02 \x01(\r\x12\x10\n\x08\x62\x61n_time\x18\x03 '
    b'\x01(\r"f\n\x0eLoginQueueInfo\x12\r\n\x05\x61llow\x18\x01 \x01(\x08\x12'
    b'\x16\n\x0equeue_position\x18\x02 \x01(\r\x12\x16\n\x0eneed_wait_secs\x18'
    b'\x03 \x01(\r\x12\x15\n\rqueue_is_full\x18\x04 \x01(\x08"\xa0\x03\n\x08'#minister_69
    b'LoginRes\x12\x12\n\naccount_id\x18\x01 \x01(\x04\x12\x13\n\x0block_region'
    b'\x18\x02 \x01(\t\x12\x13\n\x0bnoti_region\x18\x03 \x01(\t\x12\x11\n\tip_'
    b'region\x18\x04 \x01(\t\x12\x19\n\x11\x61gora_environment\x18\x05 \x01(\t'
    b'\x12\x19\n\x11new_active_region\x18\x06 \x01(\t\x12\x19\n\x11recommend_'
    b'regions\x18\x07 \x03(\t\x12\r\n\x05token\x18\x08 \x01(\t\x12\x0b\n\x03ttl'
    b'\x18\t \x01(\r\x12\x12\n\nserver_url\x18\n \x01(\t\x12\x16\n\x0e\x65mul'
    b'ator_score\x18\x0b \x01(\r\x12$\n\tblacklist\x18\x0c \x01(\x0b\x32\x11.'
    b'BlacklistInfoRes\x12#\n\nqueue_info\x18\r \x01(\x0b\x32\x0f.LoginQueue'
    b'Info\x12\x0e\n\x06tp_url\x18\x0e \x01(\t\x12\x15\n\rapp_server_id\x18'
    b'\x0f \x01(\r\x12\x0f\n\x07\x61no_url\x18\x10 \x01(\t\x12\x0f\n\x07ip_city'
    b'\x18\x11 \x01(\t\x12\x16\n\x0eip_subdivision\x18\x12 \x01(\t*\xa8\x01\n'#minister_69
    b'\tBanReason\x12\x16\n\x12\x42\x41N_REASON_UNKNOWN\x10\x00\x12\x1b\n\x17'
    b'\x42\x41N_REASON_IN_GAME_AUTO\x10\x01\x12\x15\n\x11\x42\x41N_REASON_'
    b'REFUND\x10\x02\x12\x15\n\x11\x42\x41N_REASON_OTHERS\x10\x03\x12\x16\n'
    b'\x12\x42\x41N_REASON_SKINMOD\x10\x04\x12 \n\x1b\x42\x41N_REASON_IN_GAME'
    b'_AUTO_NEW\x10\xf6\x07\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)#minister_69
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "FreeFire_pb2", _globals)

LoginReq = _globals["LoginReq"]
LoginRes = _globals["LoginRes"]


# =========================================
#  Settings & Cryptography
# =========================================
MAIN_KEY = base64.b64decode("WWcmdGMlREV1aDYlWmNeOA==")
MAIN_IV  = base64.b64decode("Nm95WkRyMjJFM3ljaGpNJQ==")
RELEASEVERSION = "OB55"
USERAGENT = "UnityPlayer/2018.4.12f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)"
LOGIN_URL = "https://loginbp.ppmainecoonghj.com/"

REGIONAL_CLIENTS = {
    "BD": "https://clientbp.ppmainecoonghj.com",
    "IND": "https://clientbp.freefireind.in",
    "BR": "https://client.us.freefiremobile.com",
    "NA": "https://client.us.freefiremobile.com",
    "US": "https://client.us.freefiremobile.com",
    "SAC": "https://client.us.freefiremobile.com",
    "ME": "https://clientbp.ggblueshark.com",
    "VN": "https://client.vn.freefiremobile.com",
    "PK": "https://client.pk.freefiremobile.com",
    "SG": "https://client.sg.freefiremobile.com",
    "ID": "https://client.id.freefiremobile.com",
    "RU": "https://client.ru.freefiremobile.com",
    "TH": "https://client.th.freefiremobile.com",
    "TW": "https://client.tw.freefiremobile.com",
    "EU": "https://client.eu.freefiremobile.com",
    "default": "https://clientbp.ppmainecoonghj.com",
}

HTTP_LIMITS   = httpx.Limits(max_keepalive_connections=20, max_connections=50)
HTTP_TIMEOUT  = httpx.Timeout(15.0, connect=5.0)
_http_client  = httpx.Client(limits=HTTP_LIMITS, timeout=HTTP_TIMEOUT, verify=False)


def pad(text: bytes) -> bytes:
    p = AES.block_size - (len(text) % AES.block_size)
    return text + bytes([p] * p)


def aes_cbc_encrypt(key: bytes, iv: bytes, plaintext: bytes) -> bytes:
    return AES.new(key, AES.MODE_CBC, iv).encrypt(pad(plaintext))


def json_to_proto(json_data: str, proto_message: Message) -> bytes:
    json_format.ParseDict(json.loads(json_data), proto_message)#minister_69
    return proto_message.SerializeToString()


# ========================================
#  Response Parsers
# ========================================
def try_parse_login_res(data: bytes):
    try:
        msg = LoginRes()
        msg.ParseFromString(data)
        if msg.account_id and msg.account_id > 0:
            return json.loads(json_format.MessageToJson(msg))
    except Exception:
        pass
    return None


def extract_login_res(raw: bytes) -> dict:
    parsed = try_parse_login_res(raw)
    if parsed:
        return parsed
    idx = 0
    while True:
        idx = raw.find(b"\x08", idx)
        if idx == -1:#minister_69
            break
        parsed = try_parse_login_res(raw[idx:])
        if parsed:
            return parsed
        idx += 1
    marker = raw.find(b"eyJhbGciOiJIUzI1NiIs")
    if marker != -1:
        for i in range(marker - 1, max(marker - 300, -1), -1):
            if raw[i] == 0x42:
                parsed = try_parse_login_res(raw[i:])
                if parsed:
                    return parsed
                break
    raise Exception("Could not parse LoginRes from server response")


def decode_jwt_payload(jwt_token: str):
    try:
        parts = jwt_token.split(".")
        if len(parts) >= 2:
            p = parts[1] + "=" * (-len(parts[1]) % 4)
            return json.loads(base64.urlsafe_b64decode(p))
    except Exception:
        pass
    return {}


def encode_varint(n: int) -> bytes:
    r = []
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            r.append(b | 0x80)
        else:#minister_69
            r.append(b)
            break
    return bytes(r)


def parse_player_personal_show(data: bytes):
    i = 0
    basic = None
    while i < len(data):
        tag = data[i]; i += 1
        wire = tag & 0x07; fnum = tag >> 3
        if wire == 2:
            length = 0; shift = 0
            while True:
                b = data[i]; i += 1
                length |= (b & 0x7F) << shift; shift += 7
                if not (b & 0x80): break
            val = data[i:i + length]; i += length
            if fnum == 1:
                basic = val; break
        elif wire == 0:
            while data[i] & 0x80: i += 1
            i += 1
        else:
            break
    if not basic:
        return {}
    j = 0; res = {}
    while j < len(basic):
        tag = basic[j]; j += 1
        wire = tag & 0x07; fnum = tag >> 3
        if wire == 0:#minister_69
            v = 0; shift = 0
            while True:
                b = basic[j]; j += 1
                v |= (b & 0x7F) << shift; shift += 7
                if not (b & 0x80): break
            if fnum == 1: res["account_id"] = v
            elif fnum == 6: res["level"] = v
            elif fnum == 7: res["exp"] = v
        elif wire == 2:
            length = 0; shift = 0
            while True:
                b = basic[j]; j += 1
                length |= (b & 0x7F) << shift; shift += 7
                if not (b & 0x80): break
            s = basic[j:j + length]; j += length
            if fnum == 3: res["nickname"] = s.decode("utf-8", errors="ignore")
            elif fnum == 5: res["region"]   = s.decode("utf-8", errors="ignore")
        else:#minister_69
            break
    return res


# ========================================
#  Auth & Profile Pipeline
# ========================================
def get_access_token(uid: str, password: str):
    url = "https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant"
    payload = {
        "uid": str(uid), "password": str(password),
        "response_type": "token", "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067",
    }
    headers = {
        "User-Agent": USERAGENT,
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    resp = _http_client.post(url, data=payload, headers=headers)
    data = resp.json()
    return data.get("access_token"), data.get("open_id")


def fetch_player_profile(jwt_token, account_id, server_url=None, region="BD"):
    req = b"\x08" + encode_varint(account_id) + b"\x10\x07"#minister_69
    enc = aes_cbc_encrypt(MAIN_KEY, MAIN_IV, req)
    headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 14; CPH2095 Build/RKQ1.211119.001)",
        "Content-Type": "application/octet-stream",
        "Authorization": f"Bearer {jwt_token}",
        "X-Unity-Version": "2018.4.11f1",
        "X-GA": "v1 1",
        "ReleaseVersion": RELEASEVERSION,
    }
    urls = []
    if server_url:
        urls.append(server_url.rstrip("/") + "/GetPlayerPersonalShow")
    if region:
        k = str(region).upper()
        if k in REGIONAL_CLIENTS:
            urls.append(REGIONAL_CLIENTS[k] + "/GetPlayerPersonalShow")
        else:
            urls.append(f"https://client.{k.lower()}.freefiremobile.com/GetPlayerPersonalShow")
    urls.append(REGIONAL_CLIENTS["default"] + "/GetPlayerPersonalShow")
    for u in urls:#minister_69
        try:
            r = _http_client.post(u, data=enc, headers=headers, timeout=8.0)
            if r.status_code == 200 and len(r.content) > 30:
                p = parse_player_personal_show(r.content)
                if p:
                    return p
        except Exception:
            continue
    return {}


def generate_jwt_with_info(uid: str, password: str):
    start = time.time()
    tok, oid = get_access_token(uid, password)
    if not tok or not oid:
        raise Exception("Invalid UID or Password")
    body = json.dumps({
        "open_id": oid, "open_id_type": "4",
        "login_token": tok, "orign_platform_type": "4",
    })
    proto_bytes = json_to_proto(body, LoginReq())
    payload = aes_cbc_encrypt(MAIN_KEY, MAIN_IV, proto_bytes)

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "deflate, gzip",
        "Authorization": "Bearer",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "loginbp.ppmainecoonghj.com",
        "ReleaseVersion": RELEASEVERSION,
        "User-Agent": USERAGENT,
        "X-GA": "v1 1",
        "X-GA-SV": "1794159117",
        "X-Unity-Version": "2018.4.12f1",
    }

    resp = _http_client.post(f"{LOGIN_URL}MajorLogin", data=payload, headers=headers)
    msg = extract_login_res(resp.content)
    jwt_token = msg.get("token", "")
    real_uid = msg.get("accountId")
    server_url = msg.get("serverUrl", "")
    region = msg.get("lockRegion") or msg.get("notiRegion")#minister_69
    dec = decode_jwt_payload(jwt_token)
    if not real_uid and dec.get("account_id"):
        real_uid = dec["account_id"]
    if not region and dec.get("lock_region"):
        region = dec["lock_region"]
    profile = {}
    if jwt_token and real_uid:
        try:
            profile = fetch_player_profile(jwt_token, int(real_uid), server_url, region or "BD")
        except Exception:
            pass
    return {
        "account_id": str(real_uid) if real_uid else str(uid),
        "exp": profile.get("exp") if profile.get("exp") is not None else "N/A",
        "level": profile.get("level") if profile.get("level") is not None else "N/A",
        "nickname": profile.get("nickname") or "N/A",
        "region": profile.get("region") or region or "N/A",
        "status": "success",
        "time": f"{time.time() - start:.2f}s",
        "token": jwt_token,
    }


