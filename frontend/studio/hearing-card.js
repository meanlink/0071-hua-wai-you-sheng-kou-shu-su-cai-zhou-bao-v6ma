import {h,badge} from '/base.js'
import {stage,stamp} from './timing.js'

export function card(cue,user) {
  const recording=cue.stage==='draft'&&user.role==='operator'
  const reviewing=cue.stage==='recorded'&&user.role==='reviewer'
  const reverting=cue.stage==='checked'&&user.role==='reviewer'
  return `<article class="cue"><header><span>${h(cue.code)} / ${stamp(cue.in_sec)}</span>
    ${badge(stage[cue.stage],cue.stage)}</header><h2>${h(cue.cue_text)}</h2>
    <p>${h(cue.film)} · 权重 ${cue.weight}</p>
    ${recording?`<form data-action="record" data-code="${h(cue.code)}"><label>录音稿<input name="cue_text" minlength="3" value="${h(cue.cue_text)}" required></label>
    <button>提交录制</button><p role="status"></p></form>`:''}
    ${reviewing?`<form data-action="hear" data-code="${h(cue.code)}"><label>听审批注<input name="note" minlength="4" maxlength="240" required></label>
    <button value="approve">通过</button><button class="quiet" value="redo">返录</button><p role="status"></p></form>`:''}
    ${reverting?`<form data-action="hear" data-code="${h(cue.code)}"><label>退回返录批注<input name="note" minlength="4" maxlength="240" required></label>
    <button class="quiet" value="redo">退回返录</button><p role="status"></p></form>`:''}</article>`
}
