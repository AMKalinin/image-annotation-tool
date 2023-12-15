<template>
    <ul class="toolbar" >
        <li class="tool_item mark"  id="polygon"><img :src="imagePolygon" title="Polygon"></li>
        <li class="tool_item mark" id="rect"><img :src="imageRect" title="Rectangle"></li>
        <li class="tool_item mark" id="line"><img :src="imageLine" title="Line"></li>
        <li class="tool_item mark" id="circle"><img :src="imageEllipse" title="Circle"></li>

        <li class="tool_item void" ></li>
    </ul>
</template>


<script>
import imagePolygon from '../images/polygon.svg';
import imageRect from '../images/rectangle.svg';
import imageLine from '../images/line.svg';
import imageEllipse from '../images/ellipse.svg';
export default {
  data() {
    return {
        imagePolygon,
        imageRect,
        imageLine,
        imageEllipse
    };
  }
};
</script>


<style>


ul.toolbar
{
    list-style-type: none;
    margin: 0;
    padding: 0;
    overflow: hidden;
    background: #292929;
    top: 0;
    left: 0;
    height: 100%;
}

ul.toolbar li.tool_item {
    margin: 0.9%;
    line-height: 5;
}


li.tool_item img{
    position: relative;
    height: 50px;
    width: 50px;
    filter: invert(1);
    left: calc(50% - 50px/2);
}

li.tool_item.void{
    height: calc(100% - 50px * 13.5);
}

li.tool_item.size a{
    display: inline-block;
    height: 50px;
    width: 50px;
}

li.tool_item.size img{
    filter: invert(0);
    height: 20px;
    width: 20px;
    left: calc(50% - 10px/2);
}

#mashtab{
    margin: 0;
    color: white;
    position:relative;
    text-align: center;
    font-size: 120%
}
</style>