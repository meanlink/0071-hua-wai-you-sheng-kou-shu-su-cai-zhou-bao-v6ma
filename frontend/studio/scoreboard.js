import {api,empty,h} from '/base.js'
import {heading} from './common.js'
import {score} from './score-bars.js'

export async function scoreboard(root,_user,selected) {
  const films=await api('/api/description/films')
  const week=selected??films[0]?.week
  if(!week){root.innerHTML=empty('编排片目后可折算进度。');return}
  const report=await api('/api/description/weeks/'+week)
  root.innerHTML=heading('折算周报','录制待审按一半权重，听审通过按全权重。排期前查看各片目进度。')
    +`<div class="studio-grid"><section>${score('本周汇总',report.summary)}${report.films.map(row=>score(row.title,row)).join('')}</section>
    <aside><label>报告周<select>${[...new Set(films.map(row=>row.week))].map(value=>`<option>${h(value)}</option>`).join('')}</select></label>
    <p>周一是报告周起点。周报中分母为当前计划片目的权重总和。</p><a href="#delivery">安排收件</a></aside></div>`
  root.querySelector('select').value=week
  root.querySelector('select').onchange=event=>scoreboard(root,_user,event.target.value)
}
