<template>
    <div class="controlEdit">
        <mask-list 
            :masks="masks" 
            :classList="classList"
            @changeMaskVisibilityFlag="changeMaskVisibilityFlag"
            @changeMaskBacklightFlag="changeMaskBacklightFlag"
            @deleteMask="deleteMask"
        />
    </div>
</template>

<script>
import MaskList from '@/components/MaskList.vue';

export default{
    components:{MaskList},
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
.controlEdit { 
    grid-area: controlEdit;
    display: grid; 
    grid-template-columns:  1fr; 
    grid-template-rows: 0.3fr 1.7fr;
    gap: 0px 0px;
    grid-auto-flow: row;
    grid-template-areas:
        "toolMask"
        "maskList";
    overflow: auto;
    /* height: 94vh; */
    min-width: 300px;
    /* max-width: 350px; */
}
</style>
