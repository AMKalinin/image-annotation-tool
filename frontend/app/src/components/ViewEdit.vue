<template>
    <div class="edit">
        <tile-net/>
        <svg id="svg" oncontextmenu="{return false;}"></svg>
    </div>
</template>

<script>
import TileNet from '@/components/TileNet.vue'

export default{

    components:{TileNet}
    
}
</script>

<style>
</style>