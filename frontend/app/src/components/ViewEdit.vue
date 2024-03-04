<template>
    <div class="edit" @wheel="onWheel" @mousedown="mouseMove">
        <tile-net 
            id="tileNet" 
            :image-info="imageInfo" 
        />
        
        <svg id="svg" oncontextmenu="{return false;}"></svg>
    </div>
</template>


<script>
import TileNet from '@/components/TileNet.vue'
import axios from 'axios'
import { SVG } from '@svgdotjs/svg.js'

export default{
    data() {
        return {
            netInfo:{
                leftInd:0,
                topInd:0
            },
            imageInfo:{
                curTileW:4,
                countTileW: Math.ceil(2000/256),
                curTileH:4,
                countTileH: Math.ceil(2000/256),
                curLayer:0,
                countLayers:4,
                width: 2000,
                height: 2000

            }
        }
    },
    mounted() {
        this.getImageInfo()
        this.createNet(0,0)
    },
    methods: {
        getImageInfo(){
            let tileNet = document.getElementById('tileNet')
            this.imageInfo.projectName = this.$route.params.projectName
            this.imageInfo.taskId = this.$route.params.id

            let url = '/projects/' + this.imageInfo.projectName + '/tasks/' + this.imageInfo.taskId
            axios.get(url).then((response) => {
                this.imageInfo.fileName = response.data.file_name

                this.imageInfo.height = response.data.height
                this.imageInfo.width = response.data.width

                this.imageInfo.countLayers = response.data.layers_count
                this.imageInfo.curLayer = 0

                this.imageInfo.countTileW = Math.ceil((this.imageInfo.width/2**this.imageInfo.curLayer)/256)
                this.imageInfo.countTileH = Math.ceil((this.imageInfo.height/2**this.imageInfo.curLayer)/256)

                this.imageInfo.curTileW = Math.ceil(tileNet.offsetWidth/256)
                if(this.imageInfo.countTileW < this.imageInfo.curTileW){
                    this.imageInfo.curTileW = this.imageInfo.countTileW;   
                }

                if(this.imageInfo.countTileH < this.imageInfo.curTileH){
                    this.imageInfo.curTileH = this.imageInfo.countTileH;
                }
            })
        },
        createNet(topInd, leftInd){
            while(leftInd + this.imageInfo.curTileW > this.imageInfo.countTileW){
                this.imageInfo.curTileW -= 1 
            }
            while(topInd + this.imageInfo.curTileH > this.imageInfo.countTileH){
                this.imageInfo.curTileH -= 1 
            }
            
            for (let i=0; i < this.imageInfo.curTileH; i++){
                for (let j=0; j < this.imageInfo.curTileW; j++){
                    let tileNet = document.getElementById('tileNet')
                    tileNet.append(this.createTile(j,i,this.imageInfo.curLayer, leftInd, topInd))
                }   
            }
        },

        createTile(x, y, k, offsetX, offsetY, slideX=null, slideY=null){
            let img = document.createElement('img')
            img.style.position = 'absolute'
            img.id = (x+offsetX) + ':' + (y+offsetY) + ':' + k

            img.style.top = 256*y+'px'
            img.style.left= 256*x+'px'
            if(slideX != null){
                img.style.left = slideX+'px'
                img.style.top = slideY+'px'
            }

            let str_id = img.id.split(':')
            img.width = 256
            img.height = 256

            let avv = 'http://localhost:8001/api/v1/projects/'+this.$route.params.projectName+'/tasks/'+this.$route.params.id+'/layer/'+str_id[2]+'/tile/'+str_id[0]+':'+str_id[1]

            //проверить на нужность
            img.onload = function() {   
                let tmpImages = document.createElement('img')
                tmpImages.src = avv
                this.width = tmpImages.width
                this.height = tmpImages.height
            }  
            
            img.src = avv
            img.alt = img.id
            
            return img
        },

        addRow(flag){
            let tileNet = document.getElementById('tileNet')
            let imgList = tileNet.getElementsByTagName('img')

            let last_tile = imgList[imgList.length-1];
            let first_tile = imgList[0];

            if (flag){
                for (let i=this.imageInfo.curTileW-1; i>=0; i--){
                    let x = Number(first_tile.id.split(':')[0])+i
                    let y = Number(first_tile.id.split(':')[1])-1
                    let slideX = Number(first_tile.style.left.split('px')[0]) + 256 * i 
                    let slideY = Number(first_tile.style.top.split('px')[0]) - 256 
                    let img = this.createTile(x, y, this.imageInfo.curLayer, 0, 0, slideX, slideY)
                    tileNet.prepend(img);
                }
            }
            else{
                for (let i=0; i<this.imageInfo.curTileW;i++){
                    let x = Number(first_tile.id.split(':')[0])+i
                    let y = Number(last_tile.id.split(':')[1])+1
                    let slideX = Number(first_tile.style.left.split('px')[0]) + 256 * i
                    let slideY = Number(last_tile.style.top.split('px')[0]) + 256
                    let img = this.createTile(x, y, this.imageInfo.curLayer, 0, 0, slideX, slideY)
                    tileNet.append(img)
                }
            }
            this.imageInfo.curTileH += 1;
        },
        deleteRow(flag){
            let tileNet = document.getElementById('tileNet')
            let imgList = tileNet.getElementsByTagName('img')
            if(flag){
                for (let i=this.imageInfo.curTileW-1; i>=0; i--){
                    imgList[i].remove();
                }
            }
            else{
                for (let i=0; i<this.imageInfo.curTileW;i++){
                    imgList[imgList.length-1].remove();
                }
            }
            this.imageInfo.curTileH -= 1;
        },

        addCol(flag){

            let tileNet = document.getElementById('tileNet')
            let imgList = tileNet.getElementsByTagName('img')

            let last_tile = imgList[imgList.length-1]
            let first_tile = imgList[0]
        
            for (let i=this.imageInfo.curTileH-1; i>=0; i--){
                if(flag){
                    let x = Number(first_tile.id.split(':')[0])-1
                    let y = Number(first_tile.id.split(':')[1])+i
                    let slideX = Number(first_tile.style.left.split('px')[0]) - 256
                    let slideY = Number(first_tile.style.top.split('px')[0]) + 256 * i
                    let img = this.createTile(x, y,this.imageInfo.curLayer, 0, 0, slideX, slideY)
                    imgList[this.imageInfo.curTileW * i].before(img)
                }
                else{
                    let x = Number(last_tile.id.split(':')[0])+1
                    let y = Number(first_tile.id.split(':')[1])+i
                    let slideX = Number(last_tile.style.left.split('px')[0]) + 256
                    let slideY = Number(first_tile.style.top.split('px')[0]) + 256 * i
                    let img = this.createTile(x, y,this.imageInfo.curLayer, 0, 0, slideX, slideY)
                    imgList[this.imageInfo.curTileW*(i+1)-1].after(img)
                }
            }
            this.imageInfo.curTileW += 1;
        },
        
        deleteCol(flag){
            let tileNet = document.getElementById('tileNet')
            let imgList = tileNet.getElementsByTagName('img')

            for (let i=this.imageInfo.curTileH-1; i>=0; i--){
            if(flag){
                imgList[this.imageInfo.curTileW*i].remove();
            }
            else{
                imgList[(this.imageInfo.curTileW*(i+1))-1].remove();
            }
            }
            this.imageInfo.curTileW -= 1;
        },

        monitorNetChange(){
            let tileNet = document.getElementById('tileNet')
            let imgList = tileNet.getElementsByTagName('img');
            let last_tile = imgList[imgList.length-1]
            let first_tile = imgList[0]
            if (( Number(first_tile.style.top.split('px')[0]) > 1) && (Number(first_tile.id.split(':')[1])>0)){
                this.addRow(true)
            }
            if((Number(last_tile.style.top.split('px')[0]) <tileNet.offsetHeight-256) && (Number(last_tile.id.split(':')[1])<this.imageInfo.countTileH-1)){
                this.addRow(false)
            }
            if ( Number(first_tile.style.top.split('px')[0]) < -256){
                this.deleteRow(true);
            }
            if ( Number(last_tile.style.top.split('px')[0]) > imgList.offsetHeight){
                this.deleteRow(false);
            }



            if ( Number(first_tile.style.left.split('px')[0]) > 1  && (Number(first_tile.id.split(':')[0])>0)){
                this.addCol(true);
            }
            if((Number(last_tile.style.left.split('px')[0]) < tileNet.offsetWidth-256) && (Number(last_tile.id.split(':')[0])<this.imageInfo.countTileW-1)){
                this.addCol(false);
            }
            if ( Number(first_tile.style.left.split('px')[0]) < -256){
                this.deleteCol(true);
            }
            if ( Number(last_tile.style.left.split('px')[0]) > tileNet.offsetWidth){
                this.deleteCol(false);
            }
        },


        mouseMove(event){
            let xy = null
            if (event.button === 1){
                window.onmousemove = (event)=>{
                    if(event.buttons != 4){ return } // убирает залипание
                    if(!xy){
                        xy = [event.x, event.y]
                    }
                    let dx = event.x - xy[0]
                    let dy = event.y - xy[1]
                    xy = [event.x, event.y]
                    this.moveAllImg(dx, dy)
                    this.monitorNetChange()
                }
            }
        },

        moveAllImg(dx, dy){
            let tileNet = document.getElementById('tileNet')
            let imgList = tileNet.getElementsByTagName('img')
            let widthLast = imgList[imgList.length-1].width
            let heightLast = imgList[imgList.length-1].height

            if (widthLast === 0){widthLast = 256}
  
            if (heightLast === 0){heightLast = 256}

            let heightNavBar = document.getElementsByClassName('navBar')[0].offsetHeight

            if(Number(imgList[0].id.split(':')[1]) === 0 && dy>0 && Number(imgList[0].style.top.split('px')[0])>=0){
                dy = 0
            }
            if (Number(imgList[imgList.length-1].style.top.split('px')[0])- 256 + heightLast < window.innerHeight- heightNavBar-256 && dy<0){        
                dy = 0
            }
        
            if(Number(imgList[0].id.split(':')[0]) === 0 && dx>0 && Number(imgList[0].style.left.split('px')[0])>=0 ){
                dx = 0
            }
            if (Number(imgList[imgList.length-1].style.left.split('px')[0])- 256 + widthLast < tileNet.offsetWidth-256 && dx<0){
                dx = 0
            }


            for(let i=0; i<imgList.length; i++){
                let x = Number(imgList[i].style.left.split('px')[0])
                let y = Number(imgList[i].style.top.split('px')[0])
                imgList[i].style.left = x + dx + 'px';
                imgList[i].style.top = y + dy  + 'px';
            }
        },

        getTile(event){
            let cnv_mask = SVG('#svg')
            cnv_mask.hide()
            let tile = document.elementFromPoint(event.clientX, event.clientY)
            cnv_mask.show()
            if (tile.tagName === 'IMG'){
                return tile    
            }
            return null
        },

        getPointInTile(event, curTile){
            let tileNet = document.getElementById('tileNet')
            let imgList = tileNet.getElementsByTagName('img')
            let first_tile = imgList[0]
            let x = event.offsetX - ((Number(curTile.id.split(':')[0]) - Number(first_tile.id.split(':')[0])) * 256 + Number(first_tile.style.left.split('px')[0])) 
            let y = event.offsetY - ((Number(curTile.id.split(':')[1]) - Number(first_tile.id.split(':')[1])) * 256 + Number(first_tile.style.top.split('px')[0])) 
            return [x, y]
        },

        getPointInImg(event, curTile){
            let xy = this.getPointInTile(event, curTile);
            let x = xy[0] + Number(curTile.id.split(':')[0]) * 256;
            let y = xy[1] + Number(curTile.id.split(':')[1]) * 256;
            return [x*Math.pow(2,this.imageInfo.curLayer), y*Math.pow(2,this.imageInfo.curLayer)]
        },

        calcIdFirstBlock(curTile,  flag){
            let tileNet = document.getElementById('tileNet')
            let imgList = tileNet.getElementsByTagName('img')

            let first_tile = imgList[0]
            let numberTileX = Number(curTile.id.split(':')[0]) - Number(first_tile.id.split(':')[0])
            let numberTileY = Number(curTile.id.split(':')[1]) - Number(first_tile.id.split(':')[1])
            if(flag === '+'){
                return [Number(curTile.id.split(':')[0])*2 - numberTileX, Number(curTile.id.split(':')[1])*2 - numberTileY]
            }
            if(flag === '-'){
                let x = Math.ceil(Number(curTile.id.split(':')[0])/2) - numberTileX
                if (x<0){ x = 0}
                let y = Math.ceil(Number(curTile.id.split(':')[1])/2) - numberTileY
                if (y<0){ y = 0}
                return [x, y]
            }
        },

        deleteNet(){
            let tileNet = document.getElementById('tileNet')
            let imgList = tileNet.getElementsByTagName('img')

            for (let i=imgList.length-1; i>=0; i--){
                imgList[i].remove()
            }
        },

        updateCountTile(){
            console.log('cur layer == ', this.imageInfo.curLayer)
            this.imageInfo.countTileW = Math.ceil((this.imageInfo.width/2**this.imageInfo.curLayer)/256);
            this.imageInfo.countTileH = Math.ceil((this.imageInfo.height/2**this.imageInfo.curLayer)/256);
            console.log(this.imageInfo.countTileW, this.imageInfo.countTileH)
        },

        dXdY(start, xy, point){
            let dx = (256*start[0]+xy[0]) - point[0]/Math.pow(2,this.imageInfo.curLayer);
            let dy = (256*start[1]+xy[1]) - point[1]/Math.pow(2,this.imageInfo.curLayer);
            return [dx, dy]
        },

        scaleImg(event, flag){
            let tile = this.getTile(event)
            if (!tile){
                return 
            }
            let point = this.getPointInImg(event, tile)
            let startNewTile
            if(flag === '+'){
                if (this.imageInfo.curLayer-1<0){return}
                startNewTile = this.calcIdFirstBlock(tile, '+')
                this.imageInfo.curLayer -= 1
                // scaleSVG('+', startNewTile)
            }
            if(flag === '-'){
                if (this.imageInfo.curLayer>=this.imageInfo.countLayers-1){return 1}
                startNewTile = this.calcIdFirstBlock(tile, '-')
                this.imageInfo.curLayer += 1
                // scaleSVG('-', startNewTile)
            }
            this.deleteNet()
            this.updateCountTile();
            this.createNet(startNewTile[1], startNewTile[0]);
            let dxdy = this.dXdY(startNewTile,[event.offsetX, event.offsetY], point);
            this.moveAllImg(dxdy[0], dxdy[1]);
            this.monitorNetChange();

        },

        onWheel(event){
            if (event.deltaY<0){ this.scaleImg(event, '+'); }
            else{ this.scaleImg(event, '-'); }
        }
    },
    components:{TileNet}
    
}
</script>

<style>

.edit { 
    grid-area: edit;
    overflow: auto;
    display: inline-block;
    position: relative;
    background: #F6F8FA;
    height: 100%;
    width: 100%;
    user-select:none;
    overflow: hidden;
}

#tileNet{
    display: block;
    position: absolute;
    height: 100%;
    width: 100%;
}



#svg { /* <= optional, for responsiveness */
    display: block;
    position: absolute;
    height: 100%;
    width: 100%;
}


</style>