# scanning for hashes
import aiohttp
import asyncio


API_key = 'ffe160af23a4fcb04ad18810d61be03b0bd0d7474dfc851dd986f1b41a4fe847'

# step 1 uplaod file to vt api
async def upload_file(file):
    url = "https://www.virustotal.com/api/v3/files"

    files = {"file": open(file, "rb")}

    async with aiohttp.ClientSession() as session:
        async with session.post(url,
        data = files,
        headers = {
            "accept": "application/json",
            "x-apikey": "ffe160af23a4fcb04ad18810d61be03b0bd0d7474dfc851dd986f1b41a4fe847"
            }, 
        ) as response:
                data = await response.json()
                file_id = data['data']['id']
                return file_id

# step 2 get analysis
async def get_analysis(file_id: str) -> str:
    url = "https://www.virustotal.com/api/v3/analyses/{}".format(file_id)

    async with aiohttp.ClientSession() as session:
        async with session.get(url,
        headers = {
        "accept": "application/json",
        "x-apikey": "ffe160af23a4fcb04ad18810d61be03b0bd0d7474dfc851dd986f1b41a4fe847"
        }) as response:
            data = await response.json()
            file_hash = data['meta']['file_info']['md5']
            return file_hash

async def scan_file_hash(file_hash: str) -> str:
    
    url = "https://www.virustotal.com/api/v3/files/{}".format(file_hash)

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers = {
        "accept": "application/json",
        "x-apikey": "ffe160af23a4fcb04ad18810d61be03b0bd0d7474dfc851dd986f1b41a4fe847"
        }) as response:
            data = await response.json()
            score = data['data']['attributes']['last_analysis_stats']['malicious']
            return score

# Test using malicous file
print("Test 1: ")
score = asyncio.run(scan_file_hash('15e029c3834435150c76741e714540fcb799662db8cc2c61ba4ef192a781727b'))
if score > 0:
    print("Malicious file detected!")
else:
    print("File is safe!")

# Test using safe file
print("Test 2: ")
file_id = asyncio.run(upload_file("safe_file.txt"))
print("file is is = " + file_id)
file_hash = asyncio.run(get_analysis(file_id))
print("file hash = " + file_hash)
score = asyncio.run(scan_file_hash(file_hash))

if score > 0:
    print("Malicious file detected!")
else:
    print("File is safe!")