"""@anson201"""

import requests, json, os, sys, time, re, threading, hashlib, uuid, base64

# colors
if os.name == "nt":
    import ctypes
    kernel = ctypes.windll.kernel32
    kernel.SetConsoleMode(kernel.GetStdHandle(-11), 7)

class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    GOLD    = "\033[38;5;220m"
    CYAN    = "\033[38;5;51m"
    GREEN   = "\033[38;5;82m"
    RED     = "\033[38;5;196m"
    ORANGE  = "\033[38;5;208m"
    PURPLE  = "\033[38;5;141m"
    GREY    = "\033[38;5;244m"
    WHITE   = "\033[38;5;255m"
    DKGREY  = "\033[38;5;238m"

def c(color, text):
    return f"{color}{text}{C.RESET}"

# apis and shit
GAME_ID = "259"
CATEGORY = "CustomItem"
DELIVERY_TIME = "Minute20"
ELDORADO_HOST = "https://www.eldorado.gg"
IMAGES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
TOKEN_FILE   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lung.txt")
XSRF_FILE    = os.path.join(os.path.dirname(os.path.abspath(__file__)), "heart.txt")
REFRESH_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "refresh.txt")

COGNITO_URL       = "https://cognito-idp.us-east-2.amazonaws.com/YOUR_COGNITO_POOL_ID"
COGNITO_CLIENT_ID = "YOUR_COGNITO_CLIENT_ID"


# ms ids
MS_OPTIONS = {
    "0":       "0",
    "0-24":    "0-24-ms",
    "25-49":   "25-49-ms",
    "50-99":   "50-99-ms",
    "100-249": "100-249-ms",
    "250-499": "250-499-ms",
    "500-749": "500-749-ms",
    "750-999": "750-999-ms",
    "1-4b":    "1-4-bs",
    "5-9b":    "5-9-bs",
    "10-19b":  "10-19-bs",
    "25-49b":  "25-49-bs",
    "20+b":    "20-plus-bs",
}
# old ms ids, map to new one
_MS_LEGACY_REMAP = {
    "1-plus-bs": "1-4-bs",
}
def _remap_ms(val):
    return _MS_LEGACY_REMAP.get(val, val)
# muts
MUTATION_OPTIONS = {
    "none":        "none",
    "gold":        "gold",
    "diamond":     "diamond",
    "rainbow":     "rainbow",
    "bloodrot":    "bloodrot",
    "candy":       "candy",
    "lava":        "lava",
    "galaxy":      "galaxy",
    "yinyang":     "yin-yang",
    "radioactive": "radioactive",
    "cursed":      "cursed",
    "divine":      "divine",
    "neon":        "neon",
    "cyber":       "cyber",
}

# item names
BRAINROT_TRADE_ENV = {
    "1x1x1x1": {"rarity": "Secret", "id": "0-6-62"},
    "25": {"rarity": "Secret", "id": "0-6-101"},
    "67": {"rarity": "Secret", "id": "0-6-40"},
    "Admin Lucky Block": {"rarity": "Admin", "id": "0-8-0"},
    "Bacuru and Egguru": {"rarity": "Secret", "id": "0-6-114"},
    "Bisonte Giuppitere": {"rarity": "Secret", "id": "0-6-1"},
    "Blackhole Goat": {"rarity": "Secret", "id": "0-6-28"},
    "Brunito Marsito": {"rarity": "Secret", "id": "0-6-111"},
    "Bunito Bunito Spinito": {"rarity": "Secret", "id": "0-6-106"},
    "Burguro and Fryuro": {"rarity": "Secret", "id": "0-6-61"},
    "Burrito Bandito": {"rarity": "Secret", "id": "0-6-59"},
    "Capitano Moby": {"rarity": "Secret", "id": "0-6-65"},
    "Celestial Pegasus": {"rarity": "Secret", "id": "0-6-142"},
    "Celularcini Viciosini": {"rarity": "Secret", "id": "0-6-123"},
    "Cerberus": {"rarity": "Secret", "id": "0-6-110"},
    "Chicleteira Bicicleteira": {"rarity": "Secret", "id": "0-6-12"},
    "Chicleteira Cupideira": {"rarity": "Secret", "id": "0-6-129"},
    "Chicleteira Noelteira": {"rarity": "Secret", "id": "0-6-80"},
    "Chill Puppy": {"rarity": "Secret", "id": "0-6-115"},
    "Chillin Chili": {"rarity": "Secret", "id": "0-6-55"},
    "Chimino": {"rarity": "Secret", "id": "0-6-90"},
    "Chipso and Queso": {"rarity": "Secret", "id": "0-6-60"},
    "Cigno Fulgoro": {"rarity": "Secret", "id": "0-6-145"},
    "Cooki and Milki": {"rarity": "Secret", "id": "0-6-77"},
    "Cuadramat and Pakrahmatmamat": {"rarity": "Secret", "id": "0-6-69"},
    "Cupid Hotspot": {"rarity": "Secret", "id": "0-6-127"},
    "DJ Panda": {"rarity": "Secret", "id": "0-6-139"},
    "Donkeyturbo Express": {"rarity": "Secret", "id": "0-6-98"},
    "Dragon Cannelloni": {"rarity": "Secret", "id": "0-6-26"},
    "Dul Dul Dul": {"rarity": "Secret", "id": "0-6-33"},
    "Esok Sekolah": {"rarity": "Secret", "id": "0-6-19"},
    "Eviledon": {"rarity": "Secret", "id": "0-6-52"},
    "Festive 67": {"rarity": "Secret", "id": "0-6-92"},
    "Fishboard": {"rarity": "Secret", "id": "0-6-141"},
    "Fishino Clownino": {"rarity": "Secret", "id": "0-6-68"},
    "Fortunu and Cashuru": {"rarity": "Secret", "id": "0-6-154"},
    "Foxini Lanternini": {"rarity": "Secret", "id": "0-6-157"},
    "Foxini Lantertini": {"rarity": "Secret", "id": "0-6-157"},
    "Fragrama and Chocrama": {"rarity": "Secret", "id": "0-6-76"},
    "Garama and Madundung": {"rarity": "Secret", "id": "0-6-24"},
    "GOAT": {"rarity": "Secret", "id": "0-6-112"},
    "Ginger Gerat": {"rarity": "Secret", "id": "0-6-104"},
    "Gobblino Uniciclino": {"rarity": "Secret", "id": "0-6-78"},
    "Gold Gold Gold": {"rarity": "Secret", "id": "0-6-153"},
    "Graipuss Medussi": {"rarity": "Secret", "id": "0-6-9"},
    "Granny": {"rarity": "Secret", "id": "0-6-155"},
    "Griffin": {"rarity": "Secret", "id": "0-6-147"},
    "Guerriro Digitale": {"rarity": "Secret", "id": "0-6-30"},
    "Guest 666": {"rarity": "Secret", "id": "0-6-63"},
    "Headless Horseman": {"rarity": "OG", "id": "0-7-4"},
    "Heart Lucky Block": {"rarity": "Valentines", "id": "0-11-0"},
    "Hydra Dragon Cannelloni": {"rarity": "Secret", "id": "0-6-118"},
    "Job Job Job Sahur": {"rarity": "Secret", "id": "0-6-7"},
    "Jolly Jolly Sahur": {"rarity": "Secret", "id": "0-6-103"},
    "Ketupat Bros": {"rarity": "Secret", "id": "0-6-117"},
    "Ketupat Kepat": {"rarity": "Secret", "id": "0-6-20"},
    "Ketchuru and Musturu": {"rarity": "Secret", "id": "0-6-23"},
    "La Casa Boo": {"rarity": "Secret", "id": "0-6-58"},
    "La Extinct Grande": {"rarity": "Secret", "id": "0-6-38"},
    "La Food Combinasion": {"rarity": "Secret", "id": "0-6-135"},
    "La Ginger Sekolah": {"rarity": "Secret", "id": "0-6-93"},
    "La Grande Combinasion": {"rarity": "Secret", "id": "0-6-13"},
    "La Jolly Grande": {"rarity": "Secret", "id": "0-6-79"},
    "La Romantic Grande": {"rarity": "Secret", "id": "0-6-132"},
    "La Secret Combinasion": {"rarity": "Secret", "id": "0-6-57"},
    "La Spooky Grande": {"rarity": "Secret", "id": "0-6-49"},
    "La Supreme Combinasion": {"rarity": "Secret", "id": "0-6-22"},
    "La Taco Combinasion": {"rarity": "Secret", "id": "0-6-96"},
    "La Vacca Lepre Lepreino": {"rarity": "Secret", "id": "0-6-149"},
    "La Vacca Saturno Saturnita": {"rarity": "Secret", "id": "0-6-2"},
    "Las Sis": {"rarity": "Secret", "id": "0-6-41"},
    "Lavadorito Spinito": {"rarity": "Secret", "id": "0-6-71"},
    "List List List Sahur": {"rarity": "Secret", "id": "0-6-84"},
    "Los 25": {"rarity": "Secret", "id": "0-6-89"},
    "Los 67": {"rarity": "Secret", "id": "0-6-51"},
    "Los Amigos": {"rarity": "Secret", "id": "0-6-136"},
    "Los Bombinitos": {"rarity": "Brainrot God", "id": "0-5-19"},
    "Los Bros": {"rarity": "Secret", "id": "0-6-21"},
    "Los Burritos": {"rarity": "Secret", "id": "0-6-134"},
    "Los Candies": {"rarity": "Secret", "id": "0-6-91"},
    "Los Chicleteiras": {"rarity": "Secret", "id": "0-6-39"},
    "Los Combinasionas": {"rarity": "Secret", "id": "0-6-14"},
    "Los Cupids": {"rarity": "Secret", "id": "0-6-146"},
    "Los Hotspotsitos": {"rarity": "Secret", "id": "0-6-17"},
    "Los Jolly Combinasionas": {"rarity": "Secret", "id": "0-6-102"},
    "Los Lucky Block": {"rarity": "Admin", "id": "0-8-2"},
    "Los Mi Gatitos": {"rarity": "Secret", "id": "0-6-121"},
    "Los Mobilis": {"rarity": "Secret", "id": "0-6-50"},
    "Los Nooo My Hotspotsitos": {"rarity": "Secret", "id": "0-6-124"},
    "Los Orcalitos": {"rarity": "Brainrot God", "id": "0-5-15"},
    "Los Planitos": {"rarity": "Secret", "id": "0-6-70"},
    "Los Primos": {"rarity": "Secret", "id": "0-6-47"},
    "Los Puggies": {"rarity": "Secret", "id": "0-6-74"},
    "Los Quesadillas": {"rarity": "Secret", "id": "0-6-148"},
    "Los Sekolahs": {"rarity": "Secret", "id": "0-6-138"},
    "Los Spaghettis": {"rarity": "Secret", "id": "0-6-75"},
    "Los Tacoritas": {"rarity": "Secret", "id": "0-6-48"},
    "Los Tralaleritos": {"rarity": "Secret", "id": "0-6-5"},
    "Los Trios": {"rarity": "Secret", "id": "0-6-113"},
    "Love Love Love Sahur": {"rarity": "Secret", "id": "0-6-126"},
    "Lovin Rose": {"rarity": "Secret", "id": "0-6-133"},
    "Luck Luck Luck Sahur": {"rarity": "Secret", "id": "0-6-150"},
    "Mariachi Corazoni": {"rarity": "Secret", "id": "0-6-46"},
    "Meowl": {"rarity": "OG", "id": "0-7-2"},
    "Mi Gatito": {"rarity": "Secret", "id": "0-6-120"},
    "Mieteteira Bicicleteira": {"rarity": "Secret", "id": "0-6-54"},
    "Money Money Puggy": {"rarity": "Secret", "id": "0-6-43"},
    "Money Money Reindeer": {"rarity": "Secret", "id": "0-6-99"},
    "Naughty Naughty": {"rarity": "Secret", "id": "0-6-87"},
    "Noo my Gold": {"rarity": "Secret", "id": "0-6-151"},
    "Noo my Heart": {"rarity": "Secret", "id": "0-6-128"},
    "Noo my Present": {"rarity": "Secret", "id": "0-6-105"},
    "Nooo My Hotspot": {"rarity": "Secret", "id": "0-6-35"},
    "Nuclearo Dinossauro": {"rarity": "Secret", "id": "0-6-15"},
    "Orcaledon": {"rarity": "Secret", "id": "0-6-66"},
    "Other": {"rarity": "Secret", "id": "0-6-36"},
    "Pakrahmatmamat": {"rarity": "Brainrot God", "id": "0-5-13"},
    "Pandanini Frostini": {"rarity": "Brainrot God", "id": "0-5-30"},
    "Paradiso Axolottino": {"rarity": "Secret", "id": "0-6-143"},
    "Patteo": {"rarity": "Brainrot God", "id": "0-5-38"},
    "Please my Present": {"rarity": "Secret", "id": "0-6-105"},
    "Popcuru and Fizzuru": {"rarity": "Secret", "id": "0-6-122"},
    "Pot Hotspot": {"rarity": "Secret", "id": "0-6-11"},
    "Reinito Sleighito": {"rarity": "Secret", "id": "0-6-94"},
    "Rocco Disco": {"rarity": "Secret", "id": "0-6-108"},
    "Rosetti Tualetti": {"rarity": "Secret", "id": "0-6-130"},
    "Rosey and Teddy": {"rarity": "Secret", "id": "0-6-131"},
    "Sammyni Fattini": {"rarity": "Secret", "id": "0-6-137"},
    "Sammyni Spyderini": {"rarity": "Secret", "id": "0-6-32"},
    "Santa Hotspot": {"rarity": "Secret", "id": "0-6-86"},
    "Secret Lucky Block": {"rarity": "Secret", "id": "0-6-27"},
    "Serafinna Medusella": {"rarity": "Secret", "id": "0-6-144"},
    "Skibidi Toilet": {"rarity": "OG", "id": "0-7-3"},
    "Snailo Clovero": {"rarity": "Secret", "id": "0-6-152"},
    "Spaghetti Tualetti": {"rarity": "Secret", "id": "0-6-25"},
    "Spinny Hammy": {"rarity": "Secret", "id": "0-6-116"},
    "Spooky and Pumpky": {"rarity": "Secret", "id": "0-6-53"},
    "Swag Soda": {"rarity": "Secret", "id": "0-6-64"},
    "Swaggy Bros": {"rarity": "Secret", "id": "0-6-95"},
    "Taco Lucky Block": {"rarity": "Taco", "id": "0-9-0"},
    "Tacorita Bicicleta": {"rarity": "Secret", "id": "0-6-45"},
    "Tang Tang Keletang": {"rarity": "Secret", "id": "0-6-56"},
    "Telemorte": {"rarity": "Secret", "id": "0-6-125"},
    "Tictac Sahur": {"rarity": "Secret", "id": "0-6-42"},
    "To to to Sahur": {"rarity": "Secret", "id": "0-6-44"},
    "Torrtuginni Dragonfrutini": {"rarity": "Secret", "id": "0-6-3"},
    "Tralaledon": {"rarity": "Secret", "id": "0-6-18"},
    "Tralalero Tralala": {"rarity": "Brainrot God", "id": "0-5-2"},
    "Tralalita Tralala": {"rarity": "Brainrot God", "id": "0-5-7"},
    "Trenostruzzo Turbo 3000": {"rarity": "Brainrot God", "id": "0-5-8"},
    "Triplito Tralaleritos": {"rarity": "Secret", "id": "0-6-85"},
    "Tuff Toucan": {"rarity": "Secret", "id": "0-6-107"},
    "Ventoliero Pavonero": {"rarity": "Secret", "id": "0-6-140"},
    "W or L": {"rarity": "Secret", "id": "0-6-67"},
    "Hydra Bunny": {"rarity": "Secret", "id": "0-6-171"},
    "Bunny and Eggy": {"rarity": "Secret", "id": "0-6-160"},
}

_BRAINROT_LOWER = {k.lower(): v for k, v in BRAINROT_TRADE_ENV.items() if v.get("id")}

def _similarity(a, b):
    if not a or not b:
        return 0
    matches = sum(ca == cb for ca, cb in zip(a, b))
    return matches / max(len(a), len(b))

def get_trade_env(item_name):
    key = item_name.lower().strip()
    if key in _BRAINROT_LOWER:
        entry = _BRAINROT_LOWER[key]
        return entry["id"], entry["rarity"]
    for k, v in _BRAINROT_LOWER.items():
        if key in k or k in key:
            return v["id"], v["rarity"]
    best_v, best_score = None, 0
    for k, v in _BRAINROT_LOWER.items():
        score = _similarity(key, k)
        if score > best_score:
            best_score, best_v = score, v
    if best_score >= 0.80:
        return best_v["id"], best_v["rarity"]
    return None, "Secret"

def get_canonical_name(item_name):
    key = item_name.lower().strip()
    for k in BRAINROT_TRADE_ENV:
        if k.lower() == key:
            return k
    for k in BRAINROT_TRADE_ENV:
        if key in k.lower() or k.lower() in key:
            return k
    best_k, best_score = None, 0
    for k in BRAINROT_TRADE_ENV:
        score = _similarity(key, k.lower())
        if score > best_score:
            best_score, best_k = score, k
    if best_score >= 0.80:
        return best_k
    return item_name


def load_config():
    cfg = {}
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            cfg = json.load(f)
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            token = f.read().strip()
            if token:
                cfg["token"] = token
    if os.path.exists(XSRF_FILE):
        with open(XSRF_FILE, "r") as f:
            xsrf = f.read().strip()
            if xsrf:
                cfg["xsrf"] = xsrf
    # refresh token, config first then refresh.txt
    if not cfg.get("refresh") and os.path.exists(REFRESH_FILE):
        with open(REFRESH_FILE, "r") as f:
            refresh = f.read().strip()
            if refresh:
                cfg["refresh"] = refresh
    return cfg


def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)
    if "token" in cfg:
        with open(TOKEN_FILE, "w") as f:
            f.write(cfg["token"])
    if "xsrf" in cfg:
        with open(XSRF_FILE, "w") as f:
            f.write(cfg["xsrf"])
    if cfg.get("refresh"):
        with open(REFRESH_FILE, "w") as f:
            f.write(cfg["refresh"])


def decode_user_id(token):
    try:
        payload = token.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        data = json.loads(base64.urlsafe_b64decode(payload))
        return data.get("userId") or data.get("sub")
    except Exception:
        return None


def decode_token_exp(token):
    try:
        payload = token.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        data = json.loads(base64.urlsafe_b64decode(payload))
        return int(data.get("exp") or 0)
    except Exception:
        return 0


def _try_browser_rescue(session):
    """get fresh tokens from logged in browser"""
    token, xsrf, refresh, _ = load_cookies_from_browser()
    if not token:
        return False

    try:
        with open(TOKEN_FILE, "w") as f:
            f.write(token)
    except Exception:
        pass
    if refresh:
        try:
            with open(REFRESH_FILE, "w") as f:
                f.write(refresh)
        except Exception:
            pass

    cookie = session.headers.get("Cookie", "")
    cookies = parse_cookie_string(cookie) if cookie else {}
    cookies["__Host-EldoradoIdToken"] = token
    if refresh:
        cookies["__Host-EldoradoRefreshToken"] = refresh
    if xsrf:
        cookies["__Host-XSRF-TOKEN"] = xsrf
        session.headers["X-XSRF-TOKEN"] = xsrf
        session.headers["X-XSRF-Token"] = xsrf
    session.headers["Cookie"] = "; ".join(f"{k}={v}" for k, v in cookies.items())
    session._my_user_id = decode_user_id(token)
    print(c(C.GREEN, "  [auth] rescued tokens from browser cookie store"), flush=True)
    return True


def _read_refresh_token():
    try:
        if os.path.exists(REFRESH_FILE):
            with open(REFRESH_FILE, "r") as f:
                v = f.read().strip()
                if v:
                    return v
    except Exception:
        pass
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                return (json.load(f) or {}).get("refresh") or ""
    except Exception:
        pass
    return ""


def do_token_refresh(session):
    """get new id token from cognito, works without the refresh cookie"""
    if not session:
        return False

    refresh_token = _read_refresh_token()
    if not refresh_token:
        print("  [auth] no refresh token available — trying browser rescue", flush=True)
        return _try_browser_rescue(session)

    try:
        r = requests.post(
            COGNITO_URL,
            headers={
                "Content-Type": "application/x-amz-json-1.1",
                "X-Amz-Target": "AWSCognitoIdentityProviderService.InitiateAuth",
                "Accept": "*/*",
                "Origin": ELDORADO_HOST,
                "Referer": f"{ELDORADO_HOST}/",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            },
            json={
                "AuthFlow": "REFRESH_TOKEN_AUTH",
                "ClientId": COGNITO_CLIENT_ID,
                "AuthParameters": {"REFRESH_TOKEN": refresh_token},
            },
            timeout=15,
        )
    except Exception as e:
        print(f"  [auth] cognito refresh exception: {e}", flush=True)
        return False

    if r.status_code != 200:
        # NotAuthorized = token dead, retry wont help. try browser
        try:
            err = r.json().get("__type", "")
        except Exception:
            err = ""
        print(f"  [auth] cognito refresh failed status={r.status_code} err={err}", flush=True)
        if "NotAuthorizedException" in err:
            if _try_browser_rescue(session):
                return True
        return False

    try:
        auth_result = r.json().get("AuthenticationResult") or {}
        new_token = auth_result.get("IdToken")
        new_refresh = auth_result.get("RefreshToken")
    except Exception:
        new_token = None
        new_refresh = None
    if not new_token:
        print("  [auth] cognito response missing IdToken", flush=True)
        return False

    # save it and fix live session, no restart needed
    try:
        with open(TOKEN_FILE, "w") as f:
            f.write(new_token)
    except Exception:
        pass

    # cognito rotates refresh token, save new one
    if new_refresh:
        try:
            with open(REFRESH_FILE, "w") as f:
                f.write(new_refresh)
        except Exception:
            pass
        refresh_token = new_refresh

    cookie = session.headers.get("Cookie", "")
    cookies = parse_cookie_string(cookie) if cookie else {}
    cookies["__Host-EldoradoIdToken"] = new_token
    cookies["__Host-EldoradoRefreshToken"] = refresh_token
    session.headers["Cookie"] = "; ".join(f"{k}={v}" for k, v in cookies.items())
    session._my_user_id = decode_user_id(new_token)
    return True


def start_token_refresh_thread(session):
    """keeps id token alive, backs off on fails, quits after 6"""
    MAX_CONSECUTIVE_FAILURES = 6  # about 3h then give up
    REFRESH_LEEWAY_SECONDS   = 5 * 60

    def loop():
        consecutive_failures = 0
        backoff = 60

        while True:
            time.sleep(backoff)

            # read from disk, can change outside this
            try:
                with open(TOKEN_FILE, "r") as f:
                    cur_token = f.read().strip()
            except Exception:
                cur_token = ""

            now = int(time.time())
            exp = decode_token_exp(cur_token)
            secs_left = exp - now if exp else 0

            # still good, skip
            if cur_token and secs_left > REFRESH_LEEWAY_SECONDS:
                backoff = 60
                continue

            if do_token_refresh(session):
                consecutive_failures = 0
                backoff = 60
                print(c(C.GREEN, f"  [auth] token refreshed (was {secs_left}s from expiry)"), flush=True)
                continue

            consecutive_failures += 1
            if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
                print(c(C.ORANGE,
                    f"  [auth] giving up auto-refresh after {consecutive_failures} failures.\n"
                    f"  [auth] paste a fresh refresh token into refresh.txt or use menu option 7."),
                    flush=True)
                return

            backoff = min(backoff * 2, 30 * 60)
            print(c(C.ORANGE,
                f"  [auth] refresh failed (#{consecutive_failures}) — retrying in {backoff//60}min"),
                flush=True)

    t = threading.Thread(target=loop, daemon=True)
    t.start()


def load_cookies_from_browser():
    """eldorado cookies from chrome/edge/firefox"""
    try:
        import browser_cookie3
    except ImportError:
        return None, None, None, None

    domain = "eldorado.gg"
    for loader in (browser_cookie3.chrome, browser_cookie3.edge, browser_cookie3.firefox):
        try:
            jar = loader(domain_name=domain)
            cookies = {ck.name: ck.value for ck in jar}
            token   = cookies.get("__Host-EldoradoIdToken", "")
            xsrf    = cookies.get("__Host-XSRF-TOKEN", "")
            refresh = cookies.get("__Host-EldoradoRefreshToken", "")
            if token and xsrf:
                return token, xsrf, refresh, None
        except Exception:
            continue
    return None, None, None, None


def parse_cookie_string(cookie_str):
    cookies = {}
    for part in cookie_str.split(";"):
        part = part.strip()
        if "=" in part:
            k, _, v = part.partition("=")
            cookies[k.strip()] = v.strip()
    return cookies

def apply_cookies(session, cookie_str):
    cookies = parse_cookie_string(cookie_str)
    token      = cookies.get("__Host-EldoradoIdToken", "")
    xsrf       = cookies.get("__Host-XSRF-TOKEN", "")
    session_id = cookies.get("x-session-id", "")
    device_id  = cookies.get("x-device-id", "")
    session.headers["Cookie"] = cookie_str
    session.headers["X-XSRF-TOKEN"] = xsrf
    if xsrf:
        session.headers["X-XSRF-Token"] = xsrf
    if session_id:
        session.headers["X-Session-Id"] = session_id
    if device_id:
        session.headers["X-Device-Id"] = device_id
    session._my_user_id = decode_user_id(token)
    return token, xsrf

def get_session(token, xsrf):
    s = requests.Session()
    s.headers.update({
        "swagger": "Swager request",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Origin": ELDORADO_HOST,
        "Referer": f"{ELDORADO_HOST}/sell",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "X-XSRF-TOKEN": xsrf,
    })
    s.headers["Cookie"] = f"__Host-EldoradoIdToken={token}; __Host-XSRF-TOKEN={xsrf}"
    s._my_user_id = decode_user_id(token)
    return s


# auto chat
TALKJS_APP_ID = "YOUR_TALKJS_APP_ID"
TALKJS_CLIENT_BUILD = "jssdk-release-ab61e52"
GREETING_MSG = "Hi! Thanks for your order, I'll deliver as soon as possible!"

_chat_talk_token = None
_chat_talk_token_exp = 0
_chat_lock = threading.Lock()


def _get_talk_token(session):
    global _chat_talk_token, _chat_talk_token_exp
    now = time.time()
    if _chat_talk_token and now < _chat_talk_token_exp - 60:
        return _chat_talk_token
    try:
        r = session.get(f"{ELDORADO_HOST}/api/conversations/me/authorize", timeout=10)
        if r.status_code != 200:
            return None
        token = r.json().get("token")
        if not token:
            return None
        payload = token.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        exp = json.loads(base64.urlsafe_b64decode(payload)).get("exp", now + 3600)
        _chat_talk_token = token
        _chat_talk_token_exp = exp
        return token
    except Exception as e:
        print(c(C.RED, f"  [chat] talk token error: {e}"), flush=True)
        return None


def _nymid_from_userid(user_id):
    return hashlib.sha1(str(user_id).encode()).hexdigest()[:20] + "_n"


def _get_pending_order_convs(session, talk_token, user_id):
    """new order chats not messaged yet"""
    # orders api first
    try:
        r = session.get(f"{ELDORADO_HOST}/api/orders/me", timeout=10)
        if r.status_code == 200:
            orders = r.json()
            if isinstance(orders, dict):
                orders = orders.get("data") or orders.get("items") or orders.get("orders") or []
            if isinstance(orders, list) and orders:
                conv_ids = []
                for order in orders:
                    conv_id = (order.get("conversationId") or order.get("talkJsConversationId")
                               or order.get("chatConversationId")
                               or (order.get("conversation") or {}).get("id"))
                    messaged = order.get("hasSellerMessaged") or order.get("sellerMessaged") or False
                    if conv_id and not messaged:
                        conv_ids.append(str(conv_id))
                return conv_ids
    except Exception as e:
        print(c(C.GREY, f"  [chat] orders API: {e}"), flush=True)

    # fallback talkjs ws
    return _ws_get_order_convs(talk_token, user_id)


def _ws_get_order_convs(talk_token, user_id):
    try:
        import websocket as _ws
        nym_id = _nymid_from_userid(user_id)
        results = []
        done = threading.Event()

        ref_n = [1]

        def _send(ws, topic, event, payload, join_ref=None):
            ref = str(ref_n[0]); ref_n[0] += 1
            ws.send(json.dumps([join_ref, ref, topic, event, payload]))
            return ref

        def on_open(ws):
            topic = f"seq/sides/{nym_id}:{TALKJS_APP_ID}"
            _send(ws, topic, "phx_join", {"origin": "JSSDK"}, join_ref="1")

        def on_message(ws, msg):
            try:
                frame = json.loads(msg)
                # frame = [join_ref, ref, topic, event, payload]
                if len(frame) < 5:
                    return
                event, payload = frame[3], frame[4]
                if event == "phx_reply" and isinstance(payload, dict) and payload.get("status") == "ok":
                    # joined, ask for get_all
                    topic = f"seq/sides/{nym_id}:{TALKJS_APP_ID}"
                    if payload.get("response", {}).get("backend_instance_id"):
                        _send(ws, topic, "get_all", {"limit": 50, "oldestRecordTs": 0}, join_ref="1")
                    elif isinstance(payload.get("response", {}).get("data"), list):
                        for side in payload["response"]["data"]:
                            custom = side.get("conversationCustom") or {}
                            if custom.get("category") == "Order" and custom.get("hasSellerMessaged") == "false":
                                results.append(side.get("id") or side.get("conversationId") or "")
                        done.set()
                        ws.close()
            except Exception:
                pass

        ws_url = (f"wss://app.talkjs.com/api/v0/{TALKJS_APP_ID}/socket/websocket"
                  f"?talkjs-client-build={TALKJS_CLIENT_BUILD}&appId={TALKJS_APP_ID}"
                  f"&authToken={talk_token}&vsn=2.0.0")
        app = _ws.WebSocketApp(ws_url,
            header={"Origin": "https://www.eldorado.gg"},
            on_open=on_open, on_message=on_message)
        threading.Thread(target=app.run_forever, daemon=True).start()
        done.wait(timeout=8)
        return [r for r in results if r]
    except Exception as e:
        print(c(C.GREY, f"  [chat] WS fallback: {e}"), flush=True)
        return []


def _send_greeting(talk_token, session_id, conv_id, user_id):
    nym_id = _nymid_from_userid(user_id)
    headers = {
        "Authorization": f"Bearer {talk_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Origin": "https://app.talkjs.com",
        "Referer": "https://app.talkjs.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "x-talkjs-client-build": TALKJS_CLIENT_BUILD,
        "x-talkjs-client-date": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime()),
    }
    payload = {
        "idempotencyKey": str(uuid.uuid4()),
        "text": GREETING_MSG,
        "custom": {},
        "nymId": nym_id,
    }
    try:
        r = requests.post(
            f"https://app.talkjs.com/api/v0/{TALKJS_APP_ID}/say/{conv_id}/?sessionId={session_id}",
            headers=headers, json=payload, timeout=10,
        )
        return r.status_code == 200
    except Exception as e:
        print(c(C.RED, f"  [chat] say error: {e}"), flush=True)
        return False


def auto_chat_mode(session):
    """greet new orders till enter is pressed"""
    user_id = getattr(session, "_my_user_id", None)
    if not user_id:
        print(c(C.RED, "  Could not determine user ID from token."))
        return

    print(c(C.CYAN, f"\n  Auto-chat started (user {user_id})"))
    print(c(C.GREY,  "  Polling every 60s — press Enter to stop\n"))

    stop_event = threading.Event()
    threading.Thread(target=lambda: (input(), stop_event.set()), daemon=True).start()

    messaged_convs = set()
    session_id = str(uuid.uuid4())

    while not stop_event.is_set():
        with _chat_lock:
            talk_token = _get_talk_token(session)
        if not talk_token:
            print(c(C.ORANGE, "  [chat] No talk token — skipping"), flush=True)
        else:
            conv_ids = _get_pending_order_convs(session, talk_token, user_id)
            new_ids = [cid for cid in conv_ids if cid not in messaged_convs]
            if new_ids:
                for cid in new_ids:
                    ok = _send_greeting(talk_token, session_id, cid, user_id)
                    status = c(C.GREEN, "sent") if ok else c(C.RED, "failed")
                    print(c(C.GREY, f"  [{time.strftime('%H:%M:%S')}] conv {cid[:16]}... {status}"), flush=True)
                    if ok:
                        messaged_convs.add(cid)
            else:
                print(c(C.GREY, f"  [{time.strftime('%H:%M:%S')}] no new orders"), flush=True)

        stop_event.wait(60)

    print(c(C.WHITE, "\n  Auto-chat stopped."))


def verify_token(session):
    print(c(C.GREY, "  Verifying auth..."), end=" ", flush=True)
    try:
        cookie = session.headers.get("Cookie", "")
        token = ""
        for part in cookie.split(";"):
            part = part.strip()
            if part.startswith("__Host-EldoradoIdToken="):
                token = part.split("=", 1)[1]
                break
        r = requests.get(
            f"{ELDORADO_HOST}/api/v1/item-management/offers",
            params={"gameId": GAME_ID, "pageSize": 1},
            headers={
                "Cookie": f"__Host-EldoradoIdToken={token}",
                "swagger": "Swager request",
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            },
            timeout=10,
        )
        if r.status_code == 200:
            print(c(C.GREEN, "✓"))
            return True
        print(c(C.RED, f"✗ ({r.status_code})"))
        return False
    except Exception as e:
        print(c(C.RED, f"✗ ({e})"))
        return False


def refresh_cookies(session, cfg):
    global _xsrf_prompted
    _xsrf_prompted = False
    while True:
        print(c(C.ORANGE, "\n  Paste __Host-EldoradoIdToken value:"))
        raw = input("  > ").strip()
        if not raw:
            print(c(C.RED, "  No input — skipping."))
            return False

        if "__Host-EldoradoIdToken" in raw:
            token, xsrf = apply_cookies(session, raw)
            cfg["cookie_string"] = raw
            cfg["token"] = token
            cfg["xsrf"]  = xsrf
            parsed = parse_cookie_string(raw)
            refresh = parsed.get("__Host-EldoradoRefreshToken", "")
            if refresh:
                with open(REFRESH_FILE, "w") as f:
                    f.write(refresh)
        else:
            token = raw
            xsrf  = cfg.get("xsrf", "")
            session.headers["Cookie"] = f"__Host-EldoradoIdToken={token}" + (f"; __Host-XSRF-TOKEN={xsrf}" if xsrf else "")
            session.headers["X-XSRF-TOKEN"] = xsrf
            session.headers["X-XSRF-Token"]  = xsrf
            session._my_user_id = decode_user_id(token)
            cfg["token"] = token
            cfg["cookie_string"] = ""

        if not cfg.get("xsrf"):
            print(c(C.GREY, "  Paste x-xsrf-token value:"))
            xsrf = input("  > ").strip()
            if xsrf:
                session.headers["X-XSRF-TOKEN"] = xsrf
                session.headers["X-XSRF-Token"]  = xsrf
                cookie = session.headers.get("Cookie", "")
                if "__Host-XSRF-TOKEN=" in cookie:
                    cookie = re.sub(r'__Host-XSRF-TOKEN=[^;]*', f"__Host-XSRF-TOKEN={xsrf}", cookie)
                else:
                    cookie += f"; __Host-XSRF-TOKEN={xsrf}"
                session.headers["Cookie"] = cookie
                cfg["xsrf"] = xsrf

        save_config(cfg)

        if verify_token(session):
            print(c(C.GREEN, "  Cookies updated successfully."))
            return True

        print(c(C.RED, "  Auth failed — token may be expired or invalid. Please try again."))


def get_lowest_price(session, item_name, mutation, ms_value, no_mutation_filter=False, no_sleep=False):
    raw_gen_value = ms_value if ms_value and ms_value not in MS_OPTIONS.values() else None
    if ms_value and ms_value in MS_OPTIONS.values():
        ms_attr = ms_value
    else:
        ms_attr = resolve_ms_attr(ms_value) if ms_value else None

    canonical_name = get_canonical_name(item_name)
    _, rarity_label = get_trade_env(canonical_name)

    params = {
        "gameId": GAME_ID,
        "category": CATEGORY,
        "pageSize": 50,
        "pageIndex": 1,
        "offerSortingCriterion": "Price",
        "isAscending": "true",
        "tradeEnvironmentValue1": rarity_label,
        "tradeEnvironmentValue2": canonical_name,
    }
    if not no_mutation_filter:
        mutation_lower = (mutation or "none").lower().replace(" ", "").replace("-", "")
        mutation_attr = MUTATION_OPTIONS.get(mutation_lower, MUTATION_OPTIONS["none"])
        params["steal-a-brainrot-mutations"] = mutation_attr
    if ms_attr:
        params["steal-a-brainrot-ms"] = ms_attr

    prices = []
    is_1b_plus = ms_attr in {MS_OPTIONS[k] for k in ("1-4b", "5-9b", "10-19b", "25-49b", "20+b")}
    my_gen_num = _parse_gen_to_num(raw_gen_value) if is_1b_plus and raw_gen_value else None
    max_pages = 3 if is_1b_plus else 1

    try:
        my_id = getattr(session, "_my_user_id", None)
        for page in range(1, max_pages + 1):
            params["pageIndex"] = page
            if not no_sleep:
                time.sleep(1.0)
            r = session.get(f"{ELDORADO_HOST}/api/v1/item-management/offers", params=params)
            if r.status_code == 429:
                time.sleep(3.0)
                r = session.get(f"{ELDORADO_HOST}/api/v1/item-management/offers", params=params)
            if r.status_code != 200:
                break
            results = r.json().get("results", [])
            if not results:
                break
            for result in results:
                offer = result.get("offer", result)
                if my_id and offer.get("userId") == my_id:
                    continue
                price_obj = offer.get("pricePerUnitInUSD") or offer.get("pricePerUnit")
                if not price_obj:
                    continue
                amt = price_obj.get("amount", 0)
                if amt <= 0:
                    continue
                if is_1b_plus and my_gen_num:
                    gen_str = _extract_gen_from_title((offer.get("offerTitle") or "").lower())
                    gen_num = _parse_gen_to_num(gen_str) if gen_str else 0
                    prices.append((amt, gen_num))
                else:
                    prices.append((amt, 0))
            if len(results) < 50:
                break
    except Exception:
        return None

    if not prices:
        return None

    if is_1b_plus and my_gen_num:
        # same gen = within 30% of mine
        within = sorted([amt for amt, gn in prices if gn > 0 and my_gen_num * 0.7 <= gn <= my_gen_num * 1.3])

        if within:
            prices = within[:10]
        else:
            # none close, use all
            prices = sorted([amt for amt, _ in prices])[:10]
            if not prices:
                return None
    else:
        prices = sorted([amt for amt, _ in prices])[:10]

    if len(prices) == 1:
        return prices[0]

    # drop scam prices, 50% under median
    rough_med = prices[len(prices) // 2]
    prices = [p for p in prices if p >= rough_med * 0.5]

    if not prices:
        return None

    return _pick_target_price(prices)


def _pick_target_price(prices):
    return round(prices[0], 2)


def _parse_gen_to_num(s):
    """1.7B -> 1700000000.0"""
    s = s.strip().upper().replace("/S", "").replace(",", "")
    mult = {'K': 1e3, 'M': 1e6, 'B': 1e9, 'G': 1e9}.get(s[-1], 1) if s else 1
    try:
        return float(s[:-1]) * mult if s[-1].isalpha() else float(s)
    except (ValueError, IndexError):
        return 0


def _extract_gen_from_title(title):
    """gen from title, range gives highest"""
    pattern = r'\b(\d+(?:\.\d+)?[KkMmBbGg])(?:/[Ss])?\b'
    matches = re.findall(pattern, title)
    if not matches:
        return None
    best_str, best_num = None, 0
    for m in matches:
        n = _parse_gen_to_num(m)
        if n > best_num:
            best_num, best_str = n, m
    return best_str


def get_lowest_price_by_title(session, search_text, ms_attr_id, my_gen_num=None):
    """search by title, for items not in trade env list"""
    params = {
        "gameId": GAME_ID,
        "category": CATEGORY,
        "pageSize": 50,
        "pageIndex": 1,
        "offerSortingCriterion": "Price",
        "isAscending": "true",
        "useMinPurchasePrice": "false",
        "searchQuery": search_text,
    }
    _BS_TIERS = {"1-4-bs", "5-9-bs", "10-19-bs", "25-49-bs", "20-plus-bs"}
    is_1b_plus = ms_attr_id in _BS_TIERS

    if ms_attr_id:
        params["steal-a-brainrot-ms"] = ms_attr_id

    search_words = [w.lower() for w in re.split(r'\W+', search_text) if len(w) > 2]

    MS_BUCKET_MAP = {
        "0":           (0,      0),
        "0-24-ms":     (0,      24e6),
        "25-49-ms":    (25e6,   49e6),
        "50-99-ms":    (50e6,   99e6),
        "100-249-ms":  (100e6,  249e6),
        "250-499-ms":  (250e6,  499e6),
        "500-749-ms":  (500e6,  749e6),
        "750-999-ms":  (750e6,  999e6),
        "1-4-bs":      (1e9,    4e9),
        "5-9-bs":      (5e9,    9e9),
        "10-19-bs":    (10e9,   19e9),
        "25-49-bs":    (25e9,   49e9),
        "20-plus-bs":  (20e9,   float("inf")),
    }
    ms_bucket = MS_BUCKET_MAP.get(ms_attr_id) if ms_attr_id else None

    prices = []
    try:
        max_pages = 3 if is_1b_plus else 1
        for page in range(1, max_pages + 1):
            params["pageIndex"] = page
            r = session.get(f"{ELDORADO_HOST}/api/v1/item-management/offers", params=params)
            if r.status_code != 200:
                break
            data = r.json()
            results = data.get("results", [])
            if not results:
                break
            my_id = getattr(session, "_my_user_id", None)
            for result in results:
                offer = result.get("offer", result)
                if my_id and offer.get("userId") == my_id:
                    continue
                offer_title = (offer.get("offerTitle") or "").lower()

                # title must have item name
                if search_words and not any(w in offer_title for w in search_words[:2]):
                    continue

                if ms_bucket:
                    gen_str = _extract_gen_from_title(offer_title)
                    gen_num = _parse_gen_to_num(gen_str) if gen_str else 0
                    lo, hi = ms_bucket
                    if is_1b_plus:
                        # 1b+ only keep within 30% of mine
                        if my_gen_num and gen_num > 0:
                            if not (my_gen_num * 0.7 <= gen_num <= my_gen_num * 1.3):
                                continue
                        elif gen_num == 0:
                            continue
                    else:
                        if not (lo <= gen_num <= hi * 1.01):
                            continue

                price_obj = offer.get("pricePerUnitInUSD") or offer.get("pricePerUnit")
                if price_obj:
                    amt = price_obj.get("amount", 0)
                    if amt > 0:
                        prices.append(amt)
            if len(results) < 50:
                break
    except Exception:
        return None

    if not prices:
        return None

    prices = sorted(prices)[:10]

    if len(prices) == 1:
        return prices[0]

    rough_med = prices[len(prices) // 2]
    prices = [p for p in prices if rough_med * 0.5 <= p <= rough_med * 2.0]
    if not prices:
        return None

    return _pick_target_price(prices)


def resolve_ms_attr(ms_value):
    ms_lower = re.sub(r'/s$', '', ms_value.lower().replace(" ", "").replace(",", ""))
    for key, val in MS_OPTIONS.items():
        if key.replace(" ", "") == ms_lower:
            return val
    try:
        m = re.match(r'^(\d+(?:\.\d+)?)([kmgb]?)(\+?)$', ms_lower)
        if not m:
            return None
        num_str, suffix, _ = m.groups()
        n = float(num_str)
        def _pick_bs_tier(b_val):
            if b_val < 5:    return MS_OPTIONS["1-4b"]
            if b_val < 10:   return MS_OPTIONS["5-9b"]
            if b_val < 20:   return MS_OPTIONS["10-19b"]
            if b_val < 50:   return MS_OPTIONS["25-49b"]
            return MS_OPTIONS["20+b"]
        if suffix == 'g':
            return _pick_bs_tier(n)
        if suffix == 'b':
            return _pick_bs_tier(n)
        if suffix == 'm' and n >= 1000:
            return _pick_bs_tier(n / 1000)
        if suffix == 'k':
            return MS_OPTIONS["0"]
        n = int(n)
        if n == 0:    return MS_OPTIONS["0"]
        if n <= 24:   return MS_OPTIONS["0-24"]
        if n <= 49:   return MS_OPTIONS["25-49"]
        if n <= 99:   return MS_OPTIONS["50-99"]
        if n <= 249:  return MS_OPTIONS["100-249"]
        if n <= 499:  return MS_OPTIONS["250-499"]
        if n <= 749:  return MS_OPTIONS["500-749"]
        if n <= 999:  return MS_OPTIONS["750-999"]
        return MS_OPTIONS["1-4b"]
    except (ValueError, AttributeError):
        return None


def _ms_title_to_numeric(title):
    """375M/s -> 375.0, in M/s"""
    title = title or ""
    m = re.search(r'(\d+(?:\.\d+)?)\s*([KkMmBbGg])\s*/?\s*[Ss]', title)
    if not m:
        m = re.search(r'(\d+(?:\.\d+)?)\s*M/s', title, re.IGNORECASE)
        if m:
            return float(m.group(1))
        return None
    val = float(m.group(1))
    suffix = m.group(2).upper()
    if suffix == 'K':
        return val * 0.001
    if suffix == 'M':
        return val
    if suffix in ('B', 'G'):
        return val * 1000
    return val


def _ms_attr_to_numeric(ms_attr_id):
    """tier id -> midpoint in M/s"""
    _TIER_TO_MS = {
        "0":          0.0,
        "0-24-ms":    12.0,
        "25-49-ms":   37.0,
        "50-99-ms":   75.0,
        "100-249-ms": 175.0,
        "250-499-ms": 375.0,
        "500-749-ms": 625.0,
        "750-999-ms": 875.0,
        "1-4-bs":    2000.0,
        "5-9-bs":    7000.0,
        "10-19-bs":  15000.0,
        "25-49-bs":  37000.0,
        "20-plus-bs": 20000.0,
    }
    return _TIER_TO_MS.get(ms_attr_id, 0.0)


def _build_offer_attributes(existing_attrs, ms_attr_id, mutation_attr_id, title=""):
    """site wants list of {id, type, value}, not a dict"""
    ms_numeric = _ms_title_to_numeric(title)
    if ms_numeric is None:
        ms_numeric = _ms_attr_to_numeric(ms_attr_id)

    result = [
        {"id": "steal-a-brainrot-ms",         "type": "Select",  "value": ms_attr_id},
        {"id": "steal-a-brainrot-ms-numeric",  "type": "Numeric", "value": float(ms_numeric)},
        {"id": "steal-a-brainrot-mutations",   "type": "Select",  "value": mutation_attr_id},
    ]
    # keep other attrs from old offer
    known_ids = {"steal-a-brainrot-ms", "steal-a-brainrot-ms-numeric", "steal-a-brainrot-mutations"}
    for a in (existing_attrs or []):
        if isinstance(a, dict) and a.get("id") not in known_ids:
            result.append(a)
    return result


def parse_filename(filename):
    stem = os.path.splitext(filename)[0]
    mutation = None
    traits = None
    generation = None
    remaining = stem

    for mut in sorted(MUTATION_OPTIONS.keys(), key=len, reverse=True):
        if mut == "none":
            continue
        if remaining.lower().startswith(mut.lower()):
            mutation = mut.capitalize()
            remaining = remaining[len(mut):]
            break

    # range like 480M-800M, use higher one
    gen_range_str = None
    gen_range_match = re.search(r'(\d+(?:\.\d+)?[KkMmBbGg])-(\d+(?:\.\d+)?[KkMmBbGg])$', remaining)
    if gen_range_match:
        def _ms_to_num(s):
            s = s.upper()
            mult = {'K': 1e3, 'M': 1e6, 'B': 1e9, 'G': 1e9}.get(s[-1], 1)
            return float(s[:-1]) * mult
        v1, v2 = gen_range_match.group(1), gen_range_match.group(2)
        generation = v2 if _ms_to_num(v2) >= _ms_to_num(v1) else v1
        gen_range_str = f"{v1}-{v2}"
        remaining = remaining[:gen_range_match.start()]
    else:
        gen_match = re.search(r'(\d+(?:\.\d+)?[KkMmBbGg][\+]?)$', remaining)
        if gen_match:
            generation = gen_match.group(1)
            remaining = remaining[:gen_match.start()]

    traits_range_str = None
    traits_range_match = re.search(r'(\d+)-(\d+)[Tt]raits?$', remaining)
    if traits_range_match:
        t1, t2 = int(traits_range_match.group(1)), int(traits_range_match.group(2))
        traits = max(t1, t2)
        traits_range_str = f"{t1}-{t2}"
        remaining = remaining[:traits_range_match.start()]
    else:
        traits_match = re.search(r'(\d+)[Tt]raits?$', remaining)
        if traits_match:
            traits = int(traits_match.group(1))
            remaining = remaining[:traits_match.start()]

    item_name = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', remaining).strip()
    item_name = re.sub(r'(?<=[A-Z])(?=[A-Z][a-z])', ' ', item_name).strip()
    # BurguroAndFryuro -> Burguro and Fryuro
    for word in ("and", "or", "the", "of", "de", "van"):
        item_name = re.sub(rf'\b{word}\b', word.lower(), item_name, flags=re.IGNORECASE)
    item_name = re.sub(r' +', ' ', item_name).strip()

    if not item_name:
        return None

    return {"mutation": mutation or None, "item_name": item_name, "traits": traits, "traits_range": traits_range_str, "generation": generation or None, "gen_range": gen_range_str}


def upload_image(session, image_path):
    if not image_path or not os.path.exists(image_path):
        return None
    ext = os.path.splitext(image_path)[1].lower()
    mime = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".heic": "image/heic"}.get(ext, "image/png")
    with open(image_path, "rb") as f:
        img_data = f.read()
    headers = {k: v for k, v in session.headers.items() if k.lower() != "content-type"}
    r = requests.post(f"{ELDORADO_HOST}/api/files/me/Offer",
                      files={"image": (os.path.basename(image_path), img_data, mime)},
                      headers=headers)
    if r.status_code in (200, 201):
        resp = r.json()
        if isinstance(resp, dict) and "localPaths" in resp:
            paths = resp["localPaths"]
            s = lambda p: p.split("/")[-1] if p else ""
            small = s(paths[0]) if paths else ""
            large = s(paths[1]) if len(paths) > 1 else small
            orig  = s(paths[2]) if len(paths) > 2 else large
            return {"smallImage": small, "largeImage": large, "originalSizeImage": orig}
        if isinstance(resp, dict) and "originalSizeImage" in resp:
            return resp
        if isinstance(resp, dict) and "fileName" in resp:
            fn = resp["fileName"]
            return {"smallImage": fn, "largeImage": fn, "originalSizeImage": fn}
        if isinstance(resp, str):
            return {"smallImage": resp, "largeImage": resp, "originalSizeImage": resp}
        return resp
    print(f"  [IMG] upload failed {r.status_code}: {r.text[:200]}")
    return None


def upload_image_and_create_offer(session, listing):
    mutation   = listing["mutation"]
    item_name  = listing["item_name"]
    generation = listing["generation"]
    ms_value   = listing["ms"]
    quantity   = listing["quantity"]
    price_usd  = listing["price_usd"]
    image_path = listing.get("image_path")
    traits     = listing.get("traits", None)

    trade_env_id, rarity_label = get_trade_env(item_name)
    if not trade_env_id:
        # check own listings first
        r_search = session.get(f"{ELDORADO_HOST}/api/flexibleOffers/me/search",
                               params={"gameId": GAME_ID, "pageSize": 50, "pageIndex": 1})
        if r_search.status_code == 200:
            for res in r_search.json().get("results", []):
                o = res.get("offer", res)
                t = (o.get("offerTitle") or "").lower()
                if item_name.lower() in t:
                    tev = o.get("tradeEnvironmentValues") or []
                    if tev:
                        trade_env_id = tev[-1]["id"]
                        rarity_label = tev[-1].get("value", "Secret")
                        break
    if not trade_env_id:
        # not there, scan public listings
        print(f"  [INFO] '{item_name}' not in dict — scanning public listings...")
        for _page in range(1, 20):
            r_pub = session.get(f"{ELDORADO_HOST}/api/v1/item-management/offers",
                                params={"gameId": GAME_ID, "category": CATEGORY,
                                        "pageSize": 50, "pageIndex": _page})
            if r_pub.status_code != 200:
                break
            _results = r_pub.json().get("results", [])
            if not _results:
                break
            for res in _results:
                o = res.get("offer", res)
                tev = o.get("tradeEnvironmentValues") or []
                item_val = tev[-1].get("value", "") if tev else ""
                if item_name.lower() in item_val.lower() or item_val.lower() in item_name.lower():
                    trade_env_id = tev[-1]["id"]
                    rarity_label = tev[-2].get("value", "Secret") if len(tev) >= 2 else "Secret"
                    print(f"  [INFO] Found trade env from public listing: {trade_env_id}")
                    break
            if trade_env_id:
                break
    if not trade_env_id:
        print(f"[FAIL] '{item_name}' — could not find trade env id (no listings found anywhere)")
        return False

    mut_prefix  = f"{mutation} " if mutation and mutation.lower() != "none" else ""
    traits_range = listing.get("traits_range")
    traits_part = f" | {traits_range} Traits" if traits_range else (f" | {traits} Traits" if traits else "")
    gen_range   = listing.get("gen_range")
    if gen_range:
        gen_display = f" | {gen_range}/s"
    elif generation and str(generation) != "0":
        gen_display = f" | {generation}/s"
    else:
        gen_display = ""
    if "lucky block" in item_name.lower():
        mut_part = f"{mutation} " if mutation and mutation.lower() != "none" else ""
        title = f"❓{mut_part}Secret Lucky Block❓| 0-2 Random Trait | 5 POSSIBLE SECRETS | FASTEST DELIVERY | Steal A Brainrot"
    else:
        title = f"{mut_prefix}{item_name}{traits_part}{gen_display} | {rarity_label} | FAST | Steal a Brainrot"
    if len(title) > 160:
        title = title[:157] + "..."

    ms_attr_id = resolve_ms_attr(ms_value)
    if not ms_attr_id:
        print(f"[FAIL] Unknown M/s value: {ms_value}")
        return False

    mutation_attr_id = MUTATION_OPTIONS.get((mutation or "none").lower().replace(" ", "").replace("-", ""), MUTATION_OPTIONS["none"])

    image_obj = None
    if image_path:
        image_obj = upload_image(session, image_path)
        if not image_obj:
            return False

    offer_data = {
        "details": {
            "offerTitle": title,
            "description": """You will recieve your secrets via vip server link, if you cannot join I will add you
Message for more screenshots
Message for anything regarding the items
Also have way more secrets message me if you would like me to list them

instant delivery from 12 pm - 3 am EST

if you order at a time not during these hours and i am late, i will add extra on my behalf for being late to deliver your brainrots""",
            "guaranteedDeliveryTime": DELIVERY_TIME,
            "pricing": {
                "quantity": quantity,
                "minQuantity": 1,
                "pricePerUnit": {
                    "amount": round(price_usd, 2),
                    "currency": "USD"
                }
            },
            "mainOfferImage": image_obj,
            "offerImages": []
        },
        "augmentedGame": {
            "gameId": GAME_ID,
            "category": CATEGORY,
            "tradeEnvironmentId": trade_env_id,
            "attributeIdsCsv": None,
            "offerAttributes": _build_offer_attributes(None, ms_attr_id, mutation_attr_id, title)
        }
    }

    r = session.post(f"{ELDORADO_HOST}/api/v1/item-management/me/offers/item", json=offer_data)
    if r.status_code in (200, 201):
        return True
    if r.status_code == 401:
        print(c(C.GREY, "  [auth] 401 on create offer — attempting silent refresh..."), flush=True)
        if do_token_refresh(session):
            r = session.post(f"{ELDORADO_HOST}/api/v1/item-management/me/offers/item", json=offer_data)
            if r.status_code in (200, 201):
                return True
        print(c(C.RED, "  [401] Token expired — refresh cookies (option 7)"))
        return False
    try:
        err_text = " ".join(str(m) for m in (r.json().get("messages") or [])) or r.text[:300]
    except Exception:
        err_text = r.text[:300]
    print(f"  [FAIL] {err_text}")
    return False


def create_listing_from_parsed(session, parsed, image_path, quantity=1):
    mutation   = parsed.get("mutation")
    item_name  = parsed["item_name"]
    traits     = parsed.get("traits")
    generation = parsed.get("generation")
    gen_range  = parsed.get("gen_range")

    item_name = get_canonical_name(item_name)

    if not generation:
        generation = "0"

    mut_display = mutation.capitalize() if mutation and mutation.lower() != "none" else ""
    in_brainrot = get_canonical_name(item_name) != item_name or item_name.lower() in _BRAINROT_LOWER
    lowest = get_lowest_price(session, item_name, mutation or "none", generation) if in_brainrot else None
    if not lowest and in_brainrot and mutation and mutation.lower() != "none":
        lowest = get_lowest_price(session, item_name, mutation, generation, no_mutation_filter=True)
    if not lowest:
        ms_attr_id = resolve_ms_attr(generation) if generation else None
        gen_num = _parse_gen_to_num(_extract_gen_from_title(generation.lower())) if generation else None
        lowest = get_lowest_price_by_title(session, item_name, ms_attr_id, my_gen_num=gen_num)

    if lowest:
        price_usd = lowest
        confirm = input(f"  {mut_display} {item_name}: ${price_usd:.2f} — if not then item will be listed at your price:  ").strip()
        if confirm:
            try:
                price_usd = float(confirm)
            except ValueError:
                return False
    else:
        price_input = input(f"  No listings found for {mut_display} {item_name}. Price USD (blank to skip): ").strip()
        if not price_input:
            return False
        price_usd = float(price_input)

    return upload_image_and_create_offer(session, {
        "item_name": item_name, "mutation": mut_display, "ms": generation,
        "generation": generation, "gen_range": gen_range,
        "quantity": quantity, "price_usd": price_usd,
        "image_path": image_path, "traits": traits, "traits_range": parsed.get("traits_range"),
    })


def scan_images_mode(session):
    if not os.path.exists(IMAGES_DIR):
        print("images/ folder not found")
        return

    images = [f for f in os.listdir(IMAGES_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.heic'))]
    if not images:
        print("No images found in images/")
        return

    parsed_list = []
    for img in images:
        p = parse_filename(img)
        if p and p["item_name"]:
            parsed_list.append((img, p))
            mut = p['mutation'] or 'none'
            gen = p['gen_range'] or p['generation'] or '0'
            print(f"  {p['item_name']} | {mut} | traits={p['traits'] or 'none'} | {gen}")

    if not parsed_list:
        print("No valid images to list.")
        return

    print()
    ok = fail = 0
    for img, parsed in parsed_list:
        src = os.path.join(IMAGES_DIR, img)
        mut = parsed['mutation'] or 'none'
        qty_input = input(f"  Qty for {parsed['item_name']} ({mut}) {parsed['generation']} (default 1): ").strip()
        quantity = int(qty_input) if qty_input else 1
        success = create_listing_from_parsed(session, parsed, src, quantity)
        if success:
            ok += 1
            try:
                os.remove(src)
            except Exception as e:
                print(f"  [WARN] Could not delete {img}: {e}")
        else:
            fail += 1
        time.sleep(0.5)

    print(f"\n{ok} created, {fail} failed")


def get_my_active_offers(session):
    offers = []
    # (connect, read), no timeout = hangs forever
    _T = (10, 30)
    try:
        page = 1
        while True:
            print(f"\r  Fetching listings... page {page}", end="", flush=True)
            r = session.get(f"{ELDORADO_HOST}/api/flexibleOffers/me/search",
                            params={"gameId": GAME_ID, "offerState": "Active", "pageSize": 50, "pageIndex": page},
                            timeout=_T)
            if r.status_code == 429:
                time.sleep(5.0)
                r = session.get(f"{ELDORADO_HOST}/api/flexibleOffers/me/search",
                                params={"gameId": GAME_ID, "offerState": "Active", "pageSize": 50, "pageIndex": page},
                                timeout=_T)
            if r.status_code == 403:
                _prompt_xsrf(session)
                r = session.get(f"{ELDORADO_HOST}/api/flexibleOffers/me/search",
                                params={"gameId": GAME_ID, "offerState": "Active", "pageSize": 50, "pageIndex": page},
                                timeout=_T)
            if r.status_code == 401:
                # try refresh, saves a restart
                print(c(C.GREY, "\n  [auth] 401 — attempting silent refresh..."), flush=True)
                if do_token_refresh(session):
                    r = session.get(f"{ELDORADO_HOST}/api/flexibleOffers/me/search",
                                    params={"gameId": GAME_ID, "offerState": "Active", "pageSize": 50, "pageIndex": page},
                                    timeout=_T)
                else:
                    print("  [AUTH] 401 — cookies expired, please refresh cookies (option 7)")
                    break
            if r.status_code != 200:
                print(f"  [ERROR] get_my_active_offers page {page}: HTTP {r.status_code}")
                break
            data = r.json()
            results = data.get("results", [])
            offers.extend(results)
            if len(results) < 50:
                break
            page += 1
    except requests.Timeout as e:
        print(f"\n  [ERROR] get_my_active_offers timeout (page {page}): {e}")
    except Exception as e:
        print(f"\n  [ERROR] get_my_active_offers: {e}")
    return offers


def get_all_my_offers(session):
    offers = []
    for state in ("Active", "Paused", "Closed"):
        page = 1
        state_count = 0
        while True:
            try:
                r = session.get(f"{ELDORADO_HOST}/api/flexibleOffers/me/search",
                                params={"gameId": GAME_ID, "offerState": state, "pageSize": 50, "pageIndex": page})
            except Exception as e:
                print(f"  [ERROR] fetch {state} page {page}: {e}")
                break
            if r.status_code == 401:
                print(c(C.GREY, "\n  [auth] 401 — attempting silent refresh..."), flush=True)
                if do_token_refresh(session):
                    try:
                        r = session.get(f"{ELDORADO_HOST}/api/flexibleOffers/me/search",
                                        params={"gameId": GAME_ID, "offerState": state, "pageSize": 50, "pageIndex": page})
                    except Exception:
                        break
                    if r.status_code == 401:
                        print("  [AUTH] 401 — cookies expired, please refresh cookies (option 6)")
                        break
                else:
                    print("  [AUTH] 401 — cookies expired, please refresh cookies (option 6)")
                    break
            if r.status_code != 200:
                print(f"  [ERROR] {state} page {page}: HTTP {r.status_code} {r.text[:100]}")
                break
            data = r.json()
            results = data.get("results", [])
            for res in results:
                res["_state"] = state
                offers.append(res)
            state_count += len(results)
            if len(results) < 50:
                break
            page += 1
        print(f"  [{state}] {state_count} listing(s)")
    return offers


_xsrf_prompted = False

def _prompt_xsrf(session):
    global _xsrf_prompted
    if _xsrf_prompted:
        return
    _xsrf_prompted = True
    print(c(C.ORANGE, "\n  Request blocked (403) — XSRF token needed."))
    print(c(C.GREY,   "  In Chrome: F12 → Network → any request → Request Headers → copy 'x-xsrf-token' value"))
    while True:
        xsrf = input("  x-xsrf-token: ").strip()
        if xsrf:
            break
        print(c(C.RED, "  Cannot be blank."))
    session.headers["X-XSRF-TOKEN"] = xsrf
    session.headers["X-XSRF-Token"]  = xsrf
    cookie = session.headers.get("Cookie", "")
    if "__Host-XSRF-TOKEN=" in cookie:
        cookie = re.sub(r'__Host-XSRF-TOKEN=[^;]*', f"__Host-XSRF-TOKEN={xsrf}", cookie)
    else:
        cookie = cookie + f"; __Host-XSRF-TOKEN={xsrf}"
    session.headers["Cookie"] = cookie


def update_offer_price(session, offer_id, new_price_usd, offer_inner):

    existing_attrs = offer_inner.get("attributes") or []
    ms_attr_id = "0"
    mutation_attr_id = "none"
    for a in existing_attrs:
        if isinstance(a, dict) and "id" in a and "value" in a:
            v = a["value"] if not isinstance(a["value"], dict) else a["value"].get("id", "")
            if a["id"] == "steal-a-brainrot-ms":
                ms_attr_id = _remap_ms(str(v))
            elif a["id"] == "steal-a-brainrot-mutations":
                mutation_attr_id = str(v)

    title = offer_inner.get("offerTitle", "")
    offer_attributes = _build_offer_attributes(existing_attrs, ms_attr_id, mutation_attr_id, title)

    trade_envs = offer_inner.get("tradeEnvironmentValues") or []
    trade_env_id = trade_envs[-1]["id"] if trade_envs else ""

    payload = {
        "details": {
            "offerTitle": title,
            "description": offer_inner.get("description", ""),
            "guaranteedDeliveryTime": offer_inner.get("guaranteedDeliveryTime", 20),
            "pricing": {
                "quantity": offer_inner.get("quantity", 1),
                "minQuantity": offer_inner.get("minQuantity", 1),
                "pricePerUnit": {
                    "amount": round(new_price_usd, 2),
                    "currency": "USD"
                }
            },
            "mainOfferImage": offer_inner.get("mainOfferImage"),
            "offerImages": offer_inner.get("offerImages", [])
        },
        "augmentedGame": {
            "gameId": offer_inner.get("gameId", GAME_ID),
            "category": offer_inner.get("category", CATEGORY),
            "tradeEnvironmentId": trade_env_id,
            "attributeIdsCsv": None,
            "offerAttributes": offer_attributes
        }
    }

    r = session.put(f"{ELDORADO_HOST}/api/v1/item-management/me/offers/item/{offer_id}/details", json=payload)
    if r.status_code == 403:
        _prompt_xsrf(session)
        r = session.put(f"{ELDORADO_HOST}/api/v1/item-management/me/offers/item/{offer_id}/details", json=payload)
    if r.status_code in (200, 201, 204):
        return True
    try:
        err_msgs = r.json().get("messages") or []
        err_text = " ".join(str(m) for m in err_msgs) if isinstance(err_msgs, list) else str(err_msgs)
    except Exception:
        err_text = r.text[:300]
    print(f"    [price update] HTTP {r.status_code}: {err_text[:200]}")
    return False


def _print_edit_listing(active):
    def strip_emoji(s):
        return re.sub(r'[^\x00-\x7F\u00C0-\u024F]', '', s).strip()

    print()
    print(f"  {'#':>3}  {'$':>7}  {'Item':<28}  {'Mut':<11}  {'Gen':<10}  {'Tr'}")
    print("  " + "-" * 72)
    for i, o in enumerate(active, 1):
        raw_title = strip_emoji(o.get("offerTitle") or "")
        price = (o.get("pricePerUnitInUSD") or o.get("pricePerUnit") or {}).get("amount", 0)

        attrs = o.get("attributes") or []
        mut = next((a["value"]["id"] for a in attrs if a.get("id") == "steal-a-brainrot-mutations"), None)
        if not mut:
            tl = raw_title.lower()
            mut = next((v for k, v in sorted(MUTATION_OPTIONS.items(), key=lambda x: len(x[0]), reverse=True)
                        if k != "none" and k in tl), "none")

        gen_str = _extract_gen_from_title(raw_title.lower()) or ""

        tm = re.search(r'(\d+)\s*trait', raw_title, re.IGNORECASE)
        traits = tm.group(1) if tm else "-"

        item = raw_title
        for pat in [r'\|.*', r'(?i)\b(secret|fast|fastest|delivery|cheap|steal\s*a\s*brainrot)\b.*',
                    r'(?i)\b\d+\s*traits?\b', gen_str.replace('.', r'\.') if gen_str else r'$^',
                    r'[^\x00-\x7F\u00C0-\u024F]']:
            item = re.sub(pat, '', item).strip()
        for k in sorted(MUTATION_OPTIONS.keys(), key=len, reverse=True):
            if k != "none":
                item = re.sub(rf'(?i)\b{re.escape(k)}\b', '', item).strip()
        item = item.strip(' -|').strip()

        mut_disp = mut if mut != "none" else "-"
        paused = price >= 999
        price_disp = f"[{price:.2f}]" if paused else f"${price:.2f}"
        print(f"  {i:>3}  {price_disp:>8}  {item:<28}  {mut_disp:<11}  {gen_str:<10}  {traits}")


def edit_title_mode(session):
    all_offers = get_all_my_offers(session)
    if not all_offers:
        print("No listings found.")
        return

    active = [o for o in all_offers if o.get("_state") == "Active"]
    if not active:
        print("No active listings.")
        return

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        _print_edit_listing(active)

        raw = input("\nEnter listing number (blank to exit): ").strip()
        if not raw:
            return
        try:
            idx = int(raw) - 1
            offer = active[idx]
        except (ValueError, IndexError):
            print("Invalid selection.")
            continue

        offer_id = offer.get("id") or offer.get("offerId")
        inner = offer

        current_title = inner.get("offerTitle", "")
        try:
            import tkinter as tk
            root = tk.Tk()
            root.title("Edit Title")
            root.attributes("-topmost", True)
            root.resizable(True, False)

            tk.Label(root, text="Edit listing title:", font=("Segoe UI", 10)).pack(padx=12, pady=(12, 4), anchor="w")
            entry = tk.Entry(root, font=("Segoe UI", 11), width=80)
            entry.pack(padx=12, pady=(0, 8), fill="x")
            entry.insert(0, current_title)
            entry.select_range(0, "end")
            entry.focus_set()

            result = [None]

            def confirm():
                result[0] = entry.get()
                root.destroy()

            def cancel():
                root.destroy()

            btn_frame = tk.Frame(root)
            btn_frame.pack(pady=(0, 12))
            tk.Button(btn_frame, text="OK", width=10, command=confirm, font=("Segoe UI", 10)).pack(side="left", padx=6)
            tk.Button(btn_frame, text="Cancel", width=10, command=cancel, font=("Segoe UI", 10)).pack(side="left", padx=6)

            root.bind("<Return>", lambda *_: confirm())
            root.bind("<Escape>", lambda *_: cancel())

            root.update_idletasks()
            w = root.winfo_reqwidth()
            h = root.winfo_reqheight()
            x = (root.winfo_screenwidth() - w) // 2
            y = (root.winfo_screenheight() - h) // 2
            root.geometry(f"{w}x{h}+{x}+{y}")

            root.mainloop()
            new_title = result[0]
            if new_title is None:
                continue
            new_title = new_title.strip()
        except Exception:
            new_title = input("  New title (blank to cancel): ").strip()
        if not new_title:
            continue

        new_title_lower = new_title.lower()
        gen_str = _extract_gen_from_title(new_title_lower)
        new_ms_attr = resolve_ms_attr(gen_str) if gen_str else MS_OPTIONS["0"]

        old_ms = "none"
        for a in (inner.get("attributes") or []):
            if isinstance(a, dict) and a.get("id") == "steal-a-brainrot-ms":
                v = a["value"] if not isinstance(a["value"], dict) else a["value"].get("id", "none")
                old_ms = _remap_ms(str(v))
        if old_ms != new_ms_attr:
            print(f"  Generation: [{old_ms}] → [{new_ms_attr}]")

        detected_mut = None
        title_plain = re.sub(r'[^a-z0-9 ]', ' ', new_title_lower)
        for mut_key, mut_val in sorted(MUTATION_OPTIONS.items(), key=lambda x: len(x[0]), reverse=True):
            if mut_key == "none":
                continue
            check_key = re.sub(r'[^a-z0-9]', '', mut_key)
            check_val = re.sub(r'[^a-z0-9]', '', mut_val)
            if re.search(rf'\b{re.escape(check_key)}\b', title_plain) or re.search(rf'\b{re.escape(check_val)}\b', title_plain):
                detected_mut = mut_val
                break
        new_mut = detected_mut or "none"
        old_mut = "none"
        for a in (inner.get("attributes") or []):
            if isinstance(a, dict) and a.get("id") == "steal-a-brainrot-mutations":
                old_mut = (a["value"] if not isinstance(a["value"], dict) else a["value"].get("id", "none"))
        if old_mut != new_mut:
            print(f"  Mutation: [{old_mut}] → [{new_mut}]")

        offer_attributes = _build_offer_attributes(inner.get("attributes"), new_ms_attr, new_mut, new_title)

        tev = inner.get("tradeEnvironmentValues") or []
        trade_env_id = tev[-1]["id"] if tev else None

        payload = {
            "details": {
                "offerTitle": new_title,
                "description": inner.get("description", ""),
                "guaranteedDeliveryTime": inner.get("guaranteedDeliveryTime", 20),
                "pricing": {
                    "quantity": inner.get("quantity", 1),
                    "minQuantity": inner.get("minQuantity", 1),
                    "pricePerUnit": inner.get("pricePerUnit", {"amount": 0, "currency": "USD"})
                },
                "mainOfferImage": inner.get("mainOfferImage"),
                "offerImages": inner.get("offerImages", [])
            },
            "augmentedGame": {
                "gameId": inner.get("gameId", GAME_ID),
                "category": inner.get("category", CATEGORY),
                "tradeEnvironmentId": trade_env_id,
                "attributeIdsCsv": None,
                "offerAttributes": offer_attributes
            }
        }

        r = session.put(f"{ELDORADO_HOST}/api/v1/item-management/me/offers/item/{offer_id}/details", json=payload)
        if r.status_code in (200, 201, 204):
            print("  Updated.")
            all_offers = get_all_my_offers(session)
            active = [o for o in all_offers if o.get("_state") == "Active"]
        else:
            print(f"  Failed ({r.status_code}): {r.text[:200]}")
            input("  Press Enter to continue...")


def restock_mode(session):
    all_offers = get_all_my_offers(session)
    if not all_offers:
        print("No listings found.")
        return

    active_ct  = sum(1 for o in all_offers if o.get("_state") == "Active")
    paused_ct  = sum(1 for o in all_offers if o.get("_state") == "Paused")
    closed_ct  = sum(1 for o in all_offers if o.get("_state") == "Closed")
    input(f"\n  Fetched: {active_ct} Active  {paused_ct} Paused  {closed_ct} Closed  (Press Enter to continue...)")

    MUTATION_ORDER = ["none", "gold", "diamond", "rainbow", "bloodrot", "candy", "lava", "galaxy", "yin-yang", "radioactive", "cursed", "divine", "neon", "cyber"]

    def offer_sort_key(x):
        o = x.get("offer", x)
        tev = o.get("tradeEnvironmentValues") or []
        item_name = tev[-1]["value"].lower() if tev else "zzz"
        mut = "none"
        for a in (o.get("attributes") or []):
            if a.get("id") == "steal-a-brainrot-mutations":
                mut = (a.get("value") or {}).get("id", "none").lower()
        mut_idx = MUTATION_ORDER.index(mut) if mut in MUTATION_ORDER else 99
        traits = 0
        title = (o.get("offerTitle") or "").lower()
        m = re.search(r'(\d+)\s*trait', title)
        if m:
            traits = int(m.group(1))
        return (item_name, mut_idx, traits)

    all_offers.sort(key=offer_sort_key)

    groups = {}
    group_order = []
    for offer in all_offers:
        o = offer.get("offer", offer)
        tev = o.get("tradeEnvironmentValues") or []
        item_name = tev[-1]["value"] if tev else "Unknown"
        if item_name not in groups:
            groups[item_name] = []
            group_order.append(item_name)
        groups[item_name].append(offer)

    def print_groups():
        os.system("cls" if os.name == "nt" else "clear")
        print()
        for gi, item_name in enumerate(group_order, 1):
            print(f"  {gi:>3}. {item_name}")

    def print_group_items(item_name):
        os.system("cls" if os.name == "nt" else "clear")
        print(f"\n  {item_name}")
        print("  " + "-" * 55)
        for li, offer in enumerate(groups[item_name], 1):
            o = offer.get("offer", offer)
            state = offer.get("_state", "Active")
            qty = o.get("quantity", "?")
            price = (o.get("pricePerUnitInUSD") or o.get("pricePerUnit") or {}).get("amount", 0)
            state_tag = f"[{state}] " if state != "Active" else ""
            title = re.sub(r'[^\x00-\x7F\u00C0-\u024F]', '', o.get("offerTitle") or "")[:50].strip()
            print(f"    {li:>3}. {state_tag:10}[{qty:>7} stock]  ${price:>7.2f}  {title}")

    print_groups()
    while True:
        raw_g = input("\nEnter group number (blank to exit): ").strip()
        if not raw_g:
            return
        try:
            gi = int(raw_g) - 1
            if gi < 0 or gi >= len(group_order):
                print("Invalid group.")
                continue
        except ValueError:
            print("Invalid input.")
            continue

        current_group_name = group_order[gi]
        while True:
            print_group_items(current_group_name)
            raw_l = input("\nEnter item number (blank to go back): ").strip()
            if not raw_l:
                print_groups()
                break
            try:
                idx = int(raw_l) - 1
                selected_group = groups[current_group_name]
                if idx < 0 or idx >= len(selected_group):
                    print("Invalid selection.")
                    continue
            except ValueError:
                print("Invalid input.")
                continue

            offer = selected_group[idx]
            o = offer.get("offer", offer)
            offer_id = o.get("id")
            state = offer.get("_state", "Active")
            current_qty = o.get("quantity", 0)
            print(f"\n  {o.get('offerTitle','')[:65]}")
            print(f"  State: {state} | Stock: {current_qty}")

            new_qty_raw = input("  New quantity: ").strip()
            if not new_qty_raw:
                continue
            try:
                new_qty = int(new_qty_raw)
            except ValueError:
                print("Invalid quantity.")
                continue

            inner = o

            trade_envs = inner.get("tradeEnvironmentValues") or []
            trade_env_id = trade_envs[-1]["id"] if trade_envs else ""

            ms_attr_id = "0"
            mutation_attr_id = "none"
            for a in (inner.get("attributes") or []):
                if isinstance(a, dict) and "id" in a and "value" in a:
                    v = a["value"] if not isinstance(a["value"], dict) else a["value"].get("id", "")
                    if a["id"] == "steal-a-brainrot-ms":
                        ms_attr_id = _remap_ms(str(v))
                    elif a["id"] == "steal-a-brainrot-mutations":
                        mutation_attr_id = str(v)
            offer_attributes = _build_offer_attributes(
                inner.get("attributes"), ms_attr_id, mutation_attr_id, inner.get("offerTitle", "")
            )

            price_amt = 999.99
            payload = {
                "details": {
                    "offerTitle": inner.get("offerTitle", ""),
                    "description": inner.get("description", ""),
                    "guaranteedDeliveryTime": inner.get("guaranteedDeliveryTime", 20),
                    "pricing": {
                        "quantity": new_qty,
                        "minQuantity": inner.get("minQuantity", 1),
                        "pricePerUnit": {
                            "amount": round(price_amt, 2),
                            "currency": "USD"
                        }
                    },
                    "mainOfferImage": inner.get("mainOfferImage"),
                    "offerImages": inner.get("offerImages", [])
                },
                "augmentedGame": {
                    "gameId": inner.get("gameId", GAME_ID),
                    "category": inner.get("category", CATEGORY),
                    "tradeEnvironmentId": trade_env_id,
                    "attributeIdsCsv": None,
                    "offerAttributes": offer_attributes
                }
            }

            r = session.put(f"{ELDORADO_HOST}/api/v1/item-management/me/offers/item/{offer_id}/details",
                            json=payload)
            if r.status_code not in (200, 201, 204):
                try:
                    body = r.json()
                    err = body.get("messages") or body.get("message") or body.get("title") or r.text[:300]
                except Exception:
                    err = r.text[:300]
                print(f"  Failed to update stock ({r.status_code}): {err}")
                input("  Press Enter to continue...")
                continue

            print(f"  Stock: {current_qty} → {new_qty}")

            if state != "Active":
                r_resume = session.post(f"{ELDORADO_HOST}/api/v1/item-management/me/offers/{offer_id}/resume")
                if r_resume.status_code in (200, 201, 204):
                    print(f"  Enabled (was {state})")
                else:
                    try:
                        err = r_resume.json().get("messages") or r_resume.text[:200]
                    except Exception:
                        err = r_resume.text[:200]
                    print(f"  Could not enable: {err}")

            input("  Press Enter to continue...")
            all_offers = get_all_my_offers(session)
            all_offers.sort(key=offer_sort_key)
            groups = {}
            group_order = []
            for _offer in all_offers:
                _o = _offer.get("offer", _offer)
                _tev = _o.get("tradeEnvironmentValues") or []
                _name = _tev[-1]["value"] if _tev else "Unknown"
                if _name not in groups:
                    groups[_name] = []
                    group_order.append(_name)
                groups[_name].append(_offer)
            if current_group_name not in groups:
                break


def pause_all_listings_mode(session):
    """set all active to $999.99 to pause them"""
    active_offers = get_my_active_offers(session)
    if not active_offers:
        print("No active listings found.")
        return

    print(f"\n  Found {len(active_offers)} active listing(s).")
    confirm = input("  Set ALL to $999.99? (y/n): ").strip().lower()
    if confirm != "y":
        print("  Cancelled.")
        return

    updated = failed = 0
    for offer in active_offers:
        o = offer.get("offer", offer)
        offer_id = o.get("id")
        title = (o.get("offerTitle") or "")[:50].strip()
        if not offer_id:
            continue
        ok = update_offer_price(session, offer_id, 999.99, o)
        if ok:
            updated += 1
            print(f"  [paused] ${999.99:.2f}  {title}")
        else:
            failed += 1
            print(f"  [FAILED]            {title}")

    print(f"\n  Done — {updated} paused, {failed} failed.")


def update_other_prices_mode(session):
    my_offers = get_my_active_offers(session)
    if not my_offers:
        return

    other_offers = []
    for offer in my_offers:
        o = offer.get("offer", offer)
        envs = o.get("tradeEnvironmentValues", [])
        item_cat = next((e["value"] for e in envs if e["name"] == "Brainrot"), None)
        if item_cat and (item_cat == "Other" or item_cat == "OG" or item_cat.lower() not in _BRAINROT_LOWER):
            other_offers.append(o)

    if not other_offers:
        return

    total = len(other_offers)
    updated = failed = skipped = 0
    for i, o in enumerate(other_offers, 1):
        offer_id = o.get("id")
        my_price = (o.get("pricePerUnitInUSD") or o.get("pricePerUnit") or {}).get("amount", 0)
        title = (o.get("offerTitle") or "").strip()
        if not offer_id or not my_price or not title:
            continue

        # skip paused ones
        if my_price > 999.99:
            skipped += 1
            continue

        attrs = o.get("attributes", [])
        ms_attr = next((a["value"]["id"] for a in attrs if a["id"] == "steal-a-brainrot-ms"), None)
        mutation_attr = next((a["value"]["id"] for a in attrs if a["id"] == "steal-a-brainrot-mutations"), "none")

        gen_str = _extract_gen_from_title(title.lower())
        ms_value_for_price = gen_str if gen_str else (ms_attr or "")

        # other/OG is a category not a name, use title then
        tev = o.get("tradeEnvironmentValues") or []
        tev_name = next((e["value"] for e in tev if e.get("name") == "Brainrot"), None)
        if tev_name in ("Other", "OG"):
            tev_name = None
        item_name_raw = tev_name if tev_name else title.split("|")[0].strip()
        # Gold Cloverat Clapat -> Cloverat Clapat
        if not tev_name:
            item_name_raw = re.sub(r'[^\x00-\x7F]+', ' ', item_name_raw).strip()
            item_name_raw = re.sub(r'\s+', ' ', item_name_raw).strip()
            _mut_words = set(MUTATION_OPTIONS.keys()) | {"yin", "yinyang"}
            parts = item_name_raw.split()
            if parts and parts[0].lower().replace("-", "").replace(" ", "") in _mut_words:
                item_name_raw = " ".join(parts[1:])
        canonical = get_canonical_name(item_name_raw)
        trade_id, _ = get_trade_env(canonical)

        ms_display = f" [{ms_attr}]" if ms_attr else ""
        _draw_progress(i, total, f"{item_name_raw}{ms_display}")

        if trade_id:
            target = get_lowest_price(session, canonical, mutation_attr, ms_value_for_price)
            if not target and mutation_attr and mutation_attr != "none":
                target = get_lowest_price(session, canonical, mutation_attr, ms_value_for_price, no_mutation_filter=True)
        else:
            my_gen_num = _parse_gen_to_num(gen_str) if gen_str else None
            target = get_lowest_price_by_title(session, item_name_raw, ms_attr, my_gen_num=my_gen_num)

        if not target:
            print(f"\r{' ':90}\r", end="")
            mut_str = f" ({mutation_attr})" if mutation_attr and mutation_attr != "none" else ""
            print(c(C.GREY, f"  ~ no listings found for '{item_name_raw[:40]}{mut_str}'{ms_display} — currently listed at ${my_price:.2f}"), flush=True)
            manual = input(c(C.ORANGE, f"  ? Set new price in USD (Enter to keep ${my_price:.2f}): ")).strip()
            if not manual:
                skipped += 1
                continue
            try:
                target = float(manual.replace("$", "").strip())
            except ValueError:
                print(c(C.RED, "  Invalid price — skipping."))
                skipped += 1
                continue

        if abs(target - my_price) < 0.01:
            print(c(C.GREY, f"  = {item_name_raw[:40]}{ms_display} already at ${target:.2f}"), flush=True)
            skipped += 1
            continue

        if update_offer_price(session, offer_id, target, o):
            _print_price_change(item_name_raw, mutation_attr, ms_display, my_price, target)
            updated += 1
        else:
            _print_price_fail(item_name_raw, ms_display)
            failed += 1
        time.sleep(1.5)

    print(f"\r{' ':90}\r", end="")
    if updated or failed:
        u  = c(C.GREEN, f"{updated} updated")
        f_ = c(C.RED,   f"{failed} failed") if failed else c(C.GREY, f"{failed} failed")
        s  = c(C.GREY,  f"{skipped} unchanged")
        print(f"  {u}  {f_}  {s}")


def _print_price_change(item_name, mutation, ms_display, old_price, new_price):
    mut_label = f" {c(C.PURPLE, f'({mutation})')}" if mutation and mutation != "none" else ""
    ms_label  = c(C.GREY, ms_display) if ms_display else ""
    name_str  = c(C.WHITE, C.BOLD + item_name) + mut_label + ms_label
    arrow     = c(C.GREY, " → ")
    old_str   = c(C.GREY, f"${old_price:.2f}")
    new_str   = c(C.GREEN, f"${new_price:.2f}")
    tick      = c(C.GREEN, "  ✓ ")
    print(f"\r{' ':90}\r{tick}{name_str}{arrow}{old_str}{arrow}{new_str}")

def _print_price_fail(item_name, ms_display):
    ms_label = c(C.GREY, ms_display) if ms_display else ""
    print(f"\r{' ':90}\r{c(C.RED, '  ✗ ')}{c(C.WHITE, item_name)}{ms_label}{c(C.RED, '  failed')}")

def _draw_progress(i, total, label, bar_width=32):
    filled = int(bar_width * i / total)
    bar = c(C.CYAN, "█" * filled) + c(C.DKGREY, "░" * (bar_width - filled))
    counter = c(C.GREY, f"{i}/{total}")
    lbl = c(C.GREY, f"  {label[:42]:<42}")
    print(f"\r  {bar}  {counter}{lbl}", end="", flush=True)


def update_all_prices_once(session):
    print(c(C.GREY, "\n  Fetching listings..."), end=" ", flush=True)
    my_offers = get_my_active_offers(session)
    if not my_offers:
        print(c(C.RED, "none found."))
        return

    eligible = []
    for offer in my_offers:
        o = offer.get("offer", offer)
        offer_id = o.get("id")
        my_price = (o.get("pricePerUnitInUSD") or o.get("pricePerUnit") or {}).get("amount", 0)
        if not offer_id or not my_price:
            continue
        envs = o.get("tradeEnvironmentValues", [])
        item_name = next((e["value"] for e in envs if e["name"] == "Brainrot"), None)
        if not item_name or item_name in ("Other", "OG"):
            continue
        eligible.append(offer)

    eligible.sort(key=lambda x: (x.get("offer", x).get("pricePerUnitInUSD") or x.get("offer", x).get("pricePerUnit") or {}).get("amount", 0))
    total = len(eligible)
    print(c(C.WHITE, C.BOLD + str(total)) + c(C.GREY, " listings\n"))

    # step 1 get prices, 10 threads
    price_results = {}
    price_cache   = {}
    price_lock    = threading.Lock()
    fetch_done    = [0]

    def _fetch_price(idx, offer):
        o = offer.get("offer", offer)
        envs = o.get("tradeEnvironmentValues", [])
        item_name = next((e["value"] for e in envs if e["name"] == "Brainrot"), None)
        attrs = o.get("attributes", [])
        mutation = next((a["value"]["id"] for a in attrs if a["id"] == "steal-a-brainrot-mutations"), "none")
        ms_attr  = next((a["value"]["id"] for a in attrs if a["id"] == "steal-a-brainrot-ms"), None)
        title = (o.get("offerTitle") or "")
        gen_str = _extract_gen_from_title(title.lower())
        ms_value_for_price = gen_str if gen_str else (ms_attr or "")

        cache_key = (item_name, mutation, ms_value_for_price)

        with price_lock:
            if cache_key in price_cache:
                price_results[idx] = price_cache[cache_key]
                fetch_done[0] += 1
                _draw_progress(fetch_done[0], total, f"{item_name} ({mutation}) [cached]")
                return

        lowest = get_lowest_price(session, item_name, mutation, ms_value_for_price, no_sleep=True)
        if not lowest and mutation and mutation != "none":
            lowest = get_lowest_price(session, item_name, mutation, ms_value_for_price, no_mutation_filter=True, no_sleep=True)

        with price_lock:
            price_cache[cache_key] = lowest
            price_results[idx] = lowest
            fetch_done[0] += 1
            _draw_progress(fetch_done[0], total, f"{item_name} ({mutation})")

    print(c(C.GREY, "  Fetching market prices in parallel...\n"))
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=10) as executor:
        for i, offer in enumerate(eligible):
            executor.submit(_fetch_price, i, offer)

    print(f"\r{' ':90}\r", end="")

    # step 2 push updates
    updated = failed = skipped = 0
    for i, offer in enumerate(eligible):
        o = offer.get("offer", offer)
        offer_id = o.get("id")
        my_price = (o.get("pricePerUnitInUSD") or o.get("pricePerUnit") or {}).get("amount", 0)

        envs = o.get("tradeEnvironmentValues", [])
        item_name = next((e["value"] for e in envs if e["name"] == "Brainrot"), None)
        attrs = o.get("attributes", [])
        mutation = next((a["value"]["id"] for a in attrs if a["id"] == "steal-a-brainrot-mutations"), "none")
        ms_attr  = next((a["value"]["id"] for a in attrs if a["id"] == "steal-a-brainrot-ms"), None)
        ms_display = f" [{ms_attr}]" if ms_attr else ""

        lowest = price_results.get(i)
        if not lowest:
            skipped += 1
            continue

        if abs(lowest - my_price) < 0.01:
            skipped += 1
            continue

        if update_offer_price(session, offer_id, lowest, o):
            _print_price_change(item_name, mutation, ms_display, my_price, lowest)
            updated += 1
        else:
            _print_price_fail(item_name, ms_display)
            failed += 1

        time.sleep(0.1)

    print(f"\r{' ':90}\r", end="")
    u = c(C.GREEN,  f"{updated} updated")
    f_ = c(C.RED,   f"{failed} failed") if failed else c(C.GREY, f"{failed} failed")
    s = c(C.GREY,   f"{skipped} unchanged")
    print(f"  {u}  {f_}  {s}\n")


def batch_mode(session, batch_file):
    """make listings from a json file"""
    with open(batch_file, "r") as f:
        listings = json.load(f)

    print(f"\n[BATCH] Processing {len(listings)} listings...")

    for i, listing in enumerate(listings):
        print(f"\n--- Listing {i+1}/{len(listings)} ---")

        item_name = listing["item_name"]
        mutation = listing.get("mutation", "None")
        ms_value = listing.get("ms", "0")

        # no price given, use lowest
        if "price_usd" not in listing:
            print(f"  [PRICE] Looking up lowest for {mutation} {item_name}...")
            lowest = get_lowest_price(session, item_name, mutation, ms_value)
            if lowest:
                listing["price_usd"] = lowest
                print(f"  Price: ${listing['price_usd']:.2f}")
            else:
                print(f"  [SKIP] No price found and none specified for {item_name}")
                continue

        if "image" in listing and not listing.get("image_path"):
            listing["image_path"] = os.path.join(IMAGES_DIR, listing["image"])

        success = upload_image_and_create_offer(session, listing)
        if success:
            print(f"  [OK] #{i+1} done")
        else:
            print(f"  [FAIL] #{i+1} failed")

        time.sleep(1)


def update_gen_filter_mode(session):
    """read gen from titles and fix the ms filter"""
    active_offers = get_my_active_offers(session)
    if not active_offers:
        print("No active listings found.")
        return

    print(f"\n  Found {len(active_offers)} active listing(s) — detecting generation from titles:\n")
    changes = []
    for offer in active_offers:
        o = offer.get("offer", offer)
        offer_id = o.get("id")
        title = (o.get("offerTitle") or "").strip()
        attrs = o.get("attributes") or []
        ms_cur = next((a["value"]["id"] for a in attrs if a["id"] == "steal-a-brainrot-ms"), "none")

        gen_str = _extract_gen_from_title(title.lower())
        new_ms = resolve_ms_attr(gen_str) if gen_str else None

        if new_ms and new_ms != ms_cur:
            print(f"  [CHANGE] [{ms_cur}] → [{new_ms}]  {title[:60]}")
            changes.append((offer_id, title, new_ms))
        elif new_ms:
            print(f"  [OK]     [{ms_cur}]  {title[:60]}")
        else:
            print(f"  [SKIP]   [{ms_cur}]  {title[:60]}  (no gen in title)")

    if not changes:
        print("\n  All filters already correct, nothing to update.")
        return

    print(f"\n  {len(changes)} listing(s) need updating.")
    confirm = input("  Apply changes? (y/n): ").strip().lower()
    if confirm != "y":
        print("  Cancelled.")
        return

    offer_by_id = {(o.get("offer", o)).get("id"): o.get("offer", o) for o in active_offers}
    updated = failed = 0
    for offer_id, title, new_ms_attr in changes:
        inner = offer_by_id.get(offer_id)
        if not inner:
            print(f"  [FAIL] offer not found in cache: {title[:50]}")
            failed += 1
            continue

        trade_envs = inner.get("tradeEnvironmentValues") or []
        trade_env_id = trade_envs[-1]["id"] if trade_envs else ""

        mutation_attr_id = "none"
        for a in (inner.get("attributes") or []):
            if isinstance(a, dict) and a.get("id") == "steal-a-brainrot-mutations":
                mutation_attr_id = a["value"] if not isinstance(a["value"], dict) else a["value"].get("id", "none")

        offer_attributes = _build_offer_attributes(
            inner.get("attributes"), new_ms_attr, mutation_attr_id, inner.get("offerTitle", "")
        )

        payload = {
            "details": {
                "offerTitle": inner.get("offerTitle", ""),
                "description": inner.get("description", ""),
                "guaranteedDeliveryTime": inner.get("guaranteedDeliveryTime", 20),
                "pricing": {
                    "quantity": inner.get("quantity", 1),
                    "minQuantity": inner.get("minQuantity", 1),
                    "pricePerUnit": inner.get("pricePerUnit", {"amount": 0, "currency": "USD"})
                },
                "mainOfferImage": inner.get("mainOfferImage"),
                "offerImages": inner.get("offerImages", [])
            },
            "augmentedGame": {
                "gameId": inner.get("gameId", GAME_ID),
                "category": inner.get("category", CATEGORY),
                "tradeEnvironmentId": trade_env_id,
                "attributeIdsCsv": None,
                "offerAttributes": offer_attributes
            }
        }

        r = session.put(f"{ELDORADO_HOST}/api/v1/item-management/me/offers/item/{offer_id}/details", json=payload)
        if r.status_code in (200, 201, 204):
            updated += 1
            print(f"  [OK] → [{new_ms_attr}]  {title[:60]}")
        else:
            failed += 1
            try:
                err = r.json().get("messages") or r.json().get("message") or r.text[:200]
            except Exception:
                err = r.text[:200]
            print(f"  [FAIL] {title[:50]}: {err}")
        time.sleep(0.3)

    print(f"\n  Done — {updated} updated, {failed} failed.")


def main():
    print(c(C.GOLD, C.BOLD + "  Eldorado Auto Lister") + c(C.GREY, "  by @anson201"))

    cfg = load_config()

    force_reauth = "--reauth" in sys.argv

    cookie_string = cfg.get("cookie_string", "")
    token = cfg.get("token", "")
    xsrf  = cfg.get("xsrf", "")

    if not token or force_reauth:
        print(c(C.GREY, "  Paste __Host-EldoradoIdToken value:"))
        raw = input(c(C.CYAN, "  › ")).strip()
        if raw and "__Host-EldoradoIdToken" in raw:
            cookie_string = raw
            parsed = parse_cookie_string(raw)
            token = parsed.get("__Host-EldoradoIdToken", "")
            xsrf  = parsed.get("__Host-XSRF-TOKEN", "")
            refresh = parsed.get("__Host-EldoradoRefreshToken", "")
            cfg["cookie_string"] = raw
            if refresh:
                with open(REFRESH_FILE, "w") as f:
                    f.write(refresh)
        else:
            token = raw
            cookie_string = ""
            cfg["cookie_string"] = ""

    if not xsrf:
        print(c(C.GREY, "  Paste x-xsrf-token value (F12 → Network → any request → Request Headers):"))
        xsrf = input(c(C.CYAN, "  › ")).strip()

    cfg["token"] = token
    cfg["xsrf"]  = xsrf
    save_config(cfg)

    session = get_session(token, xsrf)
    if cookie_string:
        apply_cookies(session, cookie_string)

    if not verify_token(session):
        print(c(C.GREY, "  [auth] token invalid — attempting Cognito refresh..."), flush=True)
        if _read_refresh_token() and do_token_refresh(session) and verify_token(session):
            print(c(C.GREEN, "  [auth] token refreshed OK"), flush=True)
            save_config(cfg)
        else:
            refresh_cookies(session, cfg)
    else:
        save_config(cfg)

    os.makedirs(IMAGES_DIR, exist_ok=True)
    # id token dies in ~30 min without this
    if _read_refresh_token():
        start_token_refresh_thread(session)
        print(c(C.GREY, "  [auth] token auto-refresh enabled (every 5 min)"), flush=True)
    else:
        print(c(C.ORANGE, "  [auth] no refresh token saved — IdToken will expire in ~30 min"), flush=True)

    if len(sys.argv) > 1 and sys.argv[1].endswith(".json"):
        batch_mode(session, sys.argv[1])
    else:
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            W = 44
            print(c(C.DKGREY, "  ╔" + "═"*W + "╗"))
            print(c(C.DKGREY, "  ║") + c(C.GOLD, C.BOLD + f"{'  ELDORADO AUTO LISTER':^{W}}") + c(C.DKGREY, "║"))
            print(c(C.DKGREY, "  ║") + c(C.GREY,       f"{'  by @anson201':^{W}}") + c(C.DKGREY, "║"))
            print(c(C.DKGREY, "  ╠" + "═"*W + "╣"))
            menu = [
                ("1", "List items from images"),
                ("2", "Update prices"),
                ("3", "Restock a listing"),
                ("4", "Edit listing title"),
                ("5", "Pause all listings"),
                ("6", "Update generation filters"),
                ("7", "Refresh cookies"),
                ("8", "Auto-chat (greet new orders)"),
                ("9", "Exit"),
            ]
            for key, label in menu:
                num = c(C.CYAN, C.BOLD + f" {key}")
                sep = c(C.DKGREY, " │ ")
                txt = c(C.WHITE, label)
                pad = " " * (W - 4 - len(label))
                print(c(C.DKGREY, "  ║") + num + sep + txt + pad + c(C.DKGREY, "║"))
            print(c(C.DKGREY, "  ╚" + "═"*W + "╝"))
            choice = input(c(C.CYAN, "\n  › ")).strip()
            if choice == "1":
                scan_images_mode(session)
                input("\nPress Enter to continue...")
            elif choice == "2":
                update_all_prices_once(session)
                update_other_prices_mode(session)
                input("\nPress Enter to continue...")
            elif choice == "3":
                restock_mode(session)
                input("\nPress Enter to continue...")
            elif choice == "4":
                edit_title_mode(session)
                input("\nPress Enter to continue...")
            elif choice == "5":
                pause_all_listings_mode(session)
                input("\nPress Enter to continue...")
            elif choice == "6":
                update_gen_filter_mode(session)
                input("\nPress Enter to continue...")
            elif choice == "7":
                refresh_cookies(session, cfg)
                input("\nPress Enter to continue...")
            elif choice == "8":
                auto_chat_mode(session)
            elif choice == "9":
                break

    print("\n[DONE] Finished.")
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        print(f"\n[CRASH] {e}")
        traceback.print_exc()
        input("\nPress Enter to exit...")
