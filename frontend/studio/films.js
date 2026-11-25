import {api} from '/base.js'
import {heading,options,run} from './common.js'
import {track} from './cue-track.js'

export async function films(root,user) {
  const [films,cues]=await Promise.all([api('/api/description/films'),api('/api/description/cues')])
  root.innerHTML=heading('剪辑带','口述时窗按当前剪辑版时间码落点，保留段落难度权重。')
    + `<div class="studio-grid"><section>${films.map(film=>track(film,cues.filter(row=>row.film===film.code))).join('')}</section>
    <aside><h2>录音脚本</h2><p>写入片内秒点，权重根据叙事难度从 1 到 5。版次时间窗有重叠时，需先协调脚本。</p>
    ${user.role==='operator'?`<form><label>口述点编号<input name="code" required pattern="[A-Z0-9-]{3,24}"></label>
    <label>版次<select name="film">${options(films,'code','title')}</select></label><label>入点（秒）<input name="in_sec" type="number" min="0" required></label>
    <label>出点（秒）<input type="number" name="out_sec" min="1" required></label>
    <label>口述脚本<input name="cue_text" minlength="3" maxlength="200" required></label>
    <label>难度权重<input name="weight" type="number" min="1" max="5" required></label><button>加入剪辑带</button><p role="status"></p></form>`:''}</aside></div>`
  run(root.querySelector('form'),data=>api('/api/description/cues','POST',{...data,in_sec:+data.in_sec,out_sec:+data.out_sec,weight:+data.weight}),()=>films(root,user))
}
