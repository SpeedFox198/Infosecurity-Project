<script>
import { onMount, createEventDispatcher } from "svelte";

const dispatch = createEventDispatcher();

let mounted = false;

onMount(() => {
  mounted = true;
  return () => mounted = false;
});

const gapiLoaded = () => dispatch("loadGapi", gapi);
const gisLoaded = () => dispatch("loadGis", google);
</script>


<svelte:head>
  {#if mounted}
    <script async defer src="https://apis.google.com/js/api.js" on:load={gapiLoaded}></script>
    <script async defer src="https://accounts.google.com/gsi/client" on:load={gisLoaded}></script>
  {/if}
</svelte:head>
