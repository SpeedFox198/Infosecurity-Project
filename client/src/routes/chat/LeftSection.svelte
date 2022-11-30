<script>
import Nav from "./Nav.svelte";
</script>

<style>
.left-section {
    width: 25rem;
    background-color: var(--primary-light);
}

.top-left {
    height: 4rem;
    border-top: 0.1rem solid var(--primary-shadow);
    border-right: 0.1rem solid var(--primary-shadow);
    background-color: var(--primary);
}

.bottom-left {
    height: 100%;
    border-right: 0.1rem solid var(--grey);
}
</style>


<!-- Left Section -->
<div class="d-flex flex-column flex-shrink-0 left-section">

    <!-- Profile & Settings Section -->
    <div class="d-flex top-left">
        <Nav/>
    </div>

    <!-- Chat List Section -->
    <div class="d-flex bottom-left">

    </div>
</div>
