<script>
import API from "./API.svelte";

let gapi;
let google;

let tokenClient;


/**
 * Callback after Google API is loaded
 */
function apiLoaded(event) {
  ({ gapi, google, tokenClient } = event.detail);
}


/**
 *  Sign in the user upon button click.
 */
function handleAuthClick() {
  tokenClient.callback = async resp => {
    if (resp.error !== undefined) {
      message = resp.error;
      throw resp;
    }
    displaySignOut = true;
    authButtonText = "Refresh";
    message = "Authenticated!";
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
 * Upload a new file
 * @return{string} file ID
 */
async function upload() {
  const filename = "test.txt"
  const file = new Blob([content], { type: "text/plain" });
  const metadata = {
    name: filename,
    mimeType: "text/plain",
    parents: ["appDataFolder"]
  };
  const accessToken = gapi.auth.getToken().access_token;
  const form = new FormData();
  form.append("metadata", new Blob([JSON.stringify(metadata)], { type: "application/json" }));
  form.append("file", file);

  let id, error;
  try {
    const url = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&fields=id"
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
    message = err;
    return;
  }

  message = `File uploaded!\nFile ID: ${id}\nFilename: ${filename}\nContent: ${content}`;
  content = "";

  return id;
}


/**
 * List all files inserted in the application data folder
 */
async function listFiles() {
  let response;
  try {
    response = await gapi.client.drive.files.list({
      spaces: "appDataFolder",
      fields: "nextPageToken, files(id, name)",
      pageSize: 10,
    });
  } catch (err) {
    message = err.message;
    return;
  }
  const files = response.result.files;
  if (!files || files.length == 0) {
    message = "No files found.";
    return;
  }
  // Flatten to string to display
  const output = files.reduce(
      (str, file) => `${str}${file.name} (${file.id}\n`,
      "Files:\n");
  message = output;
}


/**
 * Downloads a file
 * @param{string} realFileId file ID
 * @return{obj} file status
 */
async function downloadFile() {
  let file;
  try {
    file = await gapi.client.drive.files.get({
      fileId: content,
      alt: "media",
    });
    console.log("File:", file);
  } catch (err) {
    message = err.result.error.message;
    return;
  }
  const { body, status } = file;
  message = `File downloaded!\nContent: ${body}`;
  content = "";
  return status; 
}
</script>


<API on:load={apiLoaded}/>
