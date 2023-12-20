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
/* TODO */
.edit { 
    grid-area: edit;
    overflow: auto;
    display: inline-block;
    position: relative;
    background: #F6F8FA;
    height: 100%;
    width: 100%;
    user-select:none;
    overflow: hidden;
}
</style>