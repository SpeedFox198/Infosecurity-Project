<script context="module">
  /**
   * 
   * @param {HTMLImageElement} imgElement
   * @param {HTMLCanvasElement} canvasElement
   */
  export const processImage = async (imgElement, canvasElement) => {
    const cvImage = cv.imread(imgElement)
    let processed = new cv.Mat()
  
    cv.cvtColor(cvImage, cvImage, cv.COLOR_RGBA2GRAY, 0);
    cv.GaussianBlur(cvImage, cvImage, new cv.Size(3, 3), 0, 0, cv.BORDER_DEFAULT);
    cv.threshold(cvImage, cvImage, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU);
    let kernel = cv.getStructuringElement(cv.MORPH_RECT, new cv.Size(3, 3));
    cv.morphologyEx(cvImage, cvImage, cv.MORPH_OPEN, kernel);
    let invert = new cv.Mat(cvImage.rows, cvImage.cols, cvImage.type(), new cv.Scalar(255));
    cv.subtract(invert, cvImage, processed);
  
    cv.imshow(canvasElement.id, processed)
    cvImage.delete()
    processed.delete()
  }
</script>

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
