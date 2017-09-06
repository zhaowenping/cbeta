/*IE8*/
(function(){if(!/*@cc_on!@*/0)return;var e="abbr,article,aside,audio,canvas,datalist,details,dialog,eventsource,figure,footer,header,hgroup,mark,menu,meter,nav,output,progress,section,time,video".split(','),i=e.length;while(i--){document.createElement(e[i])}})();

/*bootstrap popver*/
$(function (){$("[data-toggle='popover']").popover({html:true});});

/*查找单字的拼音和英文解释*/
function lookup(word){
       var options = {
              method: "GET",
              mode: "same-origin",
              headers: new Headers({
                       // "Content-Type": "application/x-www-form-urlencoded"
                      'Accept': 'application/json',
                      "Content-Type": "application/json",
                      // "X-CSRF-Token": "{{request.session.get_csrf_token()}}",
              }),
              credentials: 'same-origin',
              redirect: 'manual',
              // redirect: 'follow',
              // body: JSON.stringify($('#basicForm').serializeJSON({useIntKeysAsArrayIndex: true})),
              // body: JSON.stringify($('#basicForm').serializeJSON()),
              // body: JSON.stringify($('#form.user.'+userid).serializeJSON({parseNulls: true, parseNumbers: true})),
       };
       fetch('/g/'+word, options)  
         .then(  
           function(response) {  
               console.log('回应报文');
               // console.log(response);
               // console.log(response.status);
               // console.log(response.statusText);
               console.log(response);

             if (response.ok) {
                  //alert("Perfect! Your settings are saved.");
             }
             if (response.status !== 200) {  
               console.log('Looks like there was a problem. Status Code: ' +  response.status);  
               return Promise.resolve(response);  
             }
       
             else if (response.status == 302) {  
               console.log('o Looks like there was a problem. Status Code: ' +  response.status);  
               return response;  
             }
             else if (response.status == 200) {  
                 // Examine the text in the response  
                 response.json().then(function(data) {  
                   console.log(data);  
                   console.log(word);
                   //word.innerHTML ="<a> 成功了</a>";
                   //  location.replace(data.location);
                    repaceSelectionText(word,
'<span data-toggle="popover" title="拼音/释义" data-placement="auto" data-container="body" data-trigger="hover focus" data-content="' + data.pinyin + '|'+data.definition+'">' +
word.toString() +
'</span>');
$(function (){$("[data-toggle='popover']").popover({html:true});});

// <a href="#" type="button" title="&lt;h2&gt;Title&lt;/h2&gt;" data-container="body" data-toggle="popover" data-content="h4Popover 中的一些内容options 方法/h4">Popover</a>
          // var range;
          //  if (word)
          //   {
          //    range = word.getRangeAt(0);
          //  }else {
          //    range = iframeDocument.createRange();
          //  }
          //  var oFragment = range.createContextualFragment("<a> 成功了</a>"),
          //  oLastNode = oFragment.lastChild ;
          //  range.insertNode(oFragment) ;
          //  range.setEndAfter(oLastNode ) ;
          //  range.setStartAfter(oLastNode );
          //  word.removeAllRanges();//清除选择
          //  word.addRange(range);
                  });  
              }
            } 
         )  
         .catch(function(err) {  
           console.log('Fetch Error :-S', err);  
       });

}

//替换选中文本内容，参数text为要替换的内容
function repaceSelectionText(sel, text) {
    //非IE浏览器
    if (window.getSelection) {
        // alert(sel.rangeCount); //选区个数, 通常为 1 .
        sel.deleteFromDocument(); //清除选择的内容
        var r = sel.getRangeAt(0); //即使已经执行了deleteFromDocument(), 这个函数仍然返回一个有效对象.
        var selFrag = r.cloneContents(); //克隆选择的内容
        var frag = selFrag.childNodes; //如果执行了deleteFromDocument(), 这个数组长度将会是 0
        for (var i = 0; i < frag.length; i++) {
            alert(frag[i].nodeName); //枚举选择的对象
        }
        var h1 = document.createElement('span'); //生成一个插入对象
        h1.innerHTML = text; //设置这个对象的内容
        r.insertNode(h1); //把对象插入到选区, 这个操作不会替换选择的内容, 而是追加到选区的后面, 所以如果需要普通粘贴的替换效果, 之前执行deleteFromDocument()函数.
    }
    else if (document.selection && document.selection.createRange) {
        //IE浏览器
        var sel = document.selection.createRange(); //获得选区对象
        alert(sel.htmlText); //选择区的html文本.
        sel.pasteHTML('<h1>标题</h1>'); //粘贴到选区的html内容, 会替换选择的内容.
    }
}

$(document).ready(function () {
               $(".contenttext").mouseup(function (e) {
                var txt;
                var parentOffset = $(this).offset();
                var x = e.pageX - parentOffset.left;
                var y = e.pageY - parentOffset.top;
                txt = window.getSelection();
                if (txt.toString().length == 1) {
                 //alert(txt);
                 lookup(txt);
                }
               });
              });
