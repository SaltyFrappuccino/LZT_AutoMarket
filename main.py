from datetime import datetime
from random import randrange
from time import sleep

import requests

uri = "https://api.lolz.guru/market"
token = input("Введите ваш токен, получить можно тут ---> "
              "https://api.lolz.guru/oauth/authorize?response_type=token&client_id=0sga4tlyfi&scope=read+post+market"
              " <--- \n")

# token = "4321448bd0f8ee3bc88be1a1ac092e3d234b607a"

current_ids = []


def getAccounts():
    resp = requests.get(uri + "/user/5749627/items", headers={
        "Authorization": "Bearer " + token
    })

    if resp.status_code == 200:
        return resp.json()['items']
    elif resp.status_code == 429:
        print("Too many connections, retry")
    else:
        print("Connection error, retry")
        return "error"


def bump(item_id):
    resp = requests.post(uri + "/" + str(item_id) + "/bump", headers={
        "Authorization": "Bearer " + token
    })

    print(resp.json())

    if resp.status_code == 200:
        return resp
    else:
        print("Bumping error")
        return "error"

def unstick(item_id):
    resp = requests.delete(uri + "/" + str(item_id) + "/stick", headers={
        "Authorization": "Bearer " + token
    })

    print(resp.json())

    if resp.status_code == 200:
        return resp
    elif resp.json()['errors']:
        return "error"
    else:
        return "error"

def stick(item_id):
    resp = requests.post(uri + "/" + str(item_id) + "/stick", headers={
        "Authorization": "Bearer " + token
    })

    print(resp.json())

    if resp.status_code == 200:
        return resp
    elif resp.json()['errors']:
        return "error"
    else:
        return "error"


def start():
    while True:

        sleep(8)

        accounts = getAccounts()

        sleep(8)

        if accounts == "error":
            sleep(8)
            start()

        lenght = len(accounts)

        sticked = 0

        for i in range(5):
            randInt = randrange(0, len(accounts))
            try:
                if accounts[randInt]['bumpSettings']['canBumpItem']:
                    sleep(8)
                    bump(accounts[randInt]['item_id'])
                    print(str(datetime.now().time().replace(microsecond=0)) + " bumped account - " + str(accounts[i]['item_id']))
                    sleep(8)
                elif not accounts[randInt]['bumpSettings']['canBumpItem']:
                    sleep(8)
                    print(str(datetime.now().time().replace(microsecond=0)) + " Unable to bump account " + str(accounts[randInt]['item_id']) + " need to wait until " + str(
                        datetime.utcfromtimestamp(
                            bump(accounts[randInt]['item_id']).json()['system_info']['time']).strftime(
                            '%Y-%m-%d %H:%M:%S')))
            except Exception as e:
                print(e)

        sleep(500)

        unsticked = 0

        for i in range(lenght):
            try:
                if accounts[i]['is_sticky'] == 1:
                    sleep(5)
                    result = unstick(accounts[i]['item_id'])
                    if result == "error":
                        print(str(datetime.now().time().replace(microsecond=0)) + " Unable to unstick account " + str(accounts[i]['item_id']))
                        break
                    unsticked = unsticked + 1
                    print(str(datetime.now().time().replace(microsecond=0)) + " unsticked account - " + str(accounts[i]['item_id']))
                    sleep(5)
                if unsticked > 3:
                    unsticked = 0
                    break
            except Exception as e:
                print(e)

                sleep(8)

                accounts = getAccounts()

                sleep(8)

        sticked = 0

        for i in range(lenght):
            try:
                if accounts[i]['is_sticky'] == 0:
                    sleep(5)
                    result = stick(accounts[i]['item_id'])
                    if result == "error":
                        print(str(datetime.now().time().replace(microsecond=0)) + " Unable to stick account " + str(accounts[i]['item_id']))
                        break
                    sticked = sticked + 1
                    print(str(str(datetime.now().time().replace(microsecond=0)) + " sticked account - " + str(accounts[i]['item_id'])))
                    sleep(5)
                if sticked >= 3:
                    sticked = 0
                    break
            except Exception as e:
                print(e)

        print("Cycled \n")


start()

# def getAllAccounts(token):
#     resp = requests.get(uri + "/user/3842818/items", headers={
#         "Authorization": "Bearer " + token
#     })
#
#     return resp.json()['items']
#
#
# # def lastThreeID():
# #
# #     accounts = getAllAccounts(token)
# #
# #     accounts_id = []
# #
# #     for i in range(3):
# #         accounts_id.append(accounts[i]['item_id'])
# #
# #     return accounts_id
#
#
# def pinLastAccs():
#     accounts = getAllAccounts(token)
#     for i in range(3):
#         if accounts[i]['is_sticky'] == 0:
#             resp = requests.post(uri + "/market/" + str(accounts[i]['item_id']) + "/stick", headers={
#                 "Authorization": "Bearer " + token
#             })
#             print(resp.text)
#         sleep(10)
#
#
# def bumpRandomAccs():
#     accounts = getAllAccounts(token)
#
#     for i in range(len(accounts)):
#         randInt = randrange(0, len(accounts))
#         resp = requests.post(uri + "/market/" + str(accounts[randInt]['item_id']) + "bump", headers={
#             "Authorization": "Bearer " + token
#         })
#         print(resp.json()['message'] + "\n")
#
#
# # def start():
# #     while True:
#
# def start():
#     while True:
#         sleep(30)
#         pinLastAccs()
#         sleep(30)
#         bumpRandomAccs()
#         print("Cycled")
#
#
# start()
