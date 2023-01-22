<script context="module">

let gapi;
let google;
let tokenClient;
let fileList = [];


/**
 * Authenticates user and calls callback if given
 * @param {function?} callback
 */
function authUser(callback) {
  tokenClient.callback = async resp => {
    if (resp.error !== undefined) {
      message = resp.error;
      throw resp;
    }
    if (callback !== undefined) callback();
  };
  // Request for client access token
  tokenClient.requestAccessToken({ prompt: "" });
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
 * @return {Promise<{ id?: string; error?: { message: string; code: number; }; }>} file ID
 */
async function uploadJSONFile(filename, jsonObject) {
  return await _uploadFile(filename, JSON.stringify(jsonObject), "application/json");
}


/**
 * Upload a new file
 * @param {string} filename file name
 * @param {string} content file contents
 * @param {string} type file mime type
 * @return {Promise<{ id?: string; error?: { message: string; code: number; }; }>} file ID
 */
async function _uploadFile(filename, content, type) {
  const file = new Blob([content], { type });
  const metadata = {
    name: filename,
    mimeType: type,
    parents: ["appDataFolder"]
  };
  const token = gapi.auth.getToken();
  if (token === null) return { error: { message: "User not authenticated.", code: 403 } };
  const accessToken = token.access_token;

  const form = new FormData();
  form.append("metadata", new Blob([JSON.stringify(metadata)], { type }));
  form.append("file", file);

  try {
    const url = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&fields=id";
    const response = await fetch(url, {
      method: "POST",
      headers: new Headers({ Authorization: `Bearer ${accessToken}`}),
      body: form
    });
    return await response.json();

  } catch (error) {
    return { error };
  }
}


/**
 * Updates an existing file
 * @param {string} fileId file ID
 * @param {string} content file contents
 * @return {Promise<{ content?: string; id?: string; name?: string; error?: { message: string; code: number; }; }>} file ID
 */
async function updateJSONFile(filename, key, value) {
  const { file, error } = await downloadFile(filename, true);
  if (error) return { error };

  const data = JSON.parse(file.body);
  data[key] = value;

  const content = JSON.stringify(data)

  const details = await _updateFile(file.id, content, "application/json");
  details.content = content;

  return details;
}


/**
 * Updates an existing file
 * @param {string} fileId file ID
 * @param {string} content file contents
 * @param {string} type file mime type
 * @return {Promise<{ id?: string; name?: string; error?: { message: string; code: number; }; }>} file ID
 */
async function _updateFile(fileId, content, type) {
  const file = new Blob([content], { type });
  const token = gapi.auth.getToken();
  if (token === null) return { error: { message: "User not authenticated.", code: 403 } };
  const accessToken = token.access_token;

  try {
    const url = `https://www.googleapis.com/upload/drive/v3/files/${fileId}?uploadType=media`
    const response = await fetch(url, {
      method: "PATCH",
      headers: new Headers({ Authorization: `Bearer ${accessToken}`}),
      body: file
    });
    return await response.json();

  } catch (error) {
    return { error };
  }
}


/**
 * List all files inserted in the application data folder
 * @return {Promise<{ files?: { id: string; name: string }[]; error?: { message: string; code: number; }; }>} array of files in appdata folder
 */
async function listFiles(useCached) {
  if (useCached) return { files: fileList };

  let response;
  try {
    response = await gapi.client.drive.files.list({
      spaces: "appDataFolder",
      fields: "nextPageToken, files(id, name)",
      pageSize: 10,
    });
  } catch (err) {
    if (err.status === 403) {
      return { error: err.result.error };
    }
    throw err.result.error;
  }

  const files = response.result.files;

  fileList = files;

  if (!files || files.length == 0) {
    return { files: [] };
  }
  return { files };
}


/**
 * Downloads a file by given filename
 * @param {string} filename filename
 * @return {Promise<{ file?: obj; error?: { message: string; code: number; }; }>} file object
 */
async function downloadFile(filename, useCached) {
  const { fileId, error } = await _getFileId(filename, useCached);
  if (error) return { error };
  return await _downloadFileById(fileId);
}


/**
 * Downloads a file by given fileId
 * @param {string} fileId file Id
 * @return {Promise<{ file?: obj; error?: { message: string; code: number; }; }>} file object
 */
async function _downloadFileById(fileId) {
  try {
    const file = await gapi.client.drive.files.get({ fileId, alt: "media"});
    file.id = fileId;
    return { file };
  } catch (err) {
    return { error: err.result.error };
  }
}


/**
 * Resolves given filename to file ID
 * @param {string} filename filename
 * @return {Promise<{ fileId?: string; error?: { message: string; code: number; }; }>} file ID
 */
async function _getFileId(filename, useCached) {
  const { files, error } = await listFiles(useCached);
  if (error) return { error };
  const file = files.find(file => file.name === filename);
  if (file === undefined) {
    return { error: { message: `File with filename ${filename} not found`, code: 404 } };
  }
  return { fileId: file.id };
}


// Export functions for other svelte components to use
export const service = {
  authUser,
  handleSignoutClick,
  uploadJSONFile,
  updateJSONFile,
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
