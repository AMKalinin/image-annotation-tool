<template>
    <div id="tileNet">
        <img-tile
            v-for="tile in tiles" :key="tile.id"
            :tile="tile"
        />
    </div>
</template>

<script>
import ImgTile from '@/components/ImgTile.vue'

export default{
    
    data() {
        return {
            tiles:[{
                j:0,
                i:0,
                k:0,
                offsetX:0,
                offsetY:0,
                slideX: 0,
                slideY: 0
            },{
                j:1,
                i:0,
                k:0,
                offsetX:0,
                offsetY:0,
                slideX: 0,
                slideY: 0
            },{
                j:0,
                i:1,
                k:0,
                offsetX:0,
                offsetY:0,
                slideX: 0,
                slideY: 0
            },{
                j:1,
                i:1,
                k:0,
                offsetX:0,
                offsetY:0,
                slideX: 0,
                slideY: 0
            },]
        };
    },
    components:{ImgTile}
    
}
</script>

<style scoped>
</style>