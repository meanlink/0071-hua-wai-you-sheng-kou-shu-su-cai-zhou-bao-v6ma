import {h,badge,empty} from '/base.js'
import {deliveryStage} from './timing.js'

export function channelRows(items,reviewer){
  if(!items.length)return empty('安排发出后，可在此查看冻结件和归档回执。')
  return items.map(row=>`<article class="dispatch-record"><header><b>${h(row.name)}</b>${badge(deliveryStage[row.status],row.status)}</header>
    <div class="dispatch-body"><p>报告周 ${h(row.week)}<br>折算进度 ${row.receipt.summary.completion_pct??'—'}%</p>
    <p>计划投递 ${h(new Date(row.release_at).toLocaleString('zh-CN'))}
    ${row.delivered_at?`<br>实际投递 ${h(new Date(row.delivered_at).toLocaleString('zh-CN'))}`:''}</p></div>
    ${reviewer&&row.status==='queued'?`<form data-id="${row.id}"><button class="quiet">撤回排期</button><p role="status"></p></form>`:''}</article>`).join('')
}
