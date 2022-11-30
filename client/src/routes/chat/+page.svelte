<script>
import LeftSection from "./leftSection.svelte";
import RightSection from "./RightSection.svelte";
</script>

<style>
main {
    background-color: var(--white);
}
</style>

<main class="d-flex flex-nowrap h-100">
    <LeftSection/>
    <RightSection/>
</main>
