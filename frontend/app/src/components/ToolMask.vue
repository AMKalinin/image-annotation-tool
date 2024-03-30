<template>
    <div class="toolMask">
        <a id="showAll" @mousedown="hide"><img :src="imageShow" title="Показать все маски"></a>
        <a id="hideAll" style="display: none;" @mousedown="show"><img :src="imageHide" title="Скрыть все маски"></a>
        <select id="maskClassBase" @change="changeClassCode">
            <template v-for="cls in classList" :key="cls.code">
                <option :value="cls.code">{{cls.name}}</option>
            </template>
        </select>
    </div>
</template>


<script>
import imageShow from '../images/show.svg'
import imageHide from '../images/hide.svg'

export default{
    data(){
        return{
            imageShow,
            imageHide

        }
    },
    props:{
        classList:{
            type: Array,
            // required: true
        }
    },
    methods: {
        hide(){
            document.getElementById('showAll').style.display = 'none'
            document.getElementById('hideAll').style.display = ''
            this.$parent.$emit('hideAll')

        },
        show(){
            document.getElementById('showAll').style.display = ''
            document.getElementById('hideAll').style.display = 'none'
            this.$parent.$emit('showAll')
        },
        changeClassCode(){
            let classCode = document.getElementById('maskClassBase').value
            this.$parent.$emit('changeClassCode', Number(classCode))
        }
    }
}
</script>


<style>
.tool_mask{
    grid-area: toolMask
}

#showAll img, #hideAll img{
    height: 50px;
    width: 50px;
    float: right;
}

#maskClassBase{
    margin-top: 20px;
    margin-left: 70px;
    margin-bottom: 5px;
    background: #F6F8FA;
    border: 1px solid #D9DBDE;
    border-radius: 6px;
    width: 10vw;
}

</style>