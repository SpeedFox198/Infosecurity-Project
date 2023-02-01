<script context="module">
export const encryption = {};
</script>


<script>
// TODO(mid)(SpeedFox198): change ../google/ to $lib/google/
import GDrive, { service } from "../google/GDrive.svelte";
import { masterKey, roomKeys } from "$lib/stores/key";
import { room_id } from "$lib/stores/room";
import { user_id } from "$lib/stores/user";
import { e2ee } from "./e2ee";

const MASTER_KEY_FILE_NAME = "master_key.json";
const ROOM_KEYS_FILE_NAME = "room_keys.json";

let keysInited = false;


/**
 * Initialise keys from localStorage if possible,
 * else download keys from google drive.
 */
async function initKeys() {
  // Ensure only initialise once
  if (keysInited) return;

  let file, error;

  // If masterKey failed to init from localStorage, download from google drive
  if (masterKey.init()) {
    ({ file, error } = await service.downloadFile(MASTER_KEY_FILE_NAME));

    // Init masterKey from downloaded file, else create new masterKey
    if (error && error.code === 403) {
      // If user unauthorised, authenticate user before initialising keys
      service.authUser(initKeys);
      return;

    } else if (error && error.code === 404) {
      // Create new keys
      const newMasterKey = await getNewMasterKey();

      // Upload masterKey file to gdrive
      service.uploadJSONFile(MASTER_KEY_FILE_NAME, newMasterKey);

      // Save masterKey to stores and localStorage
      masterKey.saveMasterKey(newMasterKey);

    } else {
      masterKey.initFromJson(file.body, true);
    }
  }

  // If roomKeys failed to init from localStorage, download from google drive
  if (roomKeys.init()) {
    ({ file, error } = await service.downloadFile(ROOM_KEYS_FILE_NAME));

    // Init roomKeys from downloaded file, else create new empty object
    if (error && error.code === 403) {
      // If user is unauthorised, authenticate user before initialising keys
      service.authUser(initKeys);
      return;

    } else if (error && error.code === 404) {
      // Upload roomKeys file to gdrive
      service.uploadJSONFile(ROOM_KEYS_FILE_NAME, {});

      // Save roomKeys to stores and localStorage
      roomKeys.initFromJson("{}", true);

    } else {
      roomKeys.initFromJson(file.body, true);
    }
  }

  // When all keys initiated successfully,
  // set flag to true to prevent multiple calls
  keysInited = true;
}


encryption.encryptMessage = async message => {
  const key = await getRoomKey();
  if (key === undefined) return;
  return await e2ee.encryptMessage(message, key);
};


encryption.decryptMessage = async message => {
  const key = await getRoomKey();
  if (key === undefined) return;
  return await e2ee.decryptMessage(message, key);
};


encryption.encryptFile = async image => {
  const key = await getRoomKey();
  if (key === undefined) return;
  return await e2ee.encryptFile(image, key);
}


encryption.decryptFile = async (image, iv) => {
  const key = await getRoomKey();
  if (key === undefined) return;
  return await e2ee.decryptFile(image, key, iv);
}


encryption.decryptImage = async (image, iv) => {
  const key = await getRoomKey();
  if (key === undefined) return;
  return await e2ee.decryptImage(image, key, iv);
}


async function getRoomKey() {
  let key = $roomKeys[$room_id];
  if (key === undefined) {
    key = await createAndSaveRoomKey($room_id, $user_id);
    if (key === undefined) return;
  }
  return await e2ee.importRoomKey(key);
}


/**
 * Creates and save the room key
 * @param {string} room_id current room id
 * @param {string} user_id current user id
 * @returns {Promise<string>} Base64 encoded room key
 */
async function createAndSaveRoomKey(room_id, user_id) {
  // Get other user public key from server
  const response = await fetch(`https://localhost:8443/api/user/public-key/${room_id}/${user_id}`);
  const { public_key: pubKey, message } = await response.json();
  if (message) throw new Error(message);

  // Derive room key
  const key = await deriveRoomKey(pubKey);

  if (key === undefined) {
    service.authUser(() => createAndSaveRoomKey(room_id, user_id));
  }

  // Upload room key to google drive
  saveRoomKey(room_id, key);

  return key;
}


/**
 * Creates and save the room key
 * @param {string} room_id room id
 * @param {string} key Base64 encoded room key
 */
async function saveRoomKey(room_id, key) {
  // Upload room key to google drive
  const { content, error } = await service.updateJSONFile(ROOM_KEYS_FILE_NAME, room_id, key);

  // If user is not authenticated yet
  if (error && error.code === 403) {
    service.authUser(() => saveRoomKey(room_id, key));

  // If file is not created yet
  } else if (error && error.code === 404) {
    const data = {};
    data[room_id] = key;
    service.uploadJSONFile(ROOM_KEYS_FILE_NAME, data);
    roomKeys.saveNewKey(room_id, key);
  } else {
    roomKeys.initFromJson(content, true);
  }
}


async function getNewMasterKey() {
  const key = await e2ee.generateKeyPair();
  const privKey = await e2ee.exportPrivateKey(key.privateKey);
  const pubKey = await e2ee.exportPublicKey(key.publicKey);
  return { privKey, pubKey };
}


async function deriveRoomKey(userPubKey) {
  const storedKey = $masterKey.privKey;
  if (storedKey === undefined) return;
  const privKey = await e2ee.importPrivateKey(storedKey);
  const pubKey = await e2ee.importPublickey(userPubKey);
  const roomKey = await e2ee.deriveSecretKey(privKey, pubKey);;
  return await e2ee.exportRoomKey(roomKey);
}
</script>


<!-- TODO(high)(SpeedFox198) Change from null to something -->
<GDrive on:load={initKeys}/>
