"use strict";

// let enableTableCardsUpdate;
// let disableTableCardsUpdate;

// (()=>{
//
// let pageReady = false;
// let nextUpdate = false;
// let updater;
//
// let tableCardUpdater;
//
// let doms = [];
// let ucb;
//
//
// function enableUpdate()
// {
//     if(pageReady && !nextUpdate)
//     {
//         updateTableCards();
//         updater = setInterval(updateTableCards, 5000);
//         nextUpdate = true;
//     }
// }
//
// function disableUpdate()
// {
//     if(nextUpdate)
//     {
//         clearInterval(updater);
//         nextUpdate = false;
//     }
// }
//
// function updateTableCards()
// {
//     tableCardUpdater = new XMLHttpRequest();
//     tableCardUpdater.onreadystatechange = getTableCards;
//     tableCardUpdater.open("GET", "http://140.115.200.35:8281/api/v0/tables");
//     tableCardUpdater.send();
// }
//
// function getTableCards()
// {
//     if(tableCardUpdater.readyState === XMLHttpRequest.DONE)
//     {
//         // if(tableCardUpdater.status === 304 || tableCardUpdater.status === 200)
//         if(tableCardUpdater.status === 200)
//         {
//             setTableCards(JSON.parse(tableCardUpdater.responseText));
//         }
//     }
// }
//
// function setTableCards(tableRecords)
// {
//     for(let i = 0; i < tableRecords.length && i < doms.length; i++)
//     {
//         let tableRecord = tableRecords[i];
//         let dom = doms[i];
//
//         dom.tch     .className = tableRecord.isOccupied ? "text-danger" : "text-success";
//         dom.tcht    .innerHTML = tableRecord.isOccupied ? " 已佔用 "     : " 未佔用 ";
//         dom.tcbi    .innerHTML = tableRecord.tableID;
//         dom.tcbs    .innerHTML = `<td>${tableRecord.scores.a}</td><td>${tableRecord.scores.b}</td>`;
//         dom.tcbds[0].innerHTML = tableRecord.distances.a.left  .toFixed(1);
//         dom.tcbds[1].innerHTML = tableRecord.distances.a.middle.toFixed(1);
//         dom.tcbds[2].innerHTML = tableRecord.distances.a.right .toFixed(1);
//         dom.tcbds[3].innerHTML = tableRecord.distances.b.left  .toFixed(1);
//         dom.tcbds[4].innerHTML = tableRecord.distances.b.middle.toFixed(1);
//         dom.tcbds[5].innerHTML = tableRecord.distances.b.right .toFixed(1);
//         dom.tct     .innerHTML = tableRecord.updateTime;
//     }
// }
//
// function initDOMElements()
// {
//     doms = new Array();
//
//     for(let i = 0; ; i++)
//     {
//         let dom =
//         {
//             tc   : null,
//             tch  : null,
//             tcht : null,
//             tcb  : null,
//             tcbi : null,
//             tcbs : null,
//             tcbd : null,
//             tcbds: null,
//             tct  : null
//         };
//
//         dom.tc    = document.getElementById        (`table-card-${i}`); if(dom.tc === null) break;
//         dom.tch   = dom.tc  .getElementsByClassName("taball-table-card-header")[0]
//                             .getElementsByTagName  ("span")[0];
//         dom.tcht  = dom.tch .getElementsByClassName("taball-table-card-header-text")[0];
//         dom.tcb   = dom.tc  .getElementsByClassName("card-body")[0];
//         dom.tcbi  = dom.tcb .getElementsByClassName("taball-table-card-id")[0];
//         dom.tcbs  = dom.tcb .getElementsByClassName("taball-table-card-scores")[0];
//         dom.tcbd  = dom.tcb .getElementsByClassName("taball-table-card-dists")[0];
//         dom.tcbds = dom.tcbd.querySelectorAll      ("tr > td");
//         dom.tct   = dom.tc  .getElementsByClassName("taball-table-card-time")[0];
//
//         doms.push(dom);
//     }
//
//     ucb = document.getElementById("updateAlways");
// }
//
// // enableTableCardsUpdate = enableUpdate;
// // disableTableCardsUpdate = disableUpdate;
//
// document.addEventListener("DOMContentLoaded", event => {
//     initDOMElements();
//     pageReady = true;
//     // enableUpdate();
//     updateTableCards();
//
//     ucb.addEventListener("change", event => {
//         if(ucb.checked)
//         {
//             // console.log("Start updating.");
//             enableUpdate();
//         }
//         else
//         {
//             // console.log("Stop updating.");
//             disableUpdate();
//         }
//     });
// });
//
// })();
