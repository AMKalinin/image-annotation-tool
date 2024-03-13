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
    props:{
        masks:{
            type: Array,
            required: true
        }
    },
}
</script>

<style>
.maskList{
    grid-area: maskList;
    height: 86vh; 
    overflow: auto;
}
</style>