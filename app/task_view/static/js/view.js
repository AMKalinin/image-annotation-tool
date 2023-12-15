let  imagesInfo = new Object()


var done_btn = document.getElementById('btn_chng_status_done');
var return_btn = document.getElementById('btn_chng_status_ret');
var view_win = document.getElementsByClassName('view')[0];
const plus = document.getElementById('plus');
const minus = document.getElementById('minus');
const mashtab = document.getElementById('mashtab');


let cnv_block = document.getElementById('canvas_block');
let cnv_mask = SVG('#svg');


var R = 8;

function getImgInfo(){
    let taskInformation = window.location.pathname.split('/');
    imagesInfo.projectName = taskInformation[2];
    imagesInfo.taskIndex = taskInformation.slice(-1)[0];
    let url = '/get_img_info/'+imagesInfo.projectName+'/'+imagesInfo.taskIndex;
    let handler = (res)=>{
        imagesInfo.file_name = res.response.file_name;
        
        imagesInfo.height = res.response.height;
        imagesInfo.width = res.response.width;
        
        imagesInfo.countLayers = res.response.layers;
        imagesInfo.curLayer = 0; //res.response.layers-1;
        
        imagesInfo.countTileW = Math.ceil((imagesInfo.width/2**imagesInfo.curLayer)/256);
        imagesInfo.countTileH = Math.ceil((imagesInfo.height/2**imagesInfo.curLayer)/256);

        imagesInfo.curTileW = Math.ceil(cnv_block.offsetWidth/256);
        if(imagesInfo.countTileW < imagesInfo.curTileW){
            imagesInfo.curTileW = imagesInfo.countTileW;   
        }
        
        imagesInfo.curTileH = Math.ceil(cnv_block.offsetHeight/256);
        if(imagesInfo.countTileH < imagesInfo.curTileH){
            imagesInfo.curTileH = imagesInfo.countTileH;
        }
        createNet(0, 0);
    }
    sendRequest(url, 'POST', null, handler, 'json');
}

function updateCountTile(){
    imagesInfo.countTileW = Math.ceil((imagesInfo.width/2**imagesInfo.curLayer)/256);
    imagesInfo.countTileH = Math.ceil((imagesInfo.height/2**imagesInfo.curLayer)/256);
}

function onLoad(){
    setInterval(availability_check, 10*1000);

    getImgInfo();

    createAllMask();
}

function createTile(j, i, k, offsetX, offsetY, slideX=null, slideY=null){
    let img = document.createElement('img');
    img.style.position = 'absolute';
    img.id = (j+offsetX) + ':' + (i+offsetY) + ':' + k;
    if(slideX){
        img.style.left = slideX;
        img.style.top = slideY;
    }
    else{
        img.style.top = 256*i+'px';
        img.style.left= 256*j+'px';
    }
    let str_id = img.id.split(':')
    img.width = 256;
    img.height = 256;

    img.onload = function() {   
        let tmpImages = document.createElement('img');
        tmpImages.src = "/task_tail/"+imagesInfo.projectName+'/'+imagesInfo.taskIndex+'/'+str_id[0]+"/"+str_id[1]+"/"+str_id[2];
        this.width = tmpImages.width;
        this.height = tmpImages.height;
      }  

    img.src = "/task_tail/"+imagesInfo.projectName+'/'+imagesInfo.taskIndex+'/'+str_id[0]+"/"+str_id[1]+"/"+str_id[2];
    img.alt = img.id
    return img
}

function createNet(topInd, leftInd){
    while(leftInd+imagesInfo.curTileW>imagesInfo.countTileW){
        imagesInfo.curTileW -= 1 
    }
    while(topInd+imagesInfo.curTileH>imagesInfo.countTileH){
        imagesInfo.curTileH -= 1 
    }

    for (let i=0; i<imagesInfo.curTileH;i++){
        for (let j=0; j<imagesInfo.curTileW;j++){
            let tile = createTile(j, i, imagesInfo.curLayer, leftInd, topInd);
            cnv_block.append(tile);
        }   
    }
}

function deleteNet(){
    let imgList = cnv_block.getElementsByTagName('img');
    for (let i=imgList.length-1; i>=0; i--){
        imgList[i].remove();
    }
}


function addRow(flag){
    let imgList = cnv_block.getElementsByTagName('img');
    let last_tile = imgList[imgList.length-1];
    let first_tile = imgList[0];
        if (flag){
            for (let i=imagesInfo.curTileW-1; i>=0; i--){
                let x = Number(first_tile.id.split(':')[0])+i;
                let y = Number(first_tile.id.split(':')[1])-1;
                let slideX = Number(first_tile.style.left.split('px')[0]) + 256 * i + 'px';
                let slideY = Number(first_tile.style.top.split('px')[0]) - 256 + 'px';
                let img = createTile(x, y, imagesInfo.curLayer, 0, 0, slideX, slideY);
                cnv_block.prepend(img);
            }
        }
        else{
            for (let i=0; i<imagesInfo.curTileW;i++){
                let x = Number(first_tile.id.split(':')[0])+i;
                let y = Number(last_tile.id.split(':')[1])+1;
                let slideX = Number(first_tile.style.left.split('px')[0]) + 256 * i + 'px';
                let slideY = Number(last_tile.style.top.split('px')[0]) + 256 + 'px';
                let img = createTile(x, y, imagesInfo.curLayer, 0, 0, slideX, slideY);
                cnv_block.append(img);
            }
        }
        imagesInfo.curTileH += 1;
 }

function deleteRow(flag){
    let imgList = cnv_block.getElementsByTagName('img');
    if(flag){
        for (let i=imagesInfo.curTileW-1; i>=0; i--){
            imgList[i].remove();
        }
    }
    else{
        for (let i=0; i<imagesInfo.curTileW;i++){
            imgList[imgList.length-1].remove();
        }
    }
    imagesInfo.curTileH -= 1;
}

function addCol(flag){
    let imgList = cnv_block.getElementsByTagName('img');
    let last_tile = imgList[imgList.length-1]
    let first_tile = imgList[0]
  
    for (let i=imagesInfo.curTileH-1; i>=0; i--){
        if(flag){
            let x = Number(first_tile.id.split(':')[0])-1;
            let y = Number(first_tile.id.split(':')[1])+i;
            let slideX = Number(first_tile.style.left.split('px')[0]) - 256 + 'px';
            let slideY = Number(first_tile.style.top.split('px')[0]) + 256 * i + 'px';
            let img = createTile(x, y,imagesInfo.curLayer, 0, 0, slideX, slideY);
            imgList[imagesInfo.curTileW * i].before(img);
        }
        else{
            let x = Number(last_tile.id.split(':')[0])+1;
            let y = Number(first_tile.id.split(':')[1])+i;
            let slideX = Number(last_tile.style.left.split('px')[0]) + 256 + 'px';
            let slideY = Number(first_tile.style.top.split('px')[0]) + 256 * i + 'px';
            let img = createTile(x, y,imagesInfo.curLayer, 0, 0, slideX, slideY);
            imgList[imagesInfo.curTileW*(i+1)-1].after(img);
        }
    }
    imagesInfo.curTileW += 1;
}

function deleteCol(flag){
    let imgList = cnv_block.getElementsByTagName('img');
    for (let i=imagesInfo.curTileH-1; i>=0; i--){
      if(flag){
        imgList[imagesInfo.curTileW*i].remove();
      }
      else{
        imgList[(imagesInfo.curTileW*(i+1))-1].remove();
      }
    }
    imagesInfo.curTileW -= 1;
  }

function monitorNetChange(){
    let imgList = cnv_block.getElementsByTagName('img');
    let last_tile = imgList[imgList.length-1]
    let first_tile = imgList[0]

    if (( Number(first_tile.style.top.split('px')[0]) > 1) && (Number(first_tile.id.split(':')[1])>0)){
      addRow(true);
    }
    if((Number(last_tile.style.top.split('px')[0]) < cnv_block.offsetHeight-256) && (Number(last_tile.id.split(':')[1])<imagesInfo.countTileH-1)){
      addRow(false);
    }
    if ( Number(first_tile.style.top.split('px')[0]) < -256){
      deleteRow(true);
    }
    if ( Number(last_tile.style.top.split('px')[0]) > cnv_block.offsetHeight){
      deleteRow(false);
    }



    if ( Number(first_tile.style.left.split('px')[0]) > 1  && (Number(first_tile.id.split(':')[0])>0)){
      addCol(true);
    }
    if((Number(last_tile.style.left.split('px')[0]) < cnv_block.offsetWidth-256) && (Number(last_tile.id.split(':')[0])<imagesInfo.countTileW-1)){
      addCol(false);
    }
    if ( Number(first_tile.style.left.split('px')[0]) < -256){
      deleteCol(true);
    }
    if ( Number(last_tile.style.left.split('px')[0]) > cnv_block.offsetWidth){
      deleteCol(false);
    }
}


function scaleSVG(flag, start){

    let coef;
    if (flag === '+'){
        coef = 2;
    }
    if (flag === '-'){
        coef = 1/2;
    }

    cnv_mask.each(function(i, children){
        if (this.type === 'polygon' || this.type === 'polyline'){
            let a = this.array();
            for(let i=0; i<a.length; i++){
                a[i] = [a[i][0]*coef, a[i][1]*coef]; 
            }
            this.plot(a);   
            this.transform({translateX: -256*start[0], translateY: -256*start[1]});
        }
        else if (this.type === 'rect'){
            let w = this.width()*coef;
            let h = this.height()*coef;
            this.attr('width', w);
            this.attr('height', h);
            this.attr('height', h);
            this.move(this.x()*coef, this.y()*coef)
            this.transform({translateX: -256*start[0], translateY: -256*start[1]});
        }
        else if (this.type === 'circle'){
            this.move(this.x()*coef, this.y()*coef)
            this.transform({translateX: -256*start[0], translateY: -256*start[1]});
        }
    }) 
}

function scaleMask(mask){
    let coef = 1/Math.pow(2, imagesInfo.curLayer);
    if (mask.type === 'polygon'){
        let a = mask.array();
        for(let i=0; i<a.length; i++){
            a[i] = [a[i][0]*coef, a[i][1]*coef]; 
        }
        mask.plot(a);   
        // mask.transform({translateX: -256*start[0], translateY: -256*start[1]});
    }
}

function firstOffset(){
    let imgList = cnv_block.getElementsByTagName('img');
    let first_tile = imgList[0];
    let dx =  Number(first_tile.style.left.split('px')[0])- Number(first_tile.id.split(':')[0])*256;
    let dy =  Number(first_tile.style.top.split('px')[0]) - Number(first_tile.id.split(':')[1])*256;
    return [dx, dy]
}

function getTile(event){
    cnv_mask.hide();
    let tile = document.elementFromPoint(event.clientX, event.clientY);
    cnv_mask.show();
    return tile
}

function getPointInTile(event, curTile){
    let imgList = cnv_block.getElementsByTagName('img');
    let first_tile = imgList[0];
    let x = event.offsetX - ((Number(curTile.id.split(':')[0]) - Number(first_tile.id.split(':')[0])) * 256 + Number(first_tile.style.left.split('px')[0])) ;
    let y = event.offsetY - ((Number(curTile.id.split(':')[1]) - Number(first_tile.id.split(':')[1])) * 256 + Number(first_tile.style.top.split('px')[0])) ;
    return [x, y]
}
  
function getPointInImg(event, curTile){
    let xy = getPointInTile(event, curTile);
    let x = xy[0] + Number(curTile.id.split(':')[0]) * 256;
    let y = xy[1] + Number(curTile.id.split(':')[1]) * 256;
    return [x*Math.pow(2,imagesInfo.curLayer), y*Math.pow(2,imagesInfo.curLayer)]
}

function calcIdFirstBlock(curTile,  flag){
    let imgList = cnv_block.getElementsByTagName('img');
    let first_tile = imgList[0];
    let numberTileX = Number(curTile.id.split(':')[0]) - Number(first_tile.id.split(':')[0]);
    let numberTileY = Number(curTile.id.split(':')[1]) - Number(first_tile.id.split(':')[1]);
    if(flag === '+'){
        return [Number(curTile.id.split(':')[0])*2 - numberTileX, Number(curTile.id.split(':')[1])*2 - numberTileY];
    }
    if(flag === '-'){
        let x = Math.ceil(Number(curTile.id.split(':')[0])/2) - numberTileX;
        if (x<0){ x = 0}
        let y = Math.ceil(Number(curTile.id.split(':')[1])/2) - numberTileY;
        if (y<0){ y = 0}
        return [x, y];
    }
}

function dXdY(start, xy, point){
    let dx = (256*start[0]+xy[0]) - point[0]/Math.pow(2,imagesInfo.curLayer);
    let dy = (256*start[1]+xy[1]) - point[1]/Math.pow(2,imagesInfo.curLayer);
    return [dx, dy]
}

function scaleImg(event, flag){
    let tile = getTile(event); 
    let point = getPointInImg(event, tile);
    let startNewTile;
    if(flag === '+'){
        if (imagesInfo.curLayer-1<0){return}
        startNewTile = calcIdFirstBlock(tile, '+');
        imagesInfo.curLayer -= 1;
        scaleSVG('+', startNewTile);
    }
    if(flag === '-'){
        if (imagesInfo.curLayer>=imagesInfo.countLayers-1){return 1}
        startNewTile = calcIdFirstBlock(tile, '-');
        imagesInfo.curLayer += 1;
        scaleSVG('-', startNewTile);
    }
    deleteNet();
    updateCountTile();
    createNet(startNewTile[1], startNewTile[0]);
    let dxdy = dXdY(startNewTile,[event.offsetX, event.offsetY], point);
    moveAllImg(dxdy[0], dxdy[1]);
    monitorNetChange();

}

function moveAllImg(dx, dy){
    let imgList = cnv_block.getElementsByTagName('img');
    let widthLast = imgList[imgList.length-1].width; 
    let heightLast = imgList[imgList.length-1].height; 
    
    if (widthLast === 0){widthLast = 256;}
  
    if (heightLast === 0){heightLast = 256;}
  
    let heightNavBar = document.getElementsByClassName('nav_bar')[0].offsetHeight; 
    if(Number(imgList[0].id.split(':')[1]) === 0 && dy>0 && Number(imgList[0].style.top.split('px')[0])>=0){
        dy = 0
    }
    if (Number(imgList[imgList.length-1].style.top.split('px')[0])- 256 + heightLast < window.innerHeight- heightNavBar-256 && dy<0){        
        dy = 0
    }
  
    if(Number(imgList[0].id.split(':')[0]) === 0 && dx>0 && Number(imgList[0].style.left.split('px')[0])>=0 ){
        dx = 0
    }
    if (Number(imgList[imgList.length-1].style.left.split('px')[0])- 256 + widthLast < cnv_block.offsetWidth-256 && dx<0){
        dx = 0
    }
    for(let i=0; i<imgList.length; i++){
        let x = Number(imgList[i].style.left.split('px')[0])
        let y = Number(imgList[i].style.top.split('px')[0])
        imgList[i].style.left = x + dx + 'px';
        imgList[i].style.top = y + dy  + 'px';
    }
    cnv_mask.each(function(i, children){
        let curTrans = this.transform();
        this.transform({translateX: curTrans.translateX+dx, 
                        translateY: curTrans.translateY+dy});
    }) 
  }


function onWheel(event){
    if (event.deltaY<0){ scaleImg(event, '+'); }
    else{ scaleImg(event, '-'); }
}


function mouseDown(e){

    let xy = null;
    if (e.button === 1){
        window.onmousemove = (event)=>{
            if(event.buttons != 4){
                return
            }
            if(!xy){
                xy = [event.x, event.y]
            }
            let dx = event.x - xy[0];
            let dy = event.y - xy[1];
            xy = [event.x, event.y];
            moveAllImg(dx, dy);
            monitorNetChange();
        }
    }
}



window.onload = onLoad;
cnv_mask.on('mousedown', mouseDown);
cnv_mask.on('wheel', onWheel);

done_btn.addEventListener('click', (event)=>{
    send_info2('>>');
})

return_btn.addEventListener('click', (event)=>{
    send_info2('<<');
})