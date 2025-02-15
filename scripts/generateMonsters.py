"""
    Script to generate a monsters.json of all the monsters on the OSRS Wiki, and downloads images for each of them.
    The JSON file is placed in ../src/lib/monsters.json

    The images are placed in ../cdn/monsters/. This directory is NOT included in the Next.js app bundle, and should
    be deployed separately to our file storage solution.

    Written for Python 3.9.
"""
import os.path

import requests
import json
import re

FILE_NAME = '../cdn/json/monsters.json'
WIKI_BASE = 'https://oldschool.runescape.wiki'
API_BASE = WIKI_BASE + '/api.php'
IMG_PATH = '../cdn/monsters/'

def getMonsterData():
    monsters = {}
    offset = 0
    while True:
        print('Fetching monster info: ' + str(offset))
        r = requests.get(API_BASE + '?action=ask&format=json&query=%5B%5BUses%20infobox%3A%3AMonster%5D%5D%20%7C%3FAttack%20bonus%20%7C%3FAttack%20level%20%7C%3FAttack%20speed%20%7C%3FAttack%20style%20%7C%3FCombat%20level%20%7C%3FCrush%20defence%20bonus%20%7C%3FDefence%20level%20%7C%3FHitpoints%20%7C%3FImage%20%7C%3FImmune%20to%20poison%20%7C%3FImmune%20to%20venom%20%7C%3FMagic%20Damage%20bonus%20%7C%3FMagic%20attack%20bonus%20%7C%3FMagic%20defence%20bonus%20%7C%3FMagic%20level%20%7C%3FMax%20hit%20%7C%3FMonster%20attribute%20%7C%3FNPC%20ID%20%7C%3FName%20%7C%3FRange%20attack%20bonus%20%7C%3FRanged%20Strength%20bonus%20%7C%3FRange%20defence%20bonus%20%7C%3FRanged%20level%20%7C%3FSlash%20defence%20bonus%20%7C%3FSlayer%20category%20%7C%3FSlayer%20experience%20%7C%3FStab%20defence%20bonus%20%7C%3FStrength%20bonus%20%7C%3FStrength%20level%20%7C%3FSize%20%7C%3FVersion anchor%20%7C%3FNPC%20ID%20%7C%3FImage%7Climit%3D500%7Coffset%3D' + str(offset), headers={
            'User-Agent': 'osrs-dps-calc (https://github.com/weirdgloop/osrs-dps-calc)'
        })
        data = r.json()

        if 'query' not in data or 'results' not in data['query']:
            # No results?
            break

        monsters = monsters | data['query']['results']

        if 'query-continue-offset' not in data or int(data['query-continue-offset']) < offset:
            # If we are at the end of the results, break out of this loop
            break
        else:
            offset = data['query-continue-offset']
    return monsters

def getPrintoutValue(prop):
    # SMW printouts are all arrays, so ensure that the array is not empty
    if not prop:
        return None
    else:
        return prop[0]

def main():
    # Grab the monster info using SMW, including all the relevant printouts
    wiki_data = getMonsterData()

    # Convert the data into our own JSON structure
    data = []
    required_imgs = []

    # Loop over the monsters data from the wiki
    for k, v in wiki_data.items():
        print('Processing ' + k)

        # Sanity check: make sure that this monster has printouts from SMW
        if 'printouts' not in v:
            print(k + ' is missing SMW printouts - skipping.')
            continue

        po = v['printouts']
        version = getPrintoutValue(po['Version anchor']) or ''

        # If this is a CoX monster Challenge Mode variant, remove it. This will be handled by the calculator UI.
        if 'Challenge Mode' in version:
            print(k + ' is a CoX CM variant - skipping.')
            continue

        # Skip monsters that aren't in the main namespace on the wiki
        if re.match("^([A-z]*):", k):
            continue

        monster = {
            'id': getPrintoutValue(po['NPC ID']),
            'name': k.rsplit('#', 1)[0] or '',
            'version': version,
            'image': '' if not po['Image'] else po['Image'][0]['fulltext'].replace('File:', ''),
            'level': getPrintoutValue(po['Combat level']) or 0,
            'speed': getPrintoutValue(po['Attack speed']) or 0,
            'size': getPrintoutValue(po['Size']) or 0,
            'skills': [
                getPrintoutValue(po['Attack level']) or 0,
                getPrintoutValue(po['Defence level']) or 0,
                getPrintoutValue(po['Hitpoints']) or 0,
                getPrintoutValue(po['Magic level']) or 0,
                getPrintoutValue(po['Ranged level']) or 0,
                getPrintoutValue(po['Strength level']) or 0
            ],
            'offensive': [
                getPrintoutValue(po['Attack bonus']) or 0,
                getPrintoutValue(po['Magic Damage bonus']) or 0,
                getPrintoutValue(po['Magic attack bonus']) or 0,
                getPrintoutValue(po['Range attack bonus']) or 0,
                getPrintoutValue(po['Ranged Strength bonus']) or 0,
                getPrintoutValue(po['Strength bonus']) or 0
            ],
            'defensive': [
                getPrintoutValue(po['Crush defence bonus']) or 0,
                getPrintoutValue(po['Magic defence bonus']) or 0,
                getPrintoutValue(po['Range defence bonus']) or 0,
                getPrintoutValue(po['Slash defence bonus']) or 0,
                getPrintoutValue(po['Stab defence bonus']) or 0
            ],
            'attributes': po['Monster attribute'] or []
        }

        # Skip monsters that don't have an ID
        if monster['id'] is None:
            continue

        data.append(monster)
        if not monster['image'] == '':
            required_imgs.append(monster['image'])

    print('Total monsters: ' + str(len(data)))

    # Save the JSON
    with open(FILE_NAME, 'w') as f:
        print('Saving to JSON at file: ' + FILE_NAME)
        json.dump(data, f, ensure_ascii=False, indent=2)

    success_img_dls = 0
    failed_img_dls = 0
    skipped_img_dls = 0
    required_imgs = set(required_imgs)

    # Fetch all the images from the wiki and store them for local serving
    for idx, img in enumerate(required_imgs):
        if os.path.isfile(IMG_PATH + img):
            skipped_img_dls += 1
            continue

        print(f'({idx}/{len(required_imgs)}) Fetching image: {img}')
        r = requests.get(WIKI_BASE + '/w/Special:Filepath/' + img, headers={
            'User-Agent': 'osrs-dps-calc (https://github.com/weirdgloop/osrs-dps-calc)'
        })
        if r.status_code == 200:
            with open(IMG_PATH + img, 'wb') as f:
                f.write(r.content)
                print('Saved image: ' + img)
                success_img_dls += 1
        else:
            print('Unable to save image: ' + img)
            failed_img_dls += 1

    print('Total images saved: ' + str(success_img_dls))
    print('Total images skipped (already exists): ' + str(skipped_img_dls))
    print('Total images failed to save: ' + str(failed_img_dls))


main()
