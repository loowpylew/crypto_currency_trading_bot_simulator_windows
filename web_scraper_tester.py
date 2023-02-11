from unittest import skip
import requests 
from bs4 import BeautifulSoup

if __name__ == '__main__':
    URL = "https://www.shufflup.org/volatility_vol.php"
    page = requests.get(URL)                    

    soup = BeautifulSoup(page.content, 'html.parser') 
    #results = soup.find(id="exTab3")
    #print(results.prettify())

    #elems = results.find_all('table', class_='table table-striped table-bordered table-hover table-condensed') 

    #print(elems)

    count = 0
    count2 = 0
    coin_name = []
    daily_volumes = []
    volatilities = []
    rows = soup.find("table", class_='table table-striped table-bordered table-hover table-condensed').find("tbody").find_all("tr")
    for row in rows: 
        cells = row.find_all("td")
        if count == count2:
            coin_name.append(cells[1].get_text()[0:30]) # [1] - row 1. [0:29] - max length of crypto before  
                                                         # index borders over to next row
            daily_volumes.append(cells[2].get_text()[0:30]) #[2] - row 2. [0:30] - In case length of volume changes,
                                                            # outofbound index's have been called (does not produce error)
            volatilities.append(cells[3].get_text()[0:30]) # [3] - row3. [0:30] - Same applies here

        count += 1
        count2 += 1
    
    name_index = 0
    character_index = 10 # no crypto have numbers beyond 10 letters that make up the name of the crypto. 
    
    # This has been implemented as it is unknown how many characters make up the name of the crypto currency
    # given their volatility ranking will change overtime thus the index position with the table will change. 
    # Unfortunetly, this can lead us veering into the next column of the row, thus we will have unwanted numbers 
    # within the output under the coin name column. 
    # Subject to updates if volatility of crypto currencies that contain numbers within their namings make it
    # into the top 100. From the current state of the leaderboard, only '0x (ZRX)' is within the top 100, with
    # 'B2B (B2BX)' at 150 in the leaderboard so is unlikley to reach to 100 anytime soon. 

    for name in coin_name:
        for character in name:
            character_index += 1
            if character.isdigit(): 
                #print(name_index + ": " + coin_name[name_index] + " == " + character)
                #print(character)
                if "0x" in coin_name[name_index]:
                    skip
                else:
                    coin_name[name_index] = coin_name[name_index].replace(character, "")
        name_index += 1
    
    print(coin_name)
    #print(daily_volumes)
    #print(volatilities)
        
        


