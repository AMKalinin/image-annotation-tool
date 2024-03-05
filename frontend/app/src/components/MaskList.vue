<template>
    <div class="maskList">
        <mask-item 
            v-for="mask in masks" :key="mask.id"
        />
    </div>
</template>

<script>
import MaskItem from '@/components/MaskItem.vue';

export default{
    components:{MaskItem},
    data(){
        return{
            masks:[{id:1},{id:2},{id:3}]
        }
    }
}
</script>

<style>
.maskList{
    grid-area: maskList;
    height: 86vh; 
    overflow: auto;
}
</style>