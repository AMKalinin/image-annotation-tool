<template>
    <div id="tileNet" @click.left="createNet" @click.right="deleteNet">
        
        <img-tile
            v-for="tile in tiles" :key="tile.id"
            :tile="tile"
        />
    </div>
</template>

<script>
import ImgTile from '@/components/ImgTile.vue'
export default{
    data(){
        return{
            tiles:[]
        }
    },
    props:{
        netInfo: {
            type: Object,
            required: true
        },
        imageInfo:{
            type: Object,
            required: true
        }
    },
    methods: {
        deleteNet(){
            this.tiles = []
        },

        createNet(){
            // while(this.netInfo.leftInd + this.imageInfo.curTileW > this.imageInfo.countTileW){
            //     this.imageInfo.curTileW -= 1 
            // }
            // while(this.netInfo.topInd + this.imageInfo.curTileH > this.imageInfo.countTileH){
            //     this.imageInfo.curTileH -= 1 
            // }
            
            for (let i=0; i < this.imageInfo.curTileH; i++){
                for (let j=0; j < this.imageInfo.curTileW; j++){
                    this.tiles.push({
                                        j:j,
                                        i:i,
                                        k:this.imageInfo.curLayer,
                                        offsetX:this.netInfo.leftInd,
                                        offsetY:this.netInfo.topInd,
                                        slideX: 100,
                                        slideY: 100
                                    })
                }   
            }
        }
    },
    components:{ImgTile}
    
}
</script>

<style scoped>
#tileNet {
    height: 100%;
    width: 100%;
}
</style>