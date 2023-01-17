<script>
import GDrive, { service } from "../google/GDrive.svelte";
import { e2ee } from "./e2ee";
import { masterKey, roomKeys } from "$lib/stores/key";
import { onMount } from "svelte";

const MASTER_KEY_FILE_NAME = "master_key.json";
const ROOM_KEYS_FILE_NAME = "room_keys.json";


/**
 * Initialise keys from localStorage if possible,
 * else download keys from google drive.
 */
async function initKeys() {
  let file;

  // If masterKey failed to init from localStorage, download from google drive
  if (masterKey.init()) {
    file = await service.downloadFile(MASTER_KEY_FILE_NAME, true);

    if (file !== undefined) {
      masterKey.initFromJson(file.body);
    } else {
      // Create new keys
      const newMasterKey = generateNewMasterKey();  // Work on the naming lmao
      // upload file to gdrive
      service.uploadJSONFile(MASTER_KEY_FILE_NAME, newMasterKey);

      // Save keys to stores and localStorage
      masterKey.saveMasterKey(newMasterKey);
    }
  }
  // init roomKeys
  if (roomKeys.init()) {
    file = await service.downloadFile(ROOM_KEYS_FILE_NAME);
    if (file !== undefined) {
      roomKeys.initFromJson(file.body);
    } else {
      // upload file to gdrive (??? shld i really do this?)
      service.uploadJSONFile(ROOM_KEYS_FILE_NAME, {});
      roomKeys.initFromJson("{}");
    }
  }
}


async function getNewMasterKey() {
  const newMasterKey = await e2ee.generateKeyPair();
  console.log(newMasterKey);
}

onMount(getNewMasterKey);
</script>


<GDrive/>
