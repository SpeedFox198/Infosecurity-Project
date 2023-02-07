<script>
export let currentUser;
</script>


<div class="welcome-page-section d-flex flex-column flex-grow-1 align-items-center justify-content-center user-select-none">
  <img class="logo mb-3" src="/with-text.svg" alt="Bubbles">

  <!-- <div class="mx-2">Your privacy is our priority.</div> -->

  <div class="mx-3 fs-3">
    Welcome to Bubbles <span style="color: var(--primary);">{currentUser.username}</span>!
  </div>

  <div class="mx-2">
    Start chatting by clicking one of the group chats at the left.
  </div>

  <div class="mx-2">
    End-to-end-encrypted are labelled with a green lock <i class="icon fa-solid fa-lock"></i>
  </div>

</div>


<style>
.welcome-page-section {
  background-color: var(--grey);
  padding-top: 2%;
  padding-bottom: 25%;
}

.icon {
  color: var(--primary);
}

.logo {
  width: 25rem;
}
</style>
