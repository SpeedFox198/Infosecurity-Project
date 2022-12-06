<script>
    export let device
    export let current_device_id
    
    let time = new Date(device.time*1000).toLocaleString("en-SG") // JS uses milliseconds instead of seconds

</script>

<div>
    {#if (current_device_id === device.id)}
       Your current device ->  
    {/if}
    {time}
    {device.browser}
    {device.os}
    {device.location}
</div>