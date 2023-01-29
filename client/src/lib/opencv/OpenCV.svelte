<script>
	import { onMount } from "svelte";

  let mounted = false
  let opencvLoaded = false 
  export let openCv

  const loadOpenCV = () => {
    opencvLoaded = true
    console.log("OpenCV loaded?", opencvLoaded)
  }
  
  onMount(() => {
    mounted = true
    return () => mounted = false
  })
</script>

<img src="" alt="" bind:this={openCv} class="d-none">
<!-- Add canvas -->

<svelte:head>
  {#if mounted}
    <script src="js/opencv.js" async on:load={loadOpenCV}></script>
  {/if}
</svelte:head>
