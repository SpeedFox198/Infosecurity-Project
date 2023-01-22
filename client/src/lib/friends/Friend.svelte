<script>
  export let friend
</script>

<div class="friend d-flex py-2 px-3 user-select-none align-items-center">
	<div class="icon pe-2">
		<div class="img-wrapper img-1-1">
			<img class="rounded-circle" src={friend.avatar} alt="{friend.username} avatar" />
		</div>
	</div>
	<div class="d-flex align-items-center">
		<span>{friend.username}</span>
	</div>
  <slot></slot>
</div>

<style>
.friend {
  border-bottom: 0.1rem solid var(--primary-light-shadow);
}

.friend:hover {
  cursor: pointer;
  background-color: var(--primary-light-shadow);
}

.icon {
  height: 4.5rem;
  width: 4.5rem;
}
</style>
