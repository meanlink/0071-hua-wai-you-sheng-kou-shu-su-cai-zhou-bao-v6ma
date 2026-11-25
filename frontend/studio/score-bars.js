import {h} from '/base.js'
import {stage} from './timing.js'

export function score(label,row) {
  return `<article class="score"><h2>${h(label)}<span>${row.completion_pct===null?'—':h(row.completion_pct)+'%'}</span></h2>
    <div class="stage-bar">${Object.entries(row.weights).map(([key,value])=>`<span class="${key}" style="flex:${value}" title="${stage[key]} / ${value}"></span>`).join('')}</div>
    <p>已得 ${row.earned} / ${row.total} 权重点 · 通过 ${row.counts.checked} 条 · 待听审 ${row.counts.recorded} 条</p></article>`
}
