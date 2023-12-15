<template>
    <div class="workarea">
        <Tool-Bar class="tool"></Tool-Bar>
        <div class="edit">
        </div>



    </div>
</template>

<script>
import ToolBar from '@/components/ToolBar.vue';

export default{
    components:{ToolBar}
}
</script>

<style>
.workarea {  
    display: grid;
    grid-template-columns:  0.1fr 2.3fr 0.6fr; 
    grid-template-rows: 1fr;
    gap: 0px 0px;
    grid-template-areas:
        "tool edit control_edit";
}

.tool {
    grid-area: tool;
    height: 100%;
}

</style>