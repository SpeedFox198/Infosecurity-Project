<svelte:head>
  <title>Bubbles | {activity}</title>
</svelte:head>


<script>
import LeftSection from "./LeftSection.svelte";
import RightSection from "./RightSection.svelte";
import { page } from "$app/stores";
import { user_id } from "$lib/stores/users";

let activity = "Chat"; // TODO(SpeedFox198): make this change according to chat u are at :)

// Set user_id according to cookie data
user_id.set($page.data.user.user_id);

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
