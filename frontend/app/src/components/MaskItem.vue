<template>
    <div class="maska" 
        :id="'mask_'+mask.id"
        @mouseenter="mouseenter"
        @mouseleave="mouseleave">
        <div class="colorImg" :style="'background:' + ';'"></div>

        <div class="contentMask">
            <label class="maskName">Name: {{mask.id}}</label> <br>
            
            <label class="check" ondblclick="event.stopPropagation();">
                <input value="{{mask.points}}" type="checkbox" class="maskaViewCheck" :onchange="visibleCheck">
                <span class="checkbox"></span>
            </label>

            <img
                v-if="typeMask === 0" 
                class="deleteBtn" 
                :src="imageTrash"
                title="Polygon" 
                @click="deleteMask"
                ondblclick="event.stopPropagation();"
            >

            <label class="type">Type: {{mask.type}} </label> <br>
            <label v-if="typeMask === 0">Class:   
                <select class="selectClass">
                    <template v-for="cls in classList" :key="cls.code">
                        <option 
                            v-if="mask.class_code == cls.code"
                            >
                            {{cls.name}}
                        </option>
                    </template>
                    <template v-for="cls in classList" :key="cls.code">
                        <option 
                            v-if="mask.class_code != cls.code"
                            >
                            {{cls.name}}
                        </option>
                    </template>
                </select>
            </label>
            <!-- Тут возможно надо будет переделать  -->
            <label v-else-if="mask.class_code == '000'">
                Class: не выбран
            </label>
            <label v-else>
                Class: dfghdfghdfghdfgh
            </label>

        </div>
    </div>
</template>

<script>
import imageTrash from '../images/trash.svg';

export default{
    data(){
        return{
            projectName: 'asd',
            taskIndex: 0,
            imageTrash,
            typeMask:0
        }
    },
    props:{
        mask:{
            type: Object,
            required: true
        },
        classList:{
            type: Array,
            required: true
        }
    },
    watch:{
        mask:{
            handler(newVal){
                let maskControl = document.getElementById('mask_'+newVal.id)
                    if (newVal.backlightFlag){
                        maskControl.style.background = 'LightGrey'
                    }
                    else{
                        maskControl.style.background = 'White'
                    }
            },
            deep: true
        }
    },
    methods:{
        mouseenter(){
            this.$emit('changeMaskBacklightFlag', this.mask.id)
        },
        mouseleave(){
            this.$emit('changeMaskBacklightFlag', this.mask.id)
        },
        visibleCheck(){
            this.$emit('changeMaskVisibilityFlag', this.mask.id)
        },
        deleteMask(){
            this.$emit('deleteMask', this.mask.id)
        }
    }
}
</script>

<style scoped>
.maska{
    position:relative;
    height: 70px;
    padding: 0px;
    border: 1px solid #D9DBDE;
    overflow: hidden;
}

.colorImg{
    width: 20px;
    height: 70px;
    position:absolute; 
    top: 0px;
    left: 0px;
}

.deleteBtn{
    position:absolute; 
    bottom: 0px;
    right: 10px;
}

.check{
    position:absolute; 
    top: 5px;
    right: 30px;
}

.maskaViewCheck{
    position: absolute;
    /* top: 10px;
    right: 10px; */
    -webkit-appearance: none;
    -moz-appearance: none;
    appearance: none;

}

.checkbox{
    position:absolute;
    width: 1.5em;
    height: 1.5em;
    background-image: url(../images/show.svg);
    background-size: 24px;
    background-repeat: no-repeat;
}

.maskaViewCheck:checked + .checkbox{
    background-image: url(../images/hide.svg);
}


.contentMask{
    position:relative;
    margin-left: 24px;
}

.selectClass{
    background: #F6F8FA;
    border: 1px solid #D9DBDE;
    border-radius: 6px;
    width: 10vw;
}
</style>