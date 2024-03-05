<template>
    <div class="workarea">
        <Tool-Bar class="tool"></Tool-Bar>
        <View-Edit class="edit"></View-Edit>
        <control-edit></control-edit>
    </div>
</template>

<script>
import ToolBar from '@/components/ToolBar.vue'
import ViewEdit from '@/components/ViewEdit.vue'
import ControlEdit from '@/components/ControlEdit.vue'

export default{
    components:{ToolBar, ViewEdit, ControlEdit}
}
</script>

<style>
.workarea {  
    display: grid;
    grid-template-columns:  0.1fr 2.3fr 0.6fr; 
    grid-template-rows: 1fr;
    gap: 0px 0px;
    grid-template-areas:
        "tool edit controlEdit";
}

.tool {
    grid-area: tool;
    height: 100%;
}


</style>