import {h} from '/base.js'
import {stage,stamp} from './timing.js'

export function track(film,rows) {
  return `<article class="cut"><h2>${h(film.title)}<span>${h(film.code)} / ${stamp(film.cut_length)}</span></h2>
  <div class="chenille" aria-label="片内口述区间">${rows.map(cue=>`<span class="${cue.stage}"
    style="left:${100*cue.in_sec/film.cut_length}%;width:${Math.max(.35,100*(cue.out_sec-cue.in_sec)/film.cut_length)}%"
    title="${h(cue.cue_text)} / ${stage[cue.stage]}"></span>`).join('')}</div>
  <ol>${rows.map(cue=>`<li><time>${stamp(cue.in_sec)} – ${stamp(cue.out_sec)}</time><b>${h(cue.cue_text)}</b>
    <span class="${cue.stage}">${stage[cue.stage]}</span></li>`).join('')}</ol></article>`
}
