<script>
import { page } from "$app/stores"
let currentUser = $page.data.user

export let toggleSettings;

</script>


<div class="flex-column d-flex profile">
  <div class="profile-height d-flex align-items-center p-2">
    <img src={ currentUser.avatar } alt="{ currentUser.username } profile picture" class="rounded-circle">
    <span class="px-2 fw-bolder">{ currentUser.username }</span>
    <button on:click={toggleSettings} type="button" title="Show settings" class="btn" >
      <i class="fa-solid fa-cog fs-4"></i>
    </button>
  </div>
</div>


<style>
.profile {
  background-color: var(--primary-shadow);
  color: var(--white);
}
.profile-height {
  width: 4rem;
}
</style>