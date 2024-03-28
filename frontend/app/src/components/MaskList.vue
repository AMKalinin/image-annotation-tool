<template>
    <div class="maskList">
        <mask-item 
            v-for="(mask, key) in masks" 
            :key="key" 
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
            type: Object,
            required: true
        },
        classList:{
            type: Array,
            required: true
        }
    },
    methods:{
        changeMaskVisibilityFlag(maskId){
            this.$emit('changeMaskVisibilityFlag', maskId)
        },
        changeMaskBacklightFlag(maskId){
            this.$emit('changeMaskBacklightFlag', maskId)
        },
        deleteMask(maskId){
            this.$emit('deleteMask', maskId)
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