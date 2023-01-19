<script>
// TODO(mid)(SpeedFox198): change ../google/ to $lib/google/
import GDrive, { service } from "../google/GDrive.svelte";
import { masterKey, roomKeys } from "$lib/stores/key";
import { e2ee } from "./e2ee";

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
    file = await service.downloadFile(MASTER_KEY_FILE_NAME);

    // Init masterKey from downloaded file, else create new masterKey
    if (file !== undefined) {
      masterKey.initFromJson(file.body, true);
    } else {
      // Create new keys
      const newMasterKey = getNewMasterKey();

      // Upload masterKey file to gdrive
      service.uploadJSONFile(MASTER_KEY_FILE_NAME, newMasterKey);

      // Save masterKey to stores and localStorage
      masterKey.saveMasterKey(newMasterKey);
    }
  }

  // If roomKeys failed to init from localStorage, download from google drive
  if (roomKeys.init()) {
    file = await service.downloadFile(ROOM_KEYS_FILE_NAME);

    // Init roomKeys from downloaded file, else create new empty object
    if (file !== undefined) {
      roomKeys.initFromJson(file.body, true);
    } else {
      // Upload roomKeys file to gdrive
      service.uploadJSONFile(ROOM_KEYS_FILE_NAME, {});

      // Save roomKeys to stores and localStorage
      roomKeys.initFromJson("{}", true);
    }
  }
}


async function getNewMasterKey() {
  const key = await e2ee.generateKeyPair();
  const privKey = await e2ee.exportPrivateKey(key.privateKey);
  const pubKey = await e2ee.exportPublicKey(key.publicKey);
  return { privKey, pubKey };
}
</script>


<!-- TODO(high)(SpeedFox198) Change from null to something -->
<GDrive on:load={null}/>
