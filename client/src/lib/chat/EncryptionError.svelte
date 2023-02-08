<script>
export let initKeys;
</script>


<div class="welcome-page-section d-flex flex-column flex-grow-1 align-items-center justify-content-center user-select-none">

  <div class="mx-3 fs-3">
    You are not logged in to your google account!
  </div>

  <div class="mx-2">
    To view end-to-end encrypted chats, you must login to the google account that stores your private encryption keys.
  </div>

  <div class="mx-2">
    Pop-ups has to be enabled to authenticate your google account.
  </div>

  <button class="btn mx-2 mt-4" on:click={initKeys}>
    Authenticate your google account
  </button>
</div>


<style>
.welcome-page-section {
  background-color: var(--grey);
  padding-top: 2%;
  padding-bottom: 25%;
}

.btn {
  background-color: var(--primary);
  color: var(--white);
}
</style>
