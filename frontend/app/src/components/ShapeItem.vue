<template>
    <polygon 
        :points="mask.points" 
        :fill="mask.color_code+'55'"
        stroke-width="2"
        :stroke="mask.color_code"
        :id="'shape_'+mask.id"
        @mouseenter="mouseenter"
        @mouseleave="mouseleave"
        >
    </polygon>
</template>

<script>
import { SVG } from '@svgdotjs/svg.js'

export default{
    props:{
        mask:{
            type: Object,
            required: true
        }
    },
    watch:{
        mask:{
            handler(newVal){
                let maskShape = document.getElementById('shape_' + newVal.id)
                if(newVal.visibilityFlag){
                    maskShape.style.display = ''
                    if (newVal.backlightFlag){
                        maskShape.style.fill = newVal.color_code+'bb'
                    }
                    else{
                        maskShape.style.fill = newVal.color_code+'55'
                    }   
                }
                else{
                    maskShape.style.display = 'none'
                }
            },
            deep: true
        }
    },
    mounted(){
        if(this.mask.transform){
            let polyg = SVG('#shape_'+this.mask.id)
            polyg.transform({translateX: this.mask.transform.translateX, 
                                translateY: this.mask.transform.translateY})
            console.log(polyg)
        }
    },
    methods:{
        mouseenter(){
            this.$parent.$emit('changeMaskBacklightFlag', this.mask.id)
        },
        mouseleave(){
            this.$parent.$emit('changeMaskBacklightFlag', this.mask.id)
        }
    }
}
</script>


<style>
</style>