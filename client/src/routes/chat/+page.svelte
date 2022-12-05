<svelte:head>
  <title>Bubbles | {page}</title>
</svelte:head>


<script>
import LeftSection from "./LeftSection.svelte";
import RightSection from "./RightSection.svelte";

let page = "Chat"; // TODO(SpeedFox198): change this later lmao

</script>


<main class="d-flex flex-nowrap h-100">
  <LeftSection/>
  <RightSection/>
</main>


<style>
main {
  background-color: var(--white);
}
</style>
