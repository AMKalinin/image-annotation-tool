<template>
    <img :id="(tile.j + tile.offsetX) + ':' + (tile.i+tile.offsetY) + ':' + tile.k" 
    :src = "/task_tail/"
    :alt="(tile.j + tile.offsetX) + ':' + (tile.i+tile.offsetY) + ':' + tile.k" 

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
    mounted() {
      this.message = this.testA();
    },
    methods: {
        testA(){
            console.log('this.$el.style.top')
        },
        moveTile(dx, dy){
            let x = Number(this.$el.style.left.split('px')[0])
            let y = Number(this.$el.style.top.split('px')[0])
            this.$el.style.left = x + dx + 'px';
            this.$el.style.top = y + dy  + 'px'; 
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