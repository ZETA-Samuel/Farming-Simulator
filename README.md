# Farming Simulator

## Run on desktop

```powershell
python -m pip install -r requirements.txt
python main.py
```

## Run in a browser with pygbag

```powershell
python run_web.py
```

Open the local URL printed by pygbag (usually `http://localhost:8000`) in a
modern browser. Pygbag packages the game's map, tilesets, and animation assets
from this project folder. The launcher removes a stale BrowserFS script from
pygbag's default page template that otherwise causes the browser to remain on
"Loading, please wait ...".

## Shop

The shop opens with **E** when you are near the chicken coop. Buy items on the
left; click **Sell** beside an item in your inventory to sell one unit. Wheat
crops sell for 10 coins, tomatoes for 20, and seeds can be sold back at a lower
price. A sell button appears when that item is in your inventory.
