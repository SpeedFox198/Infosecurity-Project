<script>
  import {page} from "$app/stores"
  let currentUser = $page.data.user
</script>

<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <div class="container-fluid">
    <ul class="navbar-nav me-auto mb-lg-0 edit">
      <form class="d-flex">
        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
      </form>
    </ul>
  </div>
</nav>

<footer>  
</footer>

<style>
  .image-size {
    width: 50px;
    height: 50px;
  }

 .edit {
   padding-left: 80px;
   padding-right: 80px;

 }
</style>