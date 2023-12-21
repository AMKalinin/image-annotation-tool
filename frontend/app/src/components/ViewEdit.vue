<template>
    <div class="edit">
        <tile-net :net-info="netInfo" :image-info="imageInfo" @mousedown="mouseMove"/>
        <svg id="svg" oncontextmenu="{return false;}"></svg>
    </div>
</template>

<script>
import TileNet from '@/components/TileNet.vue'

export default{
    data() {
        return {
            netInfo:{
                leftInd:0,
                topInd:0
            },
            imageInfo:{
                curTileW:4,
                countTileW:12,
                curTileH:4,
                countTileH:12,
                curLayer:0    
            }
        }
    },
    methods: {
        mouseMove(event){
            console.log(event.clientX, event.clientY)
            console.log(event.button === 1)
        }
    },
    components:{TileNet}
    
}
</script>

<style>

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