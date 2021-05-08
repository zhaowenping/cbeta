/*
 *  popup.js
 *  Simon (swiles@dila.edu.tw), Jan./Feb. 2010
 *   - revised by 阿閒 Nov 2010
 *   - add showdowDOM suppoet by 阿閒 April 2021
 *   - 修改事件監聽為 delegate 版本，可避免非同步內容事件無法綁定的問題 by 阿閒 April 2021
 */
 
 

var ddbcAuthPopups = {

    init: function() {
        // define some object variables
        ddbcAuthPopups.base_href = 'http://authority.dila.edu.tw/';
        ddbcAuthPopups.data_service = 'webwidget/getAuthorityData.php';
        ddbcAuthPopups.media_path = 'webwidget/';
        ddbcAuthPopups.more_info = '<br /><br />For more information; see <a href="'+ddbcAuthPopups.base_href+'docs/annotation.php" target="_new">'+ddbcAuthPopups.base_href+'docs/annotation.php</a><br />';
        ddbcAuthPopups.date_format_error = '<div class="wrapper">Error: the date format is improperly specified - please check; and try again.'+ddbcAuthPopups.more_info+'</div>';
        ddbcAuthPopups.no_data_error = '<div class="wrapper">No data returned - unknown entity or query syntax error!'+ddbcAuthPopups.more_info+'</div>';
        ddbcAuthPopups.dor_error = '<div class="wrapper">Date out of range - please check your query!'+ddbcAuthPopups.more_info+'</div>';

        ddbcAuthPopups.attachEvent(window, 'load', function() {
            ddbcAuthPopups.insertCSS([
            '.iba\\:ddbc\\:authPerson[aid],.iba\\:ddbc\\:authPlace[aid],.iba\\:ddbc\\:authDate[aid],.iba\\:ddbc\\:authRole[aid]{cursor:pointer;cursor:url('+ddbcAuthPopups.base_href+ddbcAuthPopups.media_path+'/ddbc_query.cur),auto;}',
            '{max-width:400px;padding:0.5em;margin:0;text-align:center;border:solid #003099 1px;background:#e2e7ff;position:absolute;cursor:move;border-top-left-radius:10px;border-bottom-right-radius:10px;-webkit-border-top-left-radius:10px;-webkit-border-bottom-right-radius:10px;-moz-border-radius-topleft:10px;-moz-border-radius-bottomright:10px;}',
            '*{margin:0; padding:0;font-family:sans-serif;font-size:8pt;color:#004;}',
            'a{color:#00f;background:transparent;text-decoration:none;}',
            'table{text-align:center;}',
            'td{vertical-align:top;padding:0.1em;}',
            '.ddbc_link{float:right;}',
            '.textSize{float:left;cursor:pointer;}',
            '.authData{cursor:text;}',
            'table.authData{text-align:left;float:left;}',
            'table.authDataHide{text-align:left;float:left;display:none}',
            '.authLabel{white-space:nowrap;text-align:right;font-weight:bold;width:110px}',
            'div{float:left;}',
            'div.authData{width:100%;color:#004;background:#ccd5ff;}',
            '.wrapper{margin-right:10px;clear:both;}',
            'input{margin-top:8px;}',
            '.odd{background:#ccd5ff;}',
            '.even{background:#b3c0ff;}',
			'#authDataTable{table-layout:fixed;width:380px;}',
			'#authDataTable td{ word-wrap:break-word;}'
            ].join('\n#ddbcAuthPopup '), 'ddbcAuthPopups');
            ddbcAuthPopups.setDDBCAuthPopups();
			ddbcAuthPopups.setShadowDOMPopups();
        });
    },

    // define some fairly generic, cross-browser helper functions
    getJSON: function(url) {
        var newScript = document.createElement('script');
            newScript.type = 'text/javascript';
            newScript.src = url;
        document.getElementsByTagName('head')[0].appendChild(newScript);
    },

    insertCSS: function(stylesheet, title) {
        var newStyleSheet;
        if (document.createStyleSheet) {
            newStyleSheet = document.createStyleSheet();
            newStyleSheet.cssText = stylesheet;
            newStyleSheet.title = title;
        } else {
            newStyleSheet = document.createElement('style');
            newStyleSheet.type = 'text/css';
            newStyleSheet.title = title;
            newStyleSheet.appendChild(document.createTextNode(stylesheet));
            document.getElementsByTagName('head')[0].appendChild(newStyleSheet);
        }
    },

    getWindowDimensions: function() {
        var width = 0, height = 0;
        if (typeof(window.innerWidth) == 'number') {
            width = window.innerWidth;
            height = window.innerHeight;
        } else if (document.documentElement && (document.documentElement.clientWidth || document.documentElement.clientHeight)) {
            width = document.documentElement.clientWidth;
            height = document.documentElement.clientHeight;
        } else if (document.body && (document.body.clientWidth || document.body.clientHeight)) {
            width = document.body.clientWidth;
            height = document.body.clientHeight;
        }
        return [width,height];
    },

    getWindowScroll: function() {
        var x = 0, y = 0;
        if (typeof(window.pageYOffset) == 'number') {
            y = window.pageYOffset;
            x = window.pageXOffset;
        } else if (document.body && (document.body.scrollLeft || document.body.scrollTop)) {
            y = document.body.scrollTop;
            x = document.body.scrollLeft;
        } else if (document.documentElement && (document.documentElement.scrollLeft || document.documentElement.scrollTop)) {
            y = document.documentElement.scrollTop;
            x = document.documentElement.scrollLeft;
        }
        return [x,y];
    },

    getEventLocation: function(e) {
        var posx = 0, posy = 0;
        if (!e) e = window.event;
        if (e.pageX || e.pageY) {
            posx = e.pageX;
            posy = e.pageY;
        } else if (e.clientX || e.clientY) {
            posx = e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
            posy = e.clientY + document.body.scrollTop + document.documentElement.scrollTop;
        }
        return [posx,posy];
    },

    attachEvent: function(obj,evt,fn) {
        if (obj.addEventListener)
            obj.addEventListener(evt,fn,false);
        else if (obj.attachEvent)
            obj.attachEvent('on'+evt,fn);
    },

    detachEvent: function(obj,evt,fn) {
        if (obj.removeEventListener)
            obj.removeEventListener(evt,fn,false);
        else if (obj.detachEvent)
            obj.detachEvent('on'+evt,fn);
    },

    clearEvent: function(e) {
        if (!e) var e = window.event;
        e.cancelBubble = true;
        if (e.stopPropagation) e.stopPropagation();
    },

    startDragMouse: function (e) {
        var el = e.srcElement || this;
        ddbcAuthPopups.startDrag(el);
        var evt = e || window.event;
        ddbcAuthPopups.initialMouseX = evt.clientX;
        ddbcAuthPopups.initialMouseY = evt.clientY;
        ddbcAuthPopups.attachEvent(document,'mousemove',ddbcAuthPopups.dragMouse);
        ddbcAuthPopups.attachEvent(document,'mouseup',ddbcAuthPopups.releaseElement);
        return false;
    },

    startDrag: function (obj) {
        if (ddbcAuthPopups.draggedObject) ddbcAuthPopups.releaseElement();
        ddbcAuthPopups.startX = obj.offsetLeft;
        ddbcAuthPopups.startY = obj.offsetTop;
        ddbcAuthPopups.draggedObject = obj;
    },

    dragMouse: function (e) {
        var evt = e || window.event;
        var dX = evt.clientX - ddbcAuthPopups.initialMouseX;
        var dY = evt.clientY - ddbcAuthPopups.initialMouseY;
        ddbcAuthPopups.draggedObject.style.left = ddbcAuthPopups.startX + dX + 'px';
        ddbcAuthPopups.draggedObject.style.top = ddbcAuthPopups.startY + dY + 'px';
        return false;
    },

    releaseElement: function() {
        ddbcAuthPopups.detachEvent(document,'mousemove',ddbcAuthPopups.dragMouse);
        ddbcAuthPopups.detachEvent(document,'mouseup',ddbcAuthPopups.releaseElement);
        ddbcAuthPopups.draggedObject = null;
    },

    getElementsByClassName: function (className,tag,elm){
        var getElementsByClassName;
        if (document.getElementsByClassName) {
            getElementsByClassName = function (className,tag,elm) {
                elm = elm || document;
                var elements = elm.getElementsByClassName(className),
                    nodeName = (tag)? new RegExp("\\b" + tag + "\\b", "i") : null,
                    returnElements = [],
                    current;
                for(var i=0,il=elements.length;i<il;i+=1){
                    current = elements[i];
                    if(!nodeName || nodeName.test(current.nodeName)) {
                        returnElements.push(current);
                    }
                }
                return returnElements;
            };
        }
        else if (document.evaluate) {
            getElementsByClassName = function (className,tag,elm) {
                tag = tag || "*";
                elm = elm || document;
                var classes = className.split(" "),
                    classesToCheck = "",
                    xhtmlNamespace = "http://www.w3.org/1999/xhtml",
                    namespaceResolver = (document.documentElement.namespaceURI === xhtmlNamespace)?xhtmlNamespace:null,
                    returnElements = [],
                    elements,
                    node;
                for(var j=0,jl=classes.length;j<jl;j+=1){
                    classesToCheck += "[contains(concat(' ', @class, ' '), ' "+classes[j]+" ')]";
                }
                try {
                    elements = document.evaluate(".//"+tag+classesToCheck,elm,namespaceResolver,0,null);
                }
                catch (e) {
                    elements = document.evaluate(".//"+tag+classesToCheck,elm,null,0,null);
                }
                while ((node = elements.iterateNext())) {
                    returnElements.push(node);
                }
                return returnElements;
            };
        }
        else {
            getElementsByClassName = function (className,tag,elm) {
                tag = tag || "*";
                elm = elm || document;
                var classes = className.split(" "),
                    classesToCheck = [],
                    elements = (tag === "*" && elm.all)?elm.all:elm.getElementsByTagName(tag),
                    current,
                    returnElements = [],
                    match;
                for(var k=0,kl=classes.length;k<kl;k+=1){
                    classesToCheck.push(new RegExp("(^|\\s)"+classes[k]+"(\\s|$)"));
                }
                for(var l=0,ll=elements.length;l<ll;l+=1){
                    current = elements[l];
                    match = false;
                    for(var m=0,ml=classesToCheck.length;m<ml;m+=1){
                        match = classesToCheck[m].test(current.className);
                        if (!match) {
                            break;
                        }
                    }
                    if (match) {
                        returnElements.push(current);
                    }
                }
                return returnElements;
            };
        }
        return getElementsByClassName(className,tag,elm);
    },

    // define some script-specific functions
    prepText: function(string) {
        //return (string !== null)?string.replace(/\n/g, '<br />'):'';  simon版
        return (string)?string.replace(/\n/g, '<br />'):'';
    },

    getAuthPersonPopup: function(json) {
        if (null === json) {
            ddbcAuthPopups.showAuthPopup(ddbcAuthPopups.no_data_error);
            return;
        }
        //if (typeof personData === undefined) {
            var personData = {
                authorityID:Array('ID','\'<a target="_blank" href="http://authority.dila.edu.tw/person/index.php?fromInner=\'+json[obj].authorityID+\'">\'+json[obj].authorityID+\'</a>\''),
                name:       Array('名稱', 'json[obj].name'),
                dynasty:    Array('朝代', 'json[obj].dynasty'),
                bornDate:   Array('生年', 'json[obj].bornDateBegin'),
                diedDate:   Array('卒年', 'json[obj].diedDateBegin'),
                note:       Array('註解(精簡)', 'json[obj].note'),
                noteFull:   Array('註解(完整)', 'json[obj].noteFull'),
                names:      Array('別名', 'json[obj].names'),
				pinyin:     Array('拼音', 'json[obj].pinyin')
            };
        //}
        var html = ddbcAuthPopups.getAuthTable(personData, json, 'person');
        ddbcAuthPopups.showAuthPopup(html);
    },

    getAuthPlacePopup: function(json) {
        if (null === json) {
            ddbcAuthPopups.showAuthPopup(ddbcAuthPopups.no_data_error);
            return;
        }
        //if (typeof placeData === undefined) {
            var placeData = {
                authorityID:        Array('ID', '\'<a target="_blank" href="http://authority.dila.edu.tw/place/index.php?fromInner=\'+json[obj].authorityID+\'">\'+json[obj].authorityID+\'</a>&nbsp;&nbsp;&nbsp;<a href="\'+ddbcAuthPopups.base_href+\'/place/produceKML.php?cno=\'+json[obj].authorityID+\'">KML</a>\''),
                name:               Array('地名', 'json[obj].name'),
                districtModern:     Array('行政區', 'json[obj].districtModern'),
                //dynasty:            Array('朝代', 'json[obj].dynasty'),
                districtHistorical: Array('歷史地名', 'json[obj].districtHistorical'),
                long:               Array('座標', 'json[obj].long+","+json[obj].lat'),
                note:               Array('註解', 'json[obj].note'),
                names:              Array('別名', 'json[obj].names')
            };
        //}
        var html = ddbcAuthPopups.getAuthTable(placeData, json, 'place');
        ddbcAuthPopups.showAuthPopup(html);
    },

    getAuthOfficialTitlePopup: function(json) {
        if (null === json) {
            ddbcAuthPopups.showAuthPopup(ddbcAuthPopups.no_data_error);
            return;
        }

            var officialTitleData = {
                authorityID:        Array('ID', 'json[obj].authorityID'),
                name:               Array('官名', 'json[obj].name'),
                note:               Array('註解', 'json[obj].note'),
                names:              Array('別名', 'json[obj].names')
            };

        var html = ddbcAuthPopups.getAuthTable(officialTitleData, json, 'officialTitle');
        ddbcAuthPopups.showAuthPopup(html);
    },

    getAuthTable: function(data, json, type) {
        var table = '', html = '' , tableHide = '';
        for (var field in data) {

            var count=0;
            table+='<tr>';
            table+='<td class="authLabel">'+data[field][0]+'：</td>';

            tableHide += '<tr><td class="authLabel">'+data[field][0]+'：</td>';

            for(var obj in json) {

                //生卒年特別處理+
                if(field == 'bornDate') {
                    data['bornDate'][1] = json[obj].bornDateBegin == json[obj].bornDateEnd ? 'json[obj].bornDateBegin':'json[obj].bornDateBegin+\' ~ \'+json[obj].bornDateEnd';
                }
                if(field == 'diedDate') {
                    data['diedDate'][1] = json[obj].diedDateBegin == json[obj].diedDateEnd ? 'json[obj].diedDateBegin':'json[obj].diedDateBegin+\' ~ \'+json[obj].diedDateEnd';
                }
                //生卒年特別處理-
				
				//漢語拼音需特別處理
				if(field == 'pinyin')	{
					var pinyin_obj = json[obj].pinyin;
					var pinyin_string = '';
					/*
					for(i in pinyin_obj)	{
						for(j in pinyin_obj[i])	{
							pinyin_string += j+pinyin_obj[i][j]+"\n";
						}
					}
					*/
					for(var lang in pinyin_obj)	{
						pinyin_string += pinyin_obj[lang]+"("+lang+")\n";
					}
					json[obj].pinyin = pinyin_string;					
				}
				
                if (count <4)
                    table+='<td class="'+((count%2===0)?'odd':'even')+'">'+ddbcAuthPopups.prepText(eval(data[field][1]))+'</td>';
                else
                    tableHide += '<td class="'+((count%2===0)?'odd':'even')+'">'+ddbcAuthPopups.prepText(eval(data[field][1]))+'</td>';

                count++;
            }
            table+='</tr>';

            tableHide += '</tr>';

            ddbcAuthPopups.authPopup.style.maxWidth = ((count>1)?(count*200):400)+'px';

        }
        if (table) table = '<table id="authDataTable" class="authData">'+table+'</table>';
        if(tableHide) tableHide = '<table id="authDataTableHide" class="authData" style="display:none">'+tableHide+'</table>';
        if (count > 1) {
            html = count+' results found for '+ddbcAuthPopups.authID;
            if (count > 3) {
                //html += ' - <a href="'+ddbcAuthPopups.base_href+'/'+type+'/index.php?fromSearch='+ddbcAuthPopups.authID+'">Show all</a>';
                html += ' - <a id="seeOtherPageLink" href="javascript:void(0)" onclick="javascript:ddbcAuthPopups.seeOtherPage();">next</a>';
            }
        }
        return html+table+tableHide;
    },

    seeOtherPage:function() {
        document.getElementById('authDataTable').style.display = (document.getElementById('authDataTable').style.display == 'none'?'':'none');
        document.getElementById('authDataTableHide').style.display = (document.getElementById('authDataTableHide').style.display == 'none'?'':'none');
        document.getElementById('seeOtherPageLink').innerHTML = (document.getElementById('seeOtherPageLink').innerHTML == 'next'?'prev':'next');
    },

    queryAuthDate: function(dateString) {
        var dateWhen, dateFrom, dateTo;
        var dateFormat = dateString.substr(0,1).toLowerCase();
        switch(dateFormat) {
            case 'j':
                if (dateString.length == 8) {
                    dateWhen = dateString.substr(1,7);
                    ddbcAuthPopups.getJSON(ddbcAuthPopups.base_href+'/'+ddbcAuthPopups.data_service+'?when='+dateWhen+'&type=time&format='+dateFormat+'&jsoncallback=ddbcAuthPopups.getAuthDatePopup');
                } else if(dateString.length == 15)  {
                    dateFrom = dateString.substr(1,7);
                    dateTo = dateString.substr(8,7);
                    ddbcAuthPopups.getJSON(ddbcAuthPopups.base_href+'/'+ddbcAuthPopups.data_service+'?from='+dateFrom+'&to='+dateTo+'&type=time&format='+dateFormat+'&jsoncallback=ddbcAuthPopups.getAuthDatePopup');
                } else ddbcAuthPopups.showAuthPopup(ddbcAuthPopups.date_format_error);
            break;

            case 's':
                if (dateString.length == 12) {
                    dateWhen = dateString.substr(1,11);
                    ddbcAuthPopups.getJSON(ddbcAuthPopups.base_href+'/'+ddbcAuthPopups.data_service+'?when='+dateWhen+'&type=time&format='+dateFormat+'&jsoncallback=ddbcAuthPopups.getAuthDatePopup');
                } else if(dateString.length == 23) {
                    dateFrom = dateString.substr(1,11);
                    dateTo = dateString.substr(12,11);
                    ddbcAuthPopups.getJSON(ddbcAuthPopups.base_href+'/'+ddbcAuthPopups.data_service+'?from='+dateFrom+'&to='+dateTo+'&type=time&format='+dateFormat+'&jsoncallback=ddbcAuthPopups.getAuthDatePopup');
                } else ddbcAuthPopups.showAuthPopup(ddbcAuthPopups.date_format_error);
            break;

            default:
                ddbcAuthPopups.showAuthPopup(ddbcAuthPopups.date_format_error);
        }
    },

    getAuthDatePopup: function(json) {
        if (null === json) {
            ddbcAuthPopups.showAuthPopup(ddbcAuthPopups.no_data_error);
            return;
        }
        var html = '';
        if (json.W) html += ddbcAuthPopups.getAuthDateTable(json.W);
        if (json.F && json.T) {
            html += '<div class="wrapper">from:';
            html += ddbcAuthPopups.getAuthDateTable(json.F);
            html += '</div><div>to:';
            html += ddbcAuthPopups.getAuthDateTable(json.T);
            html += '</div>';
        }
        ddbcAuthPopups.showAuthPopup((html)?html:ddbcAuthPopups.no_data_error);
    },

    getAuthDateTable: function(json) {
        var cell = '';
        if (json.data1) {
            cell += json.data1.ceDate+'<br />AID：'+json.data1.authorityID+'<br />J.D.：'+json.data1.JD;
            for (var obj in json) {
                if (obj != "cells") {
                    cell += '<hr />';
                    cell += json[obj].dynasty+json[obj].emperor+'<br />';
                    cell += json[obj].era+json[obj].yearNumberCh+'('+json[obj].yearGanzhi+')<br />';
                    cell += json[obj].lunar_month+'月'+json[obj].dayNumberCh+'('+json[obj].dayGanzhi+')';
                }
            }
        }
        return '<div class="authData">'+cell+'</div>';
    },

    showAuthPopup: function(html) {
        html = '<span class="textSize" onclick="return ddbcAuthPopups.textSize(\'reset\')"><img src="'+ddbcAuthPopups.base_href+ddbcAuthPopups.media_path+'/zoom-original.png" /></span>'
             + '<span class="textSize" onclick="return ddbcAuthPopups.textSize(\'up\')"><img src="'+ddbcAuthPopups.base_href+ddbcAuthPopups.media_path+'/zoom-in.png" /></span>'
             + '<span class="textSize" onclick="return ddbcAuthPopups.textSize(\'down\')"><img src="'+ddbcAuthPopups.base_href+ddbcAuthPopups.media_path+'/zoom-out.png" /></span>'
             + html
             + '<br style="clear:both;"/><input type="button" value="關閉" onclick="document.getElementById(\'ddbcAuthPopup\').style.display=\'none\';" />'
             + '<a class="ddbc_link" href="'+ddbcAuthPopups.base_href+'" target="_new">A DDBC Authority Record</a>';

        ddbcAuthPopups.authPopup.innerHTML = html;
        ddbcAuthPopups.authPopup.style.width = 'auto';
        ddbcAuthPopups.authPopup.style.display = 'block';
        //ddbcAuthPopups.authPopup.style.width = (ddbcAuthPopups.authPopup.firstChild.offsetWidth||400) + 'px';
        //if (document.all && ddbcAuthPopups.authPopup.currentStyle.opacity) {
            //ddbcAuthPopups.authPopup.style.filter = 'alpha(opacity='+ddbcAuthPopups.authPopup.currentStyle.opacity*100+')';
        //}
        var dims = ddbcAuthPopups.getWindowDimensions();
        var scroll = ddbcAuthPopups.getWindowScroll();
        var top = ddbcAuthPopups.pos[1] + scroll[1] - 200;
            top = (top < 20 ? 20 : top);
        if (top + ddbcAuthPopups.authPopup.offsetHeight > dims[1] + scroll[1] - 20) top = dims[1] + scroll[1] - ddbcAuthPopups.authPopup.offsetHeight - 20;
        var left = ddbcAuthPopups.pos[0] + scroll[0] - 200;
            left = (left < 20 ? 20 : left);
        if (left + ddbcAuthPopups.authPopup.offsetWidth > dims[0] + scroll[0] - 20) top = dims[0] + scroll[0] - ddbcAuthPopups.authPopup.offsetWidth - 20;
        ddbcAuthPopups.authPopup.style.top = top + 'px';
        ddbcAuthPopups.authPopup.style.left = left + 'px';
        ddbcAuthPopups.attachEvent(ddbcAuthPopups.authPopup, 'mousedown', ddbcAuthPopups.startDragMouse);
        els = ddbcAuthPopups.getElementsByClassName('authData');
        for (var i=0,il=els.length; i<il; i++) {
            ddbcAuthPopups.attachEvent(els[i], 'mousedown', function(e) {ddbcAuthPopups.clearEvent(e)});
        }
    },

    getAuthPopup: function(e,srcel) {
        if (ddbcAuthPopups.authPopup == null) {
            ddbcAuthPopups.authPopup = document.createElement('div');
            ddbcAuthPopups.authPopup.setAttribute('id','ddbcAuthPopup');
            document.body.appendChild(ddbcAuthPopups.authPopup);
        }
        ddbcAuthPopups.pos = ddbcAuthPopups.getEventLocation(e);
        var el = srcel || e.srcElement || this;
        ddbcAuthPopups.authID = el.getAttribute('aid');
        //ddbcAuthPopups.authID.replace('corresp','')

        switch (el.className) {
            case 'iba:ddbc:authPerson':
                ddbcAuthPopups.getJSON(ddbcAuthPopups.base_href+'/'+ddbcAuthPopups.data_service+'?id='+ddbcAuthPopups.authID+'&type=person&jsoncallback=ddbcAuthPopups.getAuthPersonPopup');
            break;

            case 'iba:ddbc:authPlace':
                ddbcAuthPopups.getJSON(ddbcAuthPopups.base_href+'/'+ddbcAuthPopups.data_service+'?id='+ddbcAuthPopups.authID+'&type=place&jsoncallback=ddbcAuthPopups.getAuthPlacePopup');
            break;

            case 'iba:ddbc:authRole':
                ddbcAuthPopups.getJSON(ddbcAuthPopups.base_href+'/'+ddbcAuthPopups.data_service+'?id='+ddbcAuthPopups.authID+'&type=officialTitle&jsoncallback=ddbcAuthPopups.getAuthOfficialTitlePopup');
            break;

            case 'iba:ddbc:authDate':
                ddbcAuthPopups.queryAuthDate(ddbcAuthPopups.authID);
            break;
        }
    },

    textSize: function(type) {
        for (var i=0,il=document.styleSheets.length;i<il;i++) {
            if (document.styleSheets[i].title == 'ddbcAuthPopups') {
                var rules = document.styleSheets[i].cssRules? document.styleSheets[i].cssRules: document.styleSheets[i].rules;
                for (var j=0,jl=rules.length;j<jl;j++) {
                    if (rules[j].selectorText == '#ddbcAuthPopup *') {
                        switch (type) {
                            case 'up':
                                rules[j].style.fontSize = parseInt(rules[j].style.fontSize.replace('pt','')) + 2 + 'pt';
                            break;
                            case 'down':
                                rules[j].style.fontSize = parseInt(rules[j].style.fontSize.replace('pt','')) - 2 + 'pt';
                            break;
                            case 'reset':
                                rules[j].style.fontSize = '8pt';
                            break;
                        }
                    }
                }
            }
        }
    },

	/*
	//原 simon 版本備份
    setDDBCAuthPopups: function(el) {
        var span, authElements = ddbcAuthPopups.getElementsByClassName('iba\:ddbc\:authPerson', 'span', el);
        authElements = authElements.concat(ddbcAuthPopups.getElementsByClassName('iba\:ddbc\:authPlace', 'span', el));
        authElements = authElements.concat(ddbcAuthPopups.getElementsByClassName('iba\:ddbc\:authRole', 'span', el));
        authElements = authElements.concat(ddbcAuthPopups.getElementsByClassName('iba\:ddbc\:authDate', 'span', el));
        for (var i=0,len=authElements.length;i<len;++i){
            span = authElements[i];
            var query = span.getAttribute('title');
            if (query) {
                span.setAttribute('aid', query);
                span.removeAttribute('title');
                ddbcAuthPopups.attachEvent(span,'click',ddbcAuthPopups.getAuthPopup);
                if (span.captureEvents) span.captureEvents(Event.CLICK);
            }
        }
    },
	*/
	
	//一般 DOM 處理
    setDDBCAuthPopups: function(el) {	
		//重設所有title為aid
		var authElements = document.querySelectorAll('.iba\\:ddbc\\:authPerson , .iba\\:ddbc\\:authPlace , .iba\\:ddbc\\:authDate , .iba\\:ddbc\\:authRole');
		for (var i=0,len=authElements.length;i<len;++i){
			span = authElements[i];
			var query = span.getAttribute('title');
			if (query) {
				span.setAttribute('aid', query);
				span.removeAttribute('title');
			}
		}		
		
		//改用 dom delegate 完成事件，可避免非同步內容沒有綁定到事件的問題
		ddbcAuthPopups.attachEvent(document,'click',function(e)	{
			var target_elm = e.composedPath()[0];
			if(target_elm && (target_elm.classList.contains('iba:ddbc:authPerson') || target_elm.classList.contains('iba:ddbc:authPlace') || target_elm.classList.contains('iba:ddbc:authDate') || target_elm.classList.contains('iba:ddbc:authRole')))	{
				var aid = target_elm.getAttribute('title') || target_elm.getAttribute('aid');
				if(aid)	{
					target_elm.setAttribute('aid', aid);
					target_elm.removeAttribute('title');
					ddbcAuthPopups.getAuthPopup(e,target_elm);
				}				
			}
		});
    },
	
	//shadow DOM 處理
	setShadowDOMPopups:function()	{
		/*
		//阿閒：取得所有shadowDOM元素並加入事件版本，因元素可能為非同步渲染，故此法可能無效
		var all_el = [...document.getElementsByTagName('*')].filter(e => e.shadowRoot).forEach(selm => {
			selm = selm.shadowRoot;
			console.log(selm)
			var authElements = selm.querySelectorAll('.iba\\:ddbc\\:authPerson , .iba\\:ddbc\\:authPlace , .iba\\:ddbc\\:authDate , .iba\\:ddbc\\:authRole');
			for (var i=0,len=authElements.length;i<len;++i){
				span = authElements[i];
				var query = span.getAttribute('title');
				if (query) {
					span.setAttribute('aid', query);
					span.removeAttribute('title');
					ddbcAuthPopups.attachEvent(span,'click',ddbcAuthPopups.getAuthPopup);
					if (span.captureEvents) span.captureEvents(Event.CLICK);
				}
			}			
		});
		*/
		
		//阿閒：Event delegate 版本，可保證非同步元素渲染的事件綁定，相當於live
		ddbcAuthPopups.attachEvent(document,'click',function(e)	{
			//console.log(e.composedPath()[0])
			var shadow_elm = e.composedPath()[0];
			if(shadow_elm && (shadow_elm.classList.contains('iba:ddbc:authPerson') || shadow_elm.classList.contains('iba:ddbc:authPlace') || shadow_elm.classList.contains('iba:ddbc:authDate') || shadow_elm.classList.contains('iba:ddbc:authRole')))	{
				var aid = shadow_elm.getAttribute('title') || shadow_elm.getAttribute('aid');
				if(aid)	{
					shadow_elm.setAttribute('aid', aid);
					shadow_elm.removeAttribute('title');
					ddbcAuthPopups.getAuthPopup(e,shadow_elm);
				}				
			}
		});
	}
};

ddbcAuthPopups.init();
