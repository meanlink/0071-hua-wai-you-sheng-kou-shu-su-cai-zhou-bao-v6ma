import {api,h,empty} from '/base.js'
import {heading,run} from './common.js'
import {card} from './hearing-card.js'

export async function hearing(root,user) {
  const [cues,events]=await Promise.all([api('/api/description/cues'),api('/api/description/hearings')])
  root.innerHTML=heading('听审台','录制后开放听审。返录的点恢复为待录制，历史听审意见仍保留；已通过的也可退回返录。')
    +`<div class="studio-grid"><div class="cue-layout">${cues.map(cue=>card(cue,user)).join('')}</div><aside><h2>听审留档</h2>
    ${events.length?events.map(e=>`<p><b>${h(e.cue)} / ${e.result==='approve'?'通过':'返录'}</b><br>${h(e.note)}</p>`).join(''):empty('听审后会在这里留下审批依据。')}</aside></div>`
  for(const form of root.querySelectorAll('form[data-action]')){
    run(form,(data,button)=>api('/api/description/cues/'+form.dataset.code+'/'+form.dataset.action,'POST',
    form.dataset.action==='hear'?{...data,result:button.value}:data),()=>hearing(root,user))
  }
}
