let  imagesInfo = new Object()

let cnv_block = document.getElementById('canvas_block');
let cnv_mask = SVG('#svg');


var R = 8;

const tools = document.getElementsByClassName('mark');
let curTool = 'None';

const modes = ['edit', 'create']
let curMode = 'None';

const btnChangeStatus = document.getElementById('btn_chng_status');

let curShape = {
    points: [],
    type: null,
    code: '000',
    tellApartDistance: 5,
    pointIndex:-1,
    object: null,
    maskID: null,
    group: null
};


function switchMode(){
    if (curMode === modes[0]){
        curShape.points = [];
        curShape.object.node.style.display = 'none';
        curShape.object = null;
        curShape.group.remove();
        curShape.group = null;
        curMode = 'create';
    }
    else if (curShape.object){
        curShape.points = [];
        curShape.object.remove();
        curShape.object = null;
        curShape.group.remove();
        curShape.group = null;
    };
}

function addToolListClick(){
    for (let i = 0; i<tools.length; i++){
        tools[i].addEventListener('click', () => {
            curTool = tools[i].id;
            curShape.type = tools[i].id;

            for (let n = 0; n<tools.length; n++){
                if (i === n){tools[n].getElementsByTagName('img')[0].style.background = '#a8a8a8'}
                else{tools[n].getElementsByTagName('img')[0].style.background = ''}
            }
            switchMode()
        });
    };
};


function pointIt(event){
    var pointX = parseInt(event.pageX)
    var pointY = parseInt(event.pageY)
    if (pointX < 0){pointX = 0}
    if (pointY < 0){pointY = 0}
    return [pointX, pointY]
};

function pointAtPos(pointWind){
    let point;
    if (!curShape.object){
        point = cnv_mask.point(pointWind[0], pointWind[1])}
    else{
        point = curShape.object.point(pointWind[0], pointWind[1])
    }
    for  (let i = 0; i<curShape.points.length; i++){
        if (distance([point.x, point.y], curShape.points[i]) < curShape.tellApartDistance){
            
            return i;
        }
    }
    return -1;
};



function drawPolygon(){
    if (!curShape.object){
        curShape.object = cnv_mask.polygon(curShape.points).fill('none').stroke({ width: 2,  color: '#000000'});
        curShape.group = cnv_mask.group();
        let dxdy = firstOffset();
        curShape.object.transform({translateX: dxdy[0], translateY: dxdy[1]});
    }
    else{
        curShape.object.plot(curShape.points);
        if (curShape.group){
            curShape.group.remove();
            curShape.group = cnv_mask.group();
        }
    }
    drawGroup();
};

function drawLine(){
    if (!curShape.object){
        curShape.object = cnv_mask.polyline(curShape.points).fill('none').stroke({ width: 2,  color: '#000000'});
        curShape.group = cnv_mask.group();
        let dxdy = firstOffset();
        curShape.object.transform({translateX: dxdy[0], translateY: dxdy[1]});
    }
    else{
        curShape.object.plot(curShape.points);
        if (curShape.group){
            curShape.group.remove();
            curShape.group = cnv_mask.group();
        }
    }
    drawGroup();
};

function drawRect(){
    let width = curShape.points[1][0] - curShape.points[0][0];
    let height = curShape.points[2][1] - curShape.points[1][1];
    let x;
    let y;
    if (width<0){x = curShape.points[1][0]}
    else {x = curShape.points[0][0] }
    if (height<0){y = curShape.points[2][1]}
    else {y = curShape.points[0][1] }

    if (curShape.object){
        curShape.object.size(Math.abs(width), Math.abs(height)).move(x, y);
        curShape.group.remove();
    }
    else{
        let dxdy = firstOffset();
        curShape.object = cnv_mask.rect(Math.abs(width), Math.abs(height))
                                    .move(x, y)
                                    .fill('none').stroke({ width: 2,  color: '#000000'});
        
        curShape.object.transform({translateX: dxdy[0], translateY: dxdy[1]});
    }

    curShape.group = cnv_mask.group();
    drawGroup();
    
};

function drawPoint(){
    if (curShape.object){
        curShape.object.move(curShape.points[0][0]-R/2, curShape.points[0][1]-R/2);
    }
    else{
        let dxdy = firstOffset();
        curShape.object = cnv_mask.circle(R).move(curShape.points[0][0]-R/2, curShape.points[0][1]-R/2)
                                            .fill('#000000').stroke({ width: 1,  color: '#000000'});

        curShape.object.transform({translateX: dxdy[0], translateY: dxdy[1]});
    }
    

}

function drawCircle(){
    let radius = distance(curShape.points[0],curShape.points[1])

    if (curShape.object){
        curShape.object.radius(radius)
        curShape.group.remove();
    }
    else{
        let dxdy = firstOffset();
        curShape.object = cnv_mask.ellipse(radius).move(curShape.points[0][0]-radius/2, curShape.points[0][1]-radius/2)
                                            .fill('none').stroke({ width: 2,  color: '#000000'});
        
        curShape.object.transform({translateX: dxdy[0], translateY: dxdy[1]});
    }

    curShape.group = cnv_mask.group();
    drawGroup();
    
};

function drawGroup(){
    let len = curShape.points.length;
    for (let i = 0; i<len; i++){
        if(i === 0)
        {
            var circle = cnv_mask.circle(R).move(curShape.points[i][0]-R/2, curShape.points[i][1]-R/2)
                                            .fill('green').stroke({ width: 1,  color: '#000000'});
        }
        else if(i === len-1)
        {
            var circle = cnv_mask.circle(R).move(curShape.points[i][0]-R/2, curShape.points[i][1]-R/2)
                                            .fill('red').stroke({ width: 1,  color: '#000000'});
        }
        else {
            var circle = cnv_mask.circle(R).move(curShape.points[i][0]-R/2, curShape.points[i][1]-R/2)
                                            .fill('white').stroke({ width: 1,  color: '#000000'});
        }  
        curShape.group.add(circle);
        curShape.group.transform(curShape.object.transform());
    }
}

function setPointRect(ind, point){
    switch(ind){
        case 0:
            curShape.points[0] = point;
            curShape.points[1] = [curShape.points[2][0], curShape.points[0][1]];
            curShape.points[3] = [curShape.points[0][0], curShape.points[2][1]];
            break;
        case 1:
            curShape.points[1] = point;
            curShape.points[0] = [curShape.points[3][0], curShape.points[1][1]];
            curShape.points[2] = [curShape.points[1][0], curShape.points[3][1]];
            break;
        case 2:
            curShape.points[2] = point;
            curShape.points[1] = [curShape.points[2][0], curShape.points[0][1]];
            curShape.points[3] = [curShape.points[0][0], curShape.points[2][1]];
            break;
        case 3:
            curShape.points[3] = point;
            curShape.points[0] = [curShape.points[3][0], curShape.points[1][1]];
            curShape.points[2] = [curShape.points[1][0], curShape.points[3][1]];
            break;
        
    }
};

// ////////////////////////////////////////////////////////////////////////////
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

    addToolListClick();
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

function mouseDown(e){

    let tile1 = getTile(e); 
    let point2 = getPointInImg(e, tile1);
    console.log(point2)

    let point1 = pointIt(e);
    curShape.pointIndex = pointAtPos(point1);

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
    else if(e.button === 0){
        if (curShape.pointIndex > -1){ return 1}
        let tile = getTile(e); 
        let point = getPointInImg(e, tile);
        console.log(point)
        if (curTool === 'rect'){
            if (curShape.points.length == 0 ){
                curShape.points.push([point[0]/Math.pow(2,imagesInfo.curLayer), point[1]/Math.pow(2,imagesInfo.curLayer)]);
                curShape.points.push([point[0]/Math.pow(2,imagesInfo.curLayer), point[1]/Math.pow(2,imagesInfo.curLayer)]);
                curShape.points.push([point[0]/Math.pow(2,imagesInfo.curLayer), point[1]/Math.pow(2,imagesInfo.curLayer)]);
                curShape.points.push([point[0]/Math.pow(2,imagesInfo.curLayer), point[1]/Math.pow(2,imagesInfo.curLayer)]);
            }
            else{
                curShape.points[0]= [point[0]/Math.pow(2,imagesInfo.curLayer), point[1]/Math.pow(2,imagesInfo.curLayer)];
                curShape.points[1]= [point[0]/Math.pow(2,imagesInfo.curLayer), point[1]/Math.pow(2,imagesInfo.curLayer)];
                curShape.points[2]= [point[0]/Math.pow(2,imagesInfo.curLayer), point[1]/Math.pow(2,imagesInfo.curLayer)];
                curShape.points[3]= [point[0]/Math.pow(2,imagesInfo.curLayer), point[1]/Math.pow(2,imagesInfo.curLayer)];
            }
            drawRect();
        }
        else if (curTool === 'point'){
            if (curShape.points.length == 0 ){
                curShape.points.push([point[0]/Math.pow(2,imagesInfo.curLayer), point[1]/Math.pow(2,imagesInfo.curLayer)]);
            }
            else{
                curShape.points[0]= [point[0]/Math.pow(2,imagesInfo.curLayer), point[1]/Math.pow(2,imagesInfo.curLayer)];
            }
        }
        else if (curTool === 'circle'){
            if (curShape.points.length == 0 ){
                curShape.points.push([point[0]/Math.pow(2,imagesInfo.curLayer), point[1]/Math.pow(2,imagesInfo.curLayer)]);
                curShape.points.push([point[0]/Math.pow(2,imagesInfo.curLayer), point[1]/Math.pow(2,imagesInfo.curLayer)]);
            }
            else{
                curShape.points[1]= [point[0]/Math.pow(2,imagesInfo.curLayer), point[1]/Math.pow(2,imagesInfo.curLayer)];
            }
            drawCircle()
        }
    }
    else if(e.button === 2){
        if (curTool === 'polygon'){
            if (curShape.pointIndex > -1){
                curShape.points.splice(curShape.pointIndex, 1);
                drawPolygon();
            }
        }
        else if (curTool === 'line'){
            if (curShape.pointIndex > -1){
                curShape.points.splice(curShape.pointIndex, 1);
                drawLine();
            }
        }
    };
}

function mouseMove(event){
    var pointWind = pointIt(event);
    if (event.buttons === 1){
        if (curTool === 'polygon' || curTool === 'line'){
            if (curShape.pointIndex > -1){
            let point = curShape.object.point(pointWind[0], pointWind[1]);
            curShape.points[curShape.pointIndex] = [point.x,point.y];
            drawPolygon();
            }
        }
        else if (curTool === 'rect'){
            let point = curShape.object.point(pointWind[0], pointWind[1]);
            if (curShape.pointIndex > -1){
                setPointRect(curShape.pointIndex, [point.x, point.y])
            }
            else if (curShape.points.length === 4){
                curShape.points[2] = [point.x, point.y];
                curShape.points[1] = [curShape.points[2][0], curShape.points[0][1]];
                curShape.points[3] = [curShape.points[0][0], curShape.points[2][1]];
            }
            drawRect();
        }
        else if (curTool === 'point'){
            let point = curShape.object.point(pointWind[0], pointWind[1]);
            if (curShape.pointIndex > -1){
                curShape.points[curShape.pointIndex]= [point.x, point.y];
            }
            drawPoint();
        }
        else if (curTool === 'circle'){
            let point = curShape.object.point(pointWind[0], pointWind[1]);
            curShape.points[1] = [point.x, point.y];
            drawCircle();
        }
    }
}

function mouseUp(event){
    if (event.button === 0){    
        if (curShape.pointIndex == -1){
            if (curTool === 'polygon'){
                let tile = getTile(event); 
                let point = getPointInImg(event, tile);
                curShape.points.push([point[0]/Math.pow(2,imagesInfo.curLayer), point[1]/Math.pow(2,imagesInfo.curLayer)]);
                drawPolygon();

            }
            else if (curTool === 'rect'){
                if (curShape.points.length == 4){
                    drawRect();
                }
            }
            else if (curTool === 'line'){
                let tile = getTile(event); 
                let point = getPointInImg(event, tile);
                curShape.points.push([point[0]/Math.pow(2,imagesInfo.curLayer), point[1]/Math.pow(2,imagesInfo.curLayer)]);
                drawLine();
            }
            else if (curTool === 'point'){
                if (curShape.points.length == 1){
                    drawPoint();
                }
            }
            else if (curTool === 'circle'){
                let tile = getTile(event); 
                let point = getPointInImg(event, tile);
                curShape.points[1] = [point[0]/Math.pow(2,imagesInfo.curLayer), point[1]/Math.pow(2,imagesInfo.curLayer)];
                drawCircle();
            }
        }
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


    if(curShape){
        for(let i=0; i<curShape.points.length; i++){
            curShape.points[i] = [curShape.points[i][0]*coef, curShape.points[i][1]*coef]; 
        }
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
        else if (this.type === 'g'){
            this.remove();
            curShape.group = cnv_mask.group();
            drawGroup();
        }
        else if (this.type === 'rect'){
            let w = this.width()*coef;
            let h = this.height()*coef;
            this.attr('width', w);
            this.attr('height', h);
            this.move(this.x()*coef, this.y()*coef)
            this.transform({translateX: -256*start[0], translateY: -256*start[1]});
        }
        else if (this.type === 'circle'){
            this.move(this.x()*coef, this.y()*coef)
            this.transform({translateX: -256*start[0], translateY: -256*start[1]});
        }
        else if (this.type === 'ellipse'){
            this.radius(this.rx()*coef, this.ry()*coef)
            
            if (flag === '+'){
                this.move(this.x()*coef+this.rx(), this.y()*coef+this.rx())
            }
            else if (flag === '-'){
                this.move(this.x()*coef-this.rx()/2, this.y()*coef-this.rx()/2)
            }
            
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
    if (tile.tagName === 'IMG'){
        return tile    
    }
    return null
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
    if (!tile){
        return 
    }
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


function sendInfo(){
    let url = "/task_edit/change_task";
    if (curShape.object){
        curShape.object.remove();
        curShape.object = null;
        if(curShape.group){
            curShape.group.remove();
            curShape.group = null;
        }  
    }

    let info = new Object();
    info.code = document.getElementById('mask_class_base').value.split(';')[0];
    info.points = curShape.points;
    info.type = curShape.type;
    info.taskIndex = imagesInfo.taskIndex;
    info.projectName = imagesInfo.projectName;

    let handler = (res)=>{
        maskaDOM = res.responseXML.getElementsByClassName('maska')[0];
        let cntr = document.getElementsByClassName('masks_list')[0];
        cntr.append(maskaDOM);

        let points_str =  maskaDOM.getElementsByTagName('input')[0].value.split(';')[0];
        let points = str_to_pointslist(points_str);
        let coef = 1/Math.pow(2, imagesInfo.curLayer);
        for(let i=0; i<points.length; i++){
            points[i] = [points[i][0]*coef, points[i][1]*coef]; 
        }
        
        let index = maskaDOM.getElementsByClassName('mask_index')[0].textContent.split(' ')[1]
        let clr = maskaDOM.getElementsByTagName('input')[0].value.split(';')[1];
        let type = maskaDOM.getElementsByClassName('type')[0].innerHTML.split(' ')[1];

        let a = createMask(cnv_mask, maskaDOM, points, clr, type, index);
        let dxdy = firstOffset();
        a.transform({translateX: dxdy[0], translateY: dxdy[1]});
        curShape.points = [];
        
        maskaDOM.getElementsByClassName('maska_view_check')[0].checked = true;
        maskaDOM.getElementsByClassName('maska_view_check')[0].dispatchEvent(new Event('change'));
    }
    console.log(distance(info.points[0], info.points[1]))
    for(let i=0; i<info.points.length; i++){
        info.points[i] = [Math.trunc(info.points[i][0]*Math.pow(2,imagesInfo.curLayer)), Math.trunc(info.points[i][1]*Math.pow(2,imagesInfo.curLayer))]
    }
    console.log(distance(info.points[0], info.points[1]))
    sendRequest(url, 'POST', info, handler, 'document');
};


function changeMaskPoint(){
    let url = "/task_edit/change_mask_point";
    
    for(let i=0; i<curShape.points.length; i++){
        // curShape.points[i] = [curShape.points[i][0]*Math.pow(2,imagesInfo.curLayer), curShape.points[i][1]*Math.pow(2,imagesInfo.curLayer)]
        curShape.points[i] = [Math.trunc(curShape.points[i][0]*Math.pow(2,imagesInfo.curLayer)), Math.trunc(curShape.points[i][1]*Math.pow(2,imagesInfo.curLayer))]
    }

    var tmp = '[';
    let len = curShape.points.length;
    for (let i = 0; i<len; i++){
        let a = '['.concat(curShape.points[i].join(', ')).concat(']');
        if (i != (len-1)){tmp = tmp.concat(a).concat(', ');}
        else {tmp = tmp.concat(a).concat(']');}
    }

    maska_list[Number(curShape.object.node.id.split('_')[1])].getElementsByTagName('input')[0].value = tmp;

    if (curMode === 'edit'){
        curShape.object.node.style.display = 'none';
        curShape.object = null;
        curShape.group.remove();
        curShape.group = null;
        curMode = 'create';
    }


    let info = new Object();
    info.points = curShape.points;
    info.taskIndex = imagesInfo.taskIndex;
    info.projectName = imagesInfo.projectName;
    info.maskID = curShape.maskID;
    let handler = (res)=>{curShape.points = [];};
    sendRequest(url, 'POST', info, handler, 'document');
};

function keyDown(event){
    if (event.key === 'Enter'){
        if (curShape.points.length>=2 || (curShape.points.length === 1 && curTool === 'point')){
            if (curMode == 'edit')
            {
                changeMaskPoint();
            }
            else{sendInfo();}
            
        }
    }
}
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////


cnv_mask.on('mousedown', mouseDown);
cnv_mask.on('mousemove', mouseMove);
cnv_mask.on('mouseup', mouseUp);
cnv_mask.on('wheel', onWheel);
window.onload = onLoad;
window.addEventListener('keydown', keyDown);

btn_chng_status.addEventListener('click', ()=>{
    send_info2('>>');
});