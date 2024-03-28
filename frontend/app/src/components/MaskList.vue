<template>
    <div class="maskList">
        <mask-item 
            v-for="mask in masks" 
            :key="mask.id" 
            :mask="mask" 
            :classList="classList"
            @changeMaskVisibilityFlag="changeMaskVisibilityFlag"
            @changeMaskBacklightFlag="changeMaskBacklightFlag"
            @deleteMask="deleteMask"
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
        },
        classList:{
            type: Array,
            required: true
        }
    },
    methods:{
        changeMaskVisibilityFlag(index){
            this.$emit('changeMaskVisibilityFlag', index)
        },
        changeMaskBacklightFlag(index){
            this.$emit('changeMaskBacklightFlag', index)
        },
        deleteMask(index){
            this.$emit('deleteMask', index)
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