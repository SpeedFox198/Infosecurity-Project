<script context="module">
import { gToken } from "$lib/stores/token";

let gapi;
let google;
let tokenClient;
let fileList = [];


/**
 *  Sign in the user.
 */
function authUser() {
  tokenClient.callback = async resp => {
    if (resp.error !== undefined) {
      message = resp.error;
      throw resp;
    }
    // TODO(high)(SpeedFox198): Event - user authenticated!
  };

  if (gapi.client.getToken() === null) {
    // Prompt the user to select a Google Account and ask for consent to share their data
    // when establishing a new session.
    tokenClient.requestAccessToken({ prompt: "consent" });
  } else {
    // Skip display of account chooser and consent dialog for an existing session.
    tokenClient.requestAccessToken({ prompt: "" });
  }
}


/**
 *  Sign out the user upon button click.
 */
function handleSignoutClick() {
  const token = gapi.client.getToken();
  if (token !== null) {
    google.accounts.oauth2.revoke(token.access_token);
    gapi.client.setToken("");
    message = "";
    authButtonText = "Authorise";
    displaySignOut  = false;
  }
}

/**
 * Upload a new JSON file with JSON content
 * @param {string} filename file name
 * @param {obj} jsonObject JSON-like object
 * @return {Promise<string>} file ID
 */
async function uploadJSONFile(filename, jsonObject) {
  return await _uploadFile(filename, JSON.stringify(jsonObject), "application/json");
}


/**
 * Upload a new file
 * @param {string} filename file name
 * @param {string} content file contents
 * @param {string} type file mime type
 * @return {Promise<string>} file ID
 */
async function _uploadFile(filename, content, type) {
  const file = new Blob([content], { type });
  const metadata = {
    name: filename,
    mimeType: type,
    parents: ["appDataFolder"]
  };
  const accessToken = gapi.auth.getToken().access_token;
  const form = new FormData();
  form.append("metadata", new Blob([JSON.stringify(metadata)], { type }));
  form.append("file", file);

  let id, error;
  try {
    const url = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&fields=id";
    const response = await fetch(url, {
      method: "POST",
      headers: new Headers({ Authorization: `Bearer ${accessToken}`}),
      body: form
    });
    ({ id, error } = await response.json());

    if (error !== undefined) {
      throw new Error(error.message);
    }

  } catch (err) {
    // TODO(high)(SpeedFox198): handle error message
    // message = err;
    return;
  }

  // TODO(high)(SpeedFox198): handle file update success
  // message = `File uploaded!\nFile ID: ${id}\nFilename: ${filename}\nContent: ${content}`;
  return id;
}


/**
 * Update aa existing file
 * @param {string} fileId file ID
 * @param {string} content file contents
 * @return {Promise<string>} file ID
 */
async function updateFile(fileId, content) {
  const file = new Blob([content], { type: "text/plain" });
  const accessToken = gapi.auth.getToken().access_token;

  let id, name, error;
  try {
    const url = `https://www.googleapis.com/upload/drive/v3/files/${fileId}?uploadType=media`
    const response = await fetch(url, {
      method: "PATCH",
      headers: new Headers({ Authorization: `Bearer ${accessToken}`}),
      body: file
    });
    ({ id, name, error } = await response.json());

    if (error !== undefined) {
      throw new Error(error.message);
    }

  } catch (err) {
    // TODO(high)(SpeedFox198): handle error
    // message = err;
    return;
  }

  // TODO(high)(SpeedFox198): handle update success
  return { id, name };
}


/**
 * List all files inserted in the application data folder
 * @param {boolean?} overwrite set to true to overwrite existing list in memory
 * @return {Promise<{ id: string, name: string }[]>} array of files in appdata folder
 */
async function listFiles(overwrite) {

  // If list of files already exist in memory, use existing list
  if (!overwrite && fileList.length > 0) {
    return fileList;
  }

  let response;
  try {
    response = await gapi.client.drive.files.list({
      spaces: "appDataFolder",
      fields: "nextPageToken, files(id, name)",
      pageSize: 10,
    });
  } catch (err) {
    // TODO(high)(SpeedFox198): handle error message
    // message = err.message;
    // Imaging catching an error just to throw it lmao
    throw err;
  }
  const files = response.result.files;
  if (!files || files.length == 0) {
    // TODO(high)(SpeedFox198): handle error message
    // message = "No files found.";
    return [];
  }
  return files;
}


/**
 * Downloads a file by given fileIfilenamed
 * @param {string} filename filename
 * @param {boolean?} overwrite set to true to overwrite existing list in memory
 * @return {Promise<obj?>} file object
 */
async function downloadFile(filename, overwrite) {
  const files = await listFiles(overwrite);
  const file = files.find(file => file.name === filename);
  if (file === undefined) {
    return;
  }
  return await _downloadFileById(file.id);
}


/**
 * Downloads a file by given fileId
 * @param {string} fileId file Id
 * @return {Promise<obj?>} file object
 */
async function _downloadFileById(fileId) {
  try {
    return await gapi.client.drive.files.get({ fileId, alt: "media"});
  } catch (err) {
    // TODO(high)(SpeedFox198): handle error message
    // message = err.result.error.message;
    return;
  }
}


// Export functions for other svelte components to use
export const service = {
  authUser,
  handleSignoutClick,
  uploadJSONFile,
  updateFile,
  downloadFile,
};
</script>


<script>
import GAPI from "./GAPI.svelte";
import { createEventDispatcher } from "svelte";

const dispatch = createEventDispatcher();


/**
 * Callback after Google API is loaded
 */
function apiLoaded(event) {
  ({ gapi, google, tokenClient } = event.detail);
  dispatch("load");
}
</script>


<GAPI on:load={apiLoaded}/>
