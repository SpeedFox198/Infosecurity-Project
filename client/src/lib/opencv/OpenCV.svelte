<script>
	import { onMount } from "svelte";

  let mounted = false
  let opencvLoaded = false 
  export let openCv
  export let canvas

  const loadOpenCV = () => {
    opencvLoaded = true
    console.log("OpenCV loaded?", opencvLoaded)
  }
  
  onMount(() => {
    mounted = true
    return () => mounted = false
  })
</script>

<div class="d-none">
  <img src="" alt="" bind:this={openCv}>
  <canvas id="openCvCanvas" bind:this={canvas}></canvas>
</div>

<svelte:head>
  {#if mounted}
    <script src="js/opencv.js" async on:load={loadOpenCV}></script>
  {/if}
</svelte:head>
