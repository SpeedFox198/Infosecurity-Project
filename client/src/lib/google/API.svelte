<script>
import { onMount, createEventDispatcher } from "svelte";

const client_id = "758319541478-uflvh47eoagk6hl73ss1m2hnj35vk9bq.apps.googleusercontent.com";
const scope = "https://www.googleapis.com/auth/drive.appdata";
const discoveryDocs = ["https://www.googleapis.com/discovery/v1/apis/drive/v3/rest"];
const dispatch = createEventDispatcher();

let tokenClient;

let mounted = false;
let gapiInited = false;
let gisInited = false;


onMount(() => {
  mounted = true;
  return () => mounted = false;
});


/**
 * Callback after api.js is loaded
 */
function gapiLoaded() {
  gapi.load("client", async () => {
    await gapi.client.init({ discoveryDocs });
    gapiInited = true;
    dispatchLoadEvent();
  });
}

/**
 * Callback after Google Identity Services are loaded
 */
function gisLoaded() {
  tokenClient = google.accounts.oauth2.initTokenClient({
    client_id, scope,
    callback: "", // defined later
  });
  gisInited = true;
  dispatchLoadEvent();
}

function dispatchLoadEvent() {
  if (gapiInited && gisInited) {
    dispatch("load", { gapi, google, tokenClient });
  }
}
</script>


<svelte:head>
  {#if mounted}
    <script async defer src="https://apis.google.com/js/api.js" on:load={gapiLoaded}></script>
    <script async defer src="https://accounts.google.com/gsi/client" on:load={gisLoaded}></script>
  {/if}
</svelte:head>
