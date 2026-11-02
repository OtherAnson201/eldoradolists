# eldoradolists

Console tool for selling Steal a Brainrot items on [Eldorado.gg](https://www.eldorado.gg). It lists items from images, matches the lowest price, restocks, pauses listings and greets new orders.

Use at your own risk and check Eldorado's rules first.

## Setup

Needs Python 3 (checked on 3.13).

```
pip install requests
pip install browser_cookie3 websocket-client
```

The second line is optional:

- `browser_cookie3` grabs a fresh login from Chrome, Edge or Firefox when your tokens die.
- `websocket-client` is the backup way to find new order chats.

### Fill in the placeholders

These are at the top of `eldorado_lister.py`. Both Cognito values are inside your own `__Host-EldoradoIdToken`, which is a JWT. Base64 decode the middle part locally, don't paste it into a website.

| Placeholder | Where to get it | Needed for |
|---|---|---|
| `YOUR_COGNITO_POOL_ID` | End of the `iss` value in the token | Token refresh |
| `YOUR_COGNITO_CLIENT_ID` | The `aud` value in the token | Token refresh |
| `YOUR_TALKJS_APP_ID` | F12 > Network on an Eldorado chat page, in `app.talkjs.com/api/v0/<app id>/` requests | Auto-chat |

### Log in

Run the script and it asks for what it needs:

- `__Host-EldoradoIdToken`, or paste your whole cookie string so it picks up the refresh token too
- `x-xsrf-token`, from F12 > Network > any request > Request Headers

Or copy `config.example.json` to `config.json` and fill it in.

Your login gets saved in plain text in `config.json`, `lung.txt`, `heart.txt` and `refresh.txt`. All four are in `.gitignore`. Never commit or share them.

### Make it yours

The listing description in `upload_image_and_create_offer` and `GREETING_MSG` are written for one shop. Change them before you list anything.

## Use

```
python eldorado_lister.py
```

| Option | What it does |
|---|---|
| 1 List items from images | Lists everything in `images/`. **Deletes each image once its listing is made.** |
| 2 Update prices | Matches the lowest price on your active listings |
| 3 Restock a listing | Sets new stock and turns the listing back on. **Also sets the price to $999.99**, so run option 2 after. |
| 4 Edit listing title | Also updates generation and mutation from the new title |
| 5 Pause all listings | Sets every active listing to $999.99 |
| 6 Update generation filters | Fixes the M/s filter from each title |
| 7 Refresh cookies | Paste a new login |
| 8 Auto-chat | Greets new orders every 60s, Enter to stop |
| 9 Exit | |

Add `--reauth` to paste a new login at startup.

### Image names

Files in `images/` are named `<Mutation><ItemName><Traits>Traits<Generation>`, and everything but the item name is optional. Types are `.png`, `.jpg`, `.jpeg` and `.heic`.

```
GoldLosBros3Traits750M.png
DiamondLaGrandeCombinasion2-3Traits500M-1.1B.png
LosBros2B.png
```

### Batch file

```
python eldorado_lister.py listings.json
```

```json
[
  {"item_name": "Los Bros", "mutation": "Gold", "ms": "900M", "generation": "900M", "quantity": 1, "image": "los_bros.png", "price_usd": 5.0}
]
```

`image` is optional and looked up in `images/`. Leave out `price_usd` to use the lowest price.
