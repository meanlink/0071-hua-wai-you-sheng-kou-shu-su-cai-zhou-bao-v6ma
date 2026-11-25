import {h,badge,empty} from '/base.js'
import {deliveryStage} from './timing.js'

export function channelRows(items,reviewer){
  if(!items.length)return empty('安排发出后，可在此查看冻结件和归档回执。')
  return items.map(row=>`<article class="dispatch-record"><header><b>${h(row.name)}</b>${badge(deliveryStage[row.status],row.status)}</header>
    <div class="dispatch-body"><p>报告周 ${h(row.week)}<br>折算进度 ${row.receipt.summary.completion_pct??'—'}%</p>
    <p>计划投递 ${h(new Date(row.release_at).toLocaleString('zh-CN'))}
    ${row.delivered_at?`<br>实际投递 ${h(new Date(row.delivered_at).toLocaleString('zh-CN'))}`:''}
    ${row.status==='paused'?`<br>暂停于 ${h(new Date(row.paused_at).toLocaleString('zh-CN'))} · 返录 ${h(row.paused_cue)}<br>听审重新排期后才会发出更新周报`:''}
    ${row.status==='delivered'?'<br>已送达，原件与回执保留':''}</p></div>
    ${reviewer&&row.status!=='delivered'&&row.status!=='cancelled'?`<form data-id="${row.id}"><button class="quiet">${row.status==='paused'?'取消暂停排期':'撤回排期'}</button><p role="status"></p></form>`:''}</article>`).join('')
}
