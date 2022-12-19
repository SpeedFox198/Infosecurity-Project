<script>
import { page } from "$app/stores"
let currentUser = $page.data.user

export let toggleSettings;

</script>


<div class="profile-height d-flex flex-row align-items-center p-2">
  <img src={ currentUser.avatar } alt="{ currentUser.username } profile picture" class="rounded-circle">
  <span class="px-2">{ currentUser.username }</span>
  <a href="/settings" on:click|preventDefault={toggleSettings}>
    <i class="fa-solid fa-cog fs-4"></i>
  </a>
</div>


<style>
.profile-height {
  width: 5rem;
}
</style>