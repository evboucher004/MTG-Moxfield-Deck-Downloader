import requests
import json
from PIL import Image
import os
from pathlib import Path

def deckdl():

    class Deck:
        commander: str
        successCount: int
        successTokenCount: int


    count = 0
    tokenCount = 0

    successfulcards = 0
    successfulTokenCount = 0

    doubleCards = 0
    badCards = 0

    CardLines = []
    CommanderLine = []
    TokenCardLines = []

    commanderName = ""

    DeckCards = []
    Commander = []
    CommanderDoubleCard = []
    DeckDoubleCards = []
    TokenCards = []
    TokenDoubleCards = []

    FailedCards = []

    Path("images/commander/").mkdir(parents=True, exist_ok=True)
    Path("images/backs/").mkdir(parents=True, exist_ok=True)
    Path("images/tokens/").mkdir(parents=True, exist_ok=True)
    Path("images/cards/").mkdir(parents=True, exist_ok=True)

    with open("../DeckDL/deckInfo.json", encoding="utf-8") as file:
        fileContents = json.load(file)

    with open(r"../DeckDL/deckInfo.json", 'r', encoding="utf-8") as fp:
        for l_no, line in enumerate(fp):
            if '"boardType": "mainboard"' in line:
                count = count + 1
                CardLines.append(l_no)
            elif '"boardType": "commanders"' in line:
                CommanderLine.append(l_no)
            elif '"layout": "token"' in line:
                tokenCount = tokenCount + 1
                TokenCardLines.append(l_no)
            elif '"layout": "double_faced_token"' in line:
                tokenCount = tokenCount + 1
                TokenCardLines.append(l_no)

    # Gets card info
    for k in CardLines:
        with open(r"../DeckDL/deckInfo.txt", 'r', encoding="utf-8") as fp:
            name = ""

            for i, line in enumerate(fp):

                if i == k+11:
                    name = line[17:-3]

                if "//" not in name and name != "":
                    DeckCards.append(name)
                    break

                if "//" in name:
                    DeckDoubleCards.append(name)
                    break

    # Gets commander info
    for k in CommanderLine:
        with open(r"../DeckDL/deckInfo.txt", 'r', encoding="utf-8") as fp:
            name = ""

            for i, line in enumerate(fp):

                if i == k+11:
                    name = line[17:-3]

                if "//" not in name and name != "":
                    commanderName = name
                    Commander.append(name)
                    break

                if "//" in name:
                    CommanderDoubleCard.append(name)
                    break

    # Downloads normal cards
    for name in DeckCards:
        id = fileContents['mainboard'][name]['card']['id']
        quantity = fileContents['mainboard'][name]['quantity']

        url = "https://assets.moxfield.net/cards/card-" + id + "-normal.webp"

        name2 = name.replace('//', '')
        name2 = name2.replace('/', '')
        name2 = name2.replace(':', '')


        if quantity > 1:
            for i in range(quantity):
                img_data = requests.get(url).content
                path = 'images/cards/' + name2 + ' ' + str(i)
                with open(path + '.webp', 'wb') as webp:
                    webp.write(img_data)

                im = Image.open(path + '.webp').convert("RGB")
                im.save(path + ".jpg", "jpeg")
                os.remove(path + '.webp')
                successfulcards += 1
        else:
            img_data = requests.get(url).content
            path = 'images/cards/' + name2
            with open(path + '.webp', 'wb') as webp:
                webp.write(img_data)

            im = Image.open(path + '.webp').convert("RGB")
            im.save(path + ".jpg", "jpeg")
            os.remove(path + '.webp')
            successfulcards += 1

    # Downloads double sided cards
    for name in DeckDoubleCards:

        url = "https://assets.moxfield.net/cards/card-face-" + fileContents['mainboard'][name]['card']['card_faces'][0]['id'] + "-normal.webp"

        name2 = name.replace('//', '-')
        name2 = name2.replace('/', '')
        name2 = name2.replace(':', '')

        img_data = requests.get(url).content
        path = 'images/cards/' + name2 + ' - front'
        with open(path + '.webp', 'wb') as webp:
            webp.write(img_data)

        im = Image.open(path + '.webp').convert("RGB")
        im.save(path + ".jpg", "jpeg")

        os.remove(path + '.webp')

        url = "https://assets.moxfield.net/cards/card-face-" + fileContents['mainboard'][name]['card']['card_faces'][1][
            'id'] + "-normal.webp"

        name2 = name.replace('//', '-')
        name2 = name2.replace('/', '')
        name2 = name2.replace(':', '')

        img_data = requests.get(url).content
        path = 'images/backs/' + name2 + ' - back'
        with open(path + '.webp', 'wb') as webp:
            webp.write(img_data)

        im = Image.open(path + '.webp').convert("RGB")
        im.save(path + ".jpg", "jpeg")
        successfulcards += 1

    # Downloads tokens
    for i in range(len(fileContents['tokens'])):

        if fileContents['tokens'][i]['layout'] == 'token' or fileContents['tokens'][i]['layout'] == 'double_faced_token':

            name = fileContents['tokens'][i]['name']

            if "//" in name:
                url = "https://assets.moxfield.net/cards/card-face-" + fileContents['tokens'][i]['card_faces'][0]['id'] + "-normal.webp"

                name2 = name.replace('//', '-')
                name2 = name2.replace('/', '')
                name2 = name2.replace(':', '')

                img_data = requests.get(url).content
                path = 'images/tokens/' + name2 + ' - front'
                with open(path + '.webp', 'wb') as webp:
                    webp.write(img_data)

                im = Image.open(path + '.webp').convert("RGB")
                im.save(path + ".jpg", "jpeg")

                os.remove(path + '.webp')

                url = "https://assets.moxfield.net/cards/card-face-" + fileContents['tokens'][i]['card_faces'][1]['id'] + "-normal.webp"

                img_data = requests.get(url).content
                path = 'images/backs/' + name2 + ' - back'
                with open(path + '.webp', 'wb') as webp:
                    webp.write(img_data)

                im = Image.open(path + '.webp').convert("RGB")
                im.save(path + ".jpg", "jpeg")

                os.remove(path + '.webp')
                successfulTokenCount += 1

            else:
                url = "https://assets.moxfield.net/cards/card-" + fileContents['tokens'][i]['id'] + "-normal.webp"

                name2 = name.replace('//', '')
                name2 = name2.replace('/', '')
                name2 = name2.replace(':', '')

                img_data = requests.get(url).content
                path = 'images/tokens/' + name2
                with open(path + '.webp', 'wb') as webp:
                    webp.write(img_data)

                im = Image.open(path + '.webp').convert("RGB")
                im.save(path + ".jpg", "jpeg")

                os.remove(path + '.webp')
                successfulTokenCount += 1

    # Downloads commander
    for name in Commander:
        id = fileContents['commanders'][name]['card']['id']

        url = "https://assets.moxfield.net/cards/card-" + id + "-normal.webp"

        name = name.replace('//', '')
        name = name.replace('/', '')
        name = name.replace(':', '')

        img_data = requests.get(url).content
        path = 'images/commander/' + name
        with open(path + '.webp', 'wb') as webp:
            webp.write(img_data)
            # successfulTokens = successfulTokens + 1

        im = Image.open(path + '.webp').convert("RGB")
        im.save(path + ".jpg", "jpeg")

        os.remove(path + '.webp')


    Deck.successCount = successfulcards
    Deck.successTokenCount = successfulTokenCount
    Deck.commander = commanderName

    return Deck