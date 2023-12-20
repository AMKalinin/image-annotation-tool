<template>
    <img :id="(tile.j + tile.offsetX) + ':' + (tile.i+tile.offsetY) + ':' + tile.k" 
    src = "./fgfgf.png"
    :alt="(tile.j + tile.offsetX) + ':' + (tile.i+tile.offsetY) + ':' + tile.k" 

    @click="testA"

    :style="{top:256*this.tile.i + this.tile.slideY +'px',
            left:256*this.tile.j + this.tile.slideX + 'px'}"

    >
</template>

<script>
export default{
    props:{
        tile:{
            type: Object,
            required: true
        }
    },
    methods: {
        testA(){
            console.log('hello')
        }
    }
}
</script>

<style scoped>
img{
    position: absolute;
    width: 256px;
    height: 256px;
}
</style>