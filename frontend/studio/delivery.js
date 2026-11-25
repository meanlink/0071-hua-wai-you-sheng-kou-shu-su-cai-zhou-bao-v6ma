import {api,h} from '/base.js'
import {heading,options,run} from './common.js'
import {futureMinute} from './timing.js'
import {channelRows} from './inbox.js'

export async function delivery(root,user) {
  const [films,channels,items]=await Promise.all(['films','channels','dispatches'].map(key=>api('/api/description/'+key)))
  const weeks=[...new Set(films.map(row=>row.week))]
  const reviewer=user.role==='reviewer'
  root.innerHTML=heading('回执分发','定时分发采用业务站内收件箱，排期当下留存折算结果。返录会暂停该周尚未发出的周报，重新排期后按新折算发出。')
    +`<div class="studio-grid"><section><h2>收件组归档</h2>${channelRows(items,reviewer)}<button class="quiet" id="refresh">刷新状态</button></section><aside><h2>周报排期</h2>
    ${reviewer&&weeks.length?`<form id="dispatch"><label>报告周<select name="week">${weeks.map(week=>`<option>${h(week)}</option>`).join('')}</select></label>
    <label>接收组<select name="channel">${options(channels,'code','name')}</select></label>
    <label>投递时间<input type="datetime-local" name="release_at" required value="${futureMinute()}"></label>
    <button>保存排期</button><p role="status"></p></form>`:'<p>复核人员可为排片周设置收件排期。</p>'}</aside></div>`
  const refresh=()=>delivery(root,user)
  root.querySelector('#refresh').onclick=refresh
  run(root.querySelector('#dispatch'),data=>api('/api/description/weeks/'+data.week+'/dispatch','POST',{channel:data.channel,release_at:new Date(data.release_at).toISOString()}),refresh)
  for(const form of root.querySelectorAll('form[data-id]'))run(form,()=>api('/api/description/dispatches/'+form.dataset.id+'/cancel','POST',{}),refresh)
}
