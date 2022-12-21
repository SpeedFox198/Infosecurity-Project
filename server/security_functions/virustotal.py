# scanning for hashes
import aiohttp
import asyncio
import urllib.parse



API_KEY = 'ffe160af23a4fcb04ad18810d61be03b0bd0d7474dfc851dd986f1b41a4fe847'

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# step 1 uplaod file to vt api
async def upload_file(file):
    url = "https://www.virustotal.com/api/v3/files"

    files = {"file": open(file, "rb")}

    async with aiohttp.ClientSession() as session:
        async with session.post(url,
        data = files,
        headers = {
            "accept": "application/json",
            "x-apikey": API_KEY
            }, 
        ) as response:
                data = await response.json()
                file_id = data['data']['id']
                return file_id

# step 2 get analysis
async def get_file_analysis(file_id: str) -> str:
    url = "https://www.virustotal.com/api/v3/analyses/{}".format(file_id)

    async with aiohttp.ClientSession() as session:
        async with session.get(url,
        headers = {
        "accept": "application/json",
        "x-apikey": API_KEY
        }) as response:
            data = await response.json()
            file_hash = data['meta']['file_info']['md5']
            return file_hash

async def scan_file_hash(file_hash: str) -> str:
    
    url = "https://www.virustotal.com/api/v3/files/{}".format(file_hash)

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers = {
        "accept": "application/json",
        "x-apikey": API_KEY
        }) as response:
            data = await response.json()
            score = data['data']['attributes']['last_analysis_stats']['malicious']
            return score


#step 1 send url to vt
async def upload_url(sent_url: str) -> str:
    url = "https://www.virustotal.com/api/v3/urls"

    payload = urllib.parse.urlencode({"url":sent_url})

    async with aiohttp.ClientSession() as session:
        async with session.post(url,
        data = payload,
        headers = {
            "accept": "application/json",
            "x-apikey": API_KEY,
            "content-type": "application/x-www-form-urlencoded"
            },
        ) as response:
            data = await response.json()
            data_id = data['data']['id']
            return data_id

# step 2 get analysis
async def get_url_analysis(data_id: str) -> str:
    url = "https://www.virustotal.com/api/v3/analyses/{}".format(data_id)

    async with aiohttp.ClientSession() as session:
        async with session.get(url,
        headers = {
        "accept": "application/json",
        "x-apikey": API_KEY
        }) as response:
            data = await response.json()
            url_id = data['meta']['url_info']['id']
            return url_id

# step 3 get url report
async def get_url_report(url_id: str) -> str:
    url = "https://www.virustotal.com/api/v3/urls/{}".format(url_id)

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers = {
        "accept": "application/json",
        "x-apikey": API_KEY
        }) as response:
            data = await response.json()
            score = data['data']['attributes']['last_analysis_stats']['malicious']
            return score


# Test using malicous file
print("Test 1: ")
# score = asyncio.run(scan_file_hash('15e029c3834435150c76741e714540fcb799662db8cc2c61ba4ef192a781727b'))
# if score > 0:
#     print("Malicious file detected!")
# else:
#     print("File is safe!")

# # Test using safe file
# print("Test 2: ")
# file_id = asyncio.run(upload_file(r".\server\security_functions\safe_file_2.txt"))
# print("file id is = " + file_id)
# file_hash = asyncio.run(get_file_analysis(file_id))
# print("file hash = " + file_hash)
# score = asyncio.run(scan_file_hash(file_hash))

# if score > 0:
#     print("Malicious file detected!")
# else:
#     print("File is safe!")


# # Test using malicous url
# print("Test 3: ")
# data_id = asyncio.run(upload_url('http://www.csm-testcenter.org/download/malicious/index.html'))
# url_id = asyncio.run(get_url_analysis(data_id))
# score = asyncio.run(get_url_report(url_id))
# if score > 0:
#     print("Malicious url detected!")
# else:
#     print("Url is safe!")

# # Test using safe url
# print("Test 4: ")
# data_id = asyncio.run(upload_url('https://www.youtube.com'))
# url_id = asyncio.run(get_url_analysis(data_id))
# score = asyncio.run(get_url_report(url_id))
# if score > 0:
#     print("Malicious url detected!")
# else:
#     print("Url is safe!")