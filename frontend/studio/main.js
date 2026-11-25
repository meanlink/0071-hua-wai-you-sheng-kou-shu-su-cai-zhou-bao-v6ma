import {mount} from '/base.js'
import {films} from './films.js'
import {hearing} from './hearing.js'
import {scoreboard} from './scoreboard.js'
import {delivery} from './delivery.js'

const sections={films,hearing,scoreboard,delivery}
mount({title:'画外有声 · 口述素材周报',kicker:'灯箱无障碍制片组 / 口述影像',
 pages:{films:'剪辑带',hearing:'听审台',scoreboard:'折算周报',delivery:'回执分发'},render:(slug,el,user)=>sections[slug](el,user)})
