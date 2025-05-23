import time
import requests
import random
import string
from bs4 import BeautifulSoup
import re
import threading
from flask import *
import json
app = Flask(__name__)
@app.route("/vf",methods=["GET"]) 


def usage(nu, pw, rp):

    def get_auth_token(nu, pw):
        url = "https://web.vodafone.com.eg/auth/realms/vf-realm/protocol/openid-connect/token"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Connection": "keep-alive",
            "x-agent-operatingsystem": "R.18d8015-3fd3e-3fd3d",
            "clientId": "xxx",
            "x-agent-device": "OP4F11L1",
            "x-agent-version": "2024.10.1",
            "x-agent-build": "562",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "web.vodafone.com.eg",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/4.9.3"
        }
        data = {
            "username": nu,
            "password": pw,
            "grant_type": "password",
            "client_secret": "a2ec6fff-0b7f-4aa4-a733-96ceae5c84c3",
            "client_id": "my-vodafone-app"
        }
        r3 = requests.post(url, headers=headers, data=data)
        return r3.json().get('access_token')

    token = get_auth_token(nu, pw)

    if not token:
        print(f"فشل المصادقة للرقم {nu}")
        return

    url2 = f'https://mobile.vodafone.com.eg/services/dxl/usage/usageConsumptionReport?%40type=aggregated&bucket.product.publicIdentifier={nu}'
    headers1 = {
        "Host": "mobile.vodafone.com.eg",
        "x-dynatrace": "MT_3_13_1032261809_72-0_a556db1b-4506-43f3-854a-1d2527767923_161_82730_459",
        "Authorization": f"Bearer {token}",
        "api-version": "v2",
        "x-agent-operatingsystem": "11",
        "clientId": "AnaVodafoneAndroid",
        "x-agent-device": "Xiaomi M2010J19SG",
        "x-agent-version": "2024.7.2.1",
        "x-agent-build": "612",
        "msisdn": nu,
        "Accept": "application/json",
        "Accept-Language": "ar",
        "Content-Type": "application/json; charset=UTF-8",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/4.11.0",
    }

    try:
        r2 = requests.get(url2, headers=headers1)
        text = r2.text
        amounts = re.findall(r'"amount":\s*(-?\d+\.?\d*)', text)
        amount = list(map(float, amounts))
        # print(amount)
        mg = amount[rp]

        mgb = f"==>>  Total mb for ( {nu} ) :  {mg}"
        # print(mgb)

        total = 1000
        if mg < total:
            url2 = f'https://mobile.vodafone.com.eg/services/dxl/pim/product?relatedParty.id={nu}&place.%40referredType=Local&%40type=MIProfile'
            headers3 = {
                "Host": "mobile.vodafone.com.eg",
                "x-dynatrace": "MT_3_24_1032261809_65-0_a556db1b-4506-43f3-854a-1d2527767923_0_77471_445",
                "Authorization": f"Bearer {token}",
                "api-version": "v2",
                "x-agent-operatingsystem": "11",
                "clientId": "AnaVodafoneAndroid",
                "x-agent-device": "Xiaomi M2010J19SG",
                "x-agent-version": "2024.7.2.1",
                "x-agent-build": "612",
                "msisdn": nu,
                "Accept": "application/json",
                "Accept-Language": "ar",
                "Content-Type": "application/json; charset=UTF-8",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/4.11.0",
            }
            r2 = requests.get(url2, headers=headers3)
            data = r2.text
            pattern = r'"productOffering":\s*{\s*"id":\s*"MI_BASIC_SUPER_20"[^}]*"encProductId":\s*"([^"]+)"'
            match = re.search(pattern, data)

            if match:
                id = match.group(1)

                url3 = "https://mobile.vodafone.com.eg/services/dxl/pom/productOrder"
                headers2 = {
                    "Host": "mobile.vodafone.com.eg",
                    "x-dynatrace": "MT_3_24_1032261809_65-0_a556db1b-4506-43f3-854a-1d2527767923_0_77471_445",
                    "Authorization": f"Bearer {token}",
                    "api-version": "v2",
                    "x-agent-operatingsystem": "11",
                    "clientId": "AnaVodafoneAndroid",
                    "x-agent-device": "Xiaomi M2010J19SG",
                    "x-agent-version": "2024.7.2.1",
                    "x-agent-build": "612",
                    "msisdn": nu,
                    "Accept": "application/json",
                    "Accept-Language": "ar",
                    "Content-Type": "application/json; charset=UTF-8",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/4.11.0",
                }

                json_data = {
                    "channel": {
                        "name": "MobileApp"
                    },
                    "characteristic": [],
                    "orderItem": [
                        {
                            "action": "add",
                            "product": {
                                "characteristic": [
                                    {
                                        "name": "LangId",
                                        "value": "ar"
                                    },
                                    {
                                        "name": "ExecutionType",
                                        "value": "Sync"
                                    },
                                    {
                                        "name": "DropAddons",
                                        "value": "False"
                                    },
                                    {
                                        "name": "MigrationType",
                                        "value": "Repurchase"
                                    },
                                    {
                                        "name": "OneStepMigrationFlag",
                                        "value": "Y"
                                    },
                                    {
                                        "name": "Journey",
                                        "value": "MI_HomePage"
                                    }
                                ],
                                "encProductId": id,
                                "id": "MI_BASIC_SUPER_20",
                                "relatedParty": [
                                    {
                                        "id": nu,
                                        "name": "MSISDN",
                                        "role": "Subscriber"
                                    }
                                ],
                                "@type": "MI"
                            }
                        }
                    ],
                    "@type": "MIProfile"
                }

                r3 = requests.post(url3, headers=headers2, json=json_data).json()
                #  print(r3)
                if r3 == {"code": "2252", "reason": "Insufficient balance"}:
                    print(f"تم تجديد 1100 ميجا للرقم {nu} ==={mg}")
                else:

                    print(f"خطأ في الرقم {nu}: {r3.status_code}")
            else:
                print(f"لا يوجد encProductId كافي للرقم {nu}")
        else:

            print(f"{mg} البيانات كافية للرقم {nu} لا حاجه للتجديد")
    except Exception as e:
        print(f"حدث خطأ أثناء معالجة الرقم {nu}: {str(e)}")


credentials = [
    {"id": 1, "number": "01050254700", "password": "Zxcvbnm111#", "we": 1, "rp": 3},#gamal
    {"id": 34, "number": "01016291013", "password": "P@@@1wrd", "we": 0, "rp": 3},#ssabry
    #{"id": 2, "number": "01025007787", "password": "Qwerty@123", "we": 1, "rp": 5},
    {"id": 3, "number": "01050604197", "password": "Wegz@123", "we": 2, "rp": 3},
    #{"id": 10, "number": "01070741259", "password": "AliPro2025@", "we": 1, "rp": 3},
    #{"id": 11, "number": "01080818088", "password": "AcAcAc123@@", "we": 1, "rp": 3},
    {"id": 12, "number": "01061309619", "password": "Ahmed@123", "we": 1, "rp": 5},
    #{"id": 13, "number": "01020051185", "password": "Qwerty@123", "we": 1, "rp": 3},
    {"id": 14, "number": "01028802929", "password": "Qwerty@123", "we": 2, "rp": 3},
    #{"id": 15, "number": "01000012068", "password": "Eslam@123", "we": 1, "rp": 3},
    {"id": 17, "number": "01020052242", "password": "Eslam@123", "we": 2, "rp": 5},#اسلام بدوى
    {"id":  5, "number": "01040809466", "password": "TAREk6ABo%91", "we": 2, "rp": 3}, #boika
    {"id": 18, "number": "01005595908", "password": "Tahamay@21", "we": 1, "rp": 3},#boika
    #{"id": 19, "number": "01098360011", "password": "Ahmed010#", "we": 1, "rp": 3},#boika
    {"id": 20, "number": "01000982996", "password": "Mo7amed@123", "we": 2, "rp": 3},#boika
    {"id": 21, "number": "01000853265", "password": "Ahmed011#", "we": 1, "rp": 3},#boika
    {"id": 22, "number": "01005595908", "password": "Tahamay@21", "we": 2, "rp": 3},#boika
    {"id": 24, "number": "01050177499", "password": "Ahmed010#", "we": 1, "rp": 3},#boika
    {"id": 25, "number": "01011006746", "password": "Marey99@gmail.com", "we": 1, "rp": 3},#boika
    {"id": 26, "number": "01019511903", "password": "Wegz@123", "we": 1, "rp": 3}#eman rageb

]



def worker(cred):        
        try:
            usage(cred["number"], cred["password"], cred["rp"])

        except Exception as e:
            print(f"حدث خطأ غير متوقع للرقم {cred['number']}: {str(e)}")
        finally:
            time.sleep(1)


# عرض القائمة
print("القائمة المتاحة:")
for cred in credentials:
    print(f"ID: {cred['id']} - الرقم: {cred['number']} -rp:{cred['rp']}")

selected_ids = input("أدخل الـ IDs المراد تشغيلها (مفصولة بفاصلة أو 'all'): ").strip()

if selected_ids.lower() == 'all':
    selected_credentials = credentials
else:
    try:
        selected_ids = list(map(int, selected_ids.split(',')))
        selected_credentials = [cred for cred in credentials if cred['id'] in selected_ids]
    except:
        print("إدخال غير صحيح!")
        exit()

# بدء التشغيل

for i in range(1):
   for cred in selected_credentials:
         threading.Thread(target=worker, args=(cred,)).start()