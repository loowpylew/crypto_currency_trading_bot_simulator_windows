import requests 
from bs4 import BeautifulSoup
from tabulate import tabulate
import colorama 

import colors as c

colorama.init()

def get_asset_pairs_compatiability_finder():
    header_columns=[f"{c.bcolors.HACKER_GREEN}Base Currency", "Currency Symbol", "USD", "EUR", "CAD", "JPY", "GBP", "CHF", "AUD"]

    data = [[f"{c.bcolors.HACKER_GREEN}0x", "ZRX",f"{c.bcolors.ENDC}$", "€", " ", " ", "£", " ", " "],
            [f"{c.bcolors.HACKER_GREEN}1inch", "1INCH", f"{c.bcolors.ENDC}$", "€", " ", " ", " ", " ", " "],
            [f"{c.bcolors.HACKER_GREEN}Aave", "AAVE" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ,"£" ," " ,"a$"],
            [f"{c.bcolors.HACKER_GREEN}Aavegotchi","GHST" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ,"£" ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Acala","ACA" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Akash","AKT" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Algorand","ALGO" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ,"£" ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Altair","AIR" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Ankr","ANKR" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ,"£" ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Aragon","ANT" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Astar","ASTR" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            #[f"{c.bcolors.HACKER_GREEN}Augur","REP" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            #[f"{c.bcolors.HACKER_GREEN}Augur v2","REPV2" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Avalanche","AVAX" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Axie Infinity","AXS" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Badger DAO","BADGER" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Balancer","BNT" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ,"£" ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Bancor","BAL" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Band Protocol","BAND" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Basic Attention Token", "BAT" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Bifrost","BNC" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            #[f"{c.bcolors.HACKER_GREEN}Bitcoin","BTC" ,f"{c.bcolors.ENDC}$" ,"€" ,"c$" ,"¥" ,"£" ,"sfr." ,"a$"],
            [f"{c.bcolors.HACKER_GREEN}Bitcoin Cash","BCH" ,f"{c.bcolors.ENDC}$" ,"€" ," " ,"¥" ,"£" ," " ,"a$"],
            [f"{c.bcolors.HACKER_GREEN}Bonfida","FIDA" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Cardano","ADA" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ,"£" ," " ,"a$"],
            [f"{c.bcolors.HACKER_GREEN}Cartesi","CTSI" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Chainlink","LINK" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ,"£" ," " ,"a$"],
            [f"{c.bcolors.HACKER_GREEN}Chiliz","CHZ" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Compound","COMP" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Cosmos","ATOM" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ,"£" ," " ,"a$"],
            [f"{c.bcolors.HACKER_GREEN}Covalent","CQT" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Curve","CRV" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Dai*","DAI" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Dash","DASH" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Decentraland", "MANA" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            #[f"{c.bcolors.HACKER_GREEN}Dogecoin","DOGE" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}dYdX","DYDX" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Energy Web Token","EWT" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ,"£" ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Enjin Coin","ENJ" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ,"£" ," " ," "],
            #[f"{c.bcolors.HACKER_GREEN}Enzyme Finance","MLN" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}EOS","EOS" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            #[f"{c.bcolors.HACKER_GREEN}Ethereum ('Ether')","ETH" ,f"{c.bcolors.ENDC}$" ,"€" ,"c$" ,"¥" ,"£" ,"sfr." ,"a$"],
            #[f"{c.bcolors.HACKER_GREEN}Ethereum Classic","ETC" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Filecoin","FIL" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ,"£" ," " ,"a$"],
            [f"{c.bcolors.HACKER_GREEN}Flow","FLOW",f"{c.bcolors.ENDC}$" ,"€" ," " ," " ,"£" ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Gnosis","GNO" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}ICON","ICX",f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Injective Protocol","INJ" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Karura","KAR" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Kava","KAVA" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Keep Network" ,"KEEP" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}KILT","KILT" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Kin","KIN" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Kintsugi","KINT" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Kusama","KSM" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ,"£" ," " ,"a$"],
            [f"{c.bcolors.HACKER_GREEN}Kyber Network","KNC" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Lisk","LSK" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            #[f"{c.bcolors.HACKER_GREEN}Litecoin","LTC" ,f"{c.bcolors.ENDC}$" ,"€" ," " ,"¥" ,"£" ," " ,"a$"],
            [f"{c.bcolors.HACKER_GREEN}Livepeer","LPT" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ,"£" ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Loopring","LRC" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Mango","MNGO" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Maker","MKR" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ,"£" ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Mina","MINA" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ,"£" ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Mirror Protocol","MIR" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Monero","XMR" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Moonbeam","GLMR" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Moonriver","MOVR" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Nano","NANO" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Ocean","OCEAN" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ,"£" ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}OmiseGO","OMG" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Orca","ORCA" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Orchid","OXT" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Origin Protocol","OGN" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Oxygen","OXY" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}PAX Gold","PAXG" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Perpetual Protocol","PERP" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Phala","PHA" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Polkadot","DOT" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ,"£" ," " ,"a$"],
            [f"{c.bcolors.HACKER_GREEN}Polygon","MATIC" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ,"£" ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Qtum","QTUM" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Rarible","RARI" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ,"£" ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Raydium","RAY" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}REN Protocol","REN" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ,"£" ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Ripple","XRP" ,f"{c.bcolors.ENDC} " ,"€" ,"c$" ,"¥" ,"£" ," " ,"a$"],
            [f"{c.bcolors.HACKER_GREEN}Saber","SBR" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Serum","SRM" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ,"£" ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Shiba Inu" ,"SHIB" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Shiden","SDN" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Siacoin","SC",f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Solana","SOL" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ,"£" ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Star Atlas","ATLAS",f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Star Atlas DAO","POLIS" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Stellar Lumens","XLM" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ,"£" ," " ,"a$"],
            [f"{c.bcolors.HACKER_GREEN}Step Finance","STEP" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Storj","STORJ" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Sushi","SUSHI" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ,"£" ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Synthetix","SNX" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ,"£" ," " ,"a$"],
            [f"{c.bcolors.HACKER_GREEN}tBTC","TBTC" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Terra","LUNA" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}TerraUSD","UST" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Tether*","USDT" ,f"{c.bcolors.ENDC}$" ,"€" ,"c$" ,"¥" ,"£" ,"sfr." ,"a$"],
            [f"{c.bcolors.HACKER_GREEN}Tezos","XTZ" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ,"£" ," " ,"a$"],
            [f"{c.bcolors.HACKER_GREEN}The Graph","GRT" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ,"£" ," " ,"a$"],
            [f"{c.bcolors.HACKER_GREEN}The Sandbox","SAND" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ,"£" ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Tron","TRX" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Uniswap","UNI" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}USD Coin*","USDC" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ,"£" ," " ,"a$"],
            [f"{c.bcolors.HACKER_GREEN}WAVES","WAVES" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Wrapped Bitcoin","WBTC" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Yearn Finance","YFI" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ,"£" ," " ,"a$"],
            [f"{c.bcolors.HACKER_GREEN}Zcash","ZEC",f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "]] 

    print(f"\n{c.bcolors.HACKER_GREEN}                                                          Quote currency")
    print(f"                                                         ----------------{c.bcolors.ENDC}")
    print(tabulate(data, header_columns))
     
    print("\n")
    print(f"{c.bcolors.HACKER_GREEN}Kraken API only accepts real tender with{c.bcolors.ENDC} 'Z' {c.bcolors.HACKER_GREEN}in front of its symbol for some crypto currencies")
    print(f"{c.bcolors.ENDC}(<Z>Real Tender) {c.bcolors.HACKER_GREEN}symbols only work with the following... {c.bcolors.ENDC}")
    print("\n")
    header_columns=[f"{c.bcolors.HACKER_GREEN}Base Currency", "Currency Symbol", "ZUSD", "ZEUR", "ZCAD", "ZJPY", "ZGBP", "ZCHF", "ZAUD"]
    data = [[f"{c.bcolors.HACKER_GREEN}Augur","XREP" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Augur v2","XREPV2" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Bitcoin","XXBT" ,f"{c.bcolors.ENDC}$" ,"€" ,"c$" ,"¥" ,"£" ,"sfr." ,"a$"],
            [f"{c.bcolors.HACKER_GREEN}Dogecoin","XXDG" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Enzyme Finance","XMLN" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Ethereum ('Ether')","XETH" ,f"{c.bcolors.ENDC}$" ,"€" ,"c$" ,"¥" ,"£" ,"sfr." ,"a$"],
            [f"{c.bcolors.HACKER_GREEN}Ethereum Classic","XETC" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Litecoin","XLTC" ,f"{c.bcolors.ENDC}$" ,"€" ," " ,"¥" ,"£" ," " ,"a$"],
            [f"{c.bcolors.HACKER_GREEN}Monero","XXMR" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Ripple","XXRP" ,f"{c.bcolors.ENDC}$" ,"€" ,"c$" ,"¥" ,"£" ," " ,"a$"],
            [f"{c.bcolors.HACKER_GREEN}Stellar Lumens","XXLM" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ,"£" ," " ,"a$"],
            [f"{c.bcolors.HACKER_GREEN}Tezos","XXTZ" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ,"£" ," " ,"a$"],
            [f"{c.bcolors.HACKER_GREEN}WAVES","WAVE" ,f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "],
            [f"{c.bcolors.HACKER_GREEN}Zcash","XZEC",f"{c.bcolors.ENDC}$" ,"€" ," " ," " ," " ," " ," "]] 
     
    print(tabulate(data, header_columns))


def get_live_top_100_ranking_crypto_currencies():
    URL = "https://www.shufflup.org/volatility_vol.php"
    page = requests.get(URL)                    

    soup = BeautifulSoup(page.content, 'html.parser') 

    count = 0
    count2 = 0
    coin_name = []
    daily_volumes = []
    volatilities = []
    rows = soup.find("table", class_='table table-striped table-bordered table-hover table-condensed').find("tbody").find_all("tr")
    for row in rows: 
        cells = row.find_all("td")
        if count == count2:
            coin_name.append(cells[1].get_text()[0: 30]) # [1] - row 1. [0:29] - max length of crypto before  
                                                         # index borders over to next row
            daily_volumes.append(cells[2].get_text()[0:30]) #[2] - row 2. [0:30] - In case length of volume changes,
                                                            # outofbound index's have been called (does not produce error)
            volatilities.append(cells[3].get_text()[0:30]) # [3] - row3. [0:30] - Same applies here

        count += 1
        count2 += 1

    name_index = 0
    character_index = 10 # no crypto have numbers beyond 10 letters that make up the name of the crypto. 
    
    # This has been implemented as it is unknown how many characters make up the name of the crypto currency
    # given their volatility ranking will change overtime thus the index position within the table will change. 
    # Unfortunetly, this can lead us veering into the next column of the row, thus we will have unwanted numbers 
    # within the output under the coin name column. 
    # Subject to be updated if volatility of crypto currencies that contain numbers within their namings make it
    # into the top 100. From the current state of the leaderboard, only '0x (ZRX)' is within the top 100, with
    # 'B2B (B2BX)' at 150 in the leaderboard so is unlikley to reach to rank 100 anytime soon. 

    for name in coin_name:
        for character in name:
            character_index += 1
            if character.isdigit(): 
                #print(name_index + ": " + coin_name[name_index] + " == " + character)
                #print(character)
                if "0x" in coin_name[name_index]:
                    coin_name[name_index] = "0x (ZRX)"
                else:
                    coin_name[name_index] = coin_name[name_index].replace(character, "")
        name_index += 1
                                                                                     
    print("[The volatility in this table is based off the change in volume in dollars")
    print("giving an overall indication of what crypto currency is most volatile. The")
    print("more volatile the crypto currency is, the more frequent buy and sell events")
    print("will occur, thus it is recommended for the purpose of experimentation to play")
    print("around with the most volatile currency]\n")
           
    header_columns = [f"{c.bcolors.HACKER_GREEN}Coin Rank", "Coin Name", "24Hr_Volume($)", "Volatility(%)"]

    data = [[1, coin_name[0], daily_volumes[0], volatilities[0]],
            [2, coin_name[1], daily_volumes[1], volatilities[1]],
            [3, coin_name[2], daily_volumes[2], volatilities[2]],
            [4, coin_name[3], daily_volumes[3], volatilities[3]],
            [5, coin_name[4], daily_volumes[4], volatilities[4]],
            [6, coin_name[5], daily_volumes[5], volatilities[5]],                  
            [7, coin_name[6], daily_volumes[6], volatilities[6]],                   
            [8, coin_name[7], daily_volumes[7], volatilities[7]],                   
            [9, coin_name[8], daily_volumes[8], volatilities[8]],                   
            [10, coin_name[9], daily_volumes[9], volatilities[9]],                      
            [11, coin_name[10], daily_volumes[10], volatilities[10]],                    
            [12, coin_name[11], daily_volumes[11], volatilities[11]],                     
            [13, coin_name[12], daily_volumes[12], volatilities[12]],                     
            [14, coin_name[13], daily_volumes[13], volatilities[13]],                     
            [15, coin_name[14], daily_volumes[14], volatilities[14]],                     
            [16, coin_name[15], daily_volumes[15], volatilities[15]],                     
            [17, coin_name[16], daily_volumes[16], volatilities[16]],                     
            [18, coin_name[17], daily_volumes[17], volatilities[17]],                     
            [19, coin_name[18], daily_volumes[18], volatilities[18]],                     
            [20, coin_name[19], daily_volumes[19], volatilities[19]],                     
            [21, coin_name[20], daily_volumes[20], volatilities[20]],                     
            [22, coin_name[21], daily_volumes[21], volatilities[21]],                     
            [23, coin_name[22], daily_volumes[22], volatilities[22]],                     
            [24, coin_name[23], daily_volumes[23], volatilities[23]],                     
            [25, coin_name[24], daily_volumes[24], volatilities[24]],                     
            [26, coin_name[25], daily_volumes[25], volatilities[25]],                     
            [27, coin_name[26], daily_volumes[26], volatilities[26]],                     
            [28, coin_name[27], daily_volumes[27], volatilities[27]],                     
            [29, coin_name[28], daily_volumes[28], volatilities[28]],                     
            [30, coin_name[29], daily_volumes[29], volatilities[29]],                     
            [31, coin_name[30], daily_volumes[30], volatilities[30]],                     
            [32, coin_name[31], daily_volumes[31], volatilities[31]],                    
            [33, coin_name[32], daily_volumes[32], volatilities[32]],                     
            [34, coin_name[33], daily_volumes[33], volatilities[33]],                     
            [35, coin_name[34], daily_volumes[34], volatilities[34]],                    
            [36, coin_name[35], daily_volumes[25], volatilities[35]],                     
            [37, coin_name[36], daily_volumes[36], volatilities[36]],                     
            [38, coin_name[37], daily_volumes[37], volatilities[37]],                    
            [39, coin_name[38], daily_volumes[38], volatilities[38]],                     
            [40, coin_name[39], daily_volumes[39], volatilities[39]],                     
            [41, coin_name[40], daily_volumes[40], volatilities[40]],                     
            [42, coin_name[41], daily_volumes[41], volatilities[41]],                     
            [43, coin_name[42], daily_volumes[42], volatilities[42]],                     
            [44, coin_name[43], daily_volumes[43], volatilities[43]],                     
            [45, coin_name[44], daily_volumes[44], volatilities[44]],                     
            [46, coin_name[45], daily_volumes[45], volatilities[45]],                     
            [47, coin_name[46], daily_volumes[46], volatilities[46]],                      
            [48, coin_name[47], daily_volumes[47], volatilities[47]],                      
            [49, coin_name[48], daily_volumes[48], volatilities[48]],                      
            [50, coin_name[49], daily_volumes[49], volatilities[49]],                      
            [51, coin_name[50],  daily_volumes[50], volatilities[50]],                     
            [52, coin_name[51],  daily_volumes[51], volatilities[51]],                      
            [53, coin_name[52],  daily_volumes[52], volatilities[52]],                     
            [54, coin_name[53],  daily_volumes[53], volatilities[53]],                      
            [55, coin_name[54],  daily_volumes[54], volatilities[54]],                      
            [56, coin_name[55],  daily_volumes[55], volatilities[55]],                      
            [57, coin_name[56],  daily_volumes[56], volatilities[56]],                      
            [58, coin_name[57],  daily_volumes[57], volatilities[57]],                      
            [59, coin_name[58],  daily_volumes[58], volatilities[58]],                      
            [60, coin_name[59],  daily_volumes[59], volatilities[59]],                     
            [61, coin_name[60],  daily_volumes[60], volatilities[60]],                      
            [62, coin_name[61],  daily_volumes[61], volatilities[61]],                      
            [63, coin_name[62],  daily_volumes[62], volatilities[62]],                      
            [64, coin_name[63],  daily_volumes[63], volatilities[63]],                      
            [65, coin_name[64],  daily_volumes[64], volatilities[64]],                      
            [66, coin_name[65],  daily_volumes[65], volatilities[65]],                      
            [67, coin_name[66],  daily_volumes[66], volatilities[66]],                      
            [68, coin_name[67],  daily_volumes[67], volatilities[67]],                      
            [69, coin_name[68],  daily_volumes[68], volatilities[68]],                      
            [70, coin_name[69],  daily_volumes[69], volatilities[69]],                      
            [71, coin_name[70],  daily_volumes[70], volatilities[70]],                      
            [72, coin_name[71],  daily_volumes[71], volatilities[71]],                      
            [73, coin_name[72],  daily_volumes[72], volatilities[72]],                      
            [74, coin_name[73],  daily_volumes[73], volatilities[73]],                      
            [75, coin_name[74],  daily_volumes[74], volatilities[74]],                      
            [76, coin_name[75],  daily_volumes[75], volatilities[75]],                      
            [77, coin_name[76],  daily_volumes[76], volatilities[76]],                      
            [78, coin_name[77],  daily_volumes[77], volatilities[77]],                      
            [79, coin_name[78],  daily_volumes[78], volatilities[78]],                
            [80, coin_name[79],  daily_volumes[79], volatilities[79]],                      
            [81, coin_name[80],  daily_volumes[80], volatilities[80]],                      
            [82, coin_name[81],  daily_volumes[81], volatilities[81]],                      
            [83, coin_name[82],  daily_volumes[82], volatilities[82]],                      
            [84, coin_name[83],  daily_volumes[83], volatilities[83]],                     
            [85, coin_name[84],  daily_volumes[84], volatilities[84]],                      
            [86, coin_name[85],  daily_volumes[85], volatilities[85]],                      
            [87, coin_name[86],  daily_volumes[86], volatilities[86]],                      
            [88, coin_name[87],  daily_volumes[87], volatilities[87]],                      
            [89, coin_name[88],  daily_volumes[88], volatilities[88]],                      
            [90, coin_name[89],  daily_volumes[89], volatilities[89]],                      
            [91, coin_name[90],  daily_volumes[90], volatilities[90]],                      
            [92, coin_name[91],  daily_volumes[91], volatilities[91]],                      
            [93, coin_name[92],  daily_volumes[92], volatilities[92]],                      
            [94, coin_name[93],  daily_volumes[93], volatilities[93]],                      
            [95, coin_name[94],  daily_volumes[94], volatilities[94]],                      
            [96, coin_name[95],  daily_volumes[95], volatilities[95]],                      
            [97, coin_name[96],  daily_volumes[96], volatilities[96]],                      
            [98, coin_name[97],  daily_volumes[97], volatilities[97]],                      
            [99, coin_name[98],  daily_volumes[98], volatilities[98]],                      
            [100, coin_name[99], daily_volumes[99], volatilities[99]]] 
    
    print(tabulate(data, header_columns))