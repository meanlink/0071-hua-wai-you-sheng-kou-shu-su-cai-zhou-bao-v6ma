import {h,notice} from '/base.js'

export const heading=(title,phrase)=>`<header class="studio-head"><h1>${h(title)}</h1><p>${h(phrase)}</p></header>`
export const options=(rows,code,title)=>rows.map(item=>`<option value="${h(item[code])}">${h(item[title])}</option>`).join('')

export function run(form,send,refresh) {
  if(!form)return
  form.onsubmit=async event=>{
    event.preventDefault()
    const button=event.submitter
    button.disabled=true
    try{
      await send(Object.fromEntries(new FormData(form)),button)
      await refresh()
    }catch(error){notice(form.querySelector('[role=status]'),error.message,true)}
    finally{button.disabled=false}
  }
}
