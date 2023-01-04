<script>
import SlidingMenu from "$lib/settings/templates/SlidingMenu.svelte";
import Option from "$lib/settings/templates/Option.svelte";

export let displayNewGroup;
export let toggleNewGroup;

let displayMagic = false;     // Disappearing messages menu, *MAGIC! POOF!* (๑°༥°๑)

const toggleMagic = async () => displayMagic = !displayMagic;
</script>


<SlidingMenu title="Add Group Members" display={displayNewGroup} on:click={toggleNewGroup} right={false}>
  <ul>
    <!-- {#each friends as friend}
      <li></li>
    {/each} -->
  </ul>
</SlidingMenu>

