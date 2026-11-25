export const stage={draft:'待录制',recorded:'待听审',checked:'已通过'}
export const deliveryStage={queued:'待分发',paused:'因返录暂停',delivered:'收件箱已入账',cancelled:'已撤回'}

export function stamp(seconds){
  return [Math.floor(seconds/60),seconds%60].map(n=>String(n).padStart(2,'0')).join(':')
}

export function futureMinute() {
  const value=new Date(Date.now()+2*60000)
  const local=new Date(value.getTime()-value.getTimezoneOffset()*60000)
  return local.toISOString().slice(0,16)
}
